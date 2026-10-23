"""Generate CPython's object layouts as C-layout Jac declarations.

A native Jac object-model port defines and reads CPython objects in place, so
their layouts are ABI: `PyObject`, `PyVarObject`, `PyTypeObject`, the slot
tables and the concrete object structs must match the pinned headers byte for
byte. This script writes both sides of that contract:

    jac run scripts/jacpython/gen_layouts.jac            # rewrite both files
    jac run scripts/jacpython/gen_layouts.jac --check    # fail on drift

The platform constants need `zig` (or `--zig`) to cross-compile their probe
for each target.

- jaclang/runtime/python/layouts.jac: one foreign struct per layout in LAYOUTS
  (and the structs they embed by value), function-pointer slots as
  `Callable[...]` fields, pointers to layouts as `ptr[Layout]` and pointers to
  records no port reads as opaque types; plus the header constants in
  CONSTANTS that object initializers need.
- jaclang/runtime/python/layouts_platform.<os>.<arch>.jac: the constants in
  PLATFORM_CONSTANTS, whose values differ between the supported platforms
  (where a field sits in the interpreter state, past records sized by the C
  library), each folded by `zig cc -target` for that platform. The plain
  layouts_platform.jac names no platform, and a port reading one of these
  constants refuses to start on a platform without a generated table.
- bootstrap/python/layouts_check.c: `_Static_assert`s on the offset, size and
  signedness of every generated field, each struct's size and alignment, and
  each constant's value, the platform constants under an `#if` for their
  platform. build.sh compiles it against the configured headers
  of every JacPython build, so a layout that drifts on any platform fails the
  build instead of corrupting objects.

Struct bodies are read from the headers of the pinned archive through a small
preprocessor that evaluates `#if` blocks for the release build every supported
platform shares (64-bit, little-endian, GIL-enabled, 30-bit digits); the
generated asserts are what make that assumption checked rather than trusted.
An object struct a `.c` file keeps private (`rangeobject`, `PyCapsule`) is read
from that file in OBJECT_SOURCES: its port defines the layout from then on, and
layouts_check.c repeats the upstream definition so the Jac layout is checked
against it as a header's would be.
Constant values are read back from the configured headers of a local JacPython
build, as gen_constants.jac reads system headers.
"""
import argparse;
import re;
import shlex;
import subprocess;
import sys;
import tempfile;
import from pathlib { Path }
import from common {
    BOOTSTRAP,
    JAC,
    RUNTIME,
    archive_texts,
    format_jac,
    pin,
    write_or_check
}

glob OUTPUT: Path = RUNTIME / "layouts.jac",
     CHECK: Path = BOOTSTRAP / "layouts_check.c",
     CAPI: Path = RUNTIME / "cpython_api.jac",
     PLATFORM_OUTPUT: str = "layouts_platform",
     COMMAND: str = "scripts/jacpython/gen_layouts.jac",
     # Headers the layouts are read from, in inclusion order.
     HEADERS: list[str] = [
         "Include/pytypedefs.h",
         "Include/object.h",
         "Include/cpython/object.h",
         "Include/cpython/longintrepr.h",
         "Include/cpython/tupleobject.h",
         "Include/cpython/listobject.h",
         "Include/cpython/initconfig.h",
         "Include/pycapsule.h",
         "Include/descrobject.h",
         "Include/cpython/descrobject.h",
         "Include/internal/pycore_descrobject.h",
         "Include/cpython/cellobject.h",
         "Include/sliceobject.h",
         "Include/cpython/pyerrors.h",
         "Include/internal/pycore_range.h",
         "Include/internal/pycore_tuple.h",
         "Include/internal/pycore_list.h",
         "Include/cpython/setobject.h",
         "Include/cpython/dictobject.h",
         "Include/internal/pycore_dict.h",
         "Include/cpython/methodobject.h",
         "Include/cpython/weakrefobject.h",
         "Include/moduleobject.h",
         "Include/internal/pycore_moduleobject.h",
         "Include/internal/pycore_freelist_state.h",
         "Include/datetime.h",
         "Include/pybuffer.h",
         "Include/cpython/memoryobject.h",
         "Include/cpython/floatobject.h",
         "Include/cpython/complexobject.h",
         "Include/cpython/classobject.h",
         "Include/structseq.h",
         "Include/internal/pycore_interp_structs.h"
     ],
     # Object files whose private object structs are layouts: the ports of
     # these files define the objects, so the structs are no header's.
     OBJECT_SOURCES: list[str] = [
         "Objects/namespaceobject.c",
         "Objects/capsule.c",
         "Objects/iterobject.c",
         "Objects/enumobject.c",
         "Objects/rangeobject.c",
         "Objects/picklebufobject.c",
         "Objects/interpolationobject.c",
         "Objects/templateobject.c",
         "Objects/unionobject.c",
         "Objects/genericaliasobject.c",
         "Objects/fileobject.c",
         "Objects/dictobject.c",
         "Objects/odictobject.c",
         "Objects/descrobject.c",
         "Objects/funcobject.c",
         "Objects/typevarobject.c",
         "Objects/memoryobject.c",
         # The socket object and the _socket.CAPI record: the _socket and
         # _ssl ports define and read them; the header has no C user left.
         "Modules/socketmodule.h"
     ],
     # Headers the constant probe and layouts_check.c include after Python.h
     # (datetime.h is not part of it).
     INCLUDES: list[str] = [
         "internal/pycore_long.h",
         "internal/pycore_time.h",
         "datetime.h",
         "internal/pycore_abstract.h",
         "internal/pycore_freelist_state.h",
         "internal/pycore_range.h",
         "internal/pycore_tuple.h",
         "internal/pycore_runtime.h",
         "internal/pycore_typeobject.h",
         "internal/pycore_interp_structs.h",
         "internal/pycore_gc.h",
         "internal/pycore_list.h",
         "internal/pycore_dict.h",
         "internal/pycore_descrobject.h",
         "internal/pycore_function.h",
         "internal/pycore_code.h",
         "internal/pycore_interpframe_structs.h",
         "internal/pycore_object.h"
     ],
     # Jac name and C type of each layout the object ports use. Structs a
     # layout embeds by value are emitted too; pointers to anything else are
     # opaque.
     LAYOUTS: list[tuple[str, str]] = [
         ("_object", "struct _object"),
         ("PyVarObject", "PyVarObject"),
         ("PyNumberMethods", "PyNumberMethods"),
         ("PyTypeObject", "struct _typeobject"),
         ("_PyLongValue", "_PyLongValue"),
         ("PyLongObject", "struct _longobject"),
         ("PyTupleObject", "PyTupleObject"),
         ("PyListObject", "PyListObject"),
         ("PyGC_Head", "PyGC_Head"),
         ("PyStatus", "PyStatus"),
         ("PyAsyncMethods", "PyAsyncMethods"),
         ("PySequenceMethods", "PySequenceMethods"),
         ("PyMappingMethods", "PyMappingMethods"),
         ("PyGetSetDef", "struct PyGetSetDef"),
         ("PyCellObject", "PyCellObject"),
         ("PySliceObject", "PySliceObject"),
         ("_PyRangeIterObject", "_PyRangeIterObject"),
         ("_PyTupleIterObject", "_PyTupleIterObject"),
         ("_PyListIterObject", "_PyListIterObject"),
         ("setentry", "setentry"),
         ("PySetObject", "PySetObject"),
         ("PyCFunctionObject", "PyCFunctionObject"),
         ("PyCMethodObject", "PyCMethodObject"),
         ("PyWeakReference", "struct _PyWeakReference"),
         ("PyModuleDef_Base", "PyModuleDef_Base"),
         ("ModuleDef", "struct PyModuleDef"),
         ("PyModuleDef_Slot", "struct PyModuleDef_Slot"),
         ("PyModuleObject", "PyModuleObject"),
         ("PyDictObject", "PyDictObject"),
         ("dictiterobject", "dictiterobject"),
         ("_PyDictViewObject", "_PyDictViewObject"),
         ("PyODictObject", "struct _odictobject"),
         ("_ODictNode", "struct _odictnode"),
         ("odictiterobject", "odictiterobject"),
         ("_PyManagedBufferObject", "_PyManagedBufferObject"),
         ("PyMemoryViewObject", "PyMemoryViewObject"),
         ("memoryiterobject", "memoryiterobject"),
         ("PyDescrObject", "PyDescrObject"),
         ("wrapperbase", "struct wrapperbase"),
         ("mappingproxyobject", "mappingproxyobject"),
         ("wrapperobject", "wrapperobject"),
         ("propertyobject", "propertyobject"),
         ("classmethod", "classmethod"),
         ("PyBaseExceptionObject", "PyBaseExceptionObject"),
         ("PyUnicodeErrorObject", "PyUnicodeErrorObject"),
         ("staticmethod", "staticmethod"),
         ("typevarobject", "typevarobject"),
         ("typevartupleobject", "typevartupleobject"),
         ("paramspecobject", "paramspecobject"),
         ("typealiasobject", "typealiasobject"),
         ("paramspecattrobject", "paramspecattrobject"),
         ("constevaluatorobject", "constevaluatorobject"),
         ("_Py_freelist", "struct _Py_freelist"),
         ("_PyNamespaceObject", "_PyNamespaceObject"),
         ("PyCapsule", "PyCapsule"),
         ("seqiterobject", "seqiterobject"),
         ("calliterobject", "calliterobject"),
         ("anextawaitableobject", "anextawaitableobject"),
         ("enumobject", "enumobject"),
         ("reversedobject", "reversedobject"),
         ("rangeobject", "rangeobject"),
         ("longrangeiterobject", "longrangeiterobject"),
         ("PyDateTime_Delta", "PyDateTime_Delta"),
         ("PyDateTime_TZInfo", "PyDateTime_TZInfo"),
         ("_PyDateTime_BaseTZInfo", "_PyDateTime_BaseTZInfo"),
         ("_PyDateTime_BaseTime", "_PyDateTime_BaseTime"),
         ("PyDateTime_Time", "PyDateTime_Time"),
         ("PyDateTime_Date", "PyDateTime_Date"),
         ("_PyDateTime_BaseDateTime", "_PyDateTime_BaseDateTime"),
         ("PyDateTime_DateTime", "PyDateTime_DateTime"),
         ("PyDateTime_CAPI", "PyDateTime_CAPI"),
         ("Py_buffer", "Py_buffer"),
         ("PyBufferProcs", "PyBufferProcs"),
         ("Py_complex", "Py_complex"),
         ("PyFloatObject", "PyFloatObject"),
         ("PyComplexObject", "PyComplexObject"),
         ("PyMethodObject", "PyMethodObject"),
         ("PyInstanceMethodObject", "PyInstanceMethodObject"),
         ("PyType_Slot", "PyType_Slot"),
         ("PyType_Spec", "PyType_Spec"),
         ("PyStructSequence_Field", "PyStructSequence_Field"),
         ("PyStructSequence_Desc", "PyStructSequence_Desc"),
         ("PyPickleBufferObject", "PyPickleBufferObject"),
         ("interpolationobject", "interpolationobject"),
         ("templateiterobject", "templateiterobject"),
         ("templateobject", "templateobject"),
         ("unionobject", "unionobject"),
         ("gaobject", "gaobject"),
         ("gaiterobject", "gaiterobject"),
         ("PyStdPrinter_Object", "PyStdPrinter_Object"),
         # ssl.SSLError's tp_str reads an OSError's strerror in place.
         ("PyOSErrorObject", "PyOSErrorObject"),
         ("PySocketSockObject", "PySocketSockObject"),
         ("PySocketModule_APIObject", "PySocketModule_APIObject")
     ],
     # Header constants and layout expressions object initializers need: Jac
     # name, the C expression that defines it, and the Jac type of the C
     # field it initializes.
     CONSTANTS: list[tuple[str, str, str]] = [
         (
             "_Py_STATIC_IMMORTAL_INITIAL_REFCNT",
             "_Py_STATIC_IMMORTAL_INITIAL_REFCNT",
             "i64"
         ),
         ("_Py_IMMORTAL_INITIAL_REFCNT", "_Py_IMMORTAL_INITIAL_REFCNT", "i64"),
         ("Py_TPFLAGS_DEFAULT", "Py_TPFLAGS_DEFAULT", "u64"),
         ("Py_TPFLAGS_TUPLE_SUBCLASS", "Py_TPFLAGS_TUPLE_SUBCLASS", "u64"),
         ("Py_TPFLAGS_LIST_SUBCLASS", "Py_TPFLAGS_LIST_SUBCLASS", "u64"),
         ("Py_TPFLAGS_HAVE_GC", "Py_TPFLAGS_HAVE_GC", "u64"),
         ("Py_TPFLAGS_MAPPING", "Py_TPFLAGS_MAPPING", "u64"),
         ("Py_TPFLAGS_BASETYPE", "Py_TPFLAGS_BASETYPE", "u64"),
         ("Py_TPFLAGS_SEQUENCE", "Py_TPFLAGS_SEQUENCE", "u64"),
         ("_PyLong_FALSE_TAG", "_PyLong_FALSE_TAG", "u64"),
         ("_PyLong_TRUE_TAG", "_PyLong_TRUE_TAG", "u64"),
         (
             "PyLong_DIGITS_OFFSET",
             "offsetof(struct _longobject, long_value.ob_digit)",
             "i64"
         ),
         ("PyLong_DIGIT_SIZE", "sizeof(digit)", "i64"),
         ("_PyStatus_TYPE_OK", "_PyStatus_TYPE_OK", "u32"),
         ("_PyStatus_TYPE_ERROR", "_PyStatus_TYPE_ERROR", "u32"),
         ("PY_BUFFER_SIZE", "sizeof(Py_buffer)", "u64"),
         ("PY_OBJECT_SIZE", "sizeof(PyObject)", "i64"),
         ("PY_TUPLE_OBJECT_SIZE", "sizeof(PyTupleObject)", "i64"),
         ("Py_TPFLAGS_IMMUTABLETYPE", "Py_TPFLAGS_IMMUTABLETYPE", "u64"),
         ("Py_TPFLAGS_MANAGED_DICT", "Py_TPFLAGS_MANAGED_DICT", "u64"),
         ("Py_TPFLAGS_INLINE_VALUES", "Py_TPFLAGS_INLINE_VALUES", "u64"),
         (
             "PyHeapTypeObject_CACHED_KEYS",
             "offsetof(PyHeapTypeObject, ht_cached_keys)",
             "i64"
         ),
         ("Py_TPFLAGS_MANAGED_WEAKREF", "Py_TPFLAGS_MANAGED_WEAKREF", "u64"),
         (
             "Py_TPFLAGS_DISALLOW_INSTANTIATION",
             "Py_TPFLAGS_DISALLOW_INSTANTIATION",
             "u64"
         ),
         # Method table flags, member types and rich comparison operators.
         ("METH_VARARGS", "METH_VARARGS", "i32"),
         ("METH_KEYWORDS", "METH_KEYWORDS", "i32"),
         ("METH_NOARGS", "METH_NOARGS", "i32"),
         ("METH_O", "METH_O", "i32"),
         ("METH_CLASS", "METH_CLASS", "i32"),
         ("METH_COEXIST", "METH_COEXIST", "i32"),
         ("Py_T_OBJECT_EX", "Py_T_OBJECT_EX", "i32"),
         ("_Py_T_OBJECT", "_Py_T_OBJECT", "i32"),
         ("Py_READONLY", "Py_READONLY", "i32"),
         ("Py_LT", "Py_LT", "i32"),
         ("Py_LE", "Py_LE", "i32"),
         ("Py_EQ", "Py_EQ", "i32"),
         ("Py_NE", "Py_NE", "i32"),
         ("Py_GT", "Py_GT", "i32"),
         ("Py_GE", "Py_GE", "i32"),
         ("PY_ITERSEARCH_COUNT", "PY_ITERSEARCH_COUNT", "i32"),
         ("PY_ITERSEARCH_INDEX", "PY_ITERSEARCH_INDEX", "i32"),
         ("PY_ITERSEARCH_CONTAINS", "PY_ITERSEARCH_CONTAINS", "i32"),
         # Object sizes (tp_basicsize) and member offsets (PyMemberDef).
         ("PyTupleObject_ITEMS", "offsetof(PyTupleObject, ob_item)", "i64"),
         ("PyCellObject_SIZE", "sizeof(PyCellObject)", "i64"),
         ("PySliceObject_SIZE", "sizeof(PySliceObject)", "i64"),
         ("PySliceObject_START", "offsetof(PySliceObject, start)", "i64"),
         ("PySliceObject_STOP", "offsetof(PySliceObject, stop)", "i64"),
         ("PySliceObject_STEP", "offsetof(PySliceObject, step)", "i64"),
         ("_PyRangeIterObject_SIZE", "sizeof(_PyRangeIterObject)", "i64"),
         ("_PyTupleIterObject_SIZE", "sizeof(_PyTupleIterObject)", "i64"),
         ("PyListObject_SIZE", "sizeof(PyListObject)", "i64"),
         ("_PyListIterObject_SIZE", "sizeof(_PyListIterObject)", "i64"),
         # What list.extend() and list.sort() read of dicts, sets, str and int.
         ("PyDictObject_USED", "offsetof(PyDictObject, ma_used)", "i64"),
         ("PySetObject_USED", "offsetof(PySetObject, used)", "i64"),
         ("PySetObject_SIZE", "sizeof(PySetObject)", "i64"),
         ("PyFloatObject_SIZE", "sizeof(PyFloatObject)", "i64"),
         ("PyCFunctionObject_SIZE", "sizeof(PyCFunctionObject)", "i64"),
         ("PyCMethodObject_SIZE", "sizeof(PyCMethodObject)", "i64"),
         ("PyCFunctionObject_MODULE", "offsetof(PyCFunctionObject, m_module)", "i64"),
         (
             "PyCFunctionObject_WEAKREFLIST",
             "offsetof(PyCFunctionObject, m_weakreflist)",
             "i64"
         ),
         (
             "PyCFunctionObject_VECTORCALL",
             "offsetof(PyCFunctionObject, vectorcall)",
             "i64"
         ),
         ("METH_METHOD", "METH_METHOD", "i32"),
         ("PyWeakReference_SIZE", "sizeof(PyWeakReference)", "i64"),
         ("PyWeakReference_CALLBACK", "offsetof(PyWeakReference, wr_callback)", "i64"),
         ("PyWeakReference_VECTORCALL", "offsetof(PyWeakReference, vectorcall)", "i64"),
         (
             "managed_static_type_state_TP_WEAKLIST",
             "offsetof(managed_static_type_state, tp_weaklist)",
             "i64"
         ),
         ("Py_TPFLAGS_TYPE_SUBCLASS", "Py_TPFLAGS_TYPE_SUBCLASS", "u64"),
         ("Py_TPFLAGS_DICT_SUBCLASS", "Py_TPFLAGS_DICT_SUBCLASS", "u64"),
         ("PyModuleDef_SIZE", "sizeof(PyModuleDef)", "i64"),
         ("PyModuleObject_SIZE", "sizeof(PyModuleObject)", "i64"),
         ("PyModuleObject_DICT", "offsetof(PyModuleObject, md_dict)", "i64"),
         ("PyModuleObject_WEAKLIST", "offsetof(PyModuleObject, md_weaklist)", "i64"),
         ("PyDictObject_SIZE", "sizeof(PyDictObject)", "i64"),
         ("PyDictKeysObject_REFCNT", "offsetof(PyDictKeysObject, dk_refcnt)", "i64"),
         (
             "PyDictKeysObject_LOG2_SIZE",
             "offsetof(PyDictKeysObject, dk_log2_size)",
             "i64"
         ),
         (
             "PyDictKeysObject_LOG2_INDEX_BYTES",
             "offsetof(PyDictKeysObject, dk_log2_index_bytes)",
             "i64"
         ),
         ("PyDictKeysObject_KIND", "offsetof(PyDictKeysObject, dk_kind)", "i64"),
         ("PyDictKeysObject_VERSION", "offsetof(PyDictKeysObject, dk_version)", "i64"),
         ("PyDictKeysObject_USABLE", "offsetof(PyDictKeysObject, dk_usable)", "i64"),
         (
             "PyDictKeysObject_NENTRIES",
             "offsetof(PyDictKeysObject, dk_nentries)",
             "i64"
         ),
         ("PyDictKeysObject_INDICES", "offsetof(PyDictKeysObject, dk_indices)", "i64"),
         ("PyDictValues_VALUES", "offsetof(PyDictValues, values)", "i64"),
         ("dictiterobject_SIZE", "sizeof(dictiterobject)", "i64"),
         ("_PyDictViewObject_SIZE", "sizeof(_PyDictViewObject)", "i64"),
         ("_Py_freelists_DICTS", "offsetof(struct _Py_freelists, dicts)", "i64"),
         ("_Py_freelists_DICTKEYS", "offsetof(struct _Py_freelists, dictkeys)", "i64"),
         ("Py_dicts_MAXFREELIST", "Py_dicts_MAXFREELIST", "i64"),
         ("Py_dictkeys_MAXFREELIST", "Py_dictkeys_MAXFREELIST", "i64"),
         ("_Py_TYPE_VERSION_DICT", "_Py_TYPE_VERSION_DICT", "u32"),
         ("PyODictObject_SIZE", "sizeof(struct _odictobject)", "i64"),
         (
             "PyODictObject_WEAKREFLIST",
             "offsetof(struct _odictobject, od_weakreflist)",
             "i64"
         ),
         (
             "PyODictObject_INST_DICT",
             "offsetof(struct _odictobject, od_inst_dict)",
             "i64"
         ),
         ("_ODictNode_SIZE", "sizeof(struct _odictnode)", "i64"),
         ("odictiterobject_SIZE", "sizeof(odictiterobject)", "i64"),
         ("PyDescrObject_TYPE", "offsetof(PyDescrObject, d_type)", "i64"),
         ("PyDescrObject_NAME", "offsetof(PyDescrObject, d_name)", "i64"),
         ("PyMethodDescrObject_SIZE", "sizeof(PyMethodDescrObject)", "i64"),
         (
             "PyMethodDescrObject_VECTORCALL",
             "offsetof(PyMethodDescrObject, vectorcall)",
             "i64"
         ),
         (
             "PyMethodDescrObject_METHOD",
             "offsetof(PyMethodDescrObject, d_method)",
             "i64"
         ),
         ("PyMemberDescrObject_SIZE", "sizeof(PyMemberDescrObject)", "i64"),
         (
             "PyMemberDescrObject_MEMBER",
             "offsetof(PyMemberDescrObject, d_member)",
             "i64"
         ),
         (
             "PyGetSetDescrObject_GETSET",
             "offsetof(PyGetSetDescrObject, d_getset)",
             "i64"
         ),
         ("PyWrapperDescrObject_BASE", "offsetof(PyWrapperDescrObject, d_base)", "i64"),
         (
             "PyWrapperDescrObject_WRAPPED",
             "offsetof(PyWrapperDescrObject, d_wrapped)",
             "i64"
         ),
         ("PyGetSetDescrObject_SIZE", "sizeof(PyGetSetDescrObject)", "i64"),
         ("PyWrapperDescrObject_SIZE", "sizeof(PyWrapperDescrObject)", "i64"),
         ("mappingproxyobject_SIZE", "sizeof(mappingproxyobject)", "i64"),
         ("wrapperobject_SIZE", "sizeof(wrapperobject)", "i64"),
         ("wrapperobject_SELF", "offsetof(wrapperobject, self)", "i64"),
         ("propertyobject_SIZE", "sizeof(propertyobject)", "i64"),
         ("propertyobject_GET", "offsetof(propertyobject, prop_get)", "i64"),
         ("propertyobject_SET", "offsetof(propertyobject, prop_set)", "i64"),
         ("propertyobject_DEL", "offsetof(propertyobject, prop_del)", "i64"),
         ("propertyobject_DOC", "offsetof(propertyobject, prop_doc)", "i64"),
         ("Py_AUDIT_READ", "Py_AUDIT_READ", "i32"),
         ("Py_RELATIVE_OFFSET", "Py_RELATIVE_OFFSET", "i32"),
         ("PyWrapperFlag_KEYWORDS", "PyWrapperFlag_KEYWORDS", "i32"),
         ("Py_TPFLAGS_METHOD_DESCRIPTOR", "Py_TPFLAGS_METHOD_DESCRIPTOR", "u64"),
         ("PyFunctionObject_SIZE", "sizeof(PyFunctionObject)", "i64"),
         (
             "PyFunctionObject_GLOBALS",
             "offsetof(PyFunctionObject, func_globals)",
             "i64"
         ),
         (
             "PyFunctionObject_BUILTINS",
             "offsetof(PyFunctionObject, func_builtins)",
             "i64"
         ),
         ("PyFunctionObject_NAME", "offsetof(PyFunctionObject, func_name)", "i64"),
         (
             "PyFunctionObject_QUALNAME",
             "offsetof(PyFunctionObject, func_qualname)",
             "i64"
         ),
         ("PyFunctionObject_CODE", "offsetof(PyFunctionObject, func_code)", "i64"),
         (
             "PyFunctionObject_DEFAULTS",
             "offsetof(PyFunctionObject, func_defaults)",
             "i64"
         ),
         (
             "PyFunctionObject_KWDEFAULTS",
             "offsetof(PyFunctionObject, func_kwdefaults)",
             "i64"
         ),
         (
             "PyFunctionObject_CLOSURE",
             "offsetof(PyFunctionObject, func_closure)",
             "i64"
         ),
         ("PyFunctionObject_DOC", "offsetof(PyFunctionObject, func_doc)", "i64"),
         ("PyFunctionObject_DICT", "offsetof(PyFunctionObject, func_dict)", "i64"),
         (
             "PyFunctionObject_WEAKREFLIST",
             "offsetof(PyFunctionObject, func_weakreflist)",
             "i64"
         ),
         ("PyFunctionObject_MODULE", "offsetof(PyFunctionObject, func_module)", "i64"),
         (
             "PyFunctionObject_ANNOTATIONS",
             "offsetof(PyFunctionObject, func_annotations)",
             "i64"
         ),
         (
             "PyFunctionObject_ANNOTATE",
             "offsetof(PyFunctionObject, func_annotate)",
             "i64"
         ),
         (
             "PyFunctionObject_TYPEPARAMS",
             "offsetof(PyFunctionObject, func_typeparams)",
             "i64"
         ),
         (
             "PyFunctionObject_VECTORCALL",
             "offsetof(PyFunctionObject, vectorcall)",
             "i64"
         ),
         (
             "PyFunctionObject_VERSION",
             "offsetof(PyFunctionObject, func_version)",
             "i64"
         ),
         (
             "PyFrameConstructor_GLOBALS",
             "offsetof(PyFrameConstructor, fc_globals)",
             "i64"
         ),
         (
             "PyFrameConstructor_BUILTINS",
             "offsetof(PyFrameConstructor, fc_builtins)",
             "i64"
         ),
         ("PyFrameConstructor_NAME", "offsetof(PyFrameConstructor, fc_name)", "i64"),
         (
             "PyFrameConstructor_QUALNAME",
             "offsetof(PyFrameConstructor, fc_qualname)",
             "i64"
         ),
         ("PyFrameConstructor_CODE", "offsetof(PyFrameConstructor, fc_code)", "i64"),
         (
             "PyFrameConstructor_DEFAULTS",
             "offsetof(PyFrameConstructor, fc_defaults)",
             "i64"
         ),
         (
             "PyFrameConstructor_KWDEFAULTS",
             "offsetof(PyFrameConstructor, fc_kwdefaults)",
             "i64"
         ),
         (
             "PyFrameConstructor_CLOSURE",
             "offsetof(PyFrameConstructor, fc_closure)",
             "i64"
         ),
         ("PyCodeObject_NAME", "offsetof(PyCodeObject, co_name)", "i64"),
         ("PyCodeObject_QUALNAME", "offsetof(PyCodeObject, co_qualname)", "i64"),
         ("PyCodeObject_CONSTS", "offsetof(PyCodeObject, co_consts)", "i64"),
         ("PyCodeObject_FLAGS", "offsetof(PyCodeObject, co_flags)", "i64"),
         ("PyCodeObject_NFREEVARS", "offsetof(PyCodeObject, co_nfreevars)", "i64"),
         ("PyCodeObject_VERSION", "offsetof(PyCodeObject, co_version)", "i64"),
         ("classmethod_SIZE", "sizeof(classmethod)", "i64"),
         ("classmethod_CALLABLE", "offsetof(classmethod, cm_callable)", "i64"),
         ("classmethod_DICT", "offsetof(classmethod, cm_dict)", "i64"),
         ("staticmethod_SIZE", "sizeof(staticmethod)", "i64"),
         ("staticmethod_CALLABLE", "offsetof(staticmethod, sm_callable)", "i64"),
         ("staticmethod_DICT", "offsetof(staticmethod, sm_dict)", "i64"),
         ("CO_HAS_DOCSTRING", "CO_HAS_DOCSTRING", "i32"),
         ("CO_GENERATOR", "CO_GENERATOR", "i32"),
         ("CO_COROUTINE", "CO_COROUTINE", "i32"),
         ("CO_ASYNC_GENERATOR", "CO_ASYNC_GENERATOR", "i32"),
         ("FUNC_MAX_WATCHERS", "FUNC_MAX_WATCHERS", "i64"),
         ("FUNC_VERSION_CACHE_SIZE", "FUNC_VERSION_CACHE_SIZE", "i64"),
         ("Py_TPFLAGS_BASE_EXC_SUBCLASS", "Py_TPFLAGS_BASE_EXC_SUBCLASS", "u64"),
         ("_Py_ANNOTATE_FORMAT_STRING", "_Py_ANNOTATE_FORMAT_STRING", "i32"),
         ("PyObject_HEAD_SIZE", "sizeof(PyObject)", "i64"),
         ("typevarobject_SIZE", "sizeof(typevarobject)", "i64"),
         ("typevarobject_NAME", "offsetof(typevarobject, name)", "i64"),
         ("typevarobject_BOUND", "offsetof(typevarobject, bound)", "i64"),
         (
             "typevarobject_EVALUATE_BOUND",
             "offsetof(typevarobject, evaluate_bound)",
             "i64"
         ),
         ("typevarobject_CONSTRAINTS", "offsetof(typevarobject, constraints)", "i64"),
         (
             "typevarobject_EVALUATE_CONSTRAINTS",
             "offsetof(typevarobject, evaluate_constraints)",
             "i64"
         ),
         (
             "typevarobject_DEFAULT_VALUE",
             "offsetof(typevarobject, default_value)",
             "i64"
         ),
         (
             "typevarobject_EVALUATE_DEFAULT",
             "offsetof(typevarobject, evaluate_default)",
             "i64"
         ),
         ("typevarobject_COVARIANT", "offsetof(typevarobject, covariant)", "i64"),
         (
             "typevarobject_CONTRAVARIANT",
             "offsetof(typevarobject, contravariant)",
             "i64"
         ),
         (
             "typevarobject_INFER_VARIANCE",
             "offsetof(typevarobject, infer_variance)",
             "i64"
         ),
         ("typevartupleobject_SIZE", "sizeof(typevartupleobject)", "i64"),
         ("typevartupleobject_NAME", "offsetof(typevartupleobject, name)", "i64"),
         (
             "typevartupleobject_DEFAULT_VALUE",
             "offsetof(typevartupleobject, default_value)",
             "i64"
         ),
         (
             "typevartupleobject_EVALUATE_DEFAULT",
             "offsetof(typevartupleobject, evaluate_default)",
             "i64"
         ),
         ("paramspecobject_SIZE", "sizeof(paramspecobject)", "i64"),
         ("paramspecobject_NAME", "offsetof(paramspecobject, name)", "i64"),
         ("paramspecobject_BOUND", "offsetof(paramspecobject, bound)", "i64"),
         (
             "paramspecobject_DEFAULT_VALUE",
             "offsetof(paramspecobject, default_value)",
             "i64"
         ),
         (
             "paramspecobject_EVALUATE_DEFAULT",
             "offsetof(paramspecobject, evaluate_default)",
             "i64"
         ),
         ("paramspecobject_COVARIANT", "offsetof(paramspecobject, covariant)", "i64"),
         (
             "paramspecobject_CONTRAVARIANT",
             "offsetof(paramspecobject, contravariant)",
             "i64"
         ),
         (
             "paramspecobject_INFER_VARIANCE",
             "offsetof(paramspecobject, infer_variance)",
             "i64"
         ),
         ("typealiasobject_SIZE", "sizeof(typealiasobject)", "i64"),
         ("typealiasobject_NAME", "offsetof(typealiasobject, name)", "i64"),
         (
             "typealiasobject_TYPE_PARAMS",
             "offsetof(typealiasobject, type_params)",
             "i64"
         ),
         (
             "typealiasobject_COMPUTE_VALUE",
             "offsetof(typealiasobject, compute_value)",
             "i64"
         ),
         ("typealiasobject_VALUE", "offsetof(typealiasobject, value)", "i64"),
         ("typealiasobject_MODULE", "offsetof(typealiasobject, module)", "i64"),
         ("constevaluatorobject_SIZE", "sizeof(constevaluatorobject)", "i64"),
         ("constevaluatorobject_VALUE", "offsetof(constevaluatorobject, value)", "i64"),
         ("paramspecattrobject_SIZE", "sizeof(paramspecattrobject)", "i64"),
         (
             "paramspecattrobject_ORIGIN",
             "offsetof(paramspecattrobject, __origin__)",
             "i64"
         ),
         (
             "PyBaseExceptionObject_SUPPRESS_CONTEXT",
             "offsetof(PyBaseExceptionObject, suppress_context)",
             "i64"
         ),
         ("PyBaseExceptionObject_SIZE", "sizeof(PyBaseExceptionObject)", "i64"),
         ("PyBaseExceptionObject_DICT", "offsetof(PyBaseExceptionObject, dict)", "i64"),
         ("PyStopIterationObject_SIZE", "sizeof(PyStopIterationObject)", "i64"),
         ("PyStopIterationObject_DICT", "offsetof(PyStopIterationObject, dict)", "i64"),
         (
             "PyStopIterationObject_VALUE",
             "offsetof(PyStopIterationObject, value)",
             "i64"
         ),
         ("PySystemExitObject_SIZE", "sizeof(PySystemExitObject)", "i64"),
         ("PySystemExitObject_DICT", "offsetof(PySystemExitObject, dict)", "i64"),
         ("PySystemExitObject_CODE", "offsetof(PySystemExitObject, code)", "i64"),
         (
             "PyBaseExceptionGroupObject_SIZE",
             "sizeof(PyBaseExceptionGroupObject)",
             "i64"
         ),
         (
             "PyBaseExceptionGroupObject_DICT",
             "offsetof(PyBaseExceptionGroupObject, dict)",
             "i64"
         ),
         (
             "PyBaseExceptionGroupObject_MSG",
             "offsetof(PyBaseExceptionGroupObject, msg)",
             "i64"
         ),
         (
             "PyBaseExceptionGroupObject_EXCS",
             "offsetof(PyBaseExceptionGroupObject, excs)",
             "i64"
         ),
         (
             "PyBaseExceptionGroupObject_EXCS_STR",
             "offsetof(PyBaseExceptionGroupObject, excs_str)",
             "i64"
         ),
         ("PyImportErrorObject_SIZE", "sizeof(PyImportErrorObject)", "i64"),
         ("PyImportErrorObject_DICT", "offsetof(PyImportErrorObject, dict)", "i64"),
         ("PyImportErrorObject_MSG", "offsetof(PyImportErrorObject, msg)", "i64"),
         ("PyImportErrorObject_NAME", "offsetof(PyImportErrorObject, name)", "i64"),
         ("PyImportErrorObject_PATH", "offsetof(PyImportErrorObject, path)", "i64"),
         (
             "PyImportErrorObject_NAME_FROM",
             "offsetof(PyImportErrorObject, name_from)",
             "i64"
         ),
         ("PyOSErrorObject_SIZE", "sizeof(PyOSErrorObject)", "i64"),
         ("PyOSErrorObject_DICT", "offsetof(PyOSErrorObject, dict)", "i64"),
         ("PyOSErrorObject_MYERRNO", "offsetof(PyOSErrorObject, myerrno)", "i64"),
         ("PyOSErrorObject_STRERROR", "offsetof(PyOSErrorObject, strerror)", "i64"),
         ("PyOSErrorObject_FILENAME", "offsetof(PyOSErrorObject, filename)", "i64"),
         ("PyOSErrorObject_FILENAME2", "offsetof(PyOSErrorObject, filename2)", "i64"),
         ("PyNameErrorObject_SIZE", "sizeof(PyNameErrorObject)", "i64"),
         ("PyNameErrorObject_DICT", "offsetof(PyNameErrorObject, dict)", "i64"),
         ("PyNameErrorObject_NAME", "offsetof(PyNameErrorObject, name)", "i64"),
         ("PyAttributeErrorObject_SIZE", "sizeof(PyAttributeErrorObject)", "i64"),
         (
             "PyAttributeErrorObject_DICT",
             "offsetof(PyAttributeErrorObject, dict)",
             "i64"
         ),
         (
             "PyAttributeErrorObject_NAME",
             "offsetof(PyAttributeErrorObject, name)",
             "i64"
         ),
         ("PyAttributeErrorObject_OBJ", "offsetof(PyAttributeErrorObject, obj)", "i64"),
         ("PySyntaxErrorObject_SIZE", "sizeof(PySyntaxErrorObject)", "i64"),
         ("PySyntaxErrorObject_DICT", "offsetof(PySyntaxErrorObject, dict)", "i64"),
         ("PySyntaxErrorObject_MSG", "offsetof(PySyntaxErrorObject, msg)", "i64"),
         (
             "PySyntaxErrorObject_FILENAME",
             "offsetof(PySyntaxErrorObject, filename)",
             "i64"
         ),
         ("PySyntaxErrorObject_LINENO", "offsetof(PySyntaxErrorObject, lineno)", "i64"),
         ("PySyntaxErrorObject_OFFSET", "offsetof(PySyntaxErrorObject, offset)", "i64"),
         (
             "PySyntaxErrorObject_END_LINENO",
             "offsetof(PySyntaxErrorObject, end_lineno)",
             "i64"
         ),
         (
             "PySyntaxErrorObject_END_OFFSET",
             "offsetof(PySyntaxErrorObject, end_offset)",
             "i64"
         ),
         ("PySyntaxErrorObject_TEXT", "offsetof(PySyntaxErrorObject, text)", "i64"),
         (
             "PySyntaxErrorObject_PRINT_FILE_AND_LINE",
             "offsetof(PySyntaxErrorObject, print_file_and_line)",
             "i64"
         ),
         (
             "PySyntaxErrorObject_METADATA",
             "offsetof(PySyntaxErrorObject, metadata)",
             "i64"
         ),
         ("PyUnicodeErrorObject_SIZE", "sizeof(PyUnicodeErrorObject)", "i64"),
         ("PyUnicodeErrorObject_DICT", "offsetof(PyUnicodeErrorObject, dict)", "i64"),
         (
             "PyUnicodeErrorObject_ENCODING",
             "offsetof(PyUnicodeErrorObject, encoding)",
             "i64"
         ),
         (
             "PyUnicodeErrorObject_OBJECT",
             "offsetof(PyUnicodeErrorObject, object)",
             "i64"
         ),
         ("PyUnicodeErrorObject_START", "offsetof(PyUnicodeErrorObject, start)", "i64"),
         ("PyUnicodeErrorObject_END", "offsetof(PyUnicodeErrorObject, end)", "i64"),
         (
             "PyUnicodeErrorObject_REASON",
             "offsetof(PyUnicodeErrorObject, reason)",
             "i64"
         ),
         ("Py_DTSF_ADD_DOT_0", "Py_DTSF_ADD_DOT_0", "i32"),
         ("Py_TPFLAGS_LONG_SUBCLASS", "Py_TPFLAGS_LONG_SUBCLASS", "u64"),
         ("Py_TPFLAGS_BYTES_SUBCLASS", "Py_TPFLAGS_BYTES_SUBCLASS", "u64"),
         ("Py_TPFLAGS_UNICODE_SUBCLASS", "Py_TPFLAGS_UNICODE_SUBCLASS", "u64"),
         ("PySetObject_SMALLTABLE", "offsetof(PySetObject, smalltable)", "i64"),
         ("PySetObject_WEAKREFLIST", "offsetof(PySetObject, weakreflist)", "i64"),
         ("PySet_MINSIZE", "PySet_MINSIZE", "i64"),
         ("PyASCIIObject_HASH", "offsetof(PyASCIIObject, hash)", "i64"),
         ("_PyDictViewObject_DICT", "offsetof(_PyDictViewObject, dv_dict)", "i64"),
         ("PyASCIIObject_LENGTH", "offsetof(PyASCIIObject, length)", "i64"),
         ("PyLongObject_TAG", "offsetof(PyLongObject, long_value.lv_tag)", "i64"),
         ("PyLongObject_DIGIT", "offsetof(PyLongObject, long_value.ob_digit)", "i64"),
         ("_PyLong_NON_SIZE_BITS", "_PyLong_NON_SIZE_BITS", "u64"),
         ("_PyLong_SIGN_MASK", "_PyLong_SIGN_MASK", "u64"),
         ("_PyNamespaceObject_SIZE", "sizeof(_PyNamespaceObject)", "i64"),
         ("_PyNamespaceObject_NS_DICT", "offsetof(_PyNamespaceObject, ns_dict)", "i64"),
         ("PyCapsule_SIZE", "sizeof(PyCapsule)", "i64"),
         ("seqiterobject_SIZE", "sizeof(seqiterobject)", "i64"),
         ("calliterobject_SIZE", "sizeof(calliterobject)", "i64"),
         ("anextawaitableobject_SIZE", "sizeof(anextawaitableobject)", "i64"),
         ("enumobject_SIZE", "sizeof(enumobject)", "i64"),
         ("reversedobject_SIZE", "sizeof(reversedobject)", "i64"),
         ("rangeobject_SIZE", "sizeof(rangeobject)", "i64"),
         ("rangeobject_START", "offsetof(rangeobject, start)", "i64"),
         ("rangeobject_STOP", "offsetof(rangeobject, stop)", "i64"),
         ("rangeobject_STEP", "offsetof(rangeobject, step)", "i64"),
         ("longrangeiterobject_SIZE", "sizeof(longrangeiterobject)", "i64"),
         # The interpreter's freelists: where each list sits in
         # struct _Py_freelists and how many objects it keeps.
         # The interpreter state a port reaches from the current thread
         # state: its freelists and its GC state (generation 0's list head
         # and heap size), as _Py_freelists_GET and _PyObject_GC_TRACK do.
         ("PyThreadState_INTERP", "offsetof(PyThreadState, interp)", "i64"),
         (
             "_gc_runtime_state_GENERATION0",
             "offsetof(struct _gc_runtime_state, generation0)",
             "i64"
         ),
         (
             "_gc_runtime_state_HEAP_SIZE",
             "offsetof(struct _gc_runtime_state, heap_size)",
             "i64"
         ),
         ("PyGC_Head_SIZE", "sizeof(PyGC_Head)", "i64"),
         ("_PyGC_PREV_MASK_FINALIZED", "_PyGC_PREV_MASK_FINALIZED", "i64"),
         ("_PyGC_PREV_MASK", "(Py_ssize_t)_PyGC_PREV_MASK", "i64"),
         ("_PyGC_PREV_FLAGS", "(Py_ssize_t)~_PyGC_PREV_MASK", "i64"),
         ("_Py_freelists_TUPLES", "offsetof(struct _Py_freelists, tuples)", "i64"),
         (
             "_Py_freelists_TUPLE_ITERS",
             "offsetof(struct _Py_freelists, tuple_iters)",
             "i64"
         ),
         ("_Py_freelist_SIZE", "sizeof(struct _Py_freelist)", "i64"),
         ("PyTuple_MAXSAVESIZE", "PyTuple_MAXSAVESIZE", "i64"),
         ("Py_tuple_MAXFREELIST", "Py_tuple_MAXFREELIST", "i64"),
         ("Py_tuple_iters_MAXFREELIST", "Py_tuple_iters_MAXFREELIST", "i64"),
         ("_Py_freelists_LISTS", "offsetof(struct _Py_freelists, lists)", "i64"),
         (
             "_Py_freelists_LIST_ITERS",
             "offsetof(struct _Py_freelists, list_iters)",
             "i64"
         ),
         ("Py_lists_MAXFREELIST", "Py_lists_MAXFREELIST", "i64"),
         ("Py_list_iters_MAXFREELIST", "Py_list_iters_MAXFREELIST", "i64"),
         ("_Py_freelists_FLOATS", "offsetof(struct _Py_freelists, floats)", "i64"),
         ("Py_floats_MAXFREELIST", "Py_floats_MAXFREELIST", "i64"),
         ("PyLongObject_SIZE", "sizeof(PyLongObject)", "i64"),
         ("_Py_freelists_INTS", "offsetof(struct _Py_freelists, ints)", "i64"),
         ("Py_ints_MAXFREELIST", "Py_ints_MAXFREELIST", "i64"),
         ("_Py_TYPE_VERSION_INT", "_Py_TYPE_VERSION_INT", "u32"),
         ("PyLongExport_SIZE", "sizeof(PyLongExport)", "i64"),
         ("_PyUnicodeWriter_BUFFER", "offsetof(_PyUnicodeWriter, buffer)", "i64"),
         ("_PyUnicodeWriter_KIND", "offsetof(_PyUnicodeWriter, kind)", "i64"),
         ("_PyUnicodeWriter_MAXCHAR", "offsetof(_PyUnicodeWriter, maxchar)", "i64"),
         ("_PyUnicodeWriter_SIZE_FIELD", "offsetof(_PyUnicodeWriter, size)", "i64"),
         ("_PyUnicodeWriter_POS", "offsetof(_PyUnicodeWriter, pos)", "i64"),
         (
             "_Py_freelists_PYCFUNCTIONOBJECT",
             "offsetof(struct _Py_freelists, pycfunctionobject)",
             "i64"
         ),
         (
             "_Py_freelists_PYCMETHODOBJECT",
             "offsetof(struct _Py_freelists, pycmethodobject)",
             "i64"
         ),
         (
             "Py_pycfunctionobject_MAXFREELIST",
             "Py_pycfunctionobject_MAXFREELIST",
             "i64"
         ),
         ("Py_pycmethodobject_MAXFREELIST", "Py_pycmethodobject_MAXFREELIST", "i64"),
         ("_Py_freelists_SLICES", "offsetof(struct _Py_freelists, slices)", "i64"),
         ("_Py_freelists_RANGES", "offsetof(struct _Py_freelists, ranges)", "i64"),
         (
             "_Py_freelists_RANGE_ITERS",
             "offsetof(struct _Py_freelists, range_iters)",
             "i64"
         ),
         (
             "_Py_freelists_PYMETHODOBJECTS",
             "offsetof(struct _Py_freelists, pymethodobjects)",
             "i64"
         ),
         ("Py_pymethodobjects_MAXFREELIST", "Py_pymethodobjects_MAXFREELIST", "i64"),
         (
             "_Py_freelists_FUTUREITERS",
             "offsetof(struct _Py_freelists, futureiters)",
             "i64"
         ),
         ("Py_futureiters_MAXFREELIST", "Py_futureiters_MAXFREELIST", "i64"),
         # PySendResult, the result of an am_send slot and PyIter_Send().
         ("PYGEN_RETURN", "PYGEN_RETURN", "i32"),
         ("PYGEN_ERROR", "PYGEN_ERROR", "i32"),
         ("PYGEN_NEXT", "PYGEN_NEXT", "i32"),
         # Type flags, member types and call and buffer constants of the
         # second object wave.
         ("Py_TPFLAGS_HAVE_VECTORCALL", "Py_TPFLAGS_HAVE_VECTORCALL", "u64"),
         ("Py_TPFLAGS_HEAPTYPE", "Py_TPFLAGS_HEAPTYPE", "u64"),
         ("Py_TPFLAGS_READY", "Py_TPFLAGS_READY", "u64"),
         ("_Py_TPFLAGS_STATIC_BUILTIN", "_Py_TPFLAGS_STATIC_BUILTIN", "u64"),
         ("_Py_TYPE_VERSION_COMPLEX", "_Py_TYPE_VERSION_COMPLEX", "u32"),
         ("_Py_TYPE_VERSION_TUPLE", "_Py_TYPE_VERSION_TUPLE", "u32"),
         ("_Py_TYPE_VERSION_LIST", "_Py_TYPE_VERSION_LIST", "u32"),
         ("_Py_TYPE_VERSION_SET", "_Py_TYPE_VERSION_SET", "u32"),
         ("_Py_TYPE_VERSION_FLOAT", "_Py_TYPE_VERSION_FLOAT", "u32"),
         ("_Py_TYPE_VERSION_FROZEN_SET", "_Py_TYPE_VERSION_FROZEN_SET", "u32"),
         ("_Py_TPFLAGS_MATCH_SELF", "_Py_TPFLAGS_MATCH_SELF", "u64"),
         ("Py_T_DOUBLE", "Py_T_DOUBLE", "i32"),
         ("Py_T_BOOL", "Py_T_BOOL", "i32"),
         ("Py_tp_members", "Py_tp_members", "i32"),
         ("PyBUF_FULL_RO", "PyBUF_FULL_RO", "i32"),
         ("Py_DTSF_SIGN", "Py_DTSF_SIGN", "i32"),
         ("Py_PRINT_RAW", "Py_PRINT_RAW", "i32"),
         ("PyHASH_IMAG", "_PyHASH_IMAG", "u64"),
         ("FVC_STR", "FVC_STR", "i32"),
         ("FVC_REPR", "FVC_REPR", "i32"),
         ("FVC_ASCII", "FVC_ASCII", "i32"),
         ("PY_VECTORCALL_ARGUMENTS_OFFSET", "PY_VECTORCALL_ARGUMENTS_OFFSET", "u64"),
         ("_Py_MEMORYVIEW_C", "_Py_MEMORYVIEW_C", "i32"),
         ("_Py_MEMORYVIEW_FORTRAN", "_Py_MEMORYVIEW_FORTRAN", "i32"),
         ("PyMemoryViewObject_VIEW", "offsetof(PyMemoryViewObject, view)", "i64"),
         ("PyMemoryViewObject_FLAGS", "offsetof(PyMemoryViewObject, flags)", "i64"),
         ("_PyManagedBufferObject_SIZE", "sizeof(_PyManagedBufferObject)", "i64"),
         ("_PyManagedBufferObject_MASTER", "offsetof(_PyManagedBufferObject, master)", "i64"),
         ("PyMemoryViewObject_OB_ARRAY", "offsetof(PyMemoryViewObject, ob_array)", "i64"),
         ("PyMemoryViewObject_WEAKREFLIST", "offsetof(PyMemoryViewObject, weakreflist)", "i64"),
         ("memoryiterobject_SIZE", "sizeof(memoryiterobject)", "i64"),
         ("_Py_MANAGED_BUFFER_RELEASED", "_Py_MANAGED_BUFFER_RELEASED", "i32"),
         ("_Py_MANAGED_BUFFER_FREE_FORMAT", "_Py_MANAGED_BUFFER_FREE_FORMAT", "i32"),
         ("_Py_MEMORYVIEW_RELEASED", "_Py_MEMORYVIEW_RELEASED", "i32"),
         ("_Py_MEMORYVIEW_SCALAR", "_Py_MEMORYVIEW_SCALAR", "i32"),
         ("_Py_MEMORYVIEW_PIL", "_Py_MEMORYVIEW_PIL", "i32"),
         ("_Py_MEMORYVIEW_RESTRICTED", "_Py_MEMORYVIEW_RESTRICTED", "i32"),
         ("PyBUF_WRITABLE", "PyBUF_WRITABLE", "i32"),
         ("PyBUF_FORMAT", "PyBUF_FORMAT", "i32"),
         ("PyBUF_ND", "PyBUF_ND", "i32"),
         ("PyBUF_STRIDES", "PyBUF_STRIDES", "i32"),
         ("PyBUF_C_CONTIGUOUS", "PyBUF_C_CONTIGUOUS", "i32"),
         ("PyBUF_F_CONTIGUOUS", "PyBUF_F_CONTIGUOUS", "i32"),
         ("PyBUF_ANY_CONTIGUOUS", "PyBUF_ANY_CONTIGUOUS", "i32"),
         ("PyBUF_INDIRECT", "PyBUF_INDIRECT", "i32"),
         ("PyBUF_WRITE", "PyBUF_WRITE", "i32"),
         ("PyBUF_MAX_NDIM", "PyBUF_MAX_NDIM", "i32"),
         ("PyComplexObject_SIZE", "sizeof(PyComplexObject)", "i64"),
         ("PyComplexObject_REAL", "offsetof(PyComplexObject, cval.real)", "i64"),
         ("PyComplexObject_IMAG", "offsetof(PyComplexObject, cval.imag)", "i64"),
         ("PyMethodObject_SIZE", "sizeof(PyMethodObject)", "i64"),
         ("PyMethodObject_FUNC", "offsetof(PyMethodObject, im_func)", "i64"),
         ("PyMethodObject_SELF", "offsetof(PyMethodObject, im_self)", "i64"),
         (
             "PyMethodObject_WEAKREFLIST",
             "offsetof(PyMethodObject, im_weakreflist)",
             "i64"
         ),
         ("PyMethodObject_VECTORCALL", "offsetof(PyMethodObject, vectorcall)", "i64"),
         ("PyInstanceMethodObject_SIZE", "sizeof(PyInstanceMethodObject)", "i64"),
         (
             "PyInstanceMethodObject_FUNC",
             "offsetof(PyInstanceMethodObject, func)",
             "i64"
         ),
         ("PyStructSequence_SIZE", "sizeof(PyStructSequence)", "i64"),
         ("PyPickleBufferObject_SIZE", "sizeof(PyPickleBufferObject)", "i64"),
         ("PyPickleBufferObject_VIEW", "offsetof(PyPickleBufferObject, view)", "i64"),
         ("Py_buffer_LEN", "offsetof(Py_buffer, len)", "i64"),
         ("Py_buffer_ITEMSIZE", "offsetof(Py_buffer, itemsize)", "i64"),
         ("PY_MEMBER_DEF_SIZE", "sizeof(PyMemberDef)", "i64"),
         ("PY_TYPE_SLOT_SIZE", "sizeof(PyType_Slot)", "i64"),
         ("PY_TYPE_SPEC_SIZE", "sizeof(PyType_Spec)", "i64"),
         ("PY_STRUCT_SEQUENCE_FIELD_SIZE", "sizeof(PyStructSequence_Field)", "i64"),
         ("PY_STRUCT_SEQUENCE_DESC_SIZE", "sizeof(PyStructSequence_Desc)", "i64"),
         (
             "PyPickleBufferObject_WEAKREFLIST",
             "offsetof(PyPickleBufferObject, weakreflist)",
             "i64"
         ),
         ("interpolationobject_SIZE", "sizeof(interpolationobject)", "i64"),
         ("interpolationobject_VALUE", "offsetof(interpolationobject, value)", "i64"),
         (
             "interpolationobject_EXPRESSION",
             "offsetof(interpolationobject, expression)",
             "i64"
         ),
         (
             "interpolationobject_CONVERSION",
             "offsetof(interpolationobject, conversion)",
             "i64"
         ),
         (
             "interpolationobject_FORMAT_SPEC",
             "offsetof(interpolationobject, format_spec)",
             "i64"
         ),
         ("templateiterobject_SIZE", "sizeof(templateiterobject)", "i64"),
         ("templateobject_SIZE", "sizeof(templateobject)", "i64"),
         ("templateobject_STRINGS", "offsetof(templateobject, strings)", "i64"),
         (
             "templateobject_INTERPOLATIONS",
             "offsetof(templateobject, interpolations)",
             "i64"
         ),
         ("unionobject_SIZE", "sizeof(unionobject)", "i64"),
         ("unionobject_ARGS", "offsetof(unionobject, args)", "i64"),
         ("unionobject_WEAKREFLIST", "offsetof(unionobject, weakreflist)", "i64"),
         ("gaobject_SIZE", "sizeof(gaobject)", "i64"),
         ("gaobject_ORIGIN", "offsetof(gaobject, origin)", "i64"),
         ("gaobject_ARGS", "offsetof(gaobject, args)", "i64"),
         ("gaobject_STARRED", "offsetof(gaobject, starred)", "i64"),
         ("gaobject_WEAKREFLIST", "offsetof(gaobject, weakreflist)", "i64"),
         ("gaobject_VECTORCALL", "offsetof(gaobject, vectorcall)", "i64"),
         ("gaiterobject_SIZE", "sizeof(gaiterobject)", "i64"),
         ("PyStdPrinter_Object_SIZE", "sizeof(PyStdPrinter_Object)", "i64"),
         ("Py_slices_MAXFREELIST", "Py_slices_MAXFREELIST", "i64"),
         ("Py_ranges_MAXFREELIST", "Py_ranges_MAXFREELIST", "i64"),
         ("Py_range_iters_MAXFREELIST", "Py_range_iters_MAXFREELIST", "i64"),
         ("METH_STATIC", "METH_STATIC", "i32"),
         ("METH_FASTCALL", "METH_FASTCALL", "i32"),
         ("Py_T_INT", "Py_T_INT", "i32"),
         ("Py_T_PYSSIZET", "Py_T_PYSSIZET", "i32"),
         ("PyBUF_SIMPLE", "PyBUF_SIMPLE", "i32"),
         ("Py_tp_dealloc", "Py_tp_dealloc", "i32"),
         ("Py_tp_doc", "Py_tp_doc", "i32"),
         ("Py_tp_getset", "Py_tp_getset", "i32"),
         ("Py_tp_methods", "Py_tp_methods", "i32"),
         ("Py_tp_new", "Py_tp_new", "i32"),
         ("Py_tp_repr", "Py_tp_repr", "i32"),
         ("Py_nb_or", "Py_nb_or", "i32"),
         ("Py_tp_alloc", "Py_tp_alloc", "i32"),
         ("Py_tp_free", "Py_tp_free", "i32"),
         ("Py_tp_traverse", "Py_tp_traverse", "i32"),
         ("Py_tp_clear", "Py_tp_clear", "i32"),
         ("Py_tp_getattro", "Py_tp_getattro", "i32"),
         ("Py_tp_setattro", "Py_tp_setattro", "i32"),
         ("Py_tp_hash", "Py_tp_hash", "i32"),
         ("Py_tp_str", "Py_tp_str", "i32"),
         ("Py_tp_richcompare", "Py_tp_richcompare", "i32"),
         ("Py_tp_iter", "Py_tp_iter", "i32"),
         ("Py_tp_init", "Py_tp_init", "i32"),
         ("Py_tp_token", "Py_tp_token", "i32"),
         ("Py_tp_finalize", "Py_tp_finalize", "i32"),
         ("Py_tp_call", "Py_tp_call", "i32"),
         ("Py_tp_iternext", "Py_tp_iternext", "i32"),
         ("Py_am_await", "Py_am_await", "i32"),
         ("Py_am_send", "Py_am_send", "i32"),
         ("Py_mp_length", "Py_mp_length", "i32"),
         ("Py_mp_subscript", "Py_mp_subscript", "i32"),
         ("Py_mp_ass_subscript", "Py_mp_ass_subscript", "i32"),
         ("Py_nb_add", "Py_nb_add", "i32"),
         ("Py_nb_subtract", "Py_nb_subtract", "i32"),
         ("Py_nb_multiply", "Py_nb_multiply", "i32"),
         ("Py_nb_remainder", "Py_nb_remainder", "i32"),
         ("Py_nb_divmod", "Py_nb_divmod", "i32"),
         ("Py_nb_power", "Py_nb_power", "i32"),
         ("Py_nb_negative", "Py_nb_negative", "i32"),
         ("Py_nb_positive", "Py_nb_positive", "i32"),
         ("Py_nb_absolute", "Py_nb_absolute", "i32"),
         ("Py_nb_bool", "Py_nb_bool", "i32"),
         ("Py_nb_int", "Py_nb_int", "i32"),
         ("Py_nb_float", "Py_nb_float", "i32"),
         ("Py_nb_floor_divide", "Py_nb_floor_divide", "i32"),
         ("Py_nb_true_divide", "Py_nb_true_divide", "i32"),
         ("PY_DATETIME_DELTA_SIZE", "sizeof(PyDateTime_Delta)", "i64"),
         ("PY_DATETIME_TZINFO_SIZE", "sizeof(PyDateTime_TZInfo)", "i64"),
         ("PY_DATETIME_DATE_SIZE", "sizeof(PyDateTime_Date)", "i64"),
         ("PY_DATETIME_BASE_TIME_SIZE", "sizeof(_PyDateTime_BaseTime)", "i64"),
         ("PY_DATETIME_TIME_SIZE", "sizeof(PyDateTime_Time)", "i64"),
         ("PY_DATETIME_BASE_DATETIME_SIZE", "sizeof(_PyDateTime_BaseDateTime)", "i64"),
         ("PY_DATETIME_DATETIME_SIZE", "sizeof(PyDateTime_DateTime)", "i64"),
         ("PY_DATETIME_DATA_OFFSET", "offsetof(PyDateTime_Date, data)", "i64"),
         ("PY_DATETIME_DELTA_DAYS_OFFSET", "offsetof(PyDateTime_Delta, days)", "i64"),
         (
             "PY_DATETIME_DELTA_SECONDS_OFFSET",
             "offsetof(PyDateTime_Delta, seconds)",
             "i64"
         ),
         (
             "PY_DATETIME_DELTA_MICROSECONDS_OFFSET",
             "offsetof(PyDateTime_Delta, microseconds)",
             "i64"
         ),
         ("Py_CONSTANT_ONE", "Py_CONSTANT_ONE", "u32"),
         ("Py_CONSTANT_EMPTY_STR", "Py_CONSTANT_EMPTY_STR", "u32"),
         ("_PyTime_ROUND_FLOOR", "_PyTime_ROUND_FLOOR", "i32"),
         ("_PyTime_ROUND_HALF_EVEN", "_PyTime_ROUND_HALF_EVEN", "i32"),
         ("_PyTime_ROUND_CEILING", "_PyTime_ROUND_CEILING", "i32"),
         ("_PyTime_ROUND_TIMEOUT", "_PyTime_ROUND_TIMEOUT", "i32"),
         ("PY_SOCKET_OBJECT_SIZE", "sizeof(PySocketSockObject)", "i64"),
         (
             "PY_SOCKET_FAMILY_OFFSET",
             "offsetof(PySocketSockObject, sock_family)",
             "i64"
         ),
         ("PY_SOCKET_TYPE_OFFSET", "offsetof(PySocketSockObject, sock_type)", "i64"),
         ("PY_SOCKET_PROTO_OFFSET", "offsetof(PySocketSockObject, sock_proto)", "i64"),
         ("PY_SOCKET_API_SIZE", "sizeof(PySocketModule_APIObject)", "i64"),
         ("PY_OS_ERROR_OBJECT_SIZE", "sizeof(PyOSErrorObject)", "i64"),
         ("Py_CLEANUP_SUPPORTED", "Py_CLEANUP_SUPPORTED", "i32")
     ],
     # Constants whose values differ between the supported platforms, in the
     # form of CONSTANTS.
     PLATFORM_CONSTANTS: list[tuple[str, str, str]] = [
         ("PyConfig_VERBOSE", "offsetof(PyConfig, verbose)", "i64"),
         ("PyConfig_SAFE_PATH", "offsetof(PyConfig, safe_path)", "i64"),
         ("PyConfig_SYS_PATH_0", "offsetof(PyConfig, sys_path_0)", "i64"),
         (
             "PyInterpreterState_CEVAL_OWN_GIL",
             "offsetof(PyInterpreterState, ceval.own_gil)",
             "i64"
         ),
         (
             "PyInterpreterState_FREELISTS",
             "offsetof(PyInterpreterState, object_state.freelists)",
             "i64"
         ),
         ("PyInterpreterState_GC", "offsetof(PyInterpreterState, gc)", "i64"),
         (
             "PyInterpreterState_CACHED_GENERIC_TYPE",
             "offsetof(PyInterpreterState, cached_objects.generic_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_TYPEVAR_TYPE",
             "offsetof(PyInterpreterState, cached_objects.typevar_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_TYPEVARTUPLE_TYPE",
             "offsetof(PyInterpreterState, cached_objects.typevartuple_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_PARAMSPEC_TYPE",
             "offsetof(PyInterpreterState, cached_objects.paramspec_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_PARAMSPECARGS_TYPE",
             "offsetof(PyInterpreterState, cached_objects.paramspecargs_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_PARAMSPECKWARGS_TYPE",
             "offsetof(PyInterpreterState, cached_objects.paramspeckwargs_type)",
             "i64"
         ),
         (
             "PyInterpreterState_CACHED_CONSTEVALUATOR_TYPE",
             "offsetof(PyInterpreterState, cached_objects.constevaluator_type)",
             "i64"
         ),
         (
             "PyThreadState_CURRENT_FRAME",
             "offsetof(PyThreadState, current_frame)",
             "i64"
         ),
         (
             "_PyInterpreterFrame_F_FUNCOBJ",
             "offsetof(_PyInterpreterFrame, f_funcobj)",
             "i64"
         ),
         (
             "PyInterpreterState_EXC_ERRNOMAP",
             "offsetof(PyInterpreterState, exc_state.errnomap)",
             "i64"
         ),
         (
             "PyInterpreterState_EXC_GROUP",
             "offsetof(PyInterpreterState, exc_state.PyExc_ExceptionGroup)",
             "i64"
         ),
         (
             "PyInterpreterState_EXC_MEMERRORS_FREELIST",
             "offsetof(PyInterpreterState, exc_state.memerrors_freelist)",
             "i64"
         ),
         (
             "PyInterpreterState_EXC_MEMERRORS_NUMFREE",
             "offsetof(PyInterpreterState, exc_state.memerrors_numfree)",
             "i64"
         ),
         (
             "PyInterpreterState_LAST_RESORT_MEMORY_ERROR",
             "offsetof(PyInterpreterState, static_objects.singletons.last_resort_memory_error)",
             "i64"
         ),
         (
             "PyInterpreterState_ACTIVE_FUNC_WATCHERS",
             "offsetof(PyInterpreterState, active_func_watchers)",
             "i64"
         ),
         (
             "PyInterpreterState_FUNC_WATCHERS",
             "offsetof(PyInterpreterState, func_watchers)",
             "i64"
         ),
         (
             "PyInterpreterState_FUNC_VERSION_CACHE",
             "offsetof(PyInterpreterState, func_state.func_version_cache)",
             "i64"
         ),
         (
             "PyInterpreterState_RARE_FUNC_MODIFICATION",
             "offsetof(PyInterpreterState, rare_events.func_modification)",
             "i64"
         ),
         (
             "PyInterpreterState_DICT_NEXT_KEYS_VERSION",
             "offsetof(PyInterpreterState, dict_state.next_keys_version)",
             "i64"
         ),
         (
             "PyInterpreterState_DICT_WATCHERS",
             "offsetof(PyInterpreterState, dict_state.watchers)",
             "i64"
         ),
         (
             "_PyRuntimeState_SMALL_INTS",
             "offsetof(_PyRuntimeState, static_objects.singletons.small_ints)",
             "i64"
         ),
         (
             "PyInterpreterState_LONG_MAX_STR_DIGITS",
             "offsetof(PyInterpreterState, long_state.max_str_digits)",
             "i64"
         ),
         (
             "_PyRuntimeState_REF_TRACER_FUNC",
             "offsetof(_PyRuntimeState, ref_tracer.tracer_func)",
             "i64"
         ),
         (
             "_PyRuntimeState_REF_TRACER_DATA",
             "offsetof(_PyRuntimeState, ref_tracer.tracer_data)",
             "i64"
         ),
         (
             "_PyRuntimeState_TUPLE_EMPTY",
             "offsetof(_PyRuntimeState, static_objects.singletons.tuple_empty)",
             "i64"
         )
     ],
     # The supported platforms: variant module suffix, zig target and the C
     # condition that selects the platform in layouts_check.c.
     PLATFORMS: list[tuple[str, str, str]] = [
         (
             "linux.x86_64",
             "x86_64-linux-gnu",
             "defined(__linux__) && defined(__x86_64__)"
         ),
         (
             "linux.aarch64",
             "aarch64-linux-gnu",
             "defined(__linux__) && defined(__aarch64__)"
         ),
         ("darwin.x86_64", "x86_64-macos", "defined(__APPLE__) && defined(__x86_64__)"),
         (
             "darwin.aarch64",
             "aarch64-macos",
             "defined(__APPLE__) && defined(__aarch64__)"
         )
     ],
     # The configuration pyconfig.h, pyport.h and the compiler give every
     # supported release build (linux and darwin, x86_64 and aarch64).
     CONFIG: dict[str, int] = {
         "SIZEOF_VOID_P": 8,
         "PY_BIG_ENDIAN": 0,
         "PYLONG_BITS_IN_DIGIT": 30,
         "__clang__": 1,
         "__GNUC__": 4,
         "__STDC_VERSION__": 201112
     },
     # C scalar types: Jac type and whether the C type is signed.
     SCALARS: dict[str, tuple[str, bool]] = {
         "char": ("i8", True),
         "signed char": ("i8", True),
         "unsigned char": ("u8", False),
         "short": ("i16", True),
         "unsigned short": ("u16", False),
         "int": ("i32", True),
         "unsigned int": ("u32", False),
         "long": ("i64", True),
         "unsigned long": ("u64", False),
         "long long": ("i64", True),
         "unsigned long long": ("u64", False),
         "int8_t": ("i8", True),
         "uint8_t": ("u8", False),
         "int16_t": ("i16", True),
         "uint16_t": ("u16", False),
         "int32_t": ("i32", True),
         "uint32_t": ("u32", False),
         "int64_t": ("i64", True),
         "uint64_t": ("u64", False),
         "PY_INT64_T": ("i64", True),
         "PY_UINT64_T": ("u64", False),
         "PyTime_t": ("i64", True),
         "size_t": ("u64", False),
         "Py_ssize_t": ("i64", True),
         "Py_hash_t": ("i64", True),
         "uintptr_t": ("u64", False),
         "intptr_t": ("i64", True),
         "double": ("f64", True),
         "float": ("f32", True),
         # C's bool: one unsigned byte, which the asserts hold to kind 4.
         "bool": ("u8", False),
         "_Bool": ("u8", False),
         # An enum with a negative enumerator is an int.
         "PySendResult": ("i32", True)
     },
     # Jac keywords a C member name may collide with.
     JAC_KEYWORDS: set[str] = set(
         (
             "obj node edge walker has can def glob impl sem test entry exit spawn "
             + "visit disengage report ignore by to with in is not and or if else elif "
             + "for while return yield break continue try except finally raise assert "
             + "del import from as lambda async await class enum include skip match "
             + "case switch default flow wait priv pub protect static override abs kw let"
         ).split()
     ),
     SIZES: dict[str, int] = {
         "i8": 1,
         "u8": 1,
         "i16": 2,
         "u16": 2,
         "i32": 4,
         "u32": 4,
         "f32": 4,
         "i64": 8,
         "u64": 8,
         "f64": 8
     };

"""A header's function-pointer typedef: return and parameter C types."""
obj FunctionType {
    has returns: str,
        params: list[str];
}

"""One generated field: Jac name and type, the C member it mirrors, its
offset and size, and for integers whether the C type is signed. `member` is
the C designator the asserts use: an element of a fixed array
(`data[3]`) when that differs from the Jac name."""
obj Field {
    has name: str,
        jac: str,
        offset: int,
        size: int,
        signed: (bool | None) = None,
        array: bool = False,
        member: str = "",
        boolean: bool = False;

    def designator -> str {
        return self.member or self.name;
    }
}

"""One generated struct with its computed layout."""
obj Layout {
    has name: str,
        ctype: str,
        fields: list[Field],
        size: int,
        align: int;
}

"""What the headers declare once their active `#if` branches are kept."""
obj Headers {
    has bodies: dict[str, str] = {},
        private: dict[str, str] = {},
        private_scalars: dict[str, str] = {},
        aliases: dict[str, str] = {},
        functions: dict[str, FunctionType] = {};
}

# ---------------------------------------------------------------- preprocessor
def strip_comments(text: str) -> str {
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S);
    text = re.sub(r"//[^\n]*", "", text);
    return text.replace("\\\n", " ");
}

def condition(expression: str, defines: dict[str, str]) -> bool {
    pieces: list[str] = [];
    for token in re.findall(
        r"defined\s*\(\s*\w+\s*\)|defined\s+\w+|\w+|&&|\|\||[!=<>]=|<<|>>|[!()<>+\-*]",
        expression
    ) {
        if token.startswith("defined") and token != "defined" {
            name = re.findall(r"\w+", token)[-1];
            pieces.append("1" if name in CONFIG or name in defines else "0");
        } elif token[0].isdigit() {
            pieces.append(re.sub(r"[uUlL]+$", "", token));
        } elif re.fullmatch(r"\w+", token) {
            if token in CONFIG {
                pieces.append(str(CONFIG[token]));
            } else {
                body = defines.get(token, "0").strip() or "1";
                pieces.append(body if re.fullmatch(r"\d+", body) else "0");
            }
        } else {
            words: dict[str, str] = {"&&": " and ", "||": " or ", "!": " not "};
            pieces.append(words[token] if token in words else token);
        }
    }
    try {
        return bool(eval(" ".join(pieces), {"__builtins__": {}}, {}));
    } except Exception {
        sys.exit(f"gen_layouts cannot evaluate #if {expression!r}");
    }
}

# The text of `texts` with inactive `#if` branches and directives removed, and
# object-like macros defined along the way.
def preprocess(texts: list[str], defines: dict[str, str]) -> str {
    kept: list[str] = [];
    # Each frame: (branch active, some branch already taken, parent active).
    stack: list[tuple[bool, bool, bool]] = [];
    for text in texts {
        for line in strip_comments(text).splitlines() {
            active = not stack or stack[-1][0];
            directive = re.match(r"^\s*#\s*(\w+)\s*(.*)$", line);
            if directive is None {
                if active {
                    kept.append(line);
                }
                continue;
            }
            (word, rest) = (directive.group(1), directive.group(2).strip());
            if word in ("if", "ifdef", "ifndef") {
                if word == "ifdef" {
                    taken = rest in CONFIG or rest in defines;
                } elif word == "ifndef" {
                    taken = not (rest in CONFIG or rest in defines);
                } else {
                    taken = active and condition(rest, defines);
                }
                stack.append((active and taken, active and taken, active));
            } elif word == "elif" {
                (_, done, parent) = stack.pop();
                taken = parent and not done and condition(rest, defines);
                stack.append((taken, done or taken, parent));
            } elif word == "else" {
                (_, done, parent) = stack.pop();
                stack.append((parent and not done, True, parent));
            } elif word == "endif" {
                stack.pop();
            } elif word == "define" and active {
                macro = re.match(r"^(\w+)(?!\()\s*(.*)$", rest);
                if macro is not None {
                    defines[macro.group(1)] = macro.group(2);
                }
            }
        }
    }
    return "\n".join(kept);
}

# The index just past the brace that closes the one at `start`.
def closing(text: str, start: int) -> int {
    depth = 0;
    for index in range(start, len(text)) {
        if text[index] == "{" {
            depth += 1;
        } elif text[index] == "}" {
            depth -= 1;
            if depth == 0 {
                return index + 1;
            }
        }
    }
    sys.exit("gen_layouts: unbalanced braces in the headers");
}

# The parameter C types of a function declarator's parameter list, with any
# parameter names dropped.
def parameter_types(raw: str) -> list[str] {
    params: list[str] = [];
    raw = " ".join(raw.split());
    if raw and raw != "void" {
        for piece in raw.split(",") {
            piece = piece.strip();
            # Drop a parameter name; keep the type.
            named = re.match(r"^(.*?[\s\*])(\w+)$", piece);
            if named is not None and named.group(2) not in SCALARS {
                piece = named.group(1);
            }
            params.append(" ".join(piece.split()));
        }
    }
    return params;
}

# `[NAME]` with NAME an integer macro (datetime.h's
# `data[_PyDateTime_DATETIME_DATASIZE]`) as the literal it defines.
def array_bounds(text: str, defines: dict[str, str]) -> str {
    pieces: list[str] = [];
    last = 0;
    for hit in re.finditer(r"\[\s*([A-Za-z_]\w*)\s*\]", text) {
        body = defines.get(hit.group(1), "").strip();
        if re.fullmatch(r"\d+", body) {
            pieces.append(text[last:hit.start()] + f"[{body}]");
            last = hit.end();
        }
    }
    pieces.append(text[last:]);
    return "".join(pieces);
}

def read_headers(found: Headers) {
    texts = archive_texts(tuple(HEADERS + OBJECT_SOURCES));
    missing = [
        h
        for h in HEADERS + OBJECT_SOURCES
        if h not in texts
    ];
    if missing {
        sys.exit(f"Not in the pinned archive: {', '.join(missing)}");
    }
    defines: dict[str, str] = {};
    text = preprocess([texts[h] for h in HEADERS], defines);
    # A source's own macros stay out of the headers' namespace; its typedef'd
    # structs are kept verbatim for layouts_check.c.
    for source in OBJECT_SOURCES {
        body = preprocess([texts[source]], dict(defines));
        # Scalar typedefs a private struct names (socketmodule.h's SOCKET_T).
        for hit in re.finditer(
            r"\btypedef\s+((?:unsigned\s+|signed\s+)?(?:int|long|short|char))\s+(\w+)\s*;",
            body
        ) {
            found.private_scalars[hit.group(2)] = hit.group(0);
        }
        # Forward typedefs of a source's own structs (typedef struct
        # _odictnode _ODictNode).
        for hit in re.finditer(r"\btypedef\s+struct\s+(\w+)\s+(\w+)\s*;", body) {
            found.private_scalars[hit.group(2)] = hit.group(0);
        }
        for hit in re.finditer(r"\btypedef\s+struct\s*\{", body) {
            end = closing(body, hit.end() - 1);
            alias = re.match(r"\s*(\w+)\s*;", body[end:]);
            if alias is not None {
                found.private[alias.group(1)] = " ".join(
                    body[hit.start():end + alias.end()].split()
                );
            }
        }
        # A tagged struct whose header typedef names it (odictobject.c's
        # struct _odictobject behind PyODictObject), keyed by its C type.
        for hit in re.finditer(r"(?m)^struct\s+(\w+)\s*\{", body) {
            end = closing(body, hit.end() - 1);
            if re.match(r"\s*;", body[end:]) is not None {
                found.private[f"struct {hit.group(1)}"] = " ".join(
                    body[hit.start():end].split()
                )
                    + ";";
            }
        }
        text += "\n" + body;
    }
    # Expand the object-like macros struct bodies use (PyObject_HEAD), and the
    # ones those expand to (datetime.h's _PyTZINFO_HEAD names PyObject_HEAD).
    heads = {
        name: body
        for (name, body) in defines.items()
        if body.strip().endswith(";")
    };
    for _ in range(8) {
        expanded = text;
        for (name, body) in heads.items() {
            expanded = re.sub(rf"\b{name}\b", body, expanded);
        }
        if expanded == text {
            break;
        }
        text = expanded;
    }
    text = array_bounds(text, defines);
    for hit in re.finditer(r"\b(typedef\s+)?struct\s*(\w*)\s*\{", text) {
        start = hit.end() - 1;
        end = closing(text, start);
        body = text[start + 1:end - 1];
        if hit.group(2) {
            found.bodies[f"struct {hit.group(2)}"] = body;
        }
        if hit.group(1) {
            alias = re.match(r"\s*(\w+)\s*;", text[end:]);
            if alias is not None {
                found.bodies[alias.group(1)] = body;
            }
        }
    }
    for hit in re.finditer(
        r"\btypedef\s+([\w\s\*]+?)\s*\(\s*\*\s*(\w+)\s*\)\s*\(([^;]*?)\)\s*;", text
    ) {
        found.functions[hit.group(2)] = FunctionType(
            returns=" ".join(hit.group(1).split()), params=parameter_types(hit.group(3))
        );
    }
    for hit in re.finditer(r"\btypedef\s+([\w\s]+?)\s+(\w+)\s*;", text) {
        found.aliases[hit.group(2)] = " ".join(hit.group(1).split());
    }
}

# ------------------------------------------------------------------ type model
glob:priv opaque: list[str] = [],
     emitted: dict[str, Layout] = {},
     order: list[str] = [],
     headers: Headers = Headers();

def jac_name_of(ctype: str) -> (str | None) {
    for (name, declared) in LAYOUTS {
        if declared == ctype or name == ctype {
            return name;
        }
    }
    return None;
}

# The layout a C struct type resolves to, or None for a record no port reads.
def struct_of(ctype: str) -> (str | None) {
    resolved = headers.aliases.get(ctype, ctype);
    return jac_name_of(resolved) or jac_name_of(ctype);
}

def scalar_of(ctype: str) -> (tuple[str, bool] | None) {
    seen = 0;
    while ctype not in SCALARS and ctype in headers.aliases and seen < 8 {
        ctype = headers.aliases[ctype];
        seen += 1;
    }
    return SCALARS.get(ctype);
}

def callable_of(function: FunctionType) -> str {
    params = [jac_type(p) for p in function.params];
    returns = "None" if function.returns == "void" else jac_type(function.returns);
    return f"Callable[[{', '.join(params)}], {returns}]";
}

# The Jac type of C type `ctype` in a field or a callback signature.
def jac_type(ctype: str) -> str {
    text = re.sub(r"\b(const|volatile)\b", "", ctype);
    depth = text.count("*");
    base = " ".join(text.replace("*", " ").split());
    if depth == 0 {
        if base in headers.functions {
            return callable_of(headers.functions[base]);
        }
        scalar = scalar_of(base);
        if scalar is not None {
            return scalar[0];
        }
        layout = struct_of(base);
        if layout is not None {
            require(layout);
            return layout;
        }
        sys.exit(f"gen_layouts: no Jac type for C type {ctype!r}");
    }
    if base == "void" {
        inner = "";
    } elif base == "char" {
        inner = "u8";
    } elif base == "PyObject" {
        inner = "PyObject";
    } elif base in headers.functions {
        inner = callable_of(headers.functions[base]);
    } elif scalar_of(base) is not None {
        inner = scalar_of(base)[0];
    } else {
        inner = struct_of(base) or re.sub(r"^struct\s+", "", base);
        if inner not in opaque and struct_of(base) is None {
            opaque.append(inner);
        }
    }
    result = f"ptr[{inner}]" if inner else "ptr";
    for _ in range(depth - 1) {
        result = f"ptr[{result}]";
    }
    return result;
}

def size_align(jac: str) -> tuple[int, int] {
    if jac in SIZES {
        return (SIZES[jac], SIZES[jac]);
    }
    if jac.startswith(("ptr", "Callable")) {
        return (8, 8);
    }
    layout = emitted[jac];
    return (layout.size, layout.align);
}

# The array declarator of an element count ("" for a scalar member).
def bounds(count: int) -> str {
    return "[" + str(count) + "]" if count else "";
}

# The name a function-pointer member's signature is recorded under in
# `headers.functions`, as if the header had a typedef for it.
def member_function(returns: str, raw: str) -> str {
    function = FunctionType(
        returns=" ".join(returns.split()), params=parameter_types(raw)
    );
    signature = function.returns + "_" + "_".join(function.params);
    name = "__member_fn_" + re.sub(r"\W+", "_", signature.replace("*", "P"));
    headers.functions[name] = function;
    return name;
}

# The member declarations of a struct body: (C type, member name, element
# count), the count 0 for a member that is not an array. An anonymous union
# contributes its first member, which the size asserts prove is its widest; an
# array member `T name[N]` is N elements of T (see layouts.jac). A member of
# an inline enum type (`PyStatus._type`) is the enum's integer type, unsigned
# int for enumerators that are all non-negative, which the kind and signedness
# asserts prove. A function-pointer member (`PyObject *(*f)(int)`) is typed as
# its signature.
def members(body: str) -> list[tuple[str, str, int]] {
    body = body.replace("__extension__", " ");
    while True {
        hit = re.search(r"\benum\s*\{", body);
        if hit is None {
            break;
        }
        end = closing(body, hit.end() - 1);
        if re.search(r"=\s*-", body[hit.end():end - 1]) {
            sys.exit("gen_layouts: only enums without negative values are supported");
        }
        body = body[:hit.start()] + "unsigned int" + body[end:];
    }
    while True {
        hit = re.search(r"\b(union|struct)\s*\{", body);
        if hit is None {
            break;
        }
        end = closing(body, hit.end() - 1);
        tail = re.match(r"\s*(\w*)\s*;", body[end:]);
        if tail is None or tail.group(1) {
            sys.exit("gen_layouts: only anonymous nested unions are supported");
        }
        inner = members(body[hit.end():end - 1]);
        replacement = f"{inner[0][0]} {inner[0][1]}{bounds(inner[0][2])};"
            if hit.group(1) == "union"
            else " ".join(f"{t} {n}{bounds(a)};" for (t, n, a) in inner);
        body = body[:hit.start()] + replacement + body[end + len(tail.group(0)):];
    }
    found: list[tuple[str, str, int]] = [];
    for statement in body.split(";") {
        statement = " ".join(statement.split());
        if not statement {
            continue;
        }
        pointer = re.match(r"^(.*?)\(\s*\*\s*(\w+)\s*\)\s*\((.*)\)$", statement);
        if pointer is not None {
            found.append(
                (
                    member_function(pointer.group(1), pointer.group(3)),
                    pointer.group(2),
                    0
                )
            );
            continue;
        }
        declared = re.match(
            r"^(.*?[\s\*])(\w+(?:\s*\[\s*\d+\s*\])?(?:\s*,.*)?)$", statement
        );
        if declared is None {
            sys.exit(f"gen_layouts: cannot read member {statement!r}");
        }
        # The stars before the first name are its declarator's, as the stars
        # of every later name are (`PyObject *start, *stop, *step;`).
        declared_type = declared.group(1).strip();
        lead = "*" * (len(declared_type) - len(declared_type.rstrip("*")));
        base = declared_type.rstrip("*").strip() + " ";
        first = True;
        for name in declared.group(2).split(",") {
            name = (lead if first else "") + name.strip();
            first = False;
            array = re.match(r"^(\**\w+)\s*\[\s*(\d+)\s*\]$", name);
            count = 0;
            if array is not None {
                count = int(array.group(2));
                name = array.group(1);
            }
            stars = re.match(r"^(\**)(\w+)$", name);
            if stars is None {
                sys.exit(f"gen_layouts: cannot read member name {name!r}");
            }
            found.append((base + stars.group(1), stars.group(2), count));
        }
    }
    return found;
}

def require(name: str) -> None {
    if name in emitted {
        return;
    }
    ctype = next(
        c
        for (n, c) in LAYOUTS
        if n == name
    );
    body = headers.bodies.get(ctype);
    if body is None {
        body = headers.bodies.get(headers.aliases.get(ctype, ""));
    }
    if body is None {
        sys.exit(f"gen_layouts: no definition of {ctype} in {', '.join(HEADERS)}");
    }
    # Claim the name first so a pointer back to this struct does not recurse.
    layout = Layout(name=name, ctype=ctype, fields=[], size=0, align=1);
    emitted[name] = layout;
    offset = 0;
    for (member_type, member, count) in members(body) {
        jac = jac_type(member_type);
        (size, align) = size_align(jac);
        offset = (offset + align - 1) // align * align;
        bare = " ".join(re.sub(r"\b(const|volatile)\b", "", member_type).split());
        scalar = scalar_of(bare) if "*" not in member_type else None;
        # Plain `char` is signed on x86_64 and unsigned on aarch64 Linux, so
        # its signedness is the platform's, not the layout's.
        signed = scalar[1]
            if scalar is not None
                and jac in SIZES
                and not jac.startswith("f")
                and bare != "char"
            else None;
        # `T name[1]` is one T field; a fixed array `T name[N]` is N fields,
        # `name` for element 0 and `name_<i>` for element i, so the members
        # after it keep their offsets.
        for index in range(max(count, 1)) {
            # A C member named after a Jac keyword (`obj`) takes a trailing
            # underscore in Jac, as cpython_api.jac's records do; the asserts
            # keep the C name.
            jac_member = f"{member}_" if member in JAC_KEYWORDS else member;
            layout.fields.append(
                Field(
                    name=jac_member if index == 0 else f"{jac_member}_{index}",
                    jac=jac,
                    offset=offset,
                    size=size,
                    signed=signed,
                    array=count == 1,
                    member=f"{member}[{index}]"
                        if count > 1
                        else (member if jac_member != member else ""),
                    boolean=scalar is not None
                        and " ".join(member_type.split()) in ("bool", "_Bool")
                )
            );
            offset += size;
        }
        layout.align = max(layout.align, align);
    }
    layout.size = (offset + layout.align - 1) // layout.align * layout.align;
    order.append(name);
}

# --------------------------------------------------------------------- output
# The records cpython_api.jac declares, opaque (`obj PyObject;`) or C-layout
# (`obj PyMethodDef { ... }`); layouts.jac imports them rather than
# redeclaring a distinct type.
def capi_records -> set[str] {
    return set(re.findall(r"\bobj (\w+)\s*[;{]", CAPI.read_text()));
}

# A layout cpython_api.jac already declares as a C-layout record (Py_buffer,
# Py_complex) is imported from it, so an object layout embedding it uses the
# same type the C API functions take. Its fields must match the header's
# layout position by position (the record may rename a field C names after a
# Jac keyword); the asserts check the header's side.
def check_capi_record(layout: Layout) {
    body = re.search(
        r"\bobj " + layout.name + r"\s*\{\s*has\s+(.*?);\s*\}", CAPI.read_text(), re.S
    );
    if body is None {
        sys.exit(
            f"gen_layouts: {layout.name} is not a C-layout record of cpython_api.jac"
        );
    }
    declared = [
        re.sub(r"\s*=.*$", "", piece.split(":", 1)[1]).strip()
        for piece in re.split(r",\s*(?=\w+\s*:)", body.group(1))
    ];
    expected = [f.jac for f in layout.fields];
    if [" ".join(t.split()) for t in declared] != expected {
        sys.exit(
            f"gen_layouts: cpython_api.jac's {layout.name} fields {declared} differ from the header's {expected}"
        );
    }
}

def c_type_name(layout: Layout) -> str {
    return layout.ctype;
}

def render_jac(values: dict[str, int]) -> str {
    records = capi_records();
    shared = [
        name
        for name in order
        if name in records
    ];
    for name in shared {
        check_capi_record(emitted[name]);
    }
    from_capi = sorted({"PyObject"} | (set(opaque) & records) | set(shared));
    local = sorted(set(opaque) - set(from_capi));
    lines = [
        '"""CPython object layouts for native Jac object-model ports.',
        "",
        f"Generated by scripts/jacpython/gen_layouts.jac from CPython {pin()[
            'version'
        ]}",
        "headers; do not edit. bootstrap/python/layouts_check.c asserts every offset,",
        "size and constant against the configured headers of each JacPython build.",
        "",
        "`PyObject` stays the opaque handle of cpython_api.jac; `_object` is the",
        "layout behind it (C's `struct _object`), read by casting a handle to",
        "`ptr[_object]`. Its reference count is an anonymous union whose widest",
        "member, `ob_refcnt_full`, stands for it: the release build's 32-bit count,",
        "overflow and flags are the low, middle and high parts of that i64 on every",
        "supported (little-endian) target. A trailing C array `T name[1]`",
        "(`_PyLongValue.ob_digit`, `PyTupleObject.ob_item`) is one T field with",
        "the same offset, size and alignment: element 0 is that field, and the",
        "object's further elements follow it in memory, reached by pointer",
        "arithmetic from the field's offset exactly as C indexes past the declared",
        "bound. A fixed array `T name[N]` (`PyDateTime_DateTime.data`) is N T",
        "fields, `name` for element 0 and `name_1` to `name_<N-1>` for the rest.",
        "Pointers to records no port reads yet are opaque.",
        '"""',
        "",
        "import from c {"
    ];
    lines += [f"    obj {name};" for name in local];
    for name in order {
        if name in shared {
            continue;
        }
        layout = emitted[name];
        fields = ", ".join(f"{f.name}: {f.jac}" for f in layout.fields);
        lines.append(f"    obj {name} {{ has {fields}; }}");
    }
    lines += ["}", ""];
    for (name, _, jac) in CONSTANTS {
        # The probe reads every value as a signed long long.
        value = values[name];
        if jac.startswith("u") and value < 0 {
            value += 1 << 64;
        }
        lines.append(f"glob {name}: Final[{jac}] = {value};");
    }
    return "\n".join(lines) + "\n";
}

# One platform's table of PLATFORM_CONSTANTS, or with `suffix` empty the
# table of a platform with none generated: LAYOUTS_PLATFORM is "" and every
# value 0.
def render_platform(suffix: str, values: dict[str, int]) -> str {
    target = f"the {suffix.replace('.', ' ')}" if suffix else "no generated";
    lines = [
        f'"""Platform layout constants for {target} JacPython build.',
        "",
        f"Generated by scripts/jacpython/gen_layouts.jac from CPython {pin()[
            'version'
        ]}",
        "headers; do not edit. bootstrap/python/layouts_check.c asserts each value on",
        "its platform.",
        '"""',
        "",
        f'glob LAYOUTS_PLATFORM: str = "{suffix}";'
    ];
    for (name, _, jac) in PLATFORM_CONSTANTS {
        lines.append(f"glob {name}: Final[{jac}] = {values.get(name, 0)};");
    }
    return "\n".join(lines) + "\n";
}

# The upstream definitions of the private structs among the layouts.
def private_definitions -> list[str] {
    c_types = {jac: c for (jac, c) in LAYOUTS};
    structs = [
        headers.private[name]
            if name in headers.private
            else headers.private[c_types[name]]
        for name in order
        if name in headers.private or c_types.get(name, "") in headers.private
    ];
    scalars = [
        text
        for (name, text) in headers.private_scalars.items()
        if any(re.search(rf"\b{name}\b", struct) is not None for struct in structs)
    ];
    return scalars + structs;
}

# GCC's and Clang's __builtin_classify_type class of a field's Jac type.
def type_class(jac: str) -> int {
    if jac.startswith(("ptr", "Callable")) {
        return 5;
    }
    if jac in ("f32", "f64") {
        return 8;
    }
    return 1 if jac in SIZES else 12;
}

def render_check(
    values: dict[str, int], platform_values: dict[str, dict[str, int]]
) -> str {
    lines = [
        "/* Generated by scripts/jacpython/gen_layouts.jac; do not edit.",
        " * Every layout and constant jaclang/runtime/python/layouts.jac declares,",
        " * asserted against the configured CPython headers. build.sh compiles this",
        " * for every JacPython build, so a layout drift fails the build. */",
        "#ifndef Py_BUILD_CORE",
        "#define Py_BUILD_CORE 1",
        "#endif",
        "#include \"Python.h\""
    ]
        + [f"#include \"{header}\"" for header in INCLUDES]
        + ["#include <stddef.h>", ""];
    private = private_definitions();
    if private {
        lines += [
            "/* The private object structs of the ported Objects/ files, as the",
            " * pinned sources define them. */"
        ]
            + private
            + [""];
    }
    lines += [
        "#define FIELD(type, field, offset, size) \\",
        "    _Static_assert(offsetof(type, field) == (offset), #type \".\" #field \" offset\"); \\",
        "    _Static_assert(sizeof(((type *)0)->field) == (size), #type \".\" #field \" size\")",
        "#define KIND(type, field, class) \\",
        "    _Static_assert(__builtin_classify_type(((type *)0)->field) == (class), \\",
        "                   #type \".\" #field \" kind\")",
        "#define SIGNED(type, field, is_signed) \\",
        "    _Static_assert(((__typeof__(((type *)0)->field))-1 < 0) == (is_signed), \\",
        "                   #type \".\" #field \" signedness\")",
        "#define LAYOUT(type, size, align) \\",
        "    _Static_assert(sizeof(type) == (size), #type \" size\"); \\",
        "    _Static_assert(_Alignof(type) == (align), #type \" alignment\")",
        "#define CONSTANT(expression, value) \\",
        "    _Static_assert((long long)(expression) == (value), #expression)",
        ""
    ];
    for name in order {
        layout = emitted[name];
        ctype = c_type_name(layout);
        lines.append(f"/* {name} */");
        for field in layout.fields {
            lines.append(
                f"FIELD({ctype}, {field.designator()}, {field.offset}, {field.size});"
            );
            lines.append(
                f"KIND({ctype}, {field.designator()}{'[0]' if field.array else ''}, {4
                    if field.boolean
                    else type_class(field.jac)});"
            );
            if field.signed is not None {
                lines.append(
                    f"SIGNED({ctype}, {field.designator()}{'[0]'
                        if field.array
                        else ''}, {1 if field.signed else 0});"
                );
            }
        }
        lines.append(f"LAYOUT({ctype}, {layout.size}, {layout.align});");
        lines.append("");
    }
    for (name, expression, _) in CONSTANTS {
        lines.append(f"CONSTANT({expression}, {values[name]}LL);");
    }
    lines += ["", "/* The platform constants of layouts_platform.<os>.<arch>.jac. */"];
    keyword = "#if";
    for (suffix, _, condition) in PLATFORMS {
        lines.append(f"{keyword} {condition}");
        for (name, expression, _) in PLATFORM_CONSTANTS {
            lines.append(f"CONSTANT({expression}, {platform_values[suffix][name]}LL);");
        }
        keyword = "#elif";
    }
    lines += [
        "#else",
        "#error \"no generated layouts_platform table for this platform\"",
        "#endif"
    ];
    return "\n".join(lines) + "\n";
}

# --------------------------------------------------------------- C toolchain
# The installed headers of a local JacPython build: any platform's will do,
# since the asserts hold the constants to the same values on every build.
def default_include -> Path {
    for config in sorted(
        (JAC / ".python-build/jacpython").glob(
            "*/python/install/include/python3.14/pyconfig.h"
        )
    ) {
        return config.parent;
    }
    sys.exit(
        "No configured CPython headers under jac/.python-build; run a JacPython build or pass --headers"
    );
}

def probe_flags(headers_dir: Path) -> list[str] {
    return [f"-I{headers_dir}", "-DPy_BUILD_CORE=1"];
}

# Constant values as the compiler folds them against the configured headers.
def extract(
    headers_dir: Path,
    compiler: list[str],
    constants: list[tuple[str, str, str]] = CONSTANTS
) -> dict[str, int] {
    lines = ["#define Py_BUILD_CORE 1", "#include \"Python.h\""]
        + [f"#include \"{header}\"" for header in INCLUDES]
        + ["#include <stddef.h>"]
        + private_definitions();
    for (name, expression, _) in constants {
        lines.append(
            f"const long long __jac_layout_{name} = (long long)({expression});"
        );
    }
    # The assembly goes to a file: zig cc ignores `-o -`.
    with tempfile.TemporaryDirectory() as scratch {
        probe = Path(scratch) / "constants.c";
        listing_path = Path(scratch) / "constants.s";
        probe.write_text("\n".join(lines) + "\n");
        result = subprocess.run(
            compiler
                + probe_flags(headers_dir)
                + ["-S", "-O0", "-o", str(listing_path), str(probe)],
            capture_output=True,
            text=True
        );
        if result.returncode != 0 {
            sys.exit(result.stderr);
        }
        listing = listing_path.read_text();
    }
    values: dict[str, int] = {};
    current: (str | None) = None;
    for line in listing.splitlines() {
        line = line.strip();
        label = re.match(r"^_?__jac_layout_(\w+):", line);
        if label {
            current = label.group(1);
            continue;
        }
        if current is None {
            continue;
        }
        data = re.match(r"^\.(?:quad|xword|8byte|dword)\s+(-?\w+)", line);
        if data {
            value = int(data.group(1), 0);
            values[current] = value - (1 << 64) if value >= (1 << 63) else value;
            current = None;
        } elif re.match(r"^\.zero\s+8", line) {
            values[current] = 0;
            current = None;
        }
    }
    missing = [
        n
        for (n, _, _) in constants
        if n not in values
    ];
    if missing {
        sys.exit(f"gen_layouts: no value read back for {', '.join(missing)}");
    }
    return values;
}

# Compile the generated asserts against the configured headers.
def verify(check: str, headers_dir: Path, compiler: list[str]) {
    with tempfile.TemporaryDirectory() as scratch {
        probe = Path(scratch) / "layouts_check.c";
        probe.write_text(check);
        result = subprocess.run(
            compiler
                + probe_flags(headers_dir)
                + ["-c", "-o", str(Path(scratch) / "layouts_check.o"), str(probe)],
            capture_output=True,
            text=True
        );
    }
    if result.returncode != 0 {
        sys.exit(f"Generated layouts do not match the headers:\n{result.stderr}");
    }
}

with entry:__main__ {
    parser = argparse.ArgumentParser(
        description="Generate CPython object layouts for native Jac"
    );
    parser.add_argument("--cc", help="C compiler command");
    parser.add_argument(
        "--headers", help="directory holding a configured CPython's Python.h"
    );
    parser.add_argument("--zig", help="zig, for the platform constants");
    parser.set_defaults(cc="cc", zig="zig");
    parser.add_argument("--check", action="store_true");
    args = parser.parse_args();
    read_headers(headers);
    for (name, _) in LAYOUTS {
        require(name);
    }
    headers_dir = Path(args.headers) if args.headers else default_include();
    compiler = shlex.split(args.cc);
    values = extract(headers_dir, compiler);
    platform_values: dict[str, dict[str, int]] = {};
    for (suffix, target, _) in PLATFORMS {
        platform_values[suffix] = extract(
            headers_dir, [args.zig, "cc", "-target", target], PLATFORM_CONSTANTS
        );
    }
    check = render_check(values, platform_values);
    verify(check, headers_dir, compiler);
    current = write_or_check(
        OUTPUT, format_jac(render_jac(values), OUTPUT), args.check, COMMAND
    );
    current = write_or_check(CHECK, check, args.check, COMMAND) and current;
    for (suffix, _, _) in PLATFORMS + [("", "", "")] {
        table = RUNTIME
            / (
                f"{PLATFORM_OUTPUT}.{suffix}.jac"
                    if suffix
                    else f"{PLATFORM_OUTPUT}.jac"
            );
        current = write_or_check(
            table,
            format_jac(render_platform(suffix, platform_values.get(suffix, {})), table),
            args.check,
            COMMAND
        )
            and current;
    }
    if not current {
        sys.exit(1);
    }
}
