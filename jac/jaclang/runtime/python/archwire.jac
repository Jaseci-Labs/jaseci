graph import {
    capi --> bindings.arguments { boundary_failure, object_error, required, text_value }
    capi --> bindings.array { object_error, text_object }
    capi --> bindings.collections { boundary_failure, object_error, repr_value, text_object, type_name }
    capi --> bindings.csv { object_error, type_name }
    capi --> bindings.functools { boundary_failure, object_error, text_object }
    capi --> bindings.json { boundary_failure, object_error, object_tuple, type_name }
    capi --> bindings.operator { boundary_failure, object_error, text_object }
    capi --> bindings.pickle { builtin_kind, object_error, text_value }
    capi --> bindings.struct { boundary_failure, jac_heap_size, jac_list_heap_size, object_error, repr_value, text_object, type_name }
    capi --> constant_input { boundary_failure, read_buffer }
    capi --> constant_output { checked, required, text_object, write_buffer }
    capi --> modules.array { boundary_failure, checked, jac_heap_size, object_error, object_tuple, repr_value, required, text_object }
    capi --> modules.binary_scalars { required }
    capi --> modules.binascii { module_failure, object_error, read_buffer, write_buffer }
    capi --> modules.bisect { object_error }
    capi --> modules.cmath { boundary_failure, checked, object_error, object_tuple, required }
    capi --> modules.collections { boundary_failure, checked, jac_heap_size, jac_list_heap_size, object_error, repr_value, required, text_object, text_value, type_name }
    capi --> modules.combinatorics { boundary_failure, checked, jac_heap_size, jac_list_heap_size, object_error, required }
    capi --> modules.csv { boundary_failure, checked, object_error, object_tuple, required, text_object, type_name }
    capi --> modules.functools { boundary_failure, checked, object_error, repr_value, required, text_object, text_value, type_name }
    capi --> modules.grouping { boundary_failure, checked, required }
    capi --> modules.heapq { object_error }
    capi --> modules.iterators { boundary_failure, checked, object_error, repr_value, required, text_object, type_name }
    capi --> modules.json { boundary_failure, checked, object_error, object_tuple, pair, repr_value, required, serialization_note, text_object, type_name }
    capi --> modules.math { boundary_failure, object_error, repr_value, required, type_name }
    capi --> modules.operator { boundary_failure, object_error, pair, repr_value, required, text_object, text_value }
    capi --> modules.pickle { boundary_failure, checked, jac_heap_size, jac_list_heap_size, required, text_value }
    capi --> modules.pickle_decode { boundary_failure, checked, object_tuple, required, text_value }
    capi --> modules.pickle_encode { boundary_failure, builtin_kind, checked, object_tuple, repr_value, required, serialization_note, text_object, text_value, type_name }
    capi --> modules.pickle_objects { boundary_failure, checked, object_tuple, repr_value, required, text_object, text_value }
    capi --> modules.pickle_stream { boundary_failure, checked, object_error, object_tuple, required }
    capi --> modules.queue { object_error }
    capi --> modules.random { object_error }
    capi --> modules.statistics { object_error }
    capi --> modules.struct { boundary_failure, checked, jac_heap_size, jac_list_heap_size, object_error, required }
    capi --> modules.tee { boundary_failure, checked, object_error, required }
    capi --> native_services { boundary_failure, read_buffer, required }
    capi --> symtable { boundary_failure }
    capi --> tokenize { boundary_failure, checked, required, text_object }
    compiler_integer --> constant_input { integer_from_marshal }
    compiler_integer --> constant_keys { PyBigInt, integer_decimal }
    compiler_integer --> constant_output { PyBigInt }
    compiler_integer --> native_services { integer_from_marshal }
    constant_keys --> constant_output { constant_key }
    native_services --> constant_input { take_buffer }
    native_services --> tokenize { parse_float, parse_integer, take_buffer }
    objects --> compiler_integer { PyInt, PyObj, PyStr }
    objects --> constant_input { PyBool, PyBytes, PyComplex, PyEllipsis, PyFloat, PyNoneType, PyObj, PySet, PyStr, PyTuple }
    objects --> constant_keys { PyBool, PyBytes, PyCode, PyComplex, PyFloat, PyInt, PyObj, PySet, PySlice, PyStr, PyTuple }
    objects --> constant_output { PyBool, PyBytes, PyCode, PyComplex, PyEllipsis, PyFloat, PyInt, PyNoneType, PyObj, PySet, PySlice, PyStr, PyTuple }
    objects --> native_services { PyObj }
    objects --> symtable { PyObj, py_error }
    opcode_meta --> constant_output { CO_FAST_CELL, CO_FAST_FREE, CO_FAST_HIDDEN, CO_FAST_LOCAL, CO_OPTIMIZED }
    opcode_meta --> objects { NB_ADD, NB_AND, NB_FLOOR_DIVIDE, NB_LSHIFT, NB_MULTIPLY, NB_OR, NB_POWER, NB_REMAINDER, NB_RSHIFT, NB_SUBTRACT, NB_TRUE_DIVIDE, NB_XOR }
    capi --> bindings.converters { boundary_failure, object_error, text_value, type_name }
    capi --> bindings.errno { object_error }
    capi --> bindings.grp { object_error }
    capi --> bindings.pwd { object_error }
    capi --> bindings.resource { object_error }
    capi --> bindings.stat { boundary_failure, object_error }
    capi --> bindings.syslog { boundary_failure, object_error }
    capi --> modules.bz2 { object_error }
    capi --> modules.csv | modules.json { new_writer }
    capi --> modules.grp { object_error, repr_value }
    capi --> modules.opcode { object_error, object_tuple, type_name }
    capi --> modules.output_buffer { object_error }
    capi --> modules.pwd { object_error, repr_value }
    capi --> modules.resource { object_error, object_tuple }
    capi --> modules.stat { boundary_failure, object_error }
    capi --> modules.suggestions { object_error }
    capi --> modules.syslog { object_error, object_tuple }
    capi --> modules.zlib { object_error, text_value }
    cpython_api --> bindings.arguments { NULL, PyDict_Items, PyList_GetItemRef, PyLong_AsSsize_t, PyNumber_Index, PyObject, PyTuple_Size, PyUnicode_ReadChar, Py_NewRef, jacpy_error_pending, jacpy_is_unicode, jacpy_list_size, jacpy_release, jacpy_tuple_item, jacpy_unicode_size }
    cpython_api --> bindings.array { NULL, PyImport_ImportModuleAttrString, PyIndex_Check, PyLong_FromLongLong, PyObject, PyObject_CallOneArg, PyObject_GetAttrString, PySys_AuditTuple, PyType_GetSlot, PyUnicode_FromOrdinal, Py_NewRef, Py_TYPE, Py_buffer, jacpy_dict_size, jacpy_error_pending, jacpy_is_bytearray, jacpy_is_bytes, jacpy_is_slice, jacpy_is_unicode, jacpy_release, jacpy_slice_adjust, jacpy_slice_unpack }
    cpython_api --> bindings.binascii { NULL, PyObject }
    cpython_api --> bindings.bisect { PyObject }
    cpython_api --> bindings.buffer { PyObject, Py_buffer, jacpy_buffer_acquire, jacpy_buffer_bytes, jacpy_buffer_release }
    cpython_api --> bindings.bz2 { PyObject }
    cpython_api --> bindings.clinic.bz2 { NULL, PyObject }
    cpython_api --> bindings.clinic.grp { NULL, PyObject }
    cpython_api --> bindings.clinic.opcode { NULL, PyObject }
    cpython_api --> bindings.clinic.pwd { NULL, PyObject }
    cpython_api --> bindings.clinic.resource { NULL, PyObject }
    cpython_api --> bindings.clinic.suggestions { NULL, PyObject }
    cpython_api --> bindings.clinic.sysconfig { NULL, PyObject }
    cpython_api --> bindings.clinic.syslog { NULL, PyObject }
    cpython_api --> bindings.clinic.tracemalloc { NULL, PyObject }
    cpython_api --> bindings.clinic.typing { NULL, PyObject }
    cpython_api --> bindings.clinic.weakref { NULL, PyObject, jacpy_is_dict }
    cpython_api --> bindings.clinic.zlib { NULL, PyObject }
    cpython_api --> bindings.cmath { PyFloat_FromDouble, PyObject }
    cpython_api --> bindings.collections { NULL, PyCallable_Check, PyDict_New, PyDict_Update, PyLong_FromLongLong, PyObject, PyObject_Call, PyObject_GetAttrString, PyObject_GetIter, PyTuple_GetSlice, PyTuple_New, PyTuple_Size, Py_NewRef, Py_TYPE, jacpy_is_dict, jacpy_is_tuple, jacpy_release, jacpy_tuple_item, jacpy_type_check }
    cpython_api --> bindings.converters { NULL, PyErr_Occurred, PyFloat_AsDouble, PyFloat_FromDouble, PyIndex_Check, PyLong_AsInt, PyLong_AsLong, PyLong_AsLongLong, PyLong_AsSsize_t, PyLong_AsUnsignedLongLongMask, PyLong_AsUnsignedLongMask, PyLong_FromLong, PyLong_FromSize_t, PyLong_FromSsize_t, PyLong_FromUnsignedLong, PyNumber_Index, PyObject, PyObject_IsTrue, Py_GetConstantBorrowed, Py_TYPE, jacpy_is_float, jacpy_is_unicode, jacpy_release }
    cpython_api --> bindings.csv { NULL, PyCallable_Check, PyDict_New, PyDict_SetItem, PyLong_AsLongLong, PyLong_FromLongLong, PyObject, PyObject_Call, PyObject_GetIter, PyTuple_New, PyUnicode_FromOrdinal, Py_NewRef, Py_TYPE, jacpy_error_pending, jacpy_is_unicode, jacpy_optional_attr, jacpy_release, jacpy_text, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_type_check }
    cpython_api --> bindings.errno { PyDict_New, PyDict_SetItem, PyDict_SetItemString, PyLong_FromLong, PyModule_GetDict, PyObject, PyUnicode_FromString, jacpy_release }
    cpython_api --> bindings.functools { NULL, PyCallable_Check, PyIndex_Check, PyObject, PyObject_GenericGetDict, PyObject_GenericSetDict, PyObject_GetAttrString, PyObject_IsTrue, PyObject_RichCompare, PyTuple_GetSlice, PyTuple_New, PyTuple_Size, Py_LeaveRecursiveCall, Py_NewRef, Py_TYPE, jacpy_dict_size, jacpy_error_pending, jacpy_recursion_enter, jacpy_release, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_type_check }
    cpython_api --> bindings.grp { PyObject, jacpy_struct_sequence_type }
    cpython_api --> bindings.heapq { PyObject }
    cpython_api --> bindings.itertools { PyObject }
    cpython_api --> bindings.json { NULL, PyObject, PyObject_GetAttrString, PyObject_IsTrue, Py_NewRef, jacpy_is_dict, jacpy_is_unicode, jacpy_release }
    cpython_api --> bindings.math { NULL, PyFloat_FromDouble, PyObject }
    cpython_api --> bindings.module { NULL, PyModule_AddObjectRef, PyObject, jacpy_release }
    cpython_api --> bindings.opcode { PyModule_AddIntConstant, PyObject }
    cpython_api --> bindings.operator { NULL, PyObject, PyTuple_Size, PyVectorcall_NARGS, Py_NewRef, Py_TYPE, jacpy_dict_size, jacpy_release }
    cpython_api --> bindings.payload { PyObject, Py_TYPE }
    cpython_api --> bindings.pickle { NULL, PyImport_ImportModuleAttrString, PyObject, PyObject_GenericGetAttr, PyObject_GenericSetAttr, Py_NewRef, Py_TYPE, jacpy_is_unicode, jacpy_release }
    cpython_api --> bindings.pwd { PyObject, jacpy_struct_sequence_type }
    cpython_api --> bindings.queue { NULL, PyObject }
    cpython_api --> bindings.random { NULL, PyObject, jacpy_release }
    cpython_api --> bindings.references { NULL, PyObject, PyTuple_New, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> bindings.resource { PyLong_FromLong, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, jacpy_struct_sequence_type }
    cpython_api --> bindings.runtime_objects { PyModule_AddObjectRef, PyObject }
    cpython_api --> bindings.stat { NULL, PyLong_FromUnsignedLong, PyModule_AddIntConstant, PyObject, PyUnicode_FromString }
    cpython_api --> bindings.state { PyObject }
    cpython_api --> bindings.statistics { PyObject }
    cpython_api --> bindings.struct { NULL, PyDict_New, PyLong_FromLongLong, PyObject, PyTuple_Size, Py_NewRef, jacpy_buffer_new, jacpy_bytes_address, jacpy_bytes_decode, jacpy_error_pending, jacpy_release, jacpy_tuple_item }
    cpython_api --> bindings.suggestions { PyObject }
    cpython_api --> bindings.sysconfig { PyObject }
    cpython_api --> bindings.syslog { NULL, PyModule_AddIntConstant, PyObject, PyTuple_GetItem, PyTuple_Size }
    cpython_api --> bindings.tracemalloc { PyObject }
    cpython_api --> bindings.type { NULL, PyObject, Py_buffer }
    cpython_api --> bindings.types { PyObject }
    cpython_api --> bindings.typing { PyObject }
    cpython_api --> bindings.weakref { PyObject }
    cpython_api --> bindings.zlib { NULL, PyModule_AddIntConstant, PyObject, PyUnicode_FromString, Py_NewRef, jacpy_release }
    cpython_api --> capi { PyBytes_FromStringAndSize, PyErr_GetRaisedException, PyErr_SetRaisedException, PyObject, PyObject_Repr, PyTuple_New, PyUnicodeWriter, Py_NewRef, jacpy_bytes_copy_to, jacpy_bytes_length, jacpy_qualified_type_name, jacpy_release, jacpy_text, jacpy_tuple_set_owned, jacpy_type_name, jacpy_utf8, jacpy_writer_new }
    cpython_api --> characters { _PyUnicode_IsPrintable, _PyUnicode_IsXidContinue, _PyUnicode_IsXidStart }
    cpython_api --> constant_input { PyObject, PyObject_IsTrue, PySequence_List, jacpy_float_value, jacpy_marshal, jacpy_release, jacpy_sequence_item, jacpy_sequence_size, jacpy_utf8, jacpy_value_kind }
    cpython_api --> constant_output { NULL, PyBool_FromLong, PyComplex_FromDoubles, PyFloat_FromDouble, PyLong_FromLongLong, PyNumber_Negative, PyObject, PySlice_New, PyTuple_New, Py_NewRef, jacpy_code_new, jacpy_long_from_bytes, jacpy_release, jacpy_set_new, jacpy_tuple_set_owned }
    cpython_api --> modules.array { NULL, PyByteArray_Resize, PyFloat_AsDouble, PyFloat_FromDouble, PyIter_Next, PyList_Append, PyLong_AsLongLong, PyLong_AsUnsignedLongLong, PyLong_FromLongLong, PyNumber_Index, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_GetIter, PyObject_RichCompare, PyObject_RichCompareBool, PyUnicode_FromOrdinal, PyUnicode_Join, PyUnicode_ReadChar, Py_NewRef, jacpy_bytearray_memory, jacpy_bytearray_new, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_error_pending, jacpy_float32_bits, jacpy_float_bits, jacpy_float_unpack, jacpy_is_bytes, jacpy_is_unicode, jacpy_list_new, jacpy_memory_copy, jacpy_memory_move, jacpy_native_little_endian, jacpy_native_size, jacpy_release, jacpy_unicode_decode_bytes, jacpy_unicode_size }
    cpython_api --> modules.binary_scalars { NULL, PyLong_FromLongLong, PyLong_FromUnsignedLongLong, PyObject }
    cpython_api --> modules.binascii { NULL, PyLong_FromLongLong, PyObject, jacpy_buffer_byte, jacpy_buffer_size, jacpy_set_exception }
    cpython_api --> modules.bisect { NULL, PyObject, PyObject_CallOneArg, PySequence_Size, Py_LeaveRecursiveCall, jacpy_comparison_slot, jacpy_less, jacpy_recursion_enter, jacpy_release, jacpy_same_type, jacpy_sequence_slot }
    cpython_api --> modules.bz2 { NULL, PyBytes_AsString, PyErr_NoMemory, PyEval_RestoreThread, PyEval_SaveThread, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyMem_Realloc, PyObject, PyThreadState, PyThread_acquire_lock, PyThread_allocate_lock, PyThread_free_lock, PyThread_release_lock, jacpy_buffer_new, jacpy_memory_copy, jacpy_memory_move, jacpy_release }
    cpython_api --> modules.cmath { NULL, PyFloat_AsDouble, PyFloat_FromDouble, PyNumber_TrueDivide, PyObject, jacpy_clear_errno, jacpy_complex_value, jacpy_error_pending, jacpy_math_errno, jacpy_release }
    cpython_api --> modules.collections { NULL, PyIter_Next, PyLong_FromLongLong, PyNumber_Add, PyObject, PyObject_Call, PyObject_GetAttr, PyObject_GetIter, PyObject_RichCompareBool, PyObject_SetItem, PySequence_List, PyTuple_New, Py_NewRef, Py_ReprEnter, Py_ReprLeave, jacpy_dict_default, jacpy_dict_repr, jacpy_error_pending, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.combinatorics { NULL, PyObject, PySequence_Tuple, PyTuple_New, PyTuple_Size, Py_NewRef, jacpy_release, jacpy_tuple_exchange, jacpy_tuple_item, jacpy_tuple_set_owned }
    cpython_api --> modules.csv { NULL, PyDict_Keys, PyDict_SetItem, PyErr_Clear, PyIter_Next, PyList_Append, PyLong_AsInt, PyLong_AsLongLong, PyLong_FromLongLong, PyNumber_Check, PyNumber_Float, PyObject, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_GetIter, PyObject_IsTrue, PyObject_Str, PyUnicodeWriter, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteChar, PyUnicode_ReadChar, Py_NewRef, jacpy_dict_get, jacpy_dict_pop_discard, jacpy_error_pending, jacpy_is_exact_long, jacpy_is_unicode, jacpy_list_new, jacpy_release, jacpy_set_exception, jacpy_tuple_item, jacpy_type_check, jacpy_unicode_size, jacpy_writer_new }
    cpython_api --> modules.functools { NULL, PyCallable_Check, PyDict_Clear, PyDict_Copy, PyDict_New, PyDict_SetItem, PyDict_Update, PyIter_Next, PyLong_AsLongLong, PyLong_FromLongLong, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_GetIter, PyObject_Hash, PyObject_RichCompare, PyObject_SetItem, PyObject_Str, PySequence_Tuple, PyTuple_New, PyTuple_Size, Py_NewRef, Py_ReprEnter, Py_ReprLeave, jacpy_call_two, jacpy_dict_get, jacpy_dict_size, jacpy_error_pending, jacpy_is_dict, jacpy_is_exact_dict, jacpy_is_exact_long, jacpy_is_exact_tuple, jacpy_is_exact_unicode, jacpy_is_tuple, jacpy_object_type, jacpy_release, jacpy_tuple_item, jacpy_tuple_set_owned }
    cpython_api --> modules.grouping { NULL, PyIter_Next, PyObject, PyObject_CallOneArg, PyObject_GetIter, PyObject_RichCompareBool, PyTuple_New, Py_NewRef, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.grp { NULL, PyBytes_AsString, PyErr_NoMemory, PyErr_Occurred, PyEval_RestoreThread, PyEval_SaveThread, PyList_Append, PyList_New, PyLong_FromLong, PyMem_RawFree, PyMem_RawRealloc, PyObject, PySequence_Contains, PyUnicode_EncodeFSDefault, jacpy_fs_text, jacpy_release }
    cpython_api --> modules.heapq { NULL, PyList_Append, PyList_GetItemRef, PyObject, Py_NewRef, jacpy_less, jacpy_list_delete, jacpy_list_exchange, jacpy_list_size, jacpy_list_swap, jacpy_release }
    cpython_api --> modules.iterators { NULL, PyErr_Clear, PyIter_Next, PyList_Append, PyList_GetItemRef, PyLong_AsLongLong, PyNumber_Add, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_GetIter, PyObject_IsTrue, PySequence_Tuple, PyTuple_New, PyTuple_Size, Py_NewRef, jacpy_call_two, jacpy_error_pending, jacpy_is_long, jacpy_list_exchange, jacpy_list_new, jacpy_list_size, jacpy_release, jacpy_tuple_exchange, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_tuple_unique }
    cpython_api --> modules.json { NULL, PyDict_DelItem, PyDict_New, PyDict_SetItem, PyErr_SetObject, PyImport_ImportModuleAttrString, PyList_Append, PyList_GetItemRef, PyList_Sort, PyLong_AsLongLong, PyLong_FromLongLong, PyLong_FromVoidPtr, PyMapping_Items, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_IsTrue, PySequence_Contains, PySequence_Fast, PySequence_Repeat, PyTuple_Size, PyUnicodeWriter, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteASCII, PyUnicodeWriter_WriteChar, PyUnicodeWriter_WriteStr, PyUnicodeWriter_WriteSubstring, PyUnicode_Concat, PyUnicode_ReadChar, PyUnicode_Substring, Py_LeaveRecursiveCall, Py_NewRef, jacpy_dict_default, jacpy_dict_size, jacpy_error_pending, jacpy_fast_item, jacpy_fast_size, jacpy_float_repr, jacpy_float_value, jacpy_is_bool, jacpy_is_dict, jacpy_is_exact_dict, jacpy_is_float, jacpy_is_list, jacpy_is_long, jacpy_is_tuple, jacpy_is_unicode, jacpy_list_new, jacpy_list_size, jacpy_long_repr, jacpy_recursion_enter, jacpy_release, jacpy_tuple_item, jacpy_unicode_size, jacpy_writer_new }
    cpython_api --> modules.math { NULL, PyErr_Clear, PyFloat_AsDouble, PyFloat_FromDouble, PyIter_Next, PyLong_AsDouble, PyLong_AsLongLong, PyLong_AsUnsignedLongLong, PyLong_FromDouble, PyLong_FromLongLong, PyLong_FromUnsignedLongLong, PyNumber_Absolute, PyNumber_Add, PyNumber_FloorDivide, PyNumber_Index, PyNumber_Multiply, PyNumber_Subtract, PyObject, PyObject_GetIter, PyObject_RichCompareBool, PySequence_Tuple, PyTuple_Size, Py_NewRef, _PyLong_GCD, _PyLong_NumBits, jacpy_clear_errno, jacpy_error_pending, jacpy_float_bits, jacpy_float_from_bits, jacpy_is_bool, jacpy_is_exact_float, jacpy_is_exact_long, jacpy_is_long, jacpy_is_tuple, jacpy_long_fits_i64, jacpy_long_shift, jacpy_long_sign, jacpy_math_errno, jacpy_release, jacpy_special_noargs, jacpy_tuple_item }
    cpython_api --> modules.object_ring { NULL, PyObject }
    cpython_api --> modules.opcode { NULL, PyErr_Occurred, PyList_Append, PyList_New, PyLong_AsLong, PyObject, PyUnicode_FromString, PyUnicode_InternFromString, Py_NewRef, _PyCompile_GetBinaryIntrinsicName, _PyCompile_GetUnaryIntrinsicName, jacpy_is_code, jacpy_release }
    cpython_api --> modules.operator { NULL, PyImport_ImportModuleAttrString, PyList_GetItemRef, PyLong_AsLongLong, PyNumber_Absolute, PyNumber_Add, PyNumber_And, PyNumber_FloorDivide, PyNumber_InPlaceAdd, PyNumber_InPlaceAnd, PyNumber_InPlaceFloorDivide, PyNumber_InPlaceLshift, PyNumber_InPlaceMatrixMultiply, PyNumber_InPlaceMultiply, PyNumber_InPlaceOr, PyNumber_InPlaceRemainder, PyNumber_InPlaceRshift, PyNumber_InPlaceSubtract, PyNumber_InPlaceTrueDivide, PyNumber_InPlaceXor, PyNumber_Index, PyNumber_Invert, PyNumber_Lshift, PyNumber_MatrixMultiply, PyNumber_Multiply, PyNumber_Negative, PyNumber_Or, PyNumber_Positive, PyNumber_Remainder, PyNumber_Rshift, PyNumber_Subtract, PyNumber_TrueDivide, PyNumber_Xor, PyObject, PyObject_Call, PyObject_DelItem, PyObject_GetAttr, PyObject_GetItem, PyObject_IsTrue, PyObject_LengthHint, PyObject_Repr, PyObject_RichCompare, PyObject_SetItem, PySequence_Concat, PySequence_Contains, PySequence_Count, PySequence_InPlaceConcat, PySequence_Index, PyTuple_GetSlice, PyTuple_New, PyTuple_Size, PyUnicode_Join, Py_NewRef, Py_ReprEnter, Py_ReprLeave, jacpy_dict_size, jacpy_is_unicode, jacpy_list_size, jacpy_power, jacpy_release, jacpy_text, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_unicode_split, jacpy_utf8 }
    cpython_api --> modules.output_buffer { NULL, PyBytes_AsString, PyBytes_Size, PyList_Append, PyList_GetItem, PyList_New, PyList_Size, PyObject, Py_NewRef, jacpy_buffer_new, jacpy_memory_copy, jacpy_release }
    cpython_api --> modules.pickle { NULL, PyDict_Clear, PyDict_Copy, PyDict_New, PyDict_SetItem, PyList_GetItemRef, PyLong_AsLongLong, PyLong_FromLongLong, PyLong_FromVoidPtr, PyMapping_Items, PyObject, PyObject_GetIter, PyTuple_Size, Py_NewRef, jacpy_bytearray_memory, jacpy_error_pending, jacpy_is_dict, jacpy_is_tuple, jacpy_list_size, jacpy_release, jacpy_tuple_item }
    cpython_api --> modules.pickle_decode { NULL, PyDict_Items, PyDict_New, PyDict_SetItem, PyFloat_FromDouble, PyFloat_FromString, PyImport_ImportModuleAttrString, PyIter_Next, PyList_Append, PyList_GetItemRef, PyLong_AsLongLong, PyLong_FromLongLong, PyMemoryView_FromObject, PyNumber_Long, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_IsTrue, PyObject_SetAttr, PyObject_SetItem, PyTuple_New, PyTuple_Size, Py_NewRef, jacpy_bytearray_new, jacpy_bytes_address, jacpy_bytes_decode, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_bytes_unescape, jacpy_dict_get, jacpy_dict_size, jacpy_error_pending, jacpy_float_unpack, jacpy_is_dict, jacpy_is_exact_unicode, jacpy_is_list, jacpy_is_tuple, jacpy_is_type, jacpy_is_unicode, jacpy_list_new, jacpy_list_size, jacpy_long_from_signed_bytes, jacpy_memory_copy, jacpy_optional_attr, jacpy_release, jacpy_set_new, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_type_new, jacpy_unicode_intern }
    cpython_api --> modules.pickle_encode { NULL, PyByteArray_Resize, PyCallable_Check, PyDict_SetItem, PyImport_ImportModuleAttrString, PyIter_Check, PyIter_Next, PyList_GetItemRef, PyLong_AsLongLong, PyLong_FromLongLong, PyLong_FromUnsignedLongLong, PyLong_FromVoidPtr, PyMapping_Items, PyNumber_Add, PyObject, PyObject_Call, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_GetIter, PyObject_IsTrue, PyObject_Str, PySequence_List, PyTuple_GetSlice, PyTuple_Size, PyUnicode_AsEncodedString, PyUnicode_ReadChar, Py_LeaveRecursiveCall, Py_NewRef, _PyLong_NumBits, jacpy_bytes_address, jacpy_bytes_decode, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_dict_get, jacpy_dict_size, jacpy_error_pending, jacpy_float_bits, jacpy_float_repr, jacpy_float_value, jacpy_is_dict, jacpy_is_tuple, jacpy_is_type, jacpy_is_unicode, jacpy_list_size, jacpy_long_fits_i64, jacpy_long_repr, jacpy_long_sign, jacpy_long_signed_bytes, jacpy_mapping_optional_item, jacpy_object_type, jacpy_optional_attr, jacpy_recursion_enter, jacpy_release, jacpy_tuple_item, jacpy_unicode_size }
    cpython_api --> modules.pickle_objects { NULL, PyDict_Copy, PyDict_Keys, PyErr_GetRaisedException, PyErr_SetRaisedException, PyImport_Import, PyImport_ImportModuleAttrString, PyList_GetItemRef, PyObject, PyObject_GetAttr, PyObject_Str, PyTuple_Size, Py_NewRef, jacpy_dict_get, jacpy_error_pending, jacpy_is_tuple, jacpy_is_unicode, jacpy_list_size, jacpy_optional_attr, jacpy_release, jacpy_tuple_item }
    cpython_api --> modules.pickle_stream { NULL, PyByteArray_Resize, PyErr_GetRaisedException, PyErr_SetRaisedException, PyLong_FromLongLong, PyObject, PyObject_Call, PyObject_CallOneArg, Py_NewRef, jacpy_bytearray_new, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_exception_context, jacpy_is_bytes, jacpy_memory_copy, jacpy_release, jacpy_set_exception }
    cpython_api --> modules.pwd { NULL, PyBytes_AsString, PyErr_NoMemory, PyEval_RestoreThread, PyEval_SaveThread, PyList_Append, PyList_New, PyLong_FromLong, PyMem_RawFree, PyMem_RawRealloc, PyObject, PySequence_Contains, PyThreadState, PyUnicode_EncodeFSDefault, PyUnicode_FromString, jacpy_fs_text, jacpy_release }
    cpython_api --> modules.queue { NULL, PyErr_SetNone, PyObject, PyThread_release_lock, Py_MakePendingCalls, Py_NewRef, _PyDeadline_Get, _PyDeadline_Init, jacpy_error_pending, jacpy_lock_free, jacpy_lock_wait, jacpy_release, jacpy_timeout_ns }
    cpython_api --> modules.random { NULL, PyErr_Clear, PyLong_AsLongLong, PyLong_AsUnsignedLong, PyLong_FromLongLong, PyObject, PyTuple_New, PyTuple_Size, _PyLong_NumBits, jacpy_buffer_byte, jacpy_buffer_new, jacpy_buffer_set, jacpy_buffer_size, jacpy_entropy, jacpy_error_pending, jacpy_hash_unsigned, jacpy_is_long, jacpy_is_tuple, jacpy_long_absolute, jacpy_long_bytes, jacpy_long_from_bytes, jacpy_monotonic_time, jacpy_process_id, jacpy_release, jacpy_tuple_item, jacpy_tuple_set_owned, jacpy_wall_time }
    cpython_api --> modules.resource { NULL, PyErr_SetFromErrno, PyFloat_FromDouble, PyLong_FromLong, PyLong_FromUnsignedLongLong, PyLong_IsNegative, PyNumber_Index, PyObject, PySequence_Tuple, PySys_AuditTuple, PyTuple_GetItem, PyTuple_Size, Py_NewRef, jacpy_errno, jacpy_long_u64_checked, jacpy_release }
    cpython_api --> modules.stat { PyErr_Occurred, PyLong_AsUnsignedLong, PyNumber_Index, PyObject, jacpy_is_long, jacpy_release }
    cpython_api --> modules.statistics { PyObject }
    cpython_api --> modules.struct { NULL, PyDict_Clear, PyDict_SetItem, PyErr_Clear, PyFloat_AsDouble, PyFloat_FromDouble, PyIndex_Check, PyLong_AsLongLong, PyLong_AsUnsignedLongLong, PyNumber_Index, PyObject, PyObject_CallOneArg, PyObject_IsTrue, PyTuple_New, Py_NewRef, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_complex_value, jacpy_dict_get, jacpy_dict_size, jacpy_error_pending, jacpy_float_pack, jacpy_float_unpack, jacpy_is_bytearray, jacpy_is_bytes, jacpy_is_long, jacpy_long_address, jacpy_memory_copy, jacpy_memory_zero, jacpy_native_float_store, jacpy_native_little_endian, jacpy_native_size, jacpy_release, jacpy_set_exception, jacpy_tuple_item, jacpy_tuple_set_owned }
    cpython_api --> modules.suggestions { NULL, PyErr_Occurred, PyList_GetItem, PyList_Size, PyObject, Py_NewRef, _Py_CalculateSuggestions, jacpy_is_exact_list, jacpy_is_unicode }
    cpython_api --> modules.sysconfig { NULL, PyDict_New, PyDict_SetItemString, PyLong_FromLong, PyObject, jacpy_release }
    cpython_api --> modules.syslog { NULL, PyErr_Clear, PyErr_Occurred, PyInterpreterState_Get, PyInterpreterState_Main, PyList_GetItem, PyList_Size, PyLong_FromLong, PyObject, PySys_AuditTuple, PyUnicode_AsUTF8, PyUnicode_FindChar, PyUnicode_FromString, PyUnicode_GetLength, PyUnicode_Substring, Py_NewRef, _PySys_GetOptionalAttrString, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.tee { NULL, PyIter_Next, PyList_GetItemRef, PyObject, PyObject_GetIter, PyTuple_New, Py_NewRef, jacpy_list_size, jacpy_object_type, jacpy_release, jacpy_tuple_set_owned, jacpy_type_check }
    cpython_api --> modules.tracemalloc { NULL, PyLong_FromLong, PyLong_FromSize_t, PyObject, Py_NewRef, _PyTraceMalloc_ClearTraces, _PyTraceMalloc_GetMemory, _PyTraceMalloc_GetObjectTraceback, _PyTraceMalloc_GetTracebackLimit, _PyTraceMalloc_GetTracedMemory, _PyTraceMalloc_GetTraces, _PyTraceMalloc_IsTracing, _PyTraceMalloc_ResetPeak, _PyTraceMalloc_Start, _PyTraceMalloc_Stop }
    cpython_api --> modules.typing { PyObject, Py_NewRef }
    cpython_api --> modules.weakref { NULL, PyObject, PyWeakref_NewProxy, Py_NewRef, _PyWeakref_GetWeakrefCount, jacpy_remove_dead_weakref, jacpy_weakref_list }
    cpython_api --> modules.zlib { NULL, PyBytes_AsString, PyBytes_FromStringAndSize, PyBytes_Size, PyErr_NoMemory, PyErr_SetNone, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyLong_FromUnsignedLong, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyMem_Realloc, PyObject, PyObject_CheckBuffer, PyThreadState, PyThread_acquire_lock, PyThread_allocate_lock, PyThread_free_lock, PyThread_release_lock, PyType_GetModule, Py_NewRef, Py_TYPE, _PyBytes_Resize, jacpy_buffer_acquire, jacpy_buffer_new, jacpy_buffer_release, jacpy_fs_text, jacpy_memory_copy, jacpy_memory_move, jacpy_release }
    cpython_api --> native_services { PyObject, jacpy_bytes_escape, jacpy_float_value, jacpy_parse_float, jacpy_parse_long, jacpy_release, jacpy_take_error_text, jacpy_unicode_escape }
    cpython_api --> objects { NULL, PyErr_SetFromErrnoWithFilenameObjects, PyObject_IsTrue, PyObject_RichCompare, PyObject_RichCompareBool, PySequence_Fast, PySequence_GetItem, PySequence_Tuple, PyUnicode_Format, _Py_c_pow, _Py_c_quot }
    cpython_api --> symtable { NULL, PyDict_New, PyLong_FromLongLong, PyObject, jacpy_dict_set_owned, jacpy_list_new, jacpy_release, jacpy_symtable_entry }
    cpython_api --> tokenize { NULL, PyLong_FromLongLong, PyObject, PyTuple_New, jacpy_readline, jacpy_release, jacpy_tuple_set_owned }
    opcode_meta --> modules.opcode { is_block_push_opcode, opcode_has_arg, opcode_has_const, opcode_has_free, opcode_has_jump, opcode_has_local, opcode_has_name, opcode_is_valid, stack_effect }
    capi --> modules.atexit | modules.blake2 | modules.hashlib | modules.sha3 { object_error }
    capi --> modules.hmac { object_error, text_value }
    cpython_api --> bindings.atexit { PyObject }
    cpython_api --> bindings.blake2 { PyDict_SetItemString, PyLong_FromLong, PyModule_AddIntConstant, PyObject, PyType_GetDict, Py_TYPE, jacpy_release }
    cpython_api --> bindings.clinic.blake2 | bindings.clinic.sha3 { NULL, PyObject }
    cpython_api --> bindings.clinic.hmac | bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 { NULL, PyObject }
    cpython_api --> bindings.converters { jacpy_unsigned_converter }
    cpython_api --> bindings.hmac { PyModule_AddIntConstant, PyObject }
    cpython_api --> bindings.md5 | bindings.sha1 { PyLong_FromLong, PyModule_AddIntConstant, PyObject, PyUnicode_FromString }
    cpython_api --> bindings.sha2 { NULL, PyLong_FromLong, PyModule_AddIntConstant, PyObject, PyUnicode_FromString, Py_TYPE }
    cpython_api --> bindings.sha3 { PyModule_AddIntConstant, PyModule_AddStringConstant, PyObject, Py_TYPE }
    cpython_api --> modules.atexit { NULL, PyCallable_Check, PyInterpreterState, PyInterpreterState_Get, PyList_Clear, PyList_GetItem, PyList_GetSlice, PyList_Insert, PyList_SetSlice, PyList_Size, PyLong_FromSsize_t, PyObject, PyObject_Call, PyObject_RichCompareBool, PyTuple_GetItem, PyTuple_GetSlice, PyTuple_New, PyTuple_Size, Py_NewRef, jacpy_atexit_callbacks, jacpy_atexit_detach, jacpy_atexit_push, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.blake2 { NULL, PyErr_NoMemory, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyObject, PyUnicode_FromString, Py_TYPE, jacpy_hacl_simd_features, jacpy_memory_copy, jacpy_memory_zero, jacpy_release }
    cpython_api --> modules.hashlib { NULL, PyErr_NoMemory, PyEval_RestoreThread, PyEval_SaveThread, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CheckBuffer, PyThread_acquire_lock, PyThread_allocate_lock, PyThread_free_lock, PyThread_release_lock, Py_NewRef, Py_TYPE, _Py_strhex, jacpy_bytes_from_memory, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.hmac { NULL, PyErr_NoMemory, PyErr_SetObject, PyLong_FromLong, PyLong_FromVoidPtr, PyMem_Free, PyMem_Malloc, PyNumber_ToBase, PyObject, PyObject_CallNoArgs, PyObject_GetAttrString, PyObject_Repr, PyUnicode_AsUTF8, PyUnicode_Concat, PyUnicode_FromString, Py_TYPE, _Py_strhex, jacpy_bytes_from_memory, jacpy_hacl_simd_features, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.md5 | modules.sha1 | modules.sha2 { NULL, PyErr_NoMemory, PyObject, Py_TYPE, jacpy_release }
    cpython_api --> modules.numeric { jacpy_libm_cos, jacpy_libm_exp, jacpy_libm_exp2, jacpy_libm_fma, jacpy_libm_log, jacpy_libm_log10, jacpy_libm_log2, jacpy_libm_sin, jacpy_libm_tan }
    cpython_api --> modules.sha3 { NULL, PyBytes_FromStringAndSize, PyErr_NoMemory, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyObject, PyType_GetModule, PyUnicode_FromString, Py_TYPE, _Py_strhex, jacpy_bytes_from_memory, jacpy_release }
    capi --> bindings.arguments { c_string_text, type_name }
    capi --> bindings.asyncio { c_string_copy }
    capi --> bindings.clinic.abc { boundary_failure }
    capi --> bindings.clinic.array { boundary_failure }
    capi --> bindings.clinic.asyncio { boundary_failure }
    capi --> bindings.clinic.binascii { boundary_failure }
    capi --> bindings.clinic.bisect { boundary_failure }
    capi --> bindings.clinic.blake2 { boundary_failure }
    capi --> bindings.clinic.bz2 { boundary_failure }
    capi --> bindings.clinic.cmath { boundary_failure }
    capi --> bindings.clinic.codecs { boundary_failure }
    capi --> bindings.clinic.collections { boundary_failure }
    capi --> bindings.clinic.csv { boundary_failure }
    capi --> bindings.clinic.datetime { boundary_failure }
    capi --> bindings.clinic.elementtree { boundary_failure }
    capi --> bindings.clinic.fcntl { boundary_failure }
    capi --> bindings.clinic.functools { boundary_failure }
    capi --> bindings.clinic.grp { boundary_failure }
    capi --> bindings.clinic.hashopenssl { boundary_failure }
    capi --> bindings.clinic.heapq { boundary_failure }
    capi --> bindings.clinic.hmac { boundary_failure }
    capi --> bindings.clinic.itertools { boundary_failure }
    capi --> bindings.clinic.locale { boundary_failure }
    capi --> bindings.clinic.lsprof { boundary_failure }
    capi --> bindings.clinic.lzma { boundary_failure }
    capi --> bindings.clinic.math { boundary_failure }
    capi --> bindings.clinic.md5 { boundary_failure }
    capi --> bindings.clinic.mmap { boundary_failure }
    capi --> bindings.clinic.multibytecodec { boundary_failure }
    capi --> bindings.clinic.multiprocessing { boundary_failure }
    capi --> bindings.clinic.opcode { boundary_failure }
    capi --> bindings.clinic.operator { boundary_failure }
    capi --> bindings.clinic.pickle { boundary_failure }
    capi --> bindings.clinic.posix { boundary_failure }
    capi --> bindings.clinic.posixshmem { boundary_failure }
    capi --> bindings.clinic.posixsubprocess { boundary_failure }
    capi --> bindings.clinic.pwd { boundary_failure }
    capi --> bindings.clinic.pyexpat { boundary_failure }
    capi --> bindings.clinic.queue { boundary_failure }
    capi --> bindings.clinic.random { boundary_failure }
    capi --> bindings.clinic.resource { boundary_failure }
    capi --> bindings.clinic.select { boundary_failure }
    capi --> bindings.clinic.sha1 { boundary_failure }
    capi --> bindings.clinic.sha2 { boundary_failure }
    capi --> bindings.clinic.sha3 { boundary_failure }
    capi --> bindings.clinic.socket { boundary_failure }
    capi --> bindings.clinic.sqlite3 { boundary_failure }
    capi --> bindings.clinic.sre { boundary_failure }
    capi --> bindings.clinic.ssl { boundary_failure }
    capi --> bindings.clinic.statistics { boundary_failure }
    capi --> bindings.clinic.struct { boundary_failure }
    capi --> bindings.clinic.suggestions { boundary_failure }
    capi --> bindings.clinic.sysconfig { boundary_failure }
    capi --> bindings.clinic.syslog { boundary_failure }
    capi --> bindings.clinic.termios { boundary_failure }
    capi --> bindings.clinic.time { boundary_failure }
    capi --> bindings.clinic.tracemalloc { boundary_failure }
    capi --> bindings.clinic.typing { boundary_failure }
    capi --> bindings.clinic.unicodedata { boundary_failure }
    capi --> bindings.clinic.weakref { boundary_failure }
    capi --> bindings.clinic.zlib { boundary_failure }
    capi --> bindings.clinic.zoneinfo { boundary_failure }
    capi --> bindings.clinic.zstd { boundary_failure }
    capi --> bindings.fcntl { object_error }
    capi --> bindings.locale { object_error }
    capi --> bindings.mmap { object_error }
    capi --> bindings.module { c_string_copy }
    capi --> bindings.pickle { builtin_type }
    capi --> bindings.posix { object_error }
    capi --> bindings.posixsubprocess { object_error }
    capi --> bindings.select { object_error }
    capi --> bindings.socket { object_error }
    capi --> bindings.ssl { object_error }
    capi --> bindings.termios { object_error }
    capi --> bindings.time { object_error }
    capi --> bindings.type { c_string_copy }
    capi --> bindings.zstd { c_string_text }
    capi --> modules.abc { object_error }
    capi --> modules.array | modules.hashlib { type_name }
    capi --> modules.binary_scalars { memory_byte, memory_set }
    capi --> modules.binascii { boundary_failure }
    capi --> modules.cjkcodecs { object_error }
    capi --> modules.codecs { object_error }
    capi --> modules.datetime_date { boundary_failure }
    capi --> modules.datetime_datetime { boundary_failure }
    capi --> modules.datetime_delta { boundary_failure }
    capi --> modules.datetime_time { boundary_failure }
    capi --> modules.datetime_tzinfo { boundary_failure }
    capi --> modules.decimal_context { c_string_text }
    capi --> modules.decimal_number { boundary_failure, c_string_length, c_string_text }
    capi --> modules.elementtree { StaticText, object_error, text_value }
    capi --> modules.fcntl { audit_event, object_error, type_name }
    capi --> modules.hashopenssl { c_size, c_string_copy, c_string_text, object_error, text_value }
    capi --> modules.itertools { boundary_failure, object_error, required, text_object }
    capi --> modules.locale { object_error }
    capi --> modules.lsprof { boundary_failure, object_error, text_object, text_value }
    capi --> modules.lzma { boundary_failure, object_error }
    capi --> modules.mmap { boundary_failure, object_error, type_name }
    capi --> modules.multibytecodec { boundary_failure, c_string_text, object_error, text_value, type_name }
    capi --> modules.multiprocessing { c_string_copy, c_string_text, object_error, text_value }
    capi --> modules.openssl { c_string_copy }
    capi --> modules.pickle { builtin_kind, builtin_type, object_error, text_object }
    capi --> modules.pickle_decode { memory_byte }
    capi --> modules.pickle_encode { builtin_kind_of, memory_byte }
    capi --> modules.pickle_stream { memory_byte, memory_set }
    capi --> modules.posix_core { boundary_failure }
    capi --> modules.posix_stat { audit_event, boundary_failure }
    capi --> modules.posixshmem { object_error }
    capi --> modules.posixsubprocess { audit_event, object_error, type_name }
    capi --> modules.pyexpat { StaticText, c_string_text, object_error, text_object, text_value, type_name }
    capi --> modules.select { boundary_failure, object_error, object_tuple, text_value, type_name }
    capi --> modules.socket { boundary_failure, c_string_text, object_error }
    capi --> modules.socket_address { c_string_length, c_string_text, object_error, text_value }
    capi --> modules.socket_object { c_int, object_error }
    capi --> modules.sqlite3 { boundary_failure, c_string_copy, c_string_length, c_string_text, object_error, text_value }
    capi --> modules.ssl { boundary_failure, c_int, c_string_length, c_string_text, c_text, object_error, text_value }
    capi --> modules.ssl_cert { c_int, c_text }
    capi --> modules.ssl_core { c_int, c_size, c_string_text, object_error }
    capi --> modules.struct { memory_byte, memory_set, type_name }
    capi --> modules.termios { object_error }
    capi --> modules.time { boundary_failure, c_string_text, object_error, object_tuple, text_value, type_name }
    capi --> modules.unicodedata { c_string_length, c_string_text, object_error }
    capi --> modules.zoneinfo { object_error }
    capi --> modules.zstd { boundary_failure, object_error }
    capi --> native_services { text_object, text_value }
    cpython_api --> bindings.abc { PyObject, PyUnicode_InternFromString, jacpy_release }
    cpython_api --> bindings.arguments { PyDict_GetItemStringRef, PyDict_Next, PyDict_Size, PyErr_NoMemory, PyErr_Occurred, PyErr_WarnEx, PyExc_DeprecationWarning, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyList_New, PyList_SetItem, PyLong_AsLong, PyLong_AsLongLong, PyLong_AsUnsignedLongLongMask, PyLong_AsUnsignedLongMask, PyMem_Free, PyMem_Malloc, PyObject_IsTrue, PyTuple_GetItem, PyTuple_New, PyTuple_SetItem, PyType_IsSubtype, PyUnicode_AsUTF8AndSize, PyUnicode_Equal, PyUnicode_FromString, PyUnicode_InternFromString, Py_None, Py_TYPE, _Py_CalculateSuggestions, jacpy_dict_size, jacpy_is_bytes, jacpy_tuple_items }
    cpython_api --> bindings.array { PyErr_WarnEx, PyExc_DeprecationWarning, PyExc_IndexError, PyExc_TypeError, PyNumber_AsSsize_t, Py_None, Py_NotImplemented }
    cpython_api --> bindings.asyncio { NULL, PyDict_Next, PyImport_ImportModule, PyMethodDef, PyModule_AddType, PyObject, PyObject_CallNoArgs, PyObject_GenericGetAttr, PyObject_GetAttrString, PyObject_IsTrue, PyObject_SelfIter, PySet_New, PyTuple_GetItem, PyTuple_Size, PyType_FromModuleAndSpec, PyType_GenericNew, PyType_Slot, PyType_Spec, Py_BuildValue, Py_None, jacpy_dict_size, jacpy_release }
    cpython_api --> bindings.binascii { PyExc_ValueError }
    cpython_api --> bindings.buffer { NULL, PyArg_Parse, PyErr_NoMemory, PyMem_Calloc, PyMem_Free, PyObject_GetBuffer }
    cpython_api --> bindings.clinic.abc { NULL, PyObject }
    cpython_api --> bindings.clinic.array { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.asyncio { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.binascii { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.bisect { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.blake2 { PyMem_Free, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.bz2 { PyMem_Free, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.cmath { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.codecs { NULL, PyMem_Free, PyObject, jacpy_is_bytes }
    cpython_api --> bindings.clinic.collections { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.csv { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.datetime { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.elementtree { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_is_dict, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.fcntl { NULL, PyObject }
    cpython_api --> bindings.clinic.functools { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.grp { PyMem_Free }
    cpython_api --> bindings.clinic.hashopenssl { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.heapq { NULL, PyObject, jacpy_is_list }
    cpython_api --> bindings.clinic.hmac { PyMem_Free }
    cpython_api --> bindings.clinic.itertools { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_is_list, jacpy_tuple_items }
    cpython_api --> bindings.clinic.json { NULL, PyObject }
    cpython_api --> bindings.clinic.locale { NULL, PyObject }
    cpython_api --> bindings.clinic.lsprof { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.lzma { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.math { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.md5 { PyMem_Free }
    cpython_api --> bindings.clinic.mmap { NULL, PyObject }
    cpython_api --> bindings.clinic.multibytecodec { NULL, PyMem_Free, PyObject, jacpy_is_long, jacpy_is_tuple }
    cpython_api --> bindings.clinic.multiprocessing { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.opcode { PyMem_Free }
    cpython_api --> bindings.clinic.operator { NULL, PyObject }
    cpython_api --> bindings.clinic.pickle { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.posix { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.posixshmem { NULL, PyObject, jacpy_is_unicode }
    cpython_api --> bindings.clinic.posixsubprocess { NULL, PyObject, jacpy_is_tuple }
    cpython_api --> bindings.clinic.pwd { jacpy_is_unicode }
    cpython_api --> bindings.clinic.pyexpat { NULL, PyMem_Free, PyObject }
    cpython_api --> bindings.clinic.queue { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.random { NULL, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.select { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.sha1 { PyMem_Free }
    cpython_api --> bindings.clinic.sha2 { PyMem_Free }
    cpython_api --> bindings.clinic.sha3 { PyMem_Free, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.socket { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.sqlite3 { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_is_tuple, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.sre { NULL, PyLong_AsSsize_t, PyMem_Free, PyObject, jacpy_is_dict, jacpy_is_list, jacpy_is_tuple }
    cpython_api --> bindings.clinic.ssl { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.statistics { NULL, PyObject }
    cpython_api --> bindings.clinic.struct { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_release, jacpy_tuple_items }
    cpython_api --> bindings.clinic.syslog { PyMem_Free }
    cpython_api --> bindings.clinic.termios { NULL, PyObject }
    cpython_api --> bindings.clinic.time { NULL, PyObject }
    cpython_api --> bindings.clinic.unicodedata { NULL, PyObject }
    cpython_api --> bindings.clinic.zlib { PyMem_Free }
    cpython_api --> bindings.clinic.zoneinfo { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_tuple_items }
    cpython_api --> bindings.clinic.zstd { NULL, PyMem_Free, PyObject, PyTuple_Size, jacpy_dict_size, jacpy_is_bytes, jacpy_is_tuple, jacpy_is_type, jacpy_tuple_items }
    cpython_api --> bindings.codecs { PyObject }
    cpython_api --> bindings.codecs_cn { PyObject }
    cpython_api --> bindings.codecs_hk { PyObject }
    cpython_api --> bindings.codecs_iso2022 { PyObject }
    cpython_api --> bindings.codecs_jp { PyObject }
    cpython_api --> bindings.codecs_kr { PyObject }
    cpython_api --> bindings.codecs_tw { PyObject }
    cpython_api --> bindings.collections { PyExc_AttributeError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyODict_Type, PyObject_CallNoArgs, Py_None, Py_NotImplemented }
    cpython_api --> bindings.converters { PyArg_Parse, PyErr_Clear, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyNumber_AsSsize_t, PyType_GetSlot, PyUnicode_AsUTF8AndSize, PyUnicode_FSConverter, PyUnicode_ReadChar, Py_None, _PyLong_UInt16_Converter, _PyLong_UInt32_Converter, _PyLong_UInt64_Converter, _PyLong_UInt8_Converter, _PyLong_UnsignedInt_Converter, _PyLong_UnsignedShort_Converter, jacpy_is_exact_long, jacpy_unicode_size }
    cpython_api --> bindings.csv { PyExc_SystemError, PyExc_TypeError, Py_None }
    cpython_api --> bindings.datetime { NULL, PyDict_SetItemString, PyInterpreterState, PyInterpreterState_Get, PyLong_FromDouble, PyLong_FromLong, PyMemberDef, PyMethodDef, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, PyType_FromModuleAndSpec, PyType_Slot, PyType_Spec, Py_NewRef, Py_None, _PyStaticType_InitForExtension, _PyType_GetDict, jacpy_release }
    cpython_api --> bindings.decimal { NULL, PyContextVar_New, PyDict_SetItemString, PyErr_Format, PyErr_NewException, PyErr_SetString, PyExc_ArithmeticError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ZeroDivisionError, PyImport_ImportModule, PyLong_FromSsize_t, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyMethodDef, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddStringConstant, PyModule_AddType, PyObject, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallObject, PyObject_GenericGetAttr, PyObject_GetAttrString, PyObject_HashNotImplemented, PyTuple_New, PyTuple_Pack, PyTuple_SetItem, PyType_FromMetaclass, PyType_GetDict, PyType_Slot, PyType_Spec, PyUnicode_FromString, PyUnicode_InternFromString, Py_NewRef, Py_None, jacpy_is_type, jacpy_release }
    cpython_api --> bindings.elementtree { NULL, PyExc_SyntaxError, PyImport_ImportModule, PyImport_ImportModuleAttrString, PyModule_AddObjectRef, PyObject, PyObject_GenericGetAttr, PyUnicode_InternFromString }
    cpython_api --> bindings.errno { PyExc_ImportError }
    cpython_api --> bindings.fcntl { PyExc_ImportError, PyModule_AddIntConstant, PyObject }
    cpython_api --> bindings.functools { PyBaseObject_Type, PyDict_New, PyDict_SetItem, PyExc_AttributeError, PyExc_SystemError, PyExc_TypeError, PyObject_CallNoArgs, PyTuple_GetItem, PyVectorcall_NARGS, Py_None, Py_NotImplemented }
    cpython_api --> bindings.grp { PyExc_ImportError }
    cpython_api --> bindings.hashopenssl { NULL, PyLong_FromLong, PyModule_Add, PyModule_AddIntConstant, PyObject, Py_TYPE, jacpy_release }
    cpython_api --> bindings.heapq { PyUnicode_FromString }
    cpython_api --> bindings.hmac { PyExc_ValueError }
    cpython_api --> bindings.json { PyExc_SystemError, PyExc_TypeError, Py_None }
    cpython_api --> bindings.locale { NULL, PyExc_ImportError, PyModule_AddIntConstant, PyObject, jacpy_char_max }
    cpython_api --> bindings.lsprof { PyObject, jacpy_struct_sequence_type }
    cpython_api --> bindings.lzma { NULL, PyLong_FromLongLong, PyModule_Add, PyObject, PyTuple_New, jacpy_release }
    cpython_api --> bindings.members { PyMemberDef, PyMember_GetOne, PyMember_SetOne, PyObject }
    cpython_api --> bindings.mmap { PyExc_ImportError, PyExc_OSError, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject }
    cpython_api --> bindings.module { PyCFunction_NewEx, PyErr_NoMemory, PyMem_RawCalloc, PyMethodDef }
    cpython_api --> bindings.multibytecodec { NULL, PyObject, PyUnicode_InternFromString, jacpy_release }
    cpython_api --> bindings.multiprocessing { PyDict_New, PyDict_SetItemString, PyLong_FromLong, PyObject, PyType_GetDict, jacpy_release }
    cpython_api --> bindings.operator { PyExc_SystemError, PyExc_TypeError }
    cpython_api --> bindings.pickle { PyExc_TypeError, Py_None }
    cpython_api --> bindings.posix { NULL, PyDict_New, PyDict_SetItemString, PyExc_ImportError, PyExc_OSError, PyList_Append, PyList_New, PyLong_FromLong, PyMethodDef, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, PyObject_SelfIter, PyType_Modified, PyUnicode_FromString, PyUnicode_InternFromString, _PyType_AddMethod, jacpy_release }
    cpython_api --> bindings.posixshmem { PyObject }
    cpython_api --> bindings.posixsubprocess { PyExc_ImportError, PyObject }
    cpython_api --> bindings.pwd { PyExc_ImportError }
    cpython_api --> bindings.pyexpat { NULL, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddStringConstant, PyObject, PyUnicode_InternFromString }
    cpython_api --> bindings.references { PyObject_Call, PyObject_GetAttrString }
    cpython_api --> bindings.resource { PyExc_ImportError, PyExc_OSError }
    cpython_api --> bindings.select { PyErr_Clear, PyExc_ImportError, PyExc_OSError, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, PyObject_DelAttrString, PyUnicode_InternFromString, jacpy_release }
    cpython_api --> bindings.socket { NULL, PyErr_NewException, PyErr_NoMemory, PyExc_ImportError, PyExc_OSError, PyExc_TimeoutError, PyMem_Free, PyMem_Malloc, PyMemberDef, PyMethodDef, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddType, PyObject, PyThread_allocate_lock, PyType_FromMetaclass, PyType_Slot, PyType_Spec, Py_NewRef, jacpy_release }
    cpython_api --> bindings.sqlite3 { NULL, PyDict_New, PyExc_Exception, PyImport_ImportModuleAttrString, PyLong_FromLong, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, PyObject_CallFinalizerFromDealloc, PyUnicode_InternFromString, jacpy_release }
    cpython_api --> bindings.sre { NULL, PyLong_FromUnsignedLong, PyMemberDef, PyMethodDef, PyModule_Add, PyModule_AddIntConstant, PyModule_AddStringConstant, PyObject, PyType_FromModuleAndSpec, PyType_Slot, PyType_Spec, Py_None, jacpy_release }
    cpython_api --> bindings.ssl { NULL, PyArg_ParseTuple, PyDict_New, PyDict_SetItem, PyErr_NewExceptionWithDoc, PyErr_NoMemory, PyErr_SetString, PyExc_OSError, PyExc_TypeError, PyExc_ValueError, PyLong_FromLong, PyLong_FromUnsignedLongLong, PyMem_Free, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddStringConstant, PyObject, PyObject_Str, PyThread_allocate_lock, PyTuple_Pack, PyTuple_Size, PyType_FromSpecWithBases, PyType_Slot, PyType_Spec, PyUnicode_FromString, PyUnicode_InternFromString, Py_BuildValue, Py_NewRef, Py_TYPE, Py_buffer, jacpy_buffer_release, jacpy_is_unicode, jacpy_release }
    cpython_api --> bindings.stat { PyExc_ImportError }
    cpython_api --> bindings.struct { PyExc_IndexError, PyExc_TypeError, PyNumber_AsSsize_t, Py_None }
    cpython_api --> bindings.syslog { PyExc_ImportError, PyExc_TypeError }
    cpython_api --> bindings.termios { NULL, PyExc_ImportError, PyLong_FromUnsignedLong, PyModule_AddIntConstant, PyObject }
    cpython_api --> bindings.time { PyExc_ImportError, PyModule_AddIntConstant, PyObject, jacpy_struct_sequence_type }
    cpython_api --> bindings.type { PyErr_NoMemory, PyMem_Free, PyMem_Malloc, PyMem_RawCalloc, PyType_GetSlot, Py_TYPE }
    cpython_api --> bindings.types { PyAsyncGen_Type, PyCFunction_Type, PyCapsule_Type, PyCell_Type, PyClassMethodDescr_Type, PyCode_Type, PyCoro_Type, PyDictProxy_Type, PyEllipsis_Type, PyFrame_Type, PyFunction_Type, PyGen_Type, PyGetSetDescr_Type, PyMemberDescr_Type, PyMethodDescr_Type, PyMethod_Type, PyModule_Type, PyTraceBack_Type, PyWrapperDescr_Type, Py_GenericAliasType, _PyMethodWrapper_Type, _PyNamespace_Type, _PyNone_Type, _PyNotImplemented_Type, _PyUnion_Type }
    cpython_api --> bindings.typing { _PyTypeAlias_Type, _PyUnion_Type, _Py_NoDefaultStruct, jacpy_typing_types }
    cpython_api --> bindings.unicodedata { PyModule_Add, PyModule_AddStringConstant, PyModule_AddType, PyObject, jacpy_release }
    cpython_api --> bindings.uuid { PyModule_AddIntConstant, PyObject }
    cpython_api --> bindings.weakref { _PyWeakref_CallableProxyType, _PyWeakref_ProxyType, _PyWeakref_RefType }
    cpython_api --> bindings.zoneinfo { PyModule_AddObjectRef, PyObject }
    cpython_api --> bindings.zstd { NULL, PyLong_FromLong, PyLong_FromSize_t, PyModule_AddIntConstant, PyObject, PyObject_SetAttrString, PyType_Freeze, jacpy_release }
    cpython_api --> capi { PyBool_Type, PyByteArray_Type, PyBytes_Type, PyDict_Type, PyFloat_Type, PyFrozenSet_Type, PyFunction_Type, PyList_Type, PyLong_Type, PyMem_RawMalloc, PyObject_CallMethod, PyPickleBuffer_Type, PySet_Type, PySys_AuditTuple, PyTuple_Type, PyType_Type, PyUnicode_DecodeUTF8Stateful, PyUnicode_Type, Py_TYPE, _PyNone_Type, jacpy_bytes_from_memory, jacpy_set_exception, jacpy_unicode_decode_bytes }
    cpython_api --> constant_output { Py_Ellipsis, Py_None }
    cpython_api --> layouts { PyMemberDef, PyMethodDef, PyObject, PyType_Slot, PyType_Spec, Py_buffer, Py_complex }
    cpython_api --> modules.abc { NULL, PyDict_Pop, PyErr_Clear, PyErr_ExceptionMatches, PyExc_AssertionError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyIter_Next, PyList_GetItemRef, PyLong_AsLong, PyLong_FromUnsignedLongLong, PyMapping_Items, PyObject, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_GetAttr, PyObject_GetIter, PyObject_GetOptionalAttr, PyObject_IsSubclass, PyObject_IsTrue, PyObject_SetAttr, PySequence_Fast, PySet_Add, PySet_Clear, PySet_Contains, PySet_Discard, PySet_New, PySet_Size, PyTuple_Size, PyType_GetFlags, PyType_GetModule, PyType_IsSubtype, PyWeakref_GetRef, PyWeakref_NewRef, Py_NewRef, Py_NotImplemented, Py_TYPE, _PyObject_IsAbstract, _PyType_GetDict, _PyType_SetFlags, _PyType_SetFlagsRecursive, jacpy_error_pending, jacpy_fast_item, jacpy_fast_size, jacpy_is_exact_long, jacpy_is_list, jacpy_is_tuple, jacpy_is_type, jacpy_list_size, jacpy_release, jacpy_set_new, jacpy_tuple_item }
    cpython_api --> modules.array { PyExc_BufferError, PyExc_EOFError, PyExc_IndexError, PyExc_MemoryError, PyExc_OverflowError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsSsize_t, PyLong_FromVoidPtr, PyType_IsSubtype, Py_None, Py_TYPE, jacpy_builtins, jacpy_dict_get, jacpy_is_list, jacpy_is_long, jacpy_is_type, jacpy_optional_attr }
    cpython_api --> modules.asyncio { NULL, PyCFunction_NewEx, PyContext_CopyCurrent, PyContext_Enter, PyContext_Exit, PyDict_New, PyDict_SetItem, PyErr_ExceptionMatches, PyErr_Format, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_GivenExceptionMatches, PyErr_NormalizeException, PyErr_Restore, PyErr_SetObject, PyErr_SetRaisedException, PyErr_SetString, PyErr_WarnEx, PyExc_AttributeError, PyExc_DeprecationWarning, PyExc_KeyboardInterrupt, PyExc_RuntimeError, PyExc_SystemExit, PyExc_TypeError, PyExc_ValueError, PyException_GetTraceback, PyFrozenSet_New, PyGen_Type, PyIter_Send, PyList_Append, PyList_Extend, PyList_GetItem, PyList_New, PyList_SetItem, PyList_SetSlice, PyList_Size, PyLong_FromLong, PyLong_FromSsize_t, PyLong_FromUnsignedLongLong, PyMethodDef, PyObject, PyObject_CallFinalizerFromDealloc, PyObject_CallMethodObjArgs, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_ClearManagedDict, PyObject_ClearWeakRefs, PyObject_GC_Del, PyObject_GC_Track, PyObject_GC_UnTrack, PyObject_GetAttr, PyObject_GetOptionalAttr, PyObject_IsInstance, PyObject_IsTrue, PyObject_RichCompareBool, PyObject_SetAttr, PyObject_Str, PyObject_Vectorcall, PyObject_VisitManagedDict, PySet_Add, PySet_Discard, PySet_New, PyTraceBack_Type, PyTuple_GetItem, PyTuple_New, PyTuple_Size, PyUnicode_FromFormat, PyUnicode_FromString, Py_NewRef, Py_None, Py_TYPE, _PyArg_CheckPositional, _PyErr_ChainExceptions1, _PyGen_FetchStopIterationValue, _PyGen_SetStopIterationValue, _PyObject_GC_New, _PyType_Name, jacpy_asyncio_add_tasks, jacpy_asyncio_thread_task, jacpy_dict_size, jacpy_is_exact_long, jacpy_is_exact_unicode, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.asyncio.call_with_task { PyObject_Call }
    cpython_api --> modules.asyncio_core { NULL, PyCoro_Type, PyErr_Format, PyErr_GivenExceptionMatches, PyErr_SetObject, PyErr_SetString, PyExc_BaseException, PyExc_RuntimeError, PyExc_StopIteration, PyExc_TypeError, PyException_GetTraceback, PyException_SetCause, PyException_SetContext, PyException_SetTraceback, PyInterpreterState_Get, PyList_Append, PyList_GetItem, PyList_New, PyList_SetItem, PyList_Size, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallMethodObjArgs, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_GetAttr, PyObject_GetOptionalAttr, PyObject_IsTrue, PyObject_VectorcallMethod, PySet_Add, PySet_Contains, PySet_Discard, PySet_New, PySet_Size, PyTuple_GetItem, PyTuple_New, PyType_IsSubtype, PyUnicode_FromString, PyUnicode_InternFromString, Py_NewRef, Py_None, Py_TYPE, _Py_IsInterpreterFinalizing, jacpy_asyncio_running_loop, jacpy_asyncio_running_task, jacpy_asyncio_tasks_head, jacpy_is_type, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.atexit { PyErr_FormatUnraisable, PyExc_TypeError, PyList_New, PyMem_Free, Py_None }
    cpython_api --> modules.binascii { PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsUnsignedLongMask, PySequence_Size, PyUnicode_ReadChar, jacpy_is_bytes, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.bisect { PyExc_ValueError, PyList_Insert, PyObject_CallMethod, PyObject_IsTrue, Py_NewRef, Py_None, Py_NotImplemented, jacpy_is_exact_list }
    cpython_api --> modules.blake2 { PyExc_OverflowError, PyExc_ValueError }
    cpython_api --> modules.bz2 { PyExc_EOFError, PyExc_MemoryError, PyExc_OSError, PyExc_RuntimeError, PyExc_SystemError, PyExc_ValueError }
    cpython_api --> modules.cjkcodecs { NULL, PyErr_NoMemory, PyExc_LookupError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModule, PyImport_ImportModuleAttrString, PyMem_Free, PyMem_Malloc, PyModule_Add, PyObject, PyObject_CallOneArg, PyObject_GetAttrString, PyUnicodeWriter, PyUnicodeWriter_WriteChar, PyUnicode_AsUTF8, Py_NewRef, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.cmath { PyErr_ExceptionMatches, PyExc_OverflowError, PyExc_ValueError, PyExc_ZeroDivisionError }
    cpython_api --> modules.codecs { NULL, PyBytes_AsString, PyBytes_DecodeEscape, PyBytes_Size, PyCodec_Decode, PyCodec_Encode, PyCodec_LookupError, PyCodec_Register, PyCodec_RegisterError, PyCodec_Unregister, PyExc_OverflowError, PyLong_FromLong, PyLong_FromSsize_t, PyObject, PyUnicode_AsRawUnicodeEscapeString, PyUnicode_AsUnicodeEscapeString, PyUnicode_BuildEncodingMap, PyUnicode_DecodeASCII, PyUnicode_DecodeCharmap, PyUnicode_DecodeLatin1, PyUnicode_DecodeUTF16Stateful, PyUnicode_DecodeUTF32Stateful, PyUnicode_DecodeUTF7Stateful, PyUnicode_DecodeUTF8Stateful, PyUnicode_GetDefaultEncoding, PyUnicode_GetLength, Py_NewRef, _PyBytes_Resize, _PyCodec_Lookup, _PyCodec_UnregisterError, _PyUnicode_AsASCIIString, _PyUnicode_AsLatin1String, _PyUnicode_AsUTF8String, _PyUnicode_DecodeRawUnicodeEscapeStateful, _PyUnicode_DecodeUnicodeEscapeStateful, _PyUnicode_EncodeCharmap, _PyUnicode_EncodeUTF16, _PyUnicode_EncodeUTF32, _PyUnicode_EncodeUTF7, jacpy_buffer_new, jacpy_bytes_from_memory }
    cpython_api --> modules.codecs_cn { PyObject }
    cpython_api --> modules.codecs_hk { PyObject }
    cpython_api --> modules.codecs_iso2022 { PyErr_NoMemory, PyMem_Free, PyMem_Malloc, PyObject }
    cpython_api --> modules.codecs_jp { PyObject }
    cpython_api --> modules.codecs_kr { PyObject }
    cpython_api --> modules.codecs_tw { PyObject }
    cpython_api --> modules.collections { PyErr_SetObject, PyExc_IndexError, PyExc_KeyError, PyExc_MemoryError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsSsize_t, PyTuple_Pack, Py_None, Py_TYPE, _PyObject_GetState }
    cpython_api --> modules.combinatorics { PyExc_MemoryError, PyExc_OverflowError }
    cpython_api --> modules.csv { PyErr_ExceptionMatches, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsLong, Py_None }
    cpython_api --> modules.datetime { NULL, PyArg_UnpackTuple, PyObject }
    cpython_api --> modules.datetime_date { NULL, PyBytes_Size, PyErr_ExceptionMatches, PyErr_Format, PyErr_SetString, PyExc_OverflowError, PyExc_TypeError, PyExc_UnicodeEncodeError, PyExc_ValueError, PyImport_ImportModule, PyLong_FromLong, PyObject, PyObject_CallMethod, PyObject_GenericGetAttr, PyObject_Str, PyTuple_GetItem, PyTuple_SetItem, PyTuple_Size, PyType_GetSlot, PyUnicode_AsLatin1String, PyUnicode_AsUTF8AndSize, PyUnicode_FromFormat, PyUnicode_GetLength, PyUnicode_ReadChar, Py_BuildValue, Py_HashBuffer, Py_NewRef, _PyTime_ObjectToTime_t, _PyTime_localtime, jacpy_bytes_address, jacpy_is_bytes, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.datetime_datetime { NULL, PyBytes_Size, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyErr_WarnEx, PyExc_DeprecationWarning, PyExc_OverflowError, PyExc_TypeError, PyExc_UnicodeEncodeError, PyExc_ValueError, PyFloat_FromDouble, PyLong_FromLong, PyObject, PyObject_CallMethod, PyObject_GenericGetAttr, PyObject_Hash, PyObject_Init, PyObject_Malloc, PyTime_Time, PyTuple_GetItem, PyTuple_Pack, PyTuple_Size, PyUnicode_AsLatin1String, PyUnicode_AsUTF8AndSize, PyUnicode_DecodeLocale, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_GetLength, PyUnicode_ReadChar, PyUnicode_WriteChar, Py_BuildValue, Py_NewRef, Py_None, _PyLong_AsTime_t, _PyTime_AsTimevalTime_t, _PyTime_ObjectToTimeval, _PyTime_gmtime, _PyTime_localtime, _PyUnicode_Copy, jacpy_bytes_address, jacpy_is_bytes, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.datetime_delta { NULL, PyErr_Format, PyErr_Occurred, PyErr_SetString, PyExc_TypeError, PyExc_ValueError, PyFloat_AsDouble, PyLong_AsDouble, PyLong_FromDouble, PyLong_FromLong, PyMemberDef, PyNumber_Add, PyNumber_And, PyNumber_FloorDivide, PyNumber_Multiply, PyNumber_Remainder, PyNumber_TrueDivide, PyObject, PyObject_CallMethod, PyObject_GenericGetAttr, PyObject_Hash, PyObject_IsTrue, PyTuple_GetItem, PyTuple_Pack, PyTuple_Size, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_GetLength, Py_BuildValue, Py_GetConstant, Py_GetConstantBorrowed, Py_NewRef, _PyLong_DivmodNear, jacpy_is_float, jacpy_is_long, jacpy_is_tuple, jacpy_release }
    cpython_api --> modules.datetime_format { NULL, PyErr_Occurred, PyErr_SetString, PyExc_TypeError, PyImport_ImportModuleAttrString, PyLong_AsLong, PyMem_Free, PyMem_Malloc, PyNumber_Long, PyObject, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallNoArgs, PySequence_GetItem, PyUnicodeWriter, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteStr, PyUnicodeWriter_WriteSubstring, PyUnicode_FindChar, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_GetLength, PyUnicode_ReadChar, PyUnicode_Substring, Py_NewRef, Py_None, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.datetime_objects { NULL, PyDict_GetItemRef, PyDict_New, PyDict_SetItem, PyDict_SetItemString, PyErr_Format, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_Occurred, PyErr_SetRaisedException, PyErr_SetString, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModule, PyInterpreterState, PyInterpreterState_Get, PyInterpreterState_GetDict, PyLong_AsInt, PyLong_FromLong, PyNumber_Add, PyNumber_Divmod, PyNumber_FloorDivide, PyNumber_Multiply, PyObject, PyObject_Call, PyObject_CallFunction, PyObject_CallMethod, PyTuple_GetItem, PyTuple_Size, PyUnicode_FromFormat, PyUnicode_GetLength, PyUnicode_InternFromString, PyUnicode_Substring, PyWeakref_GetRef, PyWeakref_NewRef, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, Py_XNewRef, jacpy_bytes_from_memory, jacpy_is_tuple, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.datetime_time { NULL, PyBytes_Size, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_SetString, PyExc_TypeError, PyExc_UnicodeEncodeError, PyExc_ValueError, PyLong_FromLong, PyObject, PyObject_CallFunction, PyObject_CallMethod, PyObject_GenericGetAttr, PyObject_Hash, PyObject_Init, PyObject_Malloc, PyTuple_GetItem, PyTuple_Pack, PyTuple_Size, PyUnicode_AppendAndDel, PyUnicode_AsLatin1String, PyUnicode_AsUTF8AndSize, PyUnicode_FromFormat, PyUnicode_GetLength, PyUnicode_ReadChar, Py_BuildValue, Py_NewRef, Py_None, jacpy_bytes_address, jacpy_is_bytes, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.datetime_tzinfo { NULL, PyErr_Format, PyErr_SetString, PyExc_NotImplementedError, PyExc_TypeError, PyExc_ValueError, PyObject, PyObject_CallNoArgs, PyObject_GenericGetAttr, PyObject_GetOptionalAttr, PyTuple_New, PyTuple_Pack, PyType_GenericNew, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_InternFromString, Py_BuildValue, Py_NewRef, Py_None, _PyObject_GetState, jacpy_release }
    cpython_api --> modules.decimal_context { NULL, PyErr_Clear, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyExc_AttributeError, PyExc_TypeError, PyExc_ValueError, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSsize_t, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallObject, PyObject_GC_Track, PyObject_GC_UnTrack, PyObject_GenericGetAttr, PyObject_GenericSetAttr, PyObject_GetIter, PyObject_IsTrue, PyTuple_Pack, PyType_GetModule, PyUnicode_CompareWithASCIIString, PyUnicode_FromFormat, PyUnicode_FromString, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, _PyObject_GC_New, jacpy_is_dict, jacpy_is_list, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.decimal_convert { NULL, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyFloat_AsDouble, PyFloat_FromDouble, PyList_AsTuple, PyLongExport, PyLong_AsLong, PyLong_AsSsize_t, PyLong_Export, PyLong_FreeExport, PyLong_GetNativeLayout, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_IsInstance, PyTuple_GetItem, PyTuple_Size, PyUnicode_GetLength, PyUnicode_ReadChar, Py_NewRef, Py_None, Py_NotImplemented, _PyUnicode_IsWhitespace, _PyUnicode_ToDecimalDigit, jacpy_is_float, jacpy_is_list, jacpy_is_long, jacpy_is_tuple, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.decimal_number { NULL, PyDict_GetItemWithError, PyDict_Size, PyErr_Clear, PyErr_ExceptionMatches, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyErr_WarnEx, PyExc_DeprecationWarning, PyExc_OverflowError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyFloat_AsDouble, PyFloat_FromString, PyImport_ImportModuleAttrString, PyLongWriter, PyLongWriter_Create, PyLongWriter_Finish, PyLong_AsSsize_t, PyLong_FromInt64, PyLong_FromLong, PyLong_FromSize_t, PyLong_FromSsize_t, PyLong_FromUnsignedLong, PyLong_GetNativeLayout, PyMem_Free, PyMem_Malloc, PyObject, PyObject_Call, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallOneArg, PyObject_GC_UnTrack, PyObject_GenericHash, PyTuple_GetItem, PyTuple_New, PyTuple_Pack, PyTuple_SetItem, PyTuple_Size, PyUnicode_AsUTF8AndSize, PyUnicode_AsUTF8String, PyUnicode_DecodeASCII, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_FromWideChar, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, _PyLong_GCD, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_is_dict, jacpy_is_long, jacpy_is_unicode, jacpy_memory_copy, jacpy_release, jacpy_unicode_decode_bytes }
    cpython_api --> modules.decimal_objects { NULL, PyContextVar_Get, PyContextVar_Set, PyDict_GetItemWithError, PyDict_New, PyDict_SetItem, PyDict_Size, PyErr_NoMemory, PyErr_Occurred, PyErr_SetObject, PyErr_SetString, PyExc_KeyError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyList_Append, PyList_GetItem, PyList_New, PyList_Size, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallObject, PyObject_GC_Track, PyObject_IsTrue, PyType_GetBaseByToken, PyType_GetModule, PyType_IsSubtype, PyType_Spec, PyUnicode_Compare, Py_NewRef, Py_None, _PyObject_GC_New, jacpy_is_dict, jacpy_is_unicode, jacpy_memory_copy, jacpy_release }
    cpython_api --> modules.elementtree { NULL, PyBytes_AsString, PyBytes_Concat, PyBytes_Size, PyBytes_Type, PyCallable_Check, PyDict_Copy, PyDict_GetItemStringRef, PyDict_GetItemWithError, PyDict_Items, PyDict_Keys, PyDict_New, PyDict_Next, PyDict_PopString, PyDict_SetItem, PyDict_Size, PyDict_Type, PyDict_Update, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetNone, PyErr_SetObject, PyErr_WarnEx, PyExc_AttributeError, PyExc_DeprecationWarning, PyExc_ImportError, PyExc_IndexError, PyExc_OverflowError, PyExc_RuntimeError, PyExc_RuntimeWarning, PyExc_StopIteration, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModuleAttrString, PyIndex_Check, PyList_Append, PyList_GetItem, PyList_New, PyList_SetItem, PyList_SetSlice, PyList_Size, PyLong_FromLong, PyLong_FromSsize_t, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyNumber_Add, PyNumber_AsSsize_t, PyObject, PyObject_CallFunction, PyObject_CallFunctionObjArgs, PyObject_CallMethodObjArgs, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_GetAttr, PyObject_GetAttrString, PyObject_HasAttrWithError, PyObject_IsTrue, PyObject_RichCompareBool, PyObject_SetAttr, PyObject_SetAttrString, PyObject_Vectorcall, PySequence_Fast, PyTuple_GetItem, PyTuple_New, PyTuple_Pack, PyTuple_Size, PyType_GetModule, PyUnicode_AsEncodedString, PyUnicode_AsUTF8, PyUnicode_AsUTF8AndSize, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_GetLength, PyUnicode_Join, PyUnicode_ReadChar, PyUnstable_Object_IsUniquelyReferenced, Py_GetConstant, Py_LeaveRecursiveCall, Py_NewRef, Py_None, Py_ReprEnter, Py_ReprLeave, Py_TYPE, _Py_HashSecret, jacpy_bytes_from_memory, jacpy_is_bytes, jacpy_is_dict, jacpy_is_exact_dict, jacpy_is_exact_list, jacpy_is_exact_unicode, jacpy_is_list, jacpy_is_slice, jacpy_is_unicode, jacpy_memory_copy, jacpy_recursion_enter, jacpy_release, jacpy_tuple_set_owned, jacpy_type_check, jacpy_type_name }
    cpython_api --> modules.expat { PyMem_Free, PyMem_Malloc, PyMem_Realloc }
    cpython_api --> modules.fcntl { NULL, PyErr_CheckSignals, PyErr_Clear, PyErr_ExceptionMatches, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyEval_RestoreThread, PyEval_SaveThread, PyExc_BufferError, PyExc_OSError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyLong_AsLong, PyLong_AsLongLong, PyLong_AsUnsignedLongMask, PyLong_FromLong, PyLong_FromUnsignedLong, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CheckBuffer, Py_NewRef, jacpy_bytes_from_memory, jacpy_errno, jacpy_is_bytes, jacpy_is_long, jacpy_is_unicode, jacpy_memory_copy }
    cpython_api --> modules.functools { PyDict_Next, PyErr_ExceptionMatches, PyExc_SystemError, PyExc_TypeError, PyODict_Type, PyObject_CallNoArgs, Py_None }
    cpython_api --> modules.grouping { Py_None }
    cpython_api --> modules.grp { PyExc_KeyError, PyExc_ValueError }
    cpython_api --> modules.hashlib { PyExc_BufferError, PyExc_SystemError, PyExc_TypeError, jacpy_crypto_compare, jacpy_unicode_ascii }
    cpython_api --> modules.hashopenssl { NULL, PyDictProxy_New, PyDict_GetItemWithError, PyDict_New, PyDict_SetItem, PyErr_Format, PyErr_NewException, PyErr_NoMemory, PyErr_Occurred, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyFrozenSet_New, PyLong_AsLong, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyModule_Add, PyModule_AddObjectRef, PyObject, PyObject_GetAttrString, PySet_Add, PyThread_acquire_lock, PyThread_release_lock, PyUnicode_AsUTF8, PyUnicode_FromFormat, PyUnicode_FromString, Py_NewRef, Py_None, Py_TYPE, _Py_strhex, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_is_unicode, jacpy_release }
    cpython_api --> modules.heapq { PyExc_IndexError, PyExc_RuntimeError, Py_None }
    cpython_api --> modules.hmac { PyExc_OverflowError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, Py_None }
    cpython_api --> modules.iterators { PyExc_ValueError, Py_None }
    cpython_api --> modules.itertools { NULL, PyErr_Clear, PyExc_OverflowError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsSsize_t, PyLong_FromLongLong, PyNumber_AsSsize_t, PyNumber_Check, PyObject, PyType_GetSlot, Py_NewRef, Py_None, Py_TYPE, jacpy_dict_get, jacpy_dict_size, jacpy_error_pending, jacpy_list_size, jacpy_release }
    cpython_api --> modules.json { PyDict_Next, PyExc_StopIteration, PyExc_TypeError, PyExc_ValueError, Py_None }
    cpython_api --> modules.locale { NULL, PyBytes_AsString, PyDict_New, PyDict_SetItemString, PyErr_NoMemory, PyErr_SetFromErrno, PyErr_SetString, PyExc_OSError, PyExc_RuntimeError, PyExc_RuntimeWarning, PyExc_ValueError, PyList_New, PyList_SetItem, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyObject, PyUnicode_AsWideCharString, PyUnicode_DecodeLocale, PyUnicode_FSConverter, PyUnicode_FromKindAndData, PyUnicode_FromString, Py_NewRef, _PyMem_Strdup, _Py_GetLocaleEncodingObject, _Py_GetLocaleconvNumeric, jacpy_char_max, jacpy_clear_errno, jacpy_errno, jacpy_release, lconv }
    cpython_api --> modules.lsprof { NULL, PyCFunction_Type, PyErr_Clear, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_SetRaisedException, PyExc_MemoryError, PyExc_RuntimeError, PyExc_SystemError, PyExc_ValueError, PyFloat_FromDouble, PyImport_ImportModuleAttrString, PyList_Append, PyList_New, PyLong_FromLong, PyMethodDef, PyMethodDescr_Type, PyModule_GetNameObject, PyModule_Type, PyObject, PyObject_CallNoArgs, PyObject_GetAttrString, PyObject_Repr, PyObject_Str, PyThreadState_Get, PyTime_PerfCounterRaw, PyType_GetModule, PyUnicode_FromFormat, PyUnicode_FromString, Py_NewRef, Py_TYPE, _PyEval_SetProfile, _PyTime_FromLong, _PyTime_FromSeconds, _PyTime_FromSecondsObject, _PyType_LookupRef, _PyUnicode_EqualToASCIIString, jacpy_cfunction_method, jacpy_cfunction_module, jacpy_cfunction_self, jacpy_is_unicode, jacpy_release, jacpy_type_check }
    cpython_api --> modules.lzma { NULL, PyBytes_AsString, PyDict_Keys, PyDict_New, PyDict_SetItem, PyErr_NoMemory, PyErr_Occurred, PyErr_SetNone, PyEval_RestoreThread, PyEval_SaveThread, PyExc_EOFError, PyExc_MemoryError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyList_GetItem, PyList_Size, PyLong_AsNativeBytes, PyLong_FromUnsignedLongLong, PyMapping_Check, PyMapping_GetOptionalItemString, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyMem_Realloc, PyObject, PySequence_GetItem, PySequence_Size, PyThread_acquire_lock, PyThread_allocate_lock, PyThread_free_lock, PyThread_release_lock, PyType_GetModule, PyUnicode_EqualToUTF8, PyUnicode_InternFromString, Py_None, Py_TYPE, _PyLong_UInt32_Converter, _PyLong_UInt64_Converter, jacpy_buffer_new, jacpy_is_dict, jacpy_is_unicode, jacpy_memory_copy, jacpy_memory_move, jacpy_release }
    cpython_api --> modules.math { PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyExc_ZeroDivisionError, PyObject_IsTrue, Py_BuildValue, Py_None, _PyLong_Frexp }
    cpython_api --> modules.mmap { NULL, PyBytes_AsString, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyEval_RestoreThread, PyEval_SaveThread, PyExc_BufferError, PyExc_IndexError, PyExc_OSError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSize_t, PyLong_FromSsize_t, PyMem_Free, PyMem_Malloc, PyNumber_AsSsize_t, PyObject, PySys_AuditTuple, PyUnicode_FromString, Py_NewRef, Py_buffer, _PyBytes_Find, _PyBytes_ReverseFind, _PyNumber_Index, _Py_dup, _Py_fstat, _Py_fstat_noraise, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_errno, jacpy_is_bytes, jacpy_is_slice, jacpy_release, jacpy_set_errno, jacpy_slice_adjust, jacpy_slice_unpack }
    cpython_api --> modules.multibytecodec { NULL, PyCodec_LookupError, PyCodec_StrictErrors, PyErr_Clear, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetObject, PyExc_AttributeError, PyExc_IndexError, PyExc_RuntimeError, PyExc_TypeError, PyExc_UnicodeDecodeError, PyExc_UnicodeEncodeError, PyExc_UnicodeError, PyExc_ValueError, PyLong_AsSsize_t, PyLong_FromSsize_t, PyLong_Type, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallMethodObjArgs, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_Str, PySequence_Check, PySequence_GetItem, PySequence_Length, PyTuple_GetItem, PyTuple_New, PyTuple_Pack, PyTuple_SetItem, PyTuple_Size, PyType_GetModule, PyUnicodeDecodeError_Create, PyUnicodeDecodeError_SetEnd, PyUnicodeDecodeError_SetReason, PyUnicodeDecodeError_SetStart, PyUnicodeEncodeError_SetEnd, PyUnicodeEncodeError_SetReason, PyUnicodeEncodeError_SetStart, PyUnicodeWriter, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteChar, PyUnicodeWriter_WriteStr, PyUnicode_Append, PyUnicode_AsUTF8AndSize, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromOrdinal, PyUnicode_Splitlines, PyUnicode_Substring, Py_GetConstant, Py_NewRef, Py_None, Py_TYPE, _PyBytes_Resize, _PyLong_AsByteArray, _PyLong_FromByteArray, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_is_bytes, jacpy_is_long, jacpy_is_tuple, jacpy_is_unicode, jacpy_release, jacpy_unicode_data, jacpy_unicode_kind, jacpy_unicode_size }
    cpython_api --> modules.multiprocessing { NULL, PyErr_CheckSignals, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetNone, PyEval_RestoreThread, PyEval_SaveThread, PyExc_AssertionError, PyExc_NotImplementedError, PyExc_OSError, PyExc_RuntimeError, PyExc_SystemError, PyExc_ValueError, PyFloat_AsDouble, PyLong_FromLong, PyMem_RawFree, PyObject, PyThreadState, PyThread_get_thread_ident, Py_NewRef, Py_None, jacpy_errno, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.opcode { PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, Py_None }
    cpython_api --> modules.openssl { NULL, PyErr_Format, PyErr_SetString, PyObject }
    cpython_api --> modules.operator { PyDict_Next, PyExc_RuntimeError, PyExc_TypeError, Py_None }
    cpython_api --> modules.output_buffer { PyExc_MemoryError, PyExc_SystemError }
    cpython_api --> modules.pickle { PyErr_Clear, PyErr_ExceptionMatches, PyExc_AttributeError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyObject_Call, PyObject_CallOneArg, PyObject_GetAttrString, Py_None, Py_TYPE, _PyDict_SizeOf, jacpy_optional_attr, jacpy_set_exception }
    cpython_api --> modules.pickle_decode { PyErr_ExceptionMatches, PyExc_OverflowError, PyExc_TypeError, PyExc_UnicodeDecodeError, PyExc_ValueError, Py_None }
    cpython_api --> modules.pickle_encode { PyErr_ExceptionMatches, PyExc_OverflowError, PyExc_RuntimeError, PyExc_TypeError, PyExc_UnicodeEncodeError, PyExc_ValueError, Py_Ellipsis, Py_None, Py_NotImplemented }
    cpython_api --> modules.pickle_objects { PyErr_ExceptionMatches, PyExc_AttributeError, PyExc_Exception, PyExc_ImportError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PySys_Audit, Py_None }
    cpython_api --> modules.pickle_stream { PyExc_EOFError, PyExc_OverflowError, PyExc_TypeError }
    cpython_api --> modules.posix_core { NULL, PyBytes_AsString, PyBytes_FromStringAndSize, PyBytes_Size, PyDict_New, PyDict_SetDefaultRef, PyErr_CheckSignals, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_FormatUnraisable, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetFromErrnoWithFilenameObject, PyErr_SetFromErrnoWithFilenameObjects, PyErr_WarnEx, PyErr_WarnFormat, PyEval_RestoreThread, PyEval_SaveThread, PyExc_NotImplementedError, PyExc_OSError, PyExc_OverflowError, PyExc_RuntimeWarning, PyExc_TypeError, PyExc_ValueError, PyImport_GetModule, PyIndex_Check, PyInterpreterState, PyInterpreterState_Get, PyIter_Next, PyList_Append, PyList_GetItem, PyList_GetSlice, PyList_New, PyList_Reverse, PyList_Size, PyLong_AsInt, PyLong_AsLong, PyLong_AsLongAndOverflow, PyLong_AsLongLongAndOverflow, PyLong_AsUnsignedLong, PyLong_AsUnsignedLongLong, PyLong_FromLong, PyLong_FromLongLong, PyLong_FromUnsignedLong, PyLong_FromUnsignedLongLong, PyMem_Free, PyObject, PyObject_CallNoArgs, PyObject_GetAttrString, PyObject_GetItem, PyObject_GetIter, PyThreadState, PyThreadState_GetInterpreter, PyThreadState_GetUnchecked, PyThread_get_thread_ident, PyUnicode_AsWideCharString, PyUnicode_DecodeFSDefaultAndSize, PyUnicode_EncodeFSDefault, PyUnicode_FSConverter, PyUnicode_InternFromString, Py_NewRef, Py_None, Py_TYPE, _PyEval_StartTheWorldAll, _PyEval_StopTheWorldAll, _PyImport_AcquireLock, _PyImport_ReInitLock, _PyImport_ReleaseLock, _PyInterpreterState_ReinitRunningMain, _PyNumber_Index, _PyObject_LookupSpecial, _PyRuntime, _PyRuntimeState, _PySignal_AfterFork, _PyThreadState_DeleteList, _PyThreadState_RemoveExcept, _PyType_Name, jacpy_errno, jacpy_fork_callbacks, jacpy_is_bool, jacpy_is_bytes, jacpy_is_long, jacpy_is_unicode, jacpy_release, jacpy_runtime_head_lock, jacpy_runtime_head_unlock, jacpy_stdio_fileno, jacpy_thread_state_fork_reset, jacpy_thread_state_native_id }
    cpython_api --> modules.posix_fileio { NULL, PyBuffer_Release, PyBytes_AsString, PyBytes_FromStringAndSize, PyErr_CheckSignals, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetFromErrnoWithFilenameObject, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyFloat_FromDouble, PyLong_AsLong, PyLong_FromLong, PyLong_FromSsize_t, PyLong_FromUnsignedLongLong, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyObject, PyObject_GetBuffer, PySequence_Check, PySequence_GetItem, PySequence_Size, PySys_Audit, PyTuple_Pack, PyUnicode_DecodeFSDefault, Py_BuildValue, Py_NewRef, Py_None, Py_buffer, _PyBytes_Resize, _PyTime_AsTimespec, _PyTime_FromSecondsDouble, _PyTime_FromTimespec, _Py_closerange, _Py_device_encoding, _Py_dup, _Py_get_blocking, _Py_get_inheritable, _Py_read, _Py_set_blocking, _Py_set_inheritable, _Py_write, jacpy_errno, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.posix_fileio_platform { jacpy_set_errno }
    cpython_api --> modules.posix_files { NULL, PyBytes_AsString, PyBytes_FromStringAndSize, PyErr_CheckSignals, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyList_Append, PyList_New, PyLong_AsLong, PyLong_FromLong, PyLong_FromUnsignedLong, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawRealloc, PyNumber_Divmod, PyObject, PySys_Audit, PyTuple_GetItem, PyTuple_Pack, PyTuple_Size, PyUnicode_DecodeFSDefault, PyUnicode_DecodeFSDefaultAndSize, PyUnicode_EncodeFSDefault, PyUnicode_FromOrdinal, PyUnicode_FromWideChar, Py_NewRef, Py_None, Py_TYPE, _PyBytes_Resize, _PyLong_AsTime_t, _PyTime_ObjectToTimespec, _PyType_Name, _Py_normpath_and_size, _Py_skiproot, jacpy_errno, jacpy_is_bytes, jacpy_is_exact_tuple, jacpy_is_tuple, jacpy_is_unicode, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.posix_ids { NULL, PyBytes_AsString, PyBytes_FromStringAndSize, PyBytes_Size, PyConfig_GetInt, PyErr_CheckSignals, PyErr_NoMemory, PyErr_SetFromErrno, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyList_New, PyList_SetItem, PyLong_FromLong, PyLong_FromUnsignedLong, PyMem_Free, PyMem_Malloc, PyObject, PySequence_Check, PySequence_GetItem, PySequence_Size, PySys_Audit, PyUnicode_DecodeFSDefault, PyUnicode_DecodeFSDefaultAndSize, PyUnicode_DecodeLocale, Py_BuildValue, Py_NewRef, Py_None, _PyBytes_Resize, _PyOS_URandom, jacpy_errno, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.posix_process { NULL, PyArg_Parse, PyArg_ParseTuple, PyBytes_AsString, PyBytes_FromFormat, PyBytes_Size, PyCallable_Check, PyErr_CheckSignals, PyErr_Clear, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyErr_WarnFormat, PyEval_RestoreThread, PyEval_SaveThread, PyExc_DeprecationWarning, PyExc_NotImplementedError, PyExc_OSError, PyExc_OverflowError, PyExc_PythonFinalizationError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyFloat_FromDouble, PyImport_GetModule, PyImport_ImportModuleAttrString, PyIndex_Check, PyInterpreterState_Get, PyIter_Next, PyList_Append, PyList_GetItemRef, PyList_New, PyLong_AsInt, PyLong_AsLong, PyLong_FromLong, PyMapping_Check, PyMapping_Keys, PyMapping_Length, PyMapping_Size, PyMapping_Values, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyObject, PyObject_GetAttr, PyObject_GetIter, PySequence_Fast, PySequence_GetItem, PySequence_Size, PySet_Add, PySet_New, PySys_Audit, PySys_AuditTuple, PyTuple_GetItem, PyTuple_Size, PyUnicode_FSConverter, Py_BuildValue, Py_NewRef, Py_None, Py_TYPE, _PyInterpreterState_HasFeature, _PyInterpreterState_Main, _PyType_Name, _Py_GetTicksPerSecond, jacpy_errno, jacpy_fast_item, jacpy_fast_size, jacpy_interpreter_finalizing, jacpy_is_list, jacpy_is_tuple, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.posix_stat { NULL, PyBytes_AsString, PyBytes_FromString, PyBytes_FromStringAndSize, PyErr_CheckSignals, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_NoMemory, PyErr_Occurred, PyErr_ResourceWarning, PyErr_SetRaisedException, PyEval_RestoreThread, PyEval_SaveThread, PyExc_FileNotFoundError, PyExc_NotImplementedError, PyExc_TypeError, PyExc_Warning, PyFloat_FromDouble, PyList_Append, PyList_New, PyLong_AsLong, PyLong_FromLong, PyLong_FromLongLong, PyLong_FromUnsignedLong, PyLong_FromUnsignedLongLong, PyMem_Free, PyMem_Malloc, PyNumber_Add, PyNumber_Multiply, PyObject, PyObject_CallFinalizerFromDealloc, PyObject_GetAttr, PyType_GetModule, PyUnicode_DecodeFSDefault, PyUnicode_DecodeFSDefaultAndSize, PyUnicode_FSConverter, PyUnicode_FromFormat, Py_NewRef, Py_None, Py_TYPE, Py_XNewRef, _PyLong_FromTime_t, _Py_dup, jacpy_bytes_length, jacpy_closedir, jacpy_errno, jacpy_fdopendir, jacpy_fstat, jacpy_fstatat, jacpy_is_bytes, jacpy_lstat, jacpy_opendir, jacpy_readdir_entry, jacpy_release, jacpy_rewinddir, jacpy_set_errno, jacpy_stat }
    cpython_api --> modules.posix_stat_platform { PyObject }
    cpython_api --> modules.posixshmem { NULL, PyErr_CheckSignals, PyErr_SetFromErrnoWithFilenameObject, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_ValueError, PyObject, PyUnicode_AsUTF8AndSize, Py_NewRef, jacpy_errno }
    cpython_api --> modules.posixsubprocess { NULL, PyBytes_AsString, PyBytes_FromStringAndSize, PyBytes_Size, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyEval_RestoreThread, PyEval_SaveThread, PyExc_MemoryError, PyExc_OSError, PyExc_PythonFinalizationError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyGC_Disable, PyGC_Enable, PyInterpreterState_Get, PyInterpreterState_Main, PyLong_AsLong, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyMem_RawCalloc, PyMem_RawFree, PyMem_RawMalloc, PyObject, PyObject_Call, PySequence_Fast, PySequence_GetItem, PySequence_Size, PyTuple_GetItem, PyTuple_New, PyTuple_Size, PyUnicode_FSConverter, Py_NewRef, _Py_RestoreSignals, _Py_set_inheritable_async_safe, _Py_write_noraise, jacpy_errno, jacpy_fast_item, jacpy_fast_size, jacpy_interpreter_finalizing, jacpy_is_bytes, jacpy_is_list, jacpy_is_long, jacpy_memory_copy, jacpy_release, jacpy_set_errno, jacpy_tuple_set_owned }
    cpython_api --> modules.posixsubprocess_fds { _Py_closerange }
    cpython_api --> modules.pwd { PyErr_ExceptionMatches, PyExc_KeyError, PyExc_OverflowError, PyExc_ValueError }
    cpython_api --> modules.pyexpat { NULL, PyByteArray_AsString, PyBytes_AsString, PyDict_GetItemRef, PyDict_New, PyDict_SetItem, PyErr_FormatUnraisable, PyErr_NoMemory, PyErr_Occurred, PyErr_SetObject, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyList_Append, PyList_New, PyList_SetItem, PyLong_AsLong, PyLong_FromLong, PyLong_FromSize_t, PyMem_Free, PyMem_Malloc, PyModule_Add, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddStringConstant, PyModule_New, PyObject, PyObject_Call, PyObject_CallFunction, PyObject_CallOneArg, PyObject_GetOptionalAttr, PyObject_IsTrue, PyObject_SetAttrString, PyTuple_New, PyType_GetModule, PyUnicode_AsUTF8AndSize, PyUnicode_Decode, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromFormat, PyUnicode_GetLength, PyUnicode_ReadChar, Py_LeaveRecursiveCall, Py_NewRef, Py_None, Py_TYPE, _PyImport_SetModule, _PyTraceback_Add, _Py_HashSecret, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_is_bytearray, jacpy_is_bytes, jacpy_is_dict, jacpy_is_long, jacpy_is_unicode, jacpy_memory_copy, jacpy_recursion_enter, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.queue { PyExc_SystemError, PyExc_ValueError, PyType_GetModule, Py_None, jacpy_lock_new }
    cpython_api --> modules.random { PyExc_MemoryError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyFloat_FromDouble, Py_NewRef, Py_None }
    cpython_api --> modules.resource { PyExc_OSError, PyExc_OverflowError, PyExc_ValueError }
    cpython_api --> modules.select { NULL, PyDict_Contains, PyDict_DelItem, PyDict_New, PyDict_Next, PyDict_SetItem, PyErr_CheckSignals, PyErr_ExceptionMatches, PyErr_GetRaisedException, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetRaisedException, PyErr_WarnEx, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_OverflowError, PyExc_RuntimeError, PyExc_RuntimeWarning, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModuleAttrString, PyIndex_Check, PyList_New, PyList_SetItem, PyLong_AsLong, PyLong_AsNativeBytes, PyLong_FromLong, PyLong_FromUnsignedLong, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyObject, PyObject_Call, PyObject_CallNoArgs, PyObject_GetAttr, PyObject_Str, PySequence_Fast, PyTuple_New, PyUnicode_FromString, Py_NewRef, Py_None, Py_NotImplemented, Py_TYPE, _PyDeadline_Get, _PyDeadline_Init, _PyTime_AsMilliseconds, _PyTime_AsTimespec, _PyTime_AsTimeval, _PyTime_AsTimeval_clamp, _PyTime_FromMillisecondsObject, _PyTime_FromSecondsObject, _Py_set_inheritable, jacpy_dict_size, jacpy_errno, jacpy_fast_item, jacpy_fast_size, jacpy_release, jacpy_set_errno, jacpy_tuple_set_owned }
    cpython_api --> modules.sha3 { PyExc_SystemError, PyExc_ValueError }
    cpython_api --> modules.socket { NULL, PyArg_ParseTuple, PyArg_ParseTupleAndKeywords, PyErr_Clear, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyList_Append, PyList_New, PyLong_AsLong, PyLong_FromLong, PyLong_FromSize_t, PyLong_FromUnsignedLong, PyMem_Calloc, PyMem_Free, PyNumber_Index, PyObject, PyObject_GetBuffer, PyObject_Str, PySys_Audit, PySys_AuditTuple, PyThread_acquire_lock, PyThread_release_lock, PyTuple_Pack, PyTuple_Size, PyUnicode_AsEncodedString, PyUnicode_AsUTF8, PyUnicode_FSConverter, Py_BuildValue, Py_NewRef, Py_None, Py_buffer, _Py_dup, jacpy_buffer_release, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_errno, jacpy_fs_text, jacpy_is_bytes, jacpy_is_tuple, jacpy_is_unicode, jacpy_memory_copy, jacpy_memory_zero, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.socket_address { NULL, PyArg_Parse, PyArg_ParseTuple, PyErr_ExceptionMatches, PyErr_NoMemory, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyMem_Calloc, PyMem_Free, PyObject, PyUnicode_AsEncodedString, PyUnicode_EncodeFSDefault, PyUnicode_FSConverter, Py_BuildValue, Py_NewRef, Py_None, Py_buffer, jacpy_buffer_release, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_errno, jacpy_fs_text, jacpy_is_bytearray, jacpy_is_bytes, jacpy_is_tuple, jacpy_is_unicode, jacpy_memory_copy, jacpy_memory_zero, jacpy_release, jacpy_unicode_ascii, jacpy_unicode_data, jacpy_unicode_size }
    cpython_api --> modules.socket_core { NULL, PyErr_CheckSignals, PyErr_SetFromErrno, PyErr_SetObject, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_TimeoutError, PyExc_ValueError, PyFloat_FromDouble, PyObject, PyTime_AsSecondsDouble, Py_BuildValue, Py_NewRef, Py_None, _PyDeadline_Get, _PyDeadline_Init, _PyTime_AsMilliseconds, _PyTime_FromSecondsObject, jacpy_errno, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.socket_object { NULL, PyArg_Parse, PyArg_ParseTuple, PyArg_ParseTupleAndKeywords, PyBuffer_Release, PyErr_CheckSignals, PyErr_Clear, PyErr_ExceptionMatches, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_NoMemory, PyErr_Occurred, PyErr_ResourceWarning, PyErr_SetFromErrno, PyErr_SetRaisedException, PyErr_SetString, PyErr_WarnEx, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_RuntimeError, PyExc_RuntimeWarning, PyExc_TimeoutError, PyExc_TypeError, PyExc_ValueError, PyExc_Warning, PyList_Append, PyList_New, PyLong_AsInt, PyLong_AsLong, PyLong_FromLong, PyLong_FromSsize_t, PyLong_FromUnsignedLong, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyObject, PyObject_CallFinalizerFromDealloc, PyObject_GC_UnTrack, PyObject_IsTrue, PySequence_Fast, PySequence_Tuple, PySys_Audit, PyTuple_GetItem, PyTuple_Pack, PyTuple_Size, PyUnicode_FromFormat, Py_BuildValue, Py_NewRef, Py_None, Py_buffer, _PyBytes_Resize, _PyDeadline_Get, _PyDeadline_Init, _Py_set_inheritable, jacpy_buffer_release, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_errno, jacpy_fast_item, jacpy_fast_size, jacpy_memory_copy, jacpy_memory_zero, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.sqlite3 { NULL, PyBool_Type, PyByteArray_FromObject, PyByteArray_Type, PyBytes_AsString, PyBytes_Type, PyCallable_Check, PyDict_GetItemRef, PyDict_GetItemWithError, PyDict_New, PyDict_SetItem, PyDict_SetItemString, PyDict_Size, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_NoMemory, PyErr_Occurred, PyErr_Print, PyErr_ResourceWarning, PyErr_SetObject, PyErr_SetRaisedException, PyErr_WarnEx, PyEval_RestoreThread, PyEval_SaveThread, PyExc_AttributeError, PyExc_DeprecationWarning, PyExc_Exception, PyExc_ImportError, PyExc_IndexError, PyExc_MemoryError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_UnicodeDecodeError, PyExc_ValueError, PyExc_Warning, PyFloat_AsDouble, PyFloat_FromDouble, PyFloat_Type, PyGILState_Ensure, PyGILState_Release, PyImport_ImportModuleAttrString, PyIndex_Check, PyInterpreterState_Get, PyIter_Check, PyIter_Next, PyList_Append, PyList_GetItem, PyList_New, PyList_Size, PyLong_AsInt, PyLong_AsLong, PyLong_AsLongAndOverflow, PyLong_AsLongLongAndOverflow, PyLong_AsUInt32, PyLong_FromLong, PyLong_FromLongLong, PyLong_FromUInt32, PyLong_FromUnsignedLong, PyLong_Type, PyMapping_GetOptionalItemString, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyModule_AddIntConstant, PyModule_AddObjectRef, PyModule_AddStringConstant, PyNumber_AsSsize_t, PyObject, PyObject_Call, PyObject_CallFinalizerFromDealloc, PyObject_CallFunction, PyObject_CallFunctionObjArgs, PyObject_CallMethodObjArgs, PyObject_CallNoArgs, PyObject_CallObject, PyObject_CallOneArg, PyObject_CheckBuffer, PyObject_GetAttr, PyObject_GetItem, PyObject_GetIter, PyObject_GetOptionalAttr, PyObject_Hash, PyObject_IsTrue, PyObject_RichCompare, PyObject_RichCompareBool, PyObject_SetAttrString, PyObject_Vectorcall, PySequence_Check, PySequence_GetItem, PySequence_Size, PySys_Audit, PyThread_get_thread_ident, PyTuple_GetItem, PyTuple_New, PyTuple_Pack, PyTuple_SetItem, PyTuple_Size, PyType_GetModule, PyUnicode_AsUTF8AndSize, PyUnicode_CompareWithASCIIString, PyUnicode_DecodeASCII, PyUnicode_DecodeUTF8Stateful, PyUnicode_FSConverter, PyUnicode_FromString, PyUnicode_InternFromString, PyUnicode_Type, PyWeakref_GetRef, PyWeakref_NewRef, Py_NewRef, Py_None, Py_NotImplemented, Py_TYPE, _PyErr_ChainExceptions1, _PyErr_FormatFromCause, _PyUnicode_AsUTF8NoNUL, _PyWeakref_IsDead, _Py_IsInterpreterFinalizing, jacpy_buffer_new, jacpy_bytes_from_memory, jacpy_is_bytearray, jacpy_is_dict, jacpy_is_exact_float, jacpy_is_exact_list, jacpy_is_exact_long, jacpy_is_exact_tuple, jacpy_is_exact_unicode, jacpy_is_float, jacpy_is_list, jacpy_is_long, jacpy_is_slice, jacpy_is_tuple, jacpy_is_type, jacpy_is_unicode, jacpy_memory_copy, jacpy_release, jacpy_type_check }
    cpython_api --> modules.sre { NULL, PyBuffer_Release, PyBytes_FromObject, PyBytes_Join, PyBytes_Type, PyCallable_Check, PyDictProxy_New, PyDict_GetItemWithError, PyDict_New, PyDict_Next, PyDict_SetItem, PyDict_Size, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyExc_IndexError, PyExc_OverflowError, PyExc_RecursionError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModuleAttrString, PyIndex_Check, PyList_Append, PyList_GetItem, PyList_New, PyList_Size, PyLong_AsSsize_t, PyLong_AsUnsignedLong, PyLong_FromSsize_t, PyMem_Calloc, PyMem_Free, PyMem_Malloc, PyNumber_AsSsize_t, PyObject, PyObject_CheckBuffer, PyObject_ClearWeakRefs, PyObject_GC_Del, PyObject_GC_Track, PyObject_GC_UnTrack, PyObject_GetAttrString, PyObject_GetBuffer, PyObject_Hash, PyObject_RichCompareBool, PyObject_Vectorcall, PyTuple_New, PyTuple_Size, PyType_GetModule, PyUnicode_FindChar, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_Join, PyUnicode_New, PyUnicode_Substring, Py_HashBuffer, Py_NewRef, Py_None, Py_NotImplemented, Py_XNewRef, Py_buffer, _PyObject_GC_New, _PyObject_GC_NewVar, _PyUnicode_Copy, _PyUnicode_JoinArray, jacpy_buffer_new, jacpy_bytes_from_memory, jacpy_is_bytes, jacpy_is_long, jacpy_is_unicode, jacpy_release, jacpy_unicode_data, jacpy_unicode_kind, jacpy_unicode_size }
    cpython_api --> modules.sre_engine { PyMem_Free, PyMem_Realloc, PyObject, Py_buffer, _PyUnicode_IsAlpha, _PyUnicode_IsDecimalDigit, _PyUnicode_IsDigit, _PyUnicode_IsLinebreak, _PyUnicode_IsNumeric, _PyUnicode_IsWhitespace, _PyUnicode_ToLowercase, _PyUnicode_ToUppercase }
    cpython_api --> modules.sre_ucs1 { PyErr_CheckSignals, PyMem_Malloc }
    cpython_api --> modules.sre_ucs2 { PyErr_CheckSignals, PyMem_Malloc }
    cpython_api --> modules.sre_ucs4 { PyErr_CheckSignals, PyMem_Malloc }
    cpython_api --> modules.ssl { NULL, PyArg_Parse, PyArg_ParseTuple, PyBytes_AsString, PyBytes_AsStringAndSize, PyBytes_FromString, PyCallable_Check, PyDict_New, PyDict_SetItemString, PyErr_BadArgument, PyErr_BadInternalCall, PyErr_CheckSignals, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_FormatUnraisable, PyErr_GetRaisedException, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetFromErrnoWithFilenameObject, PyErr_SetObject, PyErr_SetString, PyErr_WarnEx, PyEval_RestoreThread, PyEval_SaveThread, PyExc_AttributeError, PyExc_DeprecationWarning, PyExc_MemoryError, PyExc_NotImplementedError, PyExc_OSError, PyExc_OverflowError, PyExc_RuntimeError, PyExc_TimeoutError, PyExc_TypeError, PyExc_UnicodeEncodeError, PyExc_ValueError, PyGILState_Ensure, PyGILState_Release, PyList_Append, PyList_Insert, PyList_New, PyList_SetItem, PyLong_AsLong, PyLong_FromLong, PyLong_FromSize_t, PyLong_FromUnsignedLong, PyLong_FromUnsignedLongLong, PyMem_Free, PyMem_Malloc, PyMem_RawFree, PyMem_RawMalloc, PyMutex_Lock, PyMutex_Unlock, PyObject, PyObject_CallFunction, PyObject_CallFunctionObjArgs, PyObject_CallNoArgs, PyObject_CheckBuffer, PyObject_IsTrue, PyThreadState, PyThreadState_Swap, PyThread_acquire_lock, PyThread_release_lock, PyTuple_New, PyUnicode_AsASCIIString, PyUnicode_AsUTF8String, PyUnicode_DecodeASCII, PyUnicode_DecodeFSDefault, PyUnicode_DecodeUTF8Stateful, PyUnicode_FSConverter, PyUnicode_FromEncodedObject, PyUnicode_FromFormat, PyUnicode_FromString, PyWeakref_GetRef, PyWeakref_NewRef, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, Py_TYPE, Py_buffer, Py_fopen, _PyBytes_Resize, _PyDeadline_Get, _PyDeadline_Init, _PyLong_FromTime_t, _PyLong_UnsignedLongLong_Converter, jacpy_buffer_release, jacpy_bytes_address, jacpy_bytes_from_memory, jacpy_bytes_length, jacpy_errno, jacpy_is_bytearray, jacpy_is_bytes, jacpy_is_unicode, jacpy_release, jacpy_set_errno, jacpy_tuple_set_owned }
    cpython_api --> modules.ssl_cert { NULL, PyDict_New, PyDict_SetItemString, PyErr_Format, PyErr_NoMemory, PyErr_SetString, PyErr_WarnFormat, PyExc_MemoryError, PyExc_RuntimeWarning, PyExc_ValueError, PyList_Append, PyList_AsTuple, PyList_New, PyList_SetItem, PyList_Size, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyObject, PyTuple_New, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromFormat, PyUnicode_FromString, Py_BuildValue, Py_NewRef, Py_None, Py_TYPE, jacpy_bytes_from_memory, jacpy_release, jacpy_tuple_set_owned }
    cpython_api --> modules.ssl_core { NULL, PyDict_GetItemWithError, PyErr_Occurred, PyErr_SetFromErrno, PyErr_SetObject, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_SystemError, PyLong_FromLong, PyMem_RawFree, PyMem_RawMalloc, PyMutex, PyMutex_Lock, PyMutex_Unlock, PyObject, PyObject_CallObject, PyObject_SetAttr, PyThreadState, PyThread_free_lock, PyType_IsSubtype, PyUnicodeWriter, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_Format, PyUnicodeWriter_WriteASCII, PyUnicode_FromFormat, PyUnicode_FromString, PyWeakref_GetRef, Py_BuildValue, Py_NewRef, Py_None, Py_TYPE, _PyErr_ChainExceptions1, _PyTime_AsMilliseconds, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.stat { PyExc_OverflowError }
    cpython_api --> modules.statistics { PyExc_ValueError }
    cpython_api --> modules.struct { PyErr_ExceptionMatches, PyExc_OverflowError, PyExc_RuntimeError, PyExc_TypeError, PyUnicode_AsEncodedString, Py_None, Py_TYPE, jacpy_is_unicode }
    cpython_api --> modules.suggestions { PyExc_TypeError }
    cpython_api --> modules.syslog { PyExc_RuntimeError }
    cpython_api --> modules.tee { PyExc_RuntimeError, PyExc_ValueError }
    cpython_api --> modules.termios { NULL, PyBytes_AsString, PyBytes_Size, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OverflowError, PyExc_TypeError, PyList_GetItem, PyList_New, PyList_SetItem, PyList_Size, PyLong_AsLong, PyLong_FromLong, PyMem_Calloc, PyMem_Free, PyObject, PySequence_Check, PySequence_GetItem, PySequence_Size, PyTuple_New, PyTuple_SetItem, Py_NewRef, jacpy_bytes_from_memory, jacpy_is_bytes, jacpy_is_list, jacpy_is_long, jacpy_release }
    cpython_api --> modules.time { NULL, PyDict_New, PyDict_SetItemString, PyErr_CheckSignals, PyErr_NoMemory, PyErr_Occurred, PyErr_SetFromErrno, PyEval_RestoreThread, PyEval_SaveThread, PyExc_OSError, PyExc_OverflowError, PyExc_RuntimeError, PyExc_TypeError, PyExc_ValueError, PyFloat_FromDouble, PyImport_ImportModule, PyImport_ImportModuleAttrString, PyLong_AsInt, PyLong_AsLong, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyModule_AddIntConstant, PyModule_AddObjectRef, PyObject, PyObject_Call, PySys_AuditTuple, PyTime_AsSecondsDouble, PyTime_Monotonic, PyTime_PerfCounter, PyTime_Time, PyTuple_GetItem, PyTuple_Size, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteStr, PyUnicodeWriter_WriteSubstring, PyUnicode_AsUTF8, PyUnicode_DecodeLocale, PyUnicode_FromString, PyUnicode_FromWideChar, PyUnicode_GetLength, PyUnicode_ReadChar, Py_NewRef, Py_None, Py_TYPE, _PyArg_CheckPositional, _PyTimeFraction, _PyTimeFraction_Mul, _PyTimeFraction_Resolution, _PyTimeFraction_Set, _PyTime_Add, _PyTime_AsLong, _PyTime_AsTimespec, _PyTime_FromLong, _PyTime_FromSecondsObject, _PyTime_FromTimespec, _PyTime_FromTimeval, _PyTime_MonotonicWithInfo, _PyTime_ObjectToTime_t, _PyTime_PerfCounterWithInfo, _PyTime_TimeWithInfo, _PyTime_gmtime, _PyTime_localtime, _Py_GetTicksPerSecond, _Py_clock_info_t, jacpy_clear_errno, jacpy_errno, jacpy_is_tuple, jacpy_release, jacpy_set_errno }
    cpython_api --> modules.unicodedata { NULL, PyErr_Format, PyErr_NoMemory, PyExc_KeyError, PyExc_ValueError, PyFloat_FromDouble, PyLong_FromLong, PyMem_Free, PyMem_Malloc, PyMem_Realloc, PyModule_Type, PyObject, PyType_IsSubtype, PyUnicode_Compare, PyUnicode_CompareWithASCIIString, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromKindAndData, PyUnicode_FromObject, PyUnicode_FromOrdinal, Py_GetConstant, Py_NewRef, Py_TYPE, _PyUnicode_ToDecimalDigit, _PyUnicode_ToDigit, _PyUnicode_ToNumeric, jacpy_release, jacpy_unicode_ascii, jacpy_unicode_data, jacpy_unicode_kind, jacpy_unicode_size }
    cpython_api --> modules.uuid { NULL, PyBytes_AsString, PyLong_FromLong, PyObject, Py_NewRef, jacpy_buffer_new }
    cpython_api --> modules.zlib { PyExc_EOFError, PyExc_MemoryError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError }
    cpython_api --> modules.zoneinfo { NULL, PyBytes_AsString, PyDict_GetItemRef, PyDict_New, PyDict_SetDefaultRef, PyDict_SetItemString, PyErr_ExceptionMatches, PyErr_Format, PyErr_GetRaisedException, PyErr_Occurred, PyExc_MemoryError, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModule, PyImport_ImportModuleAttrString, PyIter_Next, PyLong_AsLong, PyLong_AsLongLong, PyLong_AsSsize_t, PyLong_FromLong, PyNumber_Add, PyObject, PyObject_Call, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallMethodObjArgs, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_GetAttrString, PyObject_GetIter, PyObject_IsTrue, PyObject_Repr, PyObject_RichCompareBool, PyObject_SetAttrString, PyTuple_GetItem, PyTuple_New, PyTuple_Size, PyTuple_Type, PyUnicode_DecodeUTF8Stateful, PyUnicode_FromFormat, PyUnicode_FromString, Py_BuildValue, Py_NewRef, Py_None, Py_TYPE, _PyErr_ChainExceptions1, _PyType_Name, jacpy_is_tuple, jacpy_release, jacpy_type_check }
    cpython_api --> modules.zstd { NULL, PyBytes_AsString, PyBytes_Size, PyDict_Next, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyEval_RestoreThread, PyEval_SaveThread, PyExc_EOFError, PyExc_OverflowError, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyLong_AsInt, PyLong_AsSize_t, PyLong_AsUnsignedLongLong, PyLong_FromSize_t, PyMem_Free, PyMem_Malloc, PyMem_RawCalloc, PyMem_RawFree, PyMutex, PyMutex_Lock, PyMutex_Unlock, PyObject, PyTuple_GetItem, PyTuple_Size, PyTuple_Type, PyType_GetModule, PyUnicode_FromFormat, Py_BuildValue, Py_GetConstant, Py_NewRef, Py_None, Py_TYPE, _PyBytes_Resize, jacpy_buffer_new, jacpy_bytes_from_memory, jacpy_is_dict, jacpy_is_long, jacpy_memory_copy, jacpy_memory_move, jacpy_release, jacpy_type_check }
    cpython_api --> native_services { NULL, PyErr_ExceptionMatches, PyErr_WarnExplicit, PyExc_SyntaxWarning, PyExc_UnicodeError, PyExc_ValueError, PyImport_ImportModule, PyObject_CallMethod }
    cpython_api --> object_model.bool { NULL, PyArg_UnpackTuple, PyErr_WarnEx, PyObject, PyObject_IsTrue, PyUnicode_InternFromString, PyVectorcall_NARGS, _PyArg_CheckPositional, _PyArg_NoKeywords, _PyArg_NoKwnames, _Py_SetImmortal }
    cpython_api --> object_model.capsule { NULL, PyErr_Format, PyErr_NoMemory, PyErr_SetString, PyExc_AttributeError, PyExc_ImportError, PyExc_ValueError, PyImport_ImportModule, PyMem_Free, PyMem_Malloc, PyObject, PyObject_GC_Del, PyObject_GC_IsTracked, PyObject_GetAttrString, PyUnicode_FromFormat, _PyObject_GC_New, jacpy_release }
    cpython_api --> object_model.cell { NULL, PyArg_UnpackTuple, PyErr_BadInternalCall, PyErr_SetString, PyExc_ValueError, PyObject, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_RichCompare, PyUnicode_FromFormat, Py_NewRef, Py_NotImplemented, Py_XNewRef, _PyArg_NoKeywords, _PyObject_GC_New, jacpy_release }
    cpython_api --> object_model.complex { NULL, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyErr_SetString, PyErr_WarnFormat, PyExc_DeprecationWarning, PyExc_OverflowError, PyExc_TypeError, PyExc_ValueError, PyExc_ZeroDivisionError, PyFloat_AsDouble, PyFloat_FromDouble, PyLong_AsDouble, PyLong_FromLong, PyMem_Free, PyMemberDef, PyMethodDef, PyNumber_Float, PyOS_double_to_string, PyOS_string_to_double, PyObject, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_Free, PyObject_GenericGetAttr, PyObject_Init, PyObject_Malloc, PyObject_RichCompare, PyType_GenericAlloc, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicode_AsUTF8AndSize, PyUnicode_FromFormat, PyUnicode_GetLength, PyUnicode_InternFromString, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, Py_complex, _PyArg_BadArgument, _PyComplex_FormatAdvancedWriter, _PyObject_LookupSpecial, _PyUnicodeWriter, _PyUnicode_TransformDecimalAndSpaceToASCII, _Py_HashDouble, _Py_string_to_number_with_underscores, jacpy_errno, jacpy_is_float, jacpy_is_long, jacpy_is_unicode, jacpy_release, jacpy_set_errno }
    cpython_api --> object_model.enumerate { NULL, PyArg_ParseTupleAndKeywords, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_Occurred, PyErr_SetString, PyExc_IndexError, PyExc_StopIteration, PyExc_TypeError, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSsize_t, PyMethodDef, PyNumber_Add, PyNumber_Index, PyObject, PyObject_CallNoArgs, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_GetIter, PyObject_SelfIter, PySequence_Check, PySequence_GetItem, PySequence_Size, PyTuple_New, PyTuple_Pack, PyType_GenericAlloc, PyUnicode_InternFromString, PyVectorcall_NARGS, Py_BuildValue, Py_IncRef, Py_NewRef, Py_None, _PyArg_CheckPositional, _PyArg_NoKeywords, _PyArg_NoKwnames, _PyObject_LookupSpecial, _PyUnicode_EqualToASCIIString, jacpy_release }
    cpython_api --> object_model.file { NULL, PyArg_ParseTuple, PyBytes_Size, PyErr_BadInternalCall, PyErr_Clear, PyErr_Format, PyErr_Occurred, PyErr_SetString, PyErr_WarnEx, PyEval_RestoreThread, PyEval_SaveThread, PyExc_EOFError, PyExc_RuntimeWarning, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyImport_ImportModuleAttrString, PyLong_AsInt, PyLong_FromLong, PyLong_FromSsize_t, PyMethodDef, PyObject, PyObject_CallFunction, PyObject_CallMethod, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_Free, PyObject_GenericGetAttr, PyObject_GetAttrString, PyObject_GetOptionalAttrString, PyObject_Repr, PyObject_Str, PySys_AuditTuple, PyType_GenericAlloc, PyUnicode_AsUTF8AndSize, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_GetLength, PyUnicode_ReadChar, PyUnicode_Substring, Py_IsInitialized, Py_NewRef, Py_None, _PyBytes_Resize, _PyObject_New, _PyUnicode_AsUTF8String, _Py_write, jacpy_bytes_address, jacpy_errno, jacpy_is_bytes, jacpy_is_long, jacpy_is_unicode, jacpy_open_code_hook, jacpy_open_code_userdata, jacpy_release, jacpy_set_errno, jacpy_stdio_fileno }
    cpython_api --> object_model.genericalias { NULL, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Format, PyErr_Occurred, PyErr_SetNone, PyErr_SetString, PyExc_AttributeError, PyExc_StopIteration, PyExc_TypeError, PyList_Append, PyList_GetItemRef, PyList_New, PyList_SetSlice, PyMemberDef, PyMethodDef, PyObject, PyObject_Call, PyObject_CallFunction, PyObject_CallOneArg, PyObject_ClearWeakRefs, PyObject_Dir, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_GetAttr, PyObject_GetItem, PyObject_GetIter, PyObject_GetOptionalAttrString, PyObject_HasAttrWithError, PyObject_Hash, PyObject_IsTrue, PyObject_RichCompare, PyObject_RichCompareBool, PyObject_SelfIter, PyObject_SetAttrString, PyObject_Vectorcall, PySequence_Contains, PySequence_List, PySequence_Tuple, PyTuple_New, PyTuple_Pack, PyType_GenericAlloc, PyUnicodeWriter, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteASCII, PyUnicodeWriter_WriteChar, PyUnicode_FromString, PyUnicode_InternFromString, PyVectorcall_Function, Py_BuildValue, Py_Ellipsis, Py_NewRef, Py_None, Py_NotImplemented, _PyArg_CheckPositional, _PyArg_NoKeywords, _PyObject_GC_New, _PyTuple_Resize, _PyUnicode_EqualToASCIIString, _Py_typing_type_repr, jacpy_is_exact_list, jacpy_is_list, jacpy_is_tuple, jacpy_is_type, jacpy_is_unicode, jacpy_release }
    cpython_api --> object_model.header { NULL, PyObject, PyThreadState_GetUnchecked, PyType_IsSubtype, PyUnicode_InternFromString, Py_NewRef, Py_NotImplemented, _PyEval_GetBuiltin, _Py_Dealloc, _Py_NewReference, jacpy_release }
    cpython_api --> object_model.interpolation { NULL, PyDict_SetItemString, PyErr_Format, PyErr_SetString, PyExc_SystemError, PyExc_TypeError, PyExc_ValueError, PyInterpreterState, PyMemberDef, PyMethodDef, PyObject, PyObject_GC_Del, PyType_GenericAlloc, PyUnicode_AsUTF8AndSize, PyUnicode_FromFormat, PyUnicode_FromOrdinal, Py_BuildValue, Py_GetConstantBorrowed, Py_NewRef, Py_None, _PyArg_BadArgument, _PyObject_GC_New, _PyType_GetDict, _PyType_Name, jacpy_is_unicode, jacpy_release }
    cpython_api --> object_model.iterator { NULL, PyErr_BadInternalCall, PyErr_Clear, PyErr_ExceptionMatches, PyErr_Occurred, PyErr_SetString, PyExc_IndexError, PyExc_OverflowError, PyExc_StopAsyncIteration, PyExc_StopIteration, PyExc_TypeError, PyIter_Check, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSsize_t, PyMethodDef, PyObject, PyObject_CallMethod, PyObject_CallNoArgs, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_RichCompareBool, PyObject_SelfIter, PySequence_Check, PySequence_GetItem, PySequence_Size, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, _PyCoro_GetAwaitableIter, _PyGen_SetStopIterationValue, _PyObject_GC_New, _PyObject_HasLen, jacpy_release }
    cpython_api --> object_model.method { NULL, PyCallable_Check, PyErr_BadInternalCall, PyErr_SetString, PyExc_TypeError, PyMemberDef, PyMethodDef, PyObject, PyObject_Call, PyObject_ClearWeakRefs, PyObject_GC_Del, PyObject_GenericHash, PyObject_GenericSetAttr, PyObject_GetAttr, PyObject_GetAttrString, PyObject_GetOptionalAttrString, PyObject_Hash, PyObject_RichCompareBool, PyThreadState_GetUnchecked, PyType_Ready, PyUnicode_FromFormat, PyVectorcall_Call, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, _PyArg_CheckPositional, _PyArg_NoKeywords, _PyObject_GC_New, _PyObject_VectorcallPrepend, _PyType_LookupRef, jacpy_is_unicode, jacpy_release }
    cpython_api --> object_model.namespace { NULL, PyArg_UnpackTuple, PyArg_ValidateKeywordArguments, PyDict_GetItemRef, PyDict_Keys, PyDict_New, PyDict_Type, PyDict_Update, PyErr_Format, PyErr_Occurred, PyExc_TypeError, PyIter_Next, PyList_Append, PyList_New, PyMemberDef, PyMethodDef, PyObject, PyObject_CallNoArgs, PyObject_CallOneArg, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_GenericSetAttr, PyObject_GetIter, PyObject_RichCompare, PyTuple_New, PyTuple_Pack, PyType_GenericAlloc, PyUnicode_FromFormat, PyUnicode_FromString, PyUnicode_Join, Py_NewRef, Py_NotImplemented, Py_ReprEnter, Py_ReprLeave, _PyArg_NoPositional, _PyType_Name, jacpy_is_exact_dict, jacpy_is_unicode, jacpy_release, jacpy_unicode_size }
    cpython_api --> object_model.picklebuffer { NULL, PyArg_ParseTupleAndKeywords, PyBuffer_IsContiguous, PyBuffer_Release, PyErr_Format, PyErr_SetString, PyExc_BufferError, PyExc_TypeError, PyExc_ValueError, PyMemoryView_FromObject, PyMethodDef, PyObject, PyObject_ClearWeakRefs, PyObject_GetBuffer, Py_NewRef, Py_None, Py_buffer, jacpy_release }
    cpython_api --> object_model.range { NULL, PyErr_BadArgument, PyErr_Clear, PyErr_Format, PyErr_Occurred, PyErr_SetString, PyExc_IndexError, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyLong_AsLong, PyLong_AsLongAndOverflow, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSsize_t, PyLong_GetSign, PyMemberDef, PyMethodDef, PyNumber_Add, PyNumber_AsSsize_t, PyNumber_FloorDivide, PyNumber_Index, PyNumber_Multiply, PyNumber_Negative, PyNumber_Remainder, PyNumber_Subtract, PyObject, PyObject_Free, PyObject_GenericGetAttr, PyObject_Hash, PyObject_IsTrue, PyObject_Not, PyObject_RichCompareBool, PyObject_SelfIter, PyTuple_New, PyUnicode_FromFormat, PyVectorcall_NARGS, Py_BuildValue, Py_IncRef, Py_NewRef, Py_None, Py_NotImplemented, _PyArg_NoKeywords, _PyArg_NoKwnames, _PyObject_New, _PySequence_IterSearch, jacpy_release }
    cpython_api --> object_model.slice { NULL, PyArg_UnpackTuple, PyDict_Size, PyErr_SetString, PyExc_TypeError, PyExc_ValueError, PyIndex_Check, PyLong_AsSsize_t, PyLong_FromLong, PyLong_FromSsize_t, PyLong_GetSign, PyMemberDef, PyMethodDef, PyNumber_Add, PyNumber_Index, PyObject, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_Hash, PyObject_RichCompare, PyObject_RichCompareBool, PyTuple_Pack, PyUnicode_FromFormat, PyUnicode_FromString, Py_BuildValue, Py_NewRef, Py_None, Py_NotImplemented, _PyArg_NoKeywords, _PyEval_SliceIndex, _PyObject_GC_New, _Py_SetImmortal, jacpy_is_long, jacpy_release }
    cpython_api --> object_model.structseq { NULL, PyDict_GetItemRef, PyDict_GetItemWithError, PyDict_Keys, PyDict_New, PyDict_Pop, PyDict_SetItem, PyDict_Size, PyErr_BadInternalCall, PyErr_Format, PyErr_NoMemory, PyErr_Occurred, PyExc_RuntimeError, PyExc_SystemError, PyExc_TypeError, PyInterpreterState, PyInterpreterState_Main, PyLong_AsSsize_t, PyLong_FromSsize_t, PyMem_Free, PyMem_Malloc, PyMemberDef, PyMethodDef, PyObject, PyObject_GC_Del, PySequence_Fast, PyTuple_New, PyType_FromSpecWithBases, PyType_Ready, PyType_Slot, PyType_Spec, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteChar, PyUnicodeWriter_WriteRepr, PyUnicodeWriter_WriteStr, PyUnicode_FromString, PyUnicode_InternFromString, Py_BuildValue, Py_IncRef, Py_NewRef, Py_None, _PyArg_NoPositional, _PyObject_GC_NewVar, _PyStaticType_FiniBuiltin, _PyStaticType_InitBuiltin, _PyTuple_FromArray, _PyTuple_Resize, _PyType_GetDict, _PyType_HasSubclasses, _Py_SetImmortal, jacpy_is_dict, jacpy_release }
    cpython_api --> object_model.template { NULL, PyErr_Format, PyErr_SetString, PyExc_TypeError, PyImport_ImportModule, PyIter_Next, PyMemberDef, PyMethodDef, PyObject, PyObject_GC_Del, PyObject_GetAttrString, PyObject_GetIter, PyObject_SelfIter, PySequence_Concat, PyTuple_New, PyType_GenericAlloc, PyUnicode_Concat, PyUnicode_FromFormat, Py_BuildValue, Py_GetConstantBorrowed, Py_NewRef, _PyObject_GC_New, _PyType_Name, jacpy_is_unicode, jacpy_release, jacpy_unicode_size }
    cpython_api --> object_model.union { NULL, PyErr_Clear, PyErr_Format, PyErr_SetString, PyExc_TypeError, PyFrozenSet_New, PyImport_ImportModule, PyList_Append, PyList_AsTuple, PyList_GetItem, PyList_New, PyMemberDef, PyMethodDef, PyObject, PyObject_CallFunctionObjArgs, PyObject_ClearWeakRefs, PyObject_GC_Del, PyObject_GenericGetAttr, PyObject_GetAttr, PyObject_GetAttrString, PyObject_Hash, PyObject_RichCompareBool, PySequence_Contains, PySet_Add, PySet_Contains, PySet_New, PyType_GenericAlloc, PyUnicodeWriter_Create, PyUnicodeWriter_Discard, PyUnicodeWriter_Finish, PyUnicodeWriter_WriteASCII, PyUnicode_FromString, Py_NewRef, Py_None, Py_NotImplemented, _PyNone_Type, _PyObject_GC_New, _PyTypeAlias_Type, _PyUnicode_EqualToASCIIString, _Py_typing_type_repr, jacpy_is_exact_tuple, jacpy_is_type, jacpy_is_unicode, jacpy_release }
    layouts --> bindings.arguments { PyTypeObject }
    layouts --> bindings.asyncio { METH_FASTCALL, METH_NOARGS, METH_O, PyGetSetDef, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_IMMUTABLETYPE, Py_TPFLAGS_MANAGED_DICT, Py_TPFLAGS_MANAGED_WEAKREF, Py_am_await, Py_am_send, Py_tp_call, Py_tp_clear, Py_tp_dealloc, Py_tp_doc, Py_tp_finalize, Py_tp_getattro, Py_tp_getset, Py_tp_init, Py_tp_iter, Py_tp_iternext, Py_tp_methods, Py_tp_new, Py_tp_repr, Py_tp_token, Py_tp_traverse }
    layouts --> bindings.buffer { PY_BUFFER_SIZE }
    layouts --> bindings.datetime { METH_CLASS, METH_FASTCALL, METH_KEYWORDS, METH_NOARGS, METH_O, METH_VARARGS, PY_TUPLE_OBJECT_SIZE, PyDateTime_CAPI, PyGetSetDef, PyStatus, PyTypeObject, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_IMMUTABLETYPE, Py_tp_dealloc, Py_tp_doc, Py_tp_getset, Py_tp_methods, Py_tp_new, Py_tp_repr, Py_tp_traverse, _PyStatus_TYPE_ERROR, _PyStatus_TYPE_OK }
    layouts --> bindings.decimal { METH_CLASS, METH_KEYWORDS, METH_NOARGS, METH_O, METH_VARARGS, PyGetSetDef, PyTypeObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_DISALLOW_INSTANTIATION, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_IMMUTABLETYPE, Py_mp_ass_subscript, Py_mp_length, Py_mp_subscript, Py_nb_absolute, Py_nb_add, Py_nb_bool, Py_nb_divmod, Py_nb_float, Py_nb_floor_divide, Py_nb_int, Py_nb_multiply, Py_nb_negative, Py_nb_positive, Py_nb_power, Py_nb_remainder, Py_nb_subtract, Py_nb_true_divide, Py_tp_clear, Py_tp_dealloc, Py_tp_doc, Py_tp_getattro, Py_tp_getset, Py_tp_hash, Py_tp_init, Py_tp_iter, Py_tp_methods, Py_tp_new, Py_tp_repr, Py_tp_richcompare, Py_tp_setattro, Py_tp_str, Py_tp_token, Py_tp_traverse }
    layouts --> bindings.posix { METH_COEXIST, METH_NOARGS, PyTypeObject as TypeLayout }
    layouts --> bindings.socket { PY_SOCKET_API_SIZE, PY_SOCKET_FAMILY_OFFSET, PY_SOCKET_OBJECT_SIZE, PY_SOCKET_PROTO_OFFSET, PY_SOCKET_TYPE_OFFSET, PyGetSetDef, PySocketModule_APIObject, PyTypeObject, Py_READONLY, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_IMMUTABLETYPE, Py_T_INT, Py_tp_dealloc, Py_tp_doc, Py_tp_finalize, Py_tp_getset, Py_tp_init, Py_tp_members, Py_tp_methods, Py_tp_new, Py_tp_repr, Py_tp_traverse }
    layouts --> bindings.sre { METH_CLASS, METH_O, METH_VARARGS, PyGetSetDef, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_DISALLOW_INSTANTIATION, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_IMMUTABLETYPE, Py_T_INT, Py_T_PYSSIZET, Py_mp_subscript, Py_tp_clear, Py_tp_dealloc, Py_tp_doc, Py_tp_getset, Py_tp_hash, Py_tp_members, Py_tp_methods, Py_tp_repr, Py_tp_richcompare, Py_tp_token, Py_tp_traverse, _Py_T_OBJECT }
    layouts --> bindings.ssl { PY_OS_ERROR_OBJECT_SIZE, PyOSErrorObject, PySocketModule_APIObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_IMMUTABLETYPE, Py_tp_doc, Py_tp_str }
    layouts --> bindings.type { PY_STRUCT_SEQUENCE_DESC_SIZE, PY_STRUCT_SEQUENCE_FIELD_SIZE, PyGetSetDef, PyStructSequence_Desc, PyStructSequence_Field }
    layouts --> modules.asyncio { PYGEN_ERROR, PYGEN_NEXT, PYGEN_RETURN, Py_futureiters_MAXFREELIST, _Py_freelists_FUTUREITERS }
    layouts --> modules.asyncio_core { _object }
    layouts --> modules.atexit { PyStatus, _PyStatus_TYPE_ERROR, _PyStatus_TYPE_OK }
    layouts --> modules.datetime { PyTypeObject }
    layouts --> modules.datetime_date { PY_DATETIME_DATE_SIZE, PyDateTime_Date, PyGetSetDef, PyNumberMethods, PyTypeObject, PyVarObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_tp_traverse, _PyTime_ROUND_FLOOR, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> modules.datetime_datetime { PY_DATETIME_BASE_DATETIME_SIZE, PY_DATETIME_DATETIME_SIZE, PyDateTime_DateTime, PyGetSetDef, PyNumberMethods, PyTypeObject, PyVarObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, _PyTime_ROUND_FLOOR, _PyTime_ROUND_HALF_EVEN, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> modules.datetime_delta { PY_DATETIME_DELTA_DAYS_OFFSET, PY_DATETIME_DELTA_MICROSECONDS_OFFSET, PY_DATETIME_DELTA_SECONDS_OFFSET, PY_DATETIME_DELTA_SIZE, PyDateTime_Delta, PyNumberMethods, PyTypeObject, PyVarObject, Py_CONSTANT_EMPTY_STR, Py_CONSTANT_ONE, Py_READONLY, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_T_INT, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> modules.datetime_objects { PY_DATETIME_DATA_OFFSET, PyDateTime_Date, PyDateTime_DateTime, PyDateTime_Delta, PyDateTime_Time, PyTypeObject, _PyDateTime_BaseTZInfo, _object }
    layouts --> modules.datetime_time { PY_DATETIME_BASE_TIME_SIZE, PY_DATETIME_TIME_SIZE, PyDateTime_Time, PyGetSetDef, PyTypeObject, PyVarObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> modules.datetime_tzinfo { PY_DATETIME_TZINFO_SIZE, PY_OBJECT_SIZE, PyDateTime_DateTime, PyTypeObject, PyVarObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> modules.decimal_context { PyTypeObject }
    layouts --> modules.decimal_number { PyTypeObject }
    layouts --> modules.decimal_objects { PyTypeObject, _object }
    layouts --> modules.posix_core { PyStatus, _PyStatus_TYPE_OK }
    layouts --> modules.posix_fileio { PY_BUFFER_SIZE }
    layouts --> modules.posix_stat { PyTypeObject as TypeLayout }
    layouts --> modules.socket_address { PY_BUFFER_SIZE, PySocketSockObject, Py_CLEANUP_SUPPORTED }
    layouts --> modules.socket_core { PySocketSockObject, PyTypeObject, _PyTime_ROUND_CEILING, _PyTime_ROUND_TIMEOUT, _socket_state }
    layouts --> modules.socket_object { PY_BUFFER_SIZE, PySocketSockObject, PyTypeObject }
    layouts --> modules.sre { PyBUF_SIMPLE, PyTypeObject, PyVarObject, Py_EQ, Py_NE, _object }
    layouts --> modules.ssl { PyTypeObject }
    layouts --> modules.ssl_cert { PyTypeObject }
    layouts --> modules.ssl_core { PySocketSockObject, _PyTime_ROUND_CEILING }
    layouts --> modules.zoneinfo { PyDateTime_CAPI, PyDateTime_DateTime }
    layouts --> object_model.bool { PyLongObject, PyLong_DIGITS_OFFSET, PyLong_DIGIT_SIZE, PyNumberMethods, PyTypeObject, PyVarObject, Py_TPFLAGS_DEFAULT, _PyLongValue, _PyLong_FALSE_TAG, _PyLong_TRUE_TAG, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> object_model.capsule { PyCapsule, PyCapsule_SIZE, PyTypeObject, PyVarObject, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> object_model.cell { PyCellObject, PyCellObject_SIZE, PyGetSetDef, PyTypeObject, PyVarObject, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> object_model.complex { METH_CLASS, METH_NOARGS, METH_O, PyComplexObject, PyComplexObject_IMAG, PyComplexObject_REAL, PyComplexObject_SIZE, PyFloatObject, PyHASH_IMAG, PyNumberMethods, PyTypeObject, PyVarObject, Py_DTSF_SIGN, Py_EQ, Py_NE, Py_READONLY, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_T_DOUBLE, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_TYPE_VERSION_COMPLEX, _object }
    layouts --> object_model.enumerate { METH_CLASS, METH_NOARGS, METH_O, PyTypeObject, PyVarObject, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object, enumobject, enumobject_SIZE, reversedobject, reversedobject_SIZE }
    layouts --> object_model.file { METH_NOARGS, METH_VARARGS, PyGetSetDef, PyStdPrinter_Object, PyStdPrinter_Object_SIZE, PyTypeObject, PyVarObject, Py_PRINT_RAW, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_DISALLOW_INSTANTIATION, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> object_model.genericalias { METH_NOARGS, METH_O, PyGetSetDef, PyMappingMethods, PyNumberMethods, PyTypeObject, PyVarObject, Py_EQ, Py_NE, Py_READONLY, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_HAVE_VECTORCALL, Py_T_BOOL, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_T_OBJECT, _object, gaiterobject, gaiterobject_SIZE, gaobject, gaobject_ARGS, gaobject_ORIGIN, gaobject_SIZE, gaobject_STARRED, gaobject_VECTORCALL, gaobject_WEAKREFLIST }
    layouts --> object_model.header { PyGC_Head_SIZE, PyListObject, PyThreadState_INTERP, PyTupleObject, PyTupleObject_ITEMS, PyTypeObject, PyVarObject, Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_NE, Py_TPFLAGS_LIST_SUBCLASS, _PyGC_PREV_FLAGS, _PyGC_PREV_MASK, _PyGC_PREV_MASK_FINALIZED, _Py_IMMORTAL_INITIAL_REFCNT, _Py_freelist, _gc_runtime_state_GENERATION0, _gc_runtime_state_HEAP_SIZE, _object }
    layouts --> object_model.interpolation { FVC_ASCII, FVC_REPR, FVC_STR, METH_CLASS, METH_NOARGS, METH_O, PyStatus, PyTypeObject, PyVarObject, Py_CONSTANT_EMPTY_STR, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_T_OBJECT_EX, _PyStatus_TYPE_ERROR, _PyStatus_TYPE_OK, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object, interpolationobject, interpolationobject_CONVERSION, interpolationobject_EXPRESSION, interpolationobject_FORMAT_SPEC, interpolationobject_SIZE, interpolationobject_VALUE }
    layouts --> object_model.iterator { METH_NOARGS, METH_O, METH_VARARGS, PyAsyncMethods, PyTypeObject, PyVarObject, Py_EQ, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object, anextawaitableobject, anextawaitableobject_SIZE, calliterobject, calliterobject_SIZE, seqiterobject, seqiterobject_SIZE }
    layouts --> object_model.method { METH_NOARGS, PyGetSetDef, PyInstanceMethodObject, PyInstanceMethodObject_FUNC, PyInstanceMethodObject_SIZE, PyMethodObject, PyMethodObject_FUNC, PyMethodObject_SELF, PyMethodObject_SIZE, PyMethodObject_VECTORCALL, PyMethodObject_WEAKREFLIST, PyTypeObject, PyVarObject, Py_EQ, Py_NE, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_HAVE_VECTORCALL, Py_pymethodobjects_MAXFREELIST, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_T_OBJECT, _Py_freelists_PYMETHODOBJECTS, _object }
    layouts --> object_model.namespace { METH_KEYWORDS, METH_NOARGS, METH_VARARGS, PyTypeObject, PyVarObject, Py_READONLY, Py_TPFLAGS_BASETYPE, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _PyNamespaceObject, _PyNamespaceObject_NS_DICT, _PyNamespaceObject_SIZE, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_T_OBJECT, _object }
    layouts --> object_model.picklebuffer { METH_NOARGS, PyBUF_FULL_RO, PyBufferProcs, PyMemoryViewObject_FLAGS, PyMemoryViewObject_VIEW, PyPickleBufferObject, PyPickleBufferObject_SIZE, PyPickleBufferObject_VIEW, PyPickleBufferObject_WEAKREFLIST, PyTypeObject, PyVarObject, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_buffer_ITEMSIZE, Py_buffer_LEN, _Py_MEMORYVIEW_C, _Py_MEMORYVIEW_FORTRAN, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object }
    layouts --> object_model.range { METH_NOARGS, METH_O, PY_ITERSEARCH_CONTAINS, PY_ITERSEARCH_COUNT, PY_ITERSEARCH_INDEX, PyMappingMethods, PyNumberMethods, PySequenceMethods, PyTypeObject, PyVarObject, Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_NE, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_SEQUENCE, Py_T_OBJECT_EX, Py_range_iters_MAXFREELIST, Py_ranges_MAXFREELIST, _PyRangeIterObject, _PyRangeIterObject_SIZE, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_freelists_RANGES, _Py_freelists_RANGE_ITERS, _object, longrangeiterobject, longrangeiterobject_SIZE, rangeobject, rangeobject_SIZE, rangeobject_START, rangeobject_STEP, rangeobject_STOP }
    layouts --> object_model.slice { METH_NOARGS, METH_O, PySliceObject, PySliceObject_SIZE, PySliceObject_START, PySliceObject_STEP, PySliceObject_STOP, PyTypeObject, PyVarObject, Py_EQ, Py_GE, Py_GT, Py_LE, Py_LT, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_slices_MAXFREELIST, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_T_OBJECT, _Py_freelists_SLICES, _object }
    layouts --> object_model.structseq { METH_KEYWORDS, METH_NOARGS, METH_VARARGS, PY_MEMBER_DEF_SIZE, PY_TYPE_SLOT_SIZE, PY_TYPE_SPEC_SIZE, PyStructSequence_Desc, PyStructSequence_Field, PyStructSequence_SIZE, PyTupleObject, PyTupleObject_ITEMS, PyTypeObject, PyVarObject, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_TPFLAGS_HEAPTYPE, Py_TPFLAGS_READY, Py_tp_dealloc, Py_tp_doc, Py_tp_members, Py_tp_methods, Py_tp_new, Py_tp_repr, Py_tp_traverse, _Py_T_OBJECT, _object }
    layouts --> object_model.template { METH_CLASS, METH_NOARGS, METH_O, PyGetSetDef, PySequenceMethods, PyTypeObject, PyVarObject, Py_CONSTANT_EMPTY_STR, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, Py_T_OBJECT_EX, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _object, templateiterobject, templateiterobject_SIZE, templateobject, templateobject_INTERPOLATIONS, templateobject_SIZE, templateobject_STRINGS }
    layouts --> object_model.union { METH_CLASS, METH_O, PyGetSetDef, PyMappingMethods, PyNumberMethods, PyTypeObject, PyVarObject, Py_EQ, Py_NE, Py_READONLY, Py_TPFLAGS_DEFAULT, Py_TPFLAGS_HAVE_GC, _Py_STATIC_IMMORTAL_INITIAL_REFCNT, _Py_T_OBJECT, _object, unionobject, unionobject_ARGS, unionobject_SIZE, unionobject_WEAKREFLIST }
    layouts_platform --> object_model.header { PyInterpreterState_FREELISTS, PyInterpreterState_GC }
    bindings.arguments --> bindings.array { BoundArguments, CallSignature, invoke }
    bindings.arguments --> bindings.collections { BoundArguments, CallSignature, index_value, invoke }
    bindings.arguments --> bindings.csv { BoundArguments, CallSignature, invoke }
    bindings.arguments --> bindings.functools { BoundArguments, CallSignature, index_value, invoke }
    bindings.arguments --> bindings.json { BoundArguments, CallSignature, index_value, invoke, invoke_one }
    bindings.buffer --> bindings.array { BufferLayout, jacpy_binding_buffer_dispose, jacpy_binding_buffer_fill }
    bindings.buffer --> bindings.struct { BufferArgument }
    bindings.module --> bindings.array { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.binascii { ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception }
    bindings.module --> bindings.bisect { ModuleDefinition }
    bindings.module --> bindings.cmath { ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.collections { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.csv { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_exception, jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_module_native_set, jacpy_binding_state_get }
    bindings.module --> bindings.functools { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.heapq { ModuleDefinition }
    bindings.module --> bindings.itertools { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.json { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.math { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.operator { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.pickle { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_exception, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.queue { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception }
    bindings.module --> bindings.random { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.statistics { ModuleDefinition }
    bindings.module --> bindings.struct { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.type { MethodDefinition, install_methods }
    bindings.payload --> bindings.array { clear_payload, dispose_payload, jacpy_binding_native_set, traverse_payload }
    bindings.payload --> bindings.collections { clear_payload, dispose_payload, jacpy_binding_native_clear, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_untrack, traverse_payload }
    bindings.payload --> bindings.csv { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set, traverse_payload }
    bindings.payload --> bindings.functools { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set, traverse_payload }
    bindings.payload --> bindings.json { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set, traverse_payload }
    bindings.payload --> bindings.operator { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set, traverse_payload }
    bindings.payload --> bindings.pickle { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> bindings.queue { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> bindings.random { jacpy_binding_native_clear, jacpy_binding_native_set }
    bindings.payload --> bindings.struct { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, traverse_payload }
    bindings.references --> bindings.array { ReferenceState, owned_tuple }
    bindings.references --> bindings.collections { ReferenceState, owned_tuple }
    bindings.references --> bindings.csv { ReferenceState }
    bindings.references --> bindings.functools { ReferenceState }
    bindings.references --> bindings.json { ReferenceState }
    bindings.references --> bindings.operator { ReferenceState }
    bindings.references --> bindings.pickle { ReferenceState }
    bindings.state --> bindings.functools { NativeState }
    bindings.state --> bindings.module { NativeState }
    bindings.state --> bindings.payload { NativeState }
    bindings.state --> bindings.references { NativeState }
    bindings.state --> modules.csv { NativeState }
    bindings.state --> modules.queue { NativeState }
    bindings.state --> modules.random { NativeState }
    bindings.type --> bindings.array { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, TypeSlot, jacpy_binding_allocate, jacpy_binding_matches }
    bindings.type --> bindings.collections { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_base_clear, jacpy_binding_base_dealloc, jacpy_binding_base_init, jacpy_binding_base_traverse, jacpy_binding_matches, jacpy_binding_parent }
    bindings.type --> bindings.csv { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate, jacpy_binding_owner }
    bindings.type --> bindings.functools { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate, jacpy_binding_dict_peek, jacpy_binding_dict_present, jacpy_binding_dict_replace, jacpy_binding_owner }
    bindings.type --> bindings.itertools { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.json { TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate }
    bindings.type --> bindings.operator { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate }
    bindings.type --> bindings.payload { jacpy_binding_dict_clear, jacpy_binding_dict_visit, jacpy_binding_free }
    bindings.type --> bindings.pickle { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.queue { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.random { TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate, jacpy_binding_free }
    bindings.type --> bindings.struct { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_allocate }
    bindings.arguments --> bindings.clinic.bz2 { CallSignature }
    bindings.arguments --> bindings.clinic.grp { CallSignature }
    bindings.arguments --> bindings.clinic.opcode { CallSignature }
    bindings.arguments --> bindings.clinic.syslog { CallSignature }
    bindings.arguments --> bindings.clinic.zlib { CallSignature }
    bindings.arguments --> bindings.zlib { BoundArguments, CallSignature, invoke }
    bindings.buffer --> bindings.clinic.bz2 { BufferArgument }
    bindings.buffer --> bindings.clinic.grp { BufferArgument }
    bindings.buffer --> bindings.clinic.opcode { BufferArgument }
    bindings.buffer --> bindings.clinic.pwd { BufferArgument }
    bindings.buffer --> bindings.clinic.resource { BufferArgument }
    bindings.buffer --> bindings.clinic.suggestions { BufferArgument }
    bindings.buffer --> bindings.clinic.sysconfig { BufferArgument }
    bindings.buffer --> bindings.clinic.syslog { BufferArgument }
    bindings.buffer --> bindings.clinic.tracemalloc { BufferArgument }
    bindings.buffer --> bindings.clinic.typing { BufferArgument }
    bindings.buffer --> bindings.clinic.weakref { BufferArgument }
    bindings.buffer --> bindings.clinic.zlib { BufferArgument }
    bindings.buffer --> bindings.converters { BufferArgument }
    bindings.buffer --> modules.bz2 { BufferArgument }
    bindings.buffer --> modules.zlib { BufferArgument }
    bindings.converters --> bindings.clinic.bz2 { argument_label, convert_buffer, convert_int, convert_ssize }
    bindings.converters --> bindings.clinic.grp { argument_label, convert_unicode }
    bindings.converters --> bindings.clinic.opcode { argument_label, borrowed_none, convert_int, return_bool, return_int }
    bindings.converters --> bindings.clinic.resource { argument_label, borrowed_none, convert_int, return_int }
    bindings.converters --> bindings.clinic.suggestions { argument_label, convert_unicode }
    bindings.converters --> bindings.clinic.syslog { argument_label, convert_long, convert_unicode, return_long }
    bindings.converters --> bindings.clinic.tracemalloc { argument_label, convert_int }
    bindings.converters --> bindings.clinic.weakref { argument_label, bad_argument, return_ssize }
    bindings.converters --> bindings.clinic.zlib { argument_label, convert_buffer, convert_int, convert_ssize, convert_unsigned_bounded, defining_class, return_unsigned }
    bindings.converters --> bindings.syslog { argument_label, convert_int, convert_str }
    bindings.converters --> bindings.zlib { convert_int }
    bindings.converters --> modules.bz2 { ClassToken }
    bindings.converters --> modules.opcode { borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.resource { borrowed_none }
    bindings.converters --> modules.suggestions { borrowed_none }
    bindings.converters --> modules.syslog { borrowed_none }
    bindings.converters --> modules.tracemalloc { borrowed_none }
    bindings.converters --> modules.weakref { borrowed_none }
    bindings.converters --> modules.zlib { ClassToken }
    bindings.module --> bindings.bz2 { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.clinic.bz2 { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.grp { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.opcode { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.pwd { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.resource { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.suggestions { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.sysconfig { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.syslog { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.tracemalloc { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.typing { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.weakref { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.zlib { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.errno { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.grp { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.opcode { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.pwd { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.resource { MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned }
    bindings.module --> bindings.stat { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.suggestions { ModuleDefinition }
    bindings.module --> bindings.sysconfig { ModuleDefinition }
    bindings.module --> bindings.syslog { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.tracemalloc { ModuleDefinition }
    bindings.module --> bindings.types { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.typing { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.weakref { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.zlib { ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_exception, jacpy_binding_state_set }
    bindings.module --> modules.grp { jacpy_binding_state_get }
    bindings.module --> modules.pwd { jacpy_binding_state_get }
    bindings.module --> modules.resource { jacpy_binding_state_get }
    bindings.module --> modules.zlib { jacpy_binding_state_get }
    bindings.payload --> bindings.bz2 { dispose_payload, traverse_payload }
    bindings.payload --> bindings.zlib { dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, traverse_payload }
    bindings.payload --> modules.bz2 { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.zlib { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.runtime_objects --> bindings.types { export_runtime_objects }
    bindings.runtime_objects --> bindings.typing { export_runtime_objects }
    bindings.runtime_objects --> bindings.weakref { export_runtime_objects }
    bindings.state --> modules.bz2 | modules.zlib { NativeState }
    bindings.type --> bindings.bz2 { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.clinic.bz2 { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.grp { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.opcode { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.pwd { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.resource { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.suggestions { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.sysconfig { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.syslog { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.tracemalloc { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.typing { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.weakref { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.zlib { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.converters { jacpy_binding_base }
    bindings.type --> bindings.zlib { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> modules.bz2 { jacpy_binding_allocate }
    bindings.type --> modules.zlib { jacpy_binding_allocate }
    bindings.arguments --> bindings.clinic.blake2 | bindings.clinic.hmac | bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 | bindings.clinic.sha3 { CallSignature }
    bindings.buffer --> bindings.clinic.blake2 | bindings.clinic.hmac | bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 | bindings.clinic.sha3 | modules.blake2 | modules.hashlib | modules.hmac { BufferArgument }
    bindings.converters --> bindings.clinic.blake2 { argument_label, convert_bool, convert_buffer, convert_int, convert_unsigned_long, convert_unsigned_long_long }
    bindings.converters --> bindings.clinic.hmac { argument_label, defining_class }
    bindings.converters --> bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 { argument_label, convert_bool, defining_class }
    bindings.converters --> bindings.clinic.sha3 { argument_label, convert_bool, convert_unsigned_long }
    bindings.converters --> bindings.sha2 | modules.blake2 | modules.hmac | modules.md5 | modules.sha1 | modules.sha2 | modules.sha3 { ClassToken }
    bindings.converters --> modules.atexit { borrowed_none }
    bindings.converters --> modules.hashlib { ClassToken, borrowed_none }
    bindings.module --> bindings.atexit { MethodCallbacks, MethodDefinition, ModuleDefinition }
    bindings.module --> bindings.blake2 { ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_state_get }
    bindings.module --> bindings.clinic.blake2 | bindings.clinic.hmac | bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 | bindings.clinic.sha3 { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.hmac { ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception }
    bindings.module --> bindings.md5 | bindings.sha1 | bindings.sha2 { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.sha3 { MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> modules.hmac | modules.md5 | modules.sha1 | modules.sha2 | modules.sha3 { jacpy_binding_state_get }
    bindings.payload --> bindings.blake2 | bindings.hmac | bindings.md5 | bindings.sha1 | bindings.sha2 | bindings.sha3 { dispose_payload, traverse_payload }
    bindings.payload --> modules.hashlib { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.state --> modules.blake2 | modules.hashlib | modules.hmac | modules.md5 | modules.sha1 | modules.sha2 | modules.sha3 { NativeState }
    bindings.type --> bindings.blake2 | bindings.md5 | bindings.sha1 | bindings.sha2 | bindings.sha3 { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.clinic.blake2 | bindings.clinic.hmac | bindings.clinic.md5 | bindings.clinic.sha1 | bindings.clinic.sha2 | bindings.clinic.sha3 { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.converters { jacpy_binding_type_matches }
    bindings.type --> bindings.hmac { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> modules.hashlib { jacpy_binding_allocate }
    bindings.arguments --> bindings.array { PARSE_FORMAT }
    bindings.arguments --> bindings.clinic.abc { check_positional }
    bindings.arguments --> bindings.clinic.array { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.asyncio { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.binascii { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.bisect { CallSignature, PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.blake2 { PARSE_KEYWORDS, invoke_tuple, unpack_mapping }
    bindings.arguments --> bindings.clinic.bz2 { PARSE_KEYWORDS, PARSE_NOTHING, PARSE_POSITIONAL, invoke_stack, invoke_tuple, unpack_stack }
    bindings.arguments --> bindings.clinic.cmath { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.codecs { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.collections { CallSignature, PARSE_KEYWORDS, PARSE_POSITIONAL, check_positional, invoke_tuple, unpack_mapping }
    bindings.arguments --> bindings.clinic.csv { CallSignature, PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.datetime { CallSignature, PARSE_KEYWORDS, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.elementtree { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.fcntl { check_positional }
    bindings.arguments --> bindings.clinic.functools { CallSignature, PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.grp { PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.hashopenssl { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.heapq { check_positional }
    bindings.arguments --> bindings.clinic.hmac { PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.itertools { CallSignature, PARSE_KEYWORDS, PARSE_POSITIONAL, check_positional, invoke_tuple, unpack_mapping }
    bindings.arguments --> bindings.clinic.locale { check_positional }
    bindings.arguments --> bindings.clinic.lsprof { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.lzma { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.math { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.md5 { PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.mmap { check_positional }
    bindings.arguments --> bindings.clinic.multibytecodec { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.multiprocessing { CallSignature, PARSE_FORMAT, PARSE_KEYWORDS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.opcode { PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.operator { check_positional }
    bindings.arguments --> bindings.clinic.pickle { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.posix { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.posixshmem { BoundArguments, CallSignature, PARSE_FORMAT_KEYWORDS, invoke }
    bindings.arguments --> bindings.clinic.posixsubprocess { check_positional }
    bindings.arguments --> bindings.clinic.pyexpat { CallSignature, PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.queue { CallSignature, PARSE_KEYWORDS, PARSE_NOTHING, PARSE_NO_ARGUMENTS, invoke_stack, invoke_tuple, unpack_stack }
    bindings.arguments --> bindings.clinic.random { CallSignature, PARSE_POSITIONAL, check_positional, invoke_tuple }
    bindings.arguments --> bindings.clinic.resource { check_positional }
    bindings.arguments --> bindings.clinic.select { CallSignature, PARSE_KEYWORDS, PARSE_NOTHING, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.sha1 { PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.sha2 { PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.sha3 { PARSE_KEYWORDS, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.socket { CallSignature, PARSE_KEYWORDS, invoke_tuple, unpack_mapping }
    bindings.arguments --> bindings.clinic.sqlite3 { CallSignature, PARSE_KEYWORDS, PARSE_POSITIONAL, check_positional, invoke_stack, invoke_tuple, unpack_stack }
    bindings.arguments --> bindings.clinic.sre { CallSignature, PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.ssl { CallSignature, PARSE_KEYWORDS, PARSE_NOTHING, PARSE_POSITIONAL, check_positional, invoke_stack, invoke_tuple, unpack_stack }
    bindings.arguments --> bindings.clinic.statistics { check_positional }
    bindings.arguments --> bindings.clinic.struct { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.suggestions { check_positional }
    bindings.arguments --> bindings.clinic.syslog { PARSE_KEYWORDS, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.termios { check_positional }
    bindings.arguments --> bindings.clinic.tracemalloc { check_positional }
    bindings.arguments --> bindings.clinic.unicodedata { check_positional }
    bindings.arguments --> bindings.clinic.weakref { check_positional }
    bindings.arguments --> bindings.clinic.zlib { PARSE_KEYWORDS, PARSE_NO_ARGUMENTS, check_positional, invoke_stack, unpack_stack }
    bindings.arguments --> bindings.clinic.zoneinfo { CallSignature, PARSE_KEYWORDS, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.clinic.zstd { CallSignature, PARSE_KEYWORDS, check_positional, invoke_stack, invoke_tuple, unpack_mapping, unpack_stack }
    bindings.arguments --> bindings.collections { PARSE_FORMAT }
    bindings.arguments --> bindings.csv { PARSE_FORMAT_KEYWORDS }
    bindings.arguments --> bindings.datetime { BoundArguments, CallSignature, PARSE_KEYWORDS, invoke_vector }
    bindings.arguments --> bindings.functools { vector_tuple }
    bindings.arguments --> bindings.json { PARSE_FORMAT }
    bindings.arguments --> bindings.math { check_positional }
    bindings.arguments --> bindings.operator { check_positional }
    bindings.arguments --> bindings.struct { vector_tuple }
    bindings.arguments --> bindings.zlib { PARSE_FORMAT_KEYWORDS }
    bindings.arguments --> modules.datetime_date { ArgumentFormat }
    bindings.arguments --> modules.datetime_datetime { ArgumentFormat }
    bindings.arguments --> modules.datetime_delta { ArgumentFormat }
    bindings.arguments --> modules.datetime_time { ArgumentFormat }
    bindings.arguments --> modules.datetime_tzinfo { ArgumentFormat }
    bindings.arguments --> modules.decimal_number { ArgumentFormat, ArgumentValue }
    bindings.arguments --> modules.itertools { BoundArguments, CallSignature, PARSE_FORMAT_KEYWORDS, index_value, keywords_of_dict }
    bindings.arguments --> modules.lzma { ArgumentFormat }
    bindings.arguments --> modules.math { vector_tuple }
    bindings.arguments --> modules.mmap { ArgumentFormat, ArgumentValue }
    bindings.arguments --> modules.multibytecodec { ArgumentFormat }
    bindings.arguments --> modules.select { ArgumentFormat }
    bindings.arguments --> modules.sqlite3 { ArgumentFormat }
    bindings.arguments --> modules.time { ArgumentFormat }
    bindings.arguments --> object_model.complex { BoundArguments, CallSignature, PARSE_KEYWORDS, invoke }
    bindings.arguments --> object_model.interpolation { BoundArguments, CallSignature, PARSE_KEYWORDS, invoke }
    bindings.arguments --> object_model.structseq { BoundArguments, CallSignature, PARSE_KEYWORDS, invoke }
    bindings.buffer --> bindings.clinic.abc { BufferArgument }
    bindings.buffer --> bindings.clinic.array { BufferArgument }
    bindings.buffer --> bindings.clinic.asyncio { BufferArgument }
    bindings.buffer --> bindings.clinic.binascii { BufferArgument }
    bindings.buffer --> bindings.clinic.bisect { BufferArgument }
    bindings.buffer --> bindings.clinic.cmath { BufferArgument }
    bindings.buffer --> bindings.clinic.codecs { BufferArgument }
    bindings.buffer --> bindings.clinic.collections { BufferArgument }
    bindings.buffer --> bindings.clinic.csv { BufferArgument }
    bindings.buffer --> bindings.clinic.datetime { BufferArgument }
    bindings.buffer --> bindings.clinic.elementtree { BufferArgument }
    bindings.buffer --> bindings.clinic.fcntl { BufferArgument }
    bindings.buffer --> bindings.clinic.functools { BufferArgument }
    bindings.buffer --> bindings.clinic.hashopenssl { BufferArgument }
    bindings.buffer --> bindings.clinic.heapq { BufferArgument }
    bindings.buffer --> bindings.clinic.itertools { BufferArgument }
    bindings.buffer --> bindings.clinic.json { BufferArgument }
    bindings.buffer --> bindings.clinic.locale { BufferArgument }
    bindings.buffer --> bindings.clinic.lsprof { BufferArgument }
    bindings.buffer --> bindings.clinic.lzma { BufferArgument }
    bindings.buffer --> bindings.clinic.math { BufferArgument }
    bindings.buffer --> bindings.clinic.mmap { BufferArgument }
    bindings.buffer --> bindings.clinic.multibytecodec { BufferArgument }
    bindings.buffer --> bindings.clinic.multiprocessing { BufferArgument }
    bindings.buffer --> bindings.clinic.operator { BufferArgument }
    bindings.buffer --> bindings.clinic.pickle { BufferArgument }
    bindings.buffer --> bindings.clinic.posix { BufferArgument }
    bindings.buffer --> bindings.clinic.posixshmem { BufferArgument }
    bindings.buffer --> bindings.clinic.posixsubprocess { BufferArgument }
    bindings.buffer --> bindings.clinic.pyexpat { BufferArgument }
    bindings.buffer --> bindings.clinic.queue { BufferArgument }
    bindings.buffer --> bindings.clinic.random { BufferArgument }
    bindings.buffer --> bindings.clinic.select { BufferArgument }
    bindings.buffer --> bindings.clinic.socket { BufferArgument }
    bindings.buffer --> bindings.clinic.sqlite3 { BufferArgument }
    bindings.buffer --> bindings.clinic.sre { BufferArgument }
    bindings.buffer --> bindings.clinic.ssl { BufferArgument }
    bindings.buffer --> bindings.clinic.statistics { BufferArgument }
    bindings.buffer --> bindings.clinic.struct { BufferArgument }
    bindings.buffer --> bindings.clinic.termios { BufferArgument }
    bindings.buffer --> bindings.clinic.time { BufferArgument }
    bindings.buffer --> bindings.clinic.unicodedata { BufferArgument }
    bindings.buffer --> bindings.clinic.zoneinfo { BufferArgument }
    bindings.buffer --> bindings.clinic.zstd { BufferArgument }
    bindings.buffer --> modules.array { BufferArgument }
    bindings.buffer --> modules.binascii { BufferArgument }
    bindings.buffer --> modules.codecs { BufferArgument }
    bindings.buffer --> modules.elementtree { BufferArgument }
    bindings.buffer --> modules.fcntl { BufferArgument }
    bindings.buffer --> modules.hashopenssl { BufferArgument }
    bindings.buffer --> modules.lzma { BufferArgument }
    bindings.buffer --> modules.mmap { BufferArgument, BufferLayout, jacpy_binding_buffer_dispose, jacpy_binding_buffer_fill }
    bindings.buffer --> modules.multibytecodec { BufferArgument }
    bindings.buffer --> modules.pickle { BufferArgument }
    bindings.buffer --> modules.posix_fileio { BufferArgument }
    bindings.buffer --> modules.posix_files { BufferArgument }
    bindings.buffer --> modules.pyexpat { BufferArgument }
    bindings.buffer --> modules.socket { BufferArgument }
    bindings.buffer --> modules.sqlite3 { BufferArgument }
    bindings.buffer --> modules.ssl { BufferArgument }
    bindings.buffer --> modules.struct { BufferArgument }
    bindings.buffer --> modules.zstd { BufferArgument }
    bindings.converters --> bindings.array { convert_unicode_char }
    bindings.converters --> bindings.clinic.abc { argument_label }
    bindings.converters --> bindings.clinic.array { argument_label, convert_buffer, convert_int, convert_slice_index_not_none, convert_ssize, convert_unicode, convert_unicode_char, defining_class }
    bindings.converters --> bindings.clinic.asyncio { argument_label, borrowed_none, convert_bool, defining_class, return_int }
    bindings.converters --> bindings.clinic.binascii { argument_label, convert_bool, convert_buffer, convert_int, convert_unsigned_bounded, return_unsigned }
    bindings.converters --> bindings.clinic.bisect { argument_label, borrowed_none, convert_optional_ssize, convert_ssize, return_ssize }
    bindings.converters --> bindings.clinic.bz2 { new_checks_arguments }
    bindings.converters --> bindings.clinic.cmath { argument_label, convert_double, return_bool }
    bindings.converters --> bindings.clinic.codecs { argument_label, bad_argument, borrowed_none, convert_bool, convert_buffer, convert_cstr, convert_int, convert_str, convert_text_buffer, convert_unicode, return_bool }
    bindings.converters --> bindings.clinic.collections { argument_label, convert_slice_index_not_none, convert_ssize, new_checks_arguments, return_int }
    bindings.converters --> bindings.clinic.csv { argument_label }
    bindings.converters --> bindings.clinic.datetime { argument_label, borrowed_none, convert_int }
    bindings.converters --> bindings.clinic.elementtree { argument_label, bad_argument, borrowed_none, convert_bool, convert_cstr, convert_ssize, defining_class, return_int, return_size }
    bindings.converters --> bindings.clinic.fcntl { argument_label, convert_bool, convert_fildes, convert_int, convert_unsigned_long }
    bindings.converters --> bindings.clinic.functools { argument_label }
    bindings.converters --> bindings.clinic.hashopenssl { argument_label, borrowed_none, convert_bool, convert_buffer, convert_long, convert_ssize, convert_str, convert_unsigned_long, return_int }
    bindings.converters --> bindings.clinic.heapq { argument_label, bad_argument }
    bindings.converters --> bindings.clinic.itertools { argument_label, bad_argument, borrowed_none, convert_bool, convert_ssize, new_checks_arguments }
    bindings.converters --> bindings.clinic.locale { argument_label, convert_cstr, convert_int, convert_str, convert_unicode }
    bindings.converters --> bindings.clinic.lsprof { argument_label, convert_bool, convert_double, defining_class, return_int }
    bindings.converters --> bindings.clinic.lzma { argument_label, borrowed_none, convert_buffer, convert_int, convert_ssize }
    bindings.converters --> bindings.clinic.math { argument_label, borrowed_none, convert_double, return_bool, return_double }
    bindings.converters --> bindings.clinic.mmap { argument_label, borrowed_none, convert_buffer, convert_int, convert_optional_ssize, convert_ssize, convert_unsigned_bounded }
    bindings.converters --> bindings.clinic.multibytecodec { argument_label, bad_argument, borrowed_none, convert_bool, convert_buffer, convert_cstr, defining_class }
    bindings.converters --> bindings.clinic.multiprocessing { argument_label, borrowed_none, convert_bool, convert_cstr, convert_int, convert_str }
    bindings.converters --> bindings.clinic.operator { argument_label, convert_ssize, return_bool, return_ssize }
    bindings.converters --> bindings.clinic.pickle { argument_label, borrowed_none, convert_bool, convert_str, defining_class, return_int, return_size }
    bindings.converters --> bindings.clinic.posix { argument_label, borrowed_none, convert_PyUnicode_FSConverter, convert_bool, convert_buffer, convert_double, convert_fildes, convert_int, convert_long_long, convert_ssize, convert_str, convert_unsigned_bounded, convert_unsigned_int, convert_unsigned_long, convert_unsigned_long_long, convert_writable_buffer, defining_class, return_bool, return_double, return_int, return_long, return_ssize }
    bindings.converters --> bindings.clinic.posixshmem { argument_label, bad_argument, convert_int, convert_unicode, return_int }
    bindings.converters --> bindings.clinic.posixsubprocess { argument_label, bad_argument, convert_bool, convert_int }
    bindings.converters --> bindings.clinic.pwd { bad_argument }
    bindings.converters --> bindings.clinic.pyexpat { argument_label, convert_bool, convert_cstr, convert_float, convert_int, convert_long, convert_str, convert_unsigned_long_long, defining_class }
    bindings.converters --> bindings.clinic.queue { argument_label, borrowed_none, convert_bool, defining_class, new_checks_arguments, return_bool, return_ssize }
    bindings.converters --> bindings.clinic.random { argument_label, borrowed_none, convert_uint64, init_checks_arguments, return_int }
    bindings.converters --> bindings.clinic.select { argument_label, borrowed_none, convert_fildes, convert_int, convert_unsigned_bounded, convert_unsigned_short, new_checks_arguments }
    bindings.converters --> bindings.clinic.socket { argument_label, convert_PyUnicode_FSConverter, convert_buffer, convert_int, convert_str, convert_uint16, convert_uint32, return_int }
    bindings.converters --> bindings.clinic.sqlite3 { argument_label, bad_argument, borrowed_none, convert_bool, convert_buffer, convert_cstr, convert_double, convert_int, convert_str, convert_text_buffer, convert_uint32, convert_unicode, defining_class, init_checks_arguments, new_checks_arguments, return_bool, return_int }
    bindings.converters --> bindings.clinic.sre { argument_label, bad_argument, borrowed_none, convert_int, convert_ssize, defining_class, defining_class_or_null, exact_int_at, failed, return_bool, return_int, return_ssize }
    bindings.converters --> bindings.clinic.ssl { argument_label, borrowed_none, convert_PyUnicode_FSConverter, convert_bool, convert_buffer, convert_cstr, convert_double, convert_int, convert_str, convert_text_buffer, new_checks_arguments }
    bindings.converters --> bindings.clinic.statistics { argument_label, convert_double, return_double }
    bindings.converters --> bindings.clinic.struct { argument_label, convert_buffer, convert_ssize, return_int, return_ssize }
    bindings.converters --> bindings.clinic.termios { argument_label, convert_fildes, convert_int }
    bindings.converters --> bindings.clinic.unicodedata { SizedText, argument_label, convert_sized_str, convert_unicode, convert_unicode_char, return_int }
    bindings.converters --> bindings.clinic.zoneinfo { argument_label, borrowed_none, convert_unsigned_bounded, defining_class, defining_class_of_type }
    bindings.converters --> bindings.clinic.zstd { argument_label, bad_argument, borrowed_none, convert_bool, convert_buffer, convert_int, convert_ssize }
    bindings.converters --> bindings.collections { bad_argument }
    bindings.converters --> bindings.datetime { convert_int }
    bindings.converters --> bindings.multibytecodec { ClassToken }
    bindings.converters --> modules.abc { ClassToken, borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.array { ClassToken }
    bindings.converters --> modules.asyncio { ClassToken }
    bindings.converters --> modules.codecs { borrowed_none }
    bindings.converters --> modules.collections { ClassToken }
    bindings.converters --> modules.elementtree { ClassToken, bad_argument }
    bindings.converters --> modules.fcntl { borrowed_none }
    bindings.converters --> modules.functools { ClassToken }
    bindings.converters --> modules.hashopenssl { ClassToken, borrowed_none }
    bindings.converters --> modules.itertools { ClassToken, bad_argument }
    bindings.converters --> modules.locale { borrowed_none }
    bindings.converters --> modules.lsprof { ClassToken, borrowed_none }
    bindings.converters --> modules.lzma { ClassToken }
    bindings.converters --> modules.mmap { ClassToken, borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.multibytecodec { ClassToken }
    bindings.converters --> modules.multiprocessing { ClassToken, borrowed_false, borrowed_none, borrowed_true, convert_unsigned_long_long }
    bindings.converters --> modules.pickle { ClassToken }
    bindings.converters --> modules.posix_stat { ClassToken }
    bindings.converters --> modules.posixshmem { borrowed_none }
    bindings.converters --> modules.posixsubprocess { borrowed_none }
    bindings.converters --> modules.pyexpat { ClassToken }
    bindings.converters --> modules.queue { ClassToken }
    bindings.converters --> modules.random { ClassToken }
    bindings.converters --> modules.select { ClassToken, borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.socket { convert_unsigned_int }
    bindings.converters --> modules.sqlite3 { ClassToken, bad_argument, borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.sre { ClassToken }
    bindings.converters --> modules.ssl { bad_argument, borrowed_false, borrowed_none, borrowed_true }
    bindings.converters --> modules.ssl_core { ClassToken }
    bindings.converters --> modules.struct { ClassToken }
    bindings.converters --> modules.termios { borrowed_none }
    bindings.converters --> modules.time { borrowed_none }
    bindings.converters --> modules.unicodedata { ClassToken }
    bindings.converters --> modules.uuid { borrowed_none }
    bindings.converters --> modules.zoneinfo { ClassToken }
    bindings.converters --> modules.zstd { ClassToken }
    bindings.members --> bindings.bz2 { MemberField, MemberType, record_clear }
    bindings.members --> bindings.collections { MemberField, MemberType, record_object, record_set_object }
    bindings.members --> bindings.csv { MemberField, MemberType, record_clear, record_set_byte, record_set_object }
    bindings.members --> bindings.functools { MemberField, MemberType, record_clear, record_set_object }
    bindings.members --> bindings.json { MemberField, MemberType, record_clear, record_set_byte, record_set_object }
    bindings.members --> bindings.lzma { MemberField, MemberType, record_clear }
    bindings.members --> bindings.multibytecodec { MemberField, MemberType, record_clear, record_set_object }
    bindings.members --> bindings.pickle { MemberField, MemberType, record_object, record_set_object }
    bindings.members --> bindings.type { MemberField }
    bindings.members --> bindings.unicodedata { MemberField, MemberType }
    bindings.members --> bindings.zlib { MemberField, MemberType, record_clear }
    bindings.members --> bindings.zoneinfo { MemberField, MemberType, record_clear }
    bindings.members --> modules.bz2 { record_set_byte, record_set_object }
    bindings.members --> modules.collections { record_set_object }
    bindings.members --> modules.elementtree { MemberField }
    bindings.members --> modules.lzma { record_set_byte, record_set_int, record_set_object }
    bindings.members --> modules.multiprocessing { MemberField, MemberType }
    bindings.members --> modules.pickle { record_int, record_set_int }
    bindings.members --> modules.posix_stat { MemberField, MemberType }
    bindings.members --> modules.pyexpat { MemberField }
    bindings.members --> modules.select_platform { MemberField }
    bindings.members --> modules.sqlite3 { MemberField }
    bindings.members --> modules.unicodedata { record_set_address }
    bindings.members --> modules.zlib { record_set_byte, record_set_object }
    bindings.members --> modules.zoneinfo { record_set_object }
    bindings.module --> bindings.abc { ModuleDefinition, ModuleHooks, jacpy_binding_module_native_set, jacpy_binding_state_set }
    bindings.module --> bindings.asyncio { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, clear_state, jacpy_binding_module_native_set, jacpy_binding_state_get, jacpy_binding_state_set, method_table, traverse_state }
    bindings.module --> bindings.clinic.abc { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.array { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.asyncio { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.binascii { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.bisect { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.cmath { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.codecs { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.collections { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.csv { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.datetime { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.elementtree { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.fcntl { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.functools { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.hashopenssl { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.heapq { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.itertools { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.json { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.locale { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.lsprof { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.lzma { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.math { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.mmap { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.multibytecodec { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.multiprocessing { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.operator { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.pickle { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.posix { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.posixshmem { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.posixsubprocess { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.pyexpat { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.queue { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.random { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.select { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.socket { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.sqlite3 { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.sre { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.ssl { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.statistics { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.struct { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.termios { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.time { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.unicodedata { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.zoneinfo { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.clinic.zstd { MethodCallbacks, MethodDefinition }
    bindings.module --> bindings.codecs { ModuleDefinition }
    bindings.module --> bindings.codecs_cn { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.codecs_hk { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.codecs_iso2022 { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.codecs_jp { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.codecs_kr { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.codecs_tw { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.collections { visit_reference }
    bindings.module --> bindings.csv { visit_reference }
    bindings.module --> bindings.datetime { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, clear_state, jacpy_binding_state_get, jacpy_binding_state_set, method_table, traverse_state }
    bindings.module --> bindings.decimal { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.elementtree { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_exception, jacpy_binding_module_native_set }
    bindings.module --> bindings.fcntl { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.functools { visit_reference }
    bindings.module --> bindings.hashopenssl { ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_module_native_set, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.heapq { ModuleHooks, add_owned }
    bindings.module --> bindings.locale { MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception }
    bindings.module --> bindings.lsprof { ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.lzma { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_exception, jacpy_binding_state_set }
    bindings.module --> bindings.mmap { MethodDefinition, ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.multibytecodec { ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_state_set }
    bindings.module --> bindings.multiprocessing { ModuleDefinition, ModuleHooks, add_owned }
    bindings.module --> bindings.payload { visit_reference }
    bindings.module --> bindings.pickle { visit_reference }
    bindings.module --> bindings.posix { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_module_native_set, jacpy_binding_state_set }
    bindings.module --> bindings.posixshmem { ModuleDefinition }
    bindings.module --> bindings.posixsubprocess { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.pyexpat { MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_exception, jacpy_binding_module_native_set }
    bindings.module --> bindings.references { visit_reference }
    bindings.module --> bindings.select { MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_module_native_set, jacpy_binding_state_set }
    bindings.module --> bindings.socket { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_module_native_set, jacpy_binding_state_set, method_table, visit_reference }
    bindings.module --> bindings.sqlite3 { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_owned, jacpy_binding_exception, jacpy_binding_module_native_set, visit_reference }
    bindings.module --> bindings.sre { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_state_set, method_table }
    bindings.module --> bindings.ssl { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned, jacpy_binding_module_native_set, jacpy_binding_state_get, jacpy_binding_state_set }
    bindings.module --> bindings.termios { ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_exception }
    bindings.module --> bindings.time { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, add_state_owned }
    bindings.module --> bindings.unicodedata { ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.uuid { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks }
    bindings.module --> bindings.zoneinfo { MethodCallbacks, MethodDefinition, ModuleDefinition, ModuleHooks, jacpy_binding_module_native_set }
    bindings.module --> bindings.zstd { ModuleDefinition, ModuleHooks, add_owned, add_state_owned, jacpy_binding_exception, jacpy_binding_state_get }
    bindings.module --> modules.abc { FunctionTable, MethodCallbacks, MethodDefinition, jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get }
    bindings.module --> modules.array { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.asyncio { PositionalMethodRecord, visit_reference }
    bindings.module --> modules.asyncio_core { jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get }
    bindings.module --> modules.binascii { jacpy_binding_state_get }
    bindings.module --> modules.collections { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.csv { jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get }
    bindings.module --> modules.datetime_date { visit_reference }
    bindings.module --> modules.datetime_objects { jacpy_binding_state_get }
    bindings.module --> modules.decimal_context { visit_reference }
    bindings.module --> modules.decimal_number { jacpy_binding_state_set, visit_reference }
    bindings.module --> modules.decimal_objects { jacpy_binding_state_get }
    bindings.module --> modules.elementtree { jacpy_binding_module_native_get, visit_reference }
    bindings.module --> modules.functools { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.hashopenssl { MethodDefinition, jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get }
    bindings.module --> modules.itertools { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.locale { jacpy_binding_state_get }
    bindings.module --> modules.lsprof { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.lzma { jacpy_binding_state_get }
    bindings.module --> modules.multibytecodec { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.pickle { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.posix_core { jacpy_binding_module_native_get, jacpy_binding_state_get }
    bindings.module --> modules.posix_fileio { add_state_owned }
    bindings.module --> modules.posix_ids { add_state_owned }
    bindings.module --> modules.posix_process { add_state_owned, jacpy_binding_state_set }
    bindings.module --> modules.posix_stat { add_state_owned, jacpy_binding_module_native_get }
    bindings.module --> modules.pyexpat { jacpy_binding_module_native_get, jacpy_binding_module_native_present, visit_reference }
    bindings.module --> modules.queue { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.select { MethodCallbacks, MethodDefinition, builtin_function, jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.socket_core { jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get }
    bindings.module --> modules.socket_object { visit_reference }
    bindings.module --> modules.sqlite3 { jacpy_binding_module_native_get, jacpy_binding_module_native_present, visit_reference }
    bindings.module --> modules.sre { jacpy_binding_state_get, jacpy_binding_state_set, visit_reference }
    bindings.module --> modules.ssl_core { jacpy_binding_module_native_get, jacpy_binding_module_native_present, jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.struct { jacpy_binding_state_get, visit_reference }
    bindings.module --> modules.termios { jacpy_binding_state_get }
    bindings.module --> modules.time { jacpy_binding_state_get }
    bindings.module --> modules.zlib { visit_reference }
    bindings.module --> modules.zoneinfo { jacpy_binding_module_native_get, jacpy_binding_module_native_present, visit_reference }
    bindings.module --> modules.zstd { jacpy_binding_state_get, jacpy_binding_state_set, visit_reference }
    bindings.module --> object_model.cell { visit_reference }
    bindings.module --> object_model.enumerate { visit_reference }
    bindings.module --> object_model.genericalias { visit_reference }
    bindings.module --> object_model.interpolation { visit_reference }
    bindings.module --> object_model.iterator { visit_reference }
    bindings.module --> object_model.method { visit_reference }
    bindings.module --> object_model.namespace { visit_reference }
    bindings.module --> object_model.picklebuffer { visit_reference }
    bindings.module --> object_model.slice { visit_reference }
    bindings.module --> object_model.structseq { visit_reference }
    bindings.module --> object_model.template { visit_reference }
    bindings.module --> object_model.union { visit_reference }
    bindings.payload --> bindings.abc { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> bindings.hashopenssl { dispose_payload }
    bindings.payload --> bindings.lsprof { dispose_payload, jacpy_binding_untrack, traverse_payload }
    bindings.payload --> bindings.lzma { dispose_payload, traverse_payload }
    bindings.payload --> bindings.mmap { dispose_payload, traverse_payload }
    bindings.payload --> bindings.multibytecodec { clear_payload, dispose_payload, jacpy_binding_native_get, jacpy_binding_native_present, traverse_payload }
    bindings.payload --> bindings.multiprocessing { dispose_payload, traverse_payload }
    bindings.payload --> bindings.pickle { jacpy_binding_untrack }
    bindings.payload --> bindings.select { dispose_payload, jacpy_binding_native_present }
    bindings.payload --> bindings.sqlite3 { clear_payload, dispose_payload, jacpy_binding_native_present, traverse_payload }
    bindings.payload --> bindings.ssl { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> bindings.unicodedata { dispose_payload, traverse_payload }
    bindings.payload --> bindings.zoneinfo { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> bindings.zstd { clear_payload, dispose_payload, traverse_payload }
    bindings.payload --> modules.abc { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.array { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.collections { clear_payload, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.elementtree { jacpy_binding_clear_weakrefs, jacpy_binding_untrack }
    bindings.payload --> modules.functools { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.itertools { clear_payload, dispose_payload, jacpy_binding_dealloc_guard, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set, jacpy_binding_own_get, jacpy_binding_own_present, traverse_payload }
    bindings.payload --> modules.lsprof { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.lzma { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.mmap { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.multibytecodec { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.multiprocessing { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.pickle { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.posix_stat { dispose_payload, jacpy_binding_native_clear, jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.pyexpat { jacpy_binding_untrack }
    bindings.payload --> modules.queue { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.random { jacpy_binding_native_get, jacpy_binding_native_present }
    bindings.payload --> modules.select { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.sqlite3 { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.ssl { jacpy_binding_native_set }
    bindings.payload --> modules.ssl_cert { jacpy_binding_native_set }
    bindings.payload --> modules.ssl_core { jacpy_binding_native_get, jacpy_binding_native_present }
    bindings.payload --> modules.struct { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.unicodedata { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.zoneinfo { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.payload --> modules.zstd { jacpy_binding_native_get, jacpy_binding_native_present, jacpy_binding_native_set }
    bindings.references --> modules.abc { ReferenceState, owned_tuple }
    bindings.references --> modules.array { ReferenceState, owned_tuple }
    bindings.references --> modules.codecs { owned_tuple }
    bindings.references --> modules.collections { ReferenceState, owned_tuple }
    bindings.references --> modules.functools { ReferenceState }
    bindings.references --> modules.itertools { ReferenceState }
    bindings.references --> modules.lsprof { call_method }
    bindings.references --> modules.mmap { owned_tuple }
    bindings.references --> modules.pickle { ReferenceState, owned_tuple }
    bindings.references --> modules.struct { ReferenceState }
    bindings.references --> modules.uuid { owned_tuple }
    bindings.state --> modules.abc { NativeState }
    bindings.state --> modules.array { NativeState }
    bindings.state --> modules.asyncio_core { NativeState }
    bindings.state --> modules.collections { NativeState }
    bindings.state --> modules.elementtree { NativeState }
    bindings.state --> modules.functools { NativeState }
    bindings.state --> modules.hashopenssl { NativeState }
    bindings.state --> modules.itertools { NativeState }
    bindings.state --> modules.lsprof { NativeState }
    bindings.state --> modules.lzma { NativeState }
    bindings.state --> modules.mmap { NativeState }
    bindings.state --> modules.multibytecodec { NativeState }
    bindings.state --> modules.multiprocessing { NativeState }
    bindings.state --> modules.pickle { NativeState }
    bindings.state --> modules.posix_core { NativeState }
    bindings.state --> modules.posix_stat { NativeState }
    bindings.state --> modules.pyexpat { NativeState }
    bindings.state --> modules.select { NativeState }
    bindings.state --> modules.socket_core { NativeState }
    bindings.state --> modules.sqlite3 { NativeState }
    bindings.state --> modules.ssl_core { NativeState }
    bindings.state --> modules.struct { NativeState }
    bindings.state --> modules.unicodedata { NativeState }
    bindings.state --> modules.zoneinfo { NativeState }
    bindings.state --> modules.zstd { NativeState }
    bindings.type --> bindings.abc { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.asyncio { PropertyDefinition, getset_table }
    bindings.type --> bindings.bz2 { jacpy_binding_record }
    bindings.type --> bindings.clinic.abc { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.array { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.asyncio { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.binascii { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.bisect { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.cmath { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.codecs { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.collections { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.csv { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.datetime { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.elementtree { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.fcntl { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.functools { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.hashopenssl { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.heapq { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.itertools { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.json { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.locale { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.lsprof { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.lzma { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.math { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.mmap { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.multibytecodec { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.multiprocessing { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.operator { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.pickle { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.posix { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.posixshmem { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.posixsubprocess { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.pyexpat { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.queue { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.random { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.select { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.socket { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.sqlite3 { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.sre { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.ssl { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.statistics { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.struct { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.termios { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.time { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.unicodedata { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.zoneinfo { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.clinic.zstd { PropertyCallbacks, PropertyDefinition }
    bindings.type --> bindings.collections { jacpy_binding_record }
    bindings.type --> bindings.converters { TypeSlot }
    bindings.type --> bindings.csv { jacpy_binding_record }
    bindings.type --> bindings.elementtree { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.functools { jacpy_binding_record }
    bindings.type --> bindings.hashopenssl { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.json { jacpy_binding_record }
    bindings.type --> bindings.lsprof { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.lzma { TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_record }
    bindings.type --> bindings.mmap { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.multibytecodec { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_record }
    bindings.type --> bindings.multiprocessing { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.posix { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.pyexpat { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.select { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.sqlite3 { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_record }
    bindings.type --> bindings.ssl { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.struct { jacpy_binding_basicsize }
    bindings.type --> bindings.unicodedata { TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> bindings.zlib { jacpy_binding_record }
    bindings.type --> bindings.zoneinfo { TypeDefinition, TypeFlags, TypeHooks, jacpy_binding_record }
    bindings.type --> bindings.zstd { PropertyCallbacks, PropertyDefinition, TypeDefinition, TypeFlags, TypeHooks }
    bindings.type --> modules.abc { jacpy_binding_allocate }
    bindings.type --> modules.array { jacpy_binding_allocate, jacpy_binding_basicsize, jacpy_binding_matches, jacpy_binding_owner }
    bindings.type --> modules.asyncio.free_object { jacpy_binding_free }
    bindings.type --> modules.asyncio_core { jacpy_binding_owner }
    bindings.type --> modules.bz2 { jacpy_binding_record }
    bindings.type --> modules.collections { jacpy_binding_allocate, jacpy_binding_basicsize, jacpy_binding_matches, jacpy_binding_owner, jacpy_binding_record }
    bindings.type --> modules.decimal_objects { jacpy_binding_owner }
    bindings.type --> modules.elementtree { jacpy_binding_allocate, jacpy_binding_basicsize, jacpy_binding_free, jacpy_binding_owner, jacpy_binding_record }
    bindings.type --> modules.functools { jacpy_binding_allocate }
    bindings.type --> modules.itertools { TypeSlot, jacpy_binding_allocate, jacpy_binding_basicsize, jacpy_binding_matches, jacpy_binding_owner, jacpy_binding_token, jacpy_binding_type_matches }
    bindings.type --> modules.lsprof { descriptor_get, jacpy_binding_allocate }
    bindings.type --> modules.lzma { jacpy_binding_allocate, jacpy_binding_record }
    bindings.type --> modules.mmap { jacpy_binding_allocate }
    bindings.type --> modules.multibytecodec { jacpy_binding_allocate, jacpy_binding_owner }
    bindings.type --> modules.multiprocessing { jacpy_binding_allocate, jacpy_binding_record }
    bindings.type --> modules.pickle { jacpy_binding_allocate, jacpy_binding_basicsize, jacpy_binding_owner, jacpy_binding_record, jacpy_binding_token }
    bindings.type --> modules.posix_fileio { struct_sequence_type }
    bindings.type --> modules.posix_ids { struct_sequence_type }
    bindings.type --> modules.posix_process { struct_sequence_type }
    bindings.type --> modules.posix_stat { jacpy_binding_allocate, jacpy_binding_record, struct_sequence_type }
    bindings.type --> modules.pyexpat { jacpy_binding_allocate, jacpy_binding_free, jacpy_binding_record }
    bindings.type --> modules.queue { jacpy_binding_allocate }
    bindings.type --> modules.select { jacpy_binding_allocate, jacpy_binding_matches, jacpy_binding_owner, jacpy_binding_record }
    bindings.type --> modules.socket_core { jacpy_binding_owner }
    bindings.type --> modules.sqlite3 { jacpy_binding_allocate, jacpy_binding_owner, jacpy_binding_record }
    bindings.type --> modules.ssl { jacpy_binding_allocate }
    bindings.type --> modules.ssl_cert { jacpy_binding_allocate }
    bindings.type --> modules.ssl_core { jacpy_binding_owner }
    bindings.type --> modules.struct { jacpy_binding_allocate, jacpy_binding_owner }
    bindings.type --> modules.unicodedata { jacpy_binding_allocate, jacpy_binding_record }
    bindings.type --> modules.zlib { jacpy_binding_record }
    bindings.type --> modules.zoneinfo { jacpy_binding_allocate, jacpy_binding_owner, jacpy_binding_record }
    bindings.type --> modules.zstd { jacpy_binding_allocate }
    modules.array --> bindings.array { jacpy_array_address, jacpy_array_assign, jacpy_array_assign_slice, jacpy_array_compare, jacpy_array_copy, jacpy_array_cursor_new, jacpy_array_cursor_next, jacpy_array_delete, jacpy_array_export, jacpy_array_extend, jacpy_array_item, jacpy_array_repeat, jacpy_array_repr, jacpy_array_search }
    modules.binary_scalars --> modules.array { integer_from_bits, read_bits, write_bits }
    modules.binary_scalars --> modules.pickle_decode { integer_from_bits }
    modules.binary_scalars --> modules.pickle_stream { read_bits, write_bits }
    modules.binary_scalars --> modules.struct { integer_from_bits, read_bits, write_bits }
    modules.collections --> bindings.collections { deque_state, jacpy_default_missing, jacpy_default_repr, jacpy_deque_assign, jacpy_deque_compare, jacpy_deque_consumed, jacpy_deque_extend, jacpy_deque_item, jacpy_deque_limit, jacpy_deque_next, jacpy_deque_remaining, jacpy_deque_repeat, jacpy_deque_repr, jacpy_deque_size }
    modules.csv --> bindings.csv { CsvConfig, csv_reader, csv_writer, jacpy_csv_dialect, jacpy_csv_read, jacpy_csv_reader_clear, jacpy_csv_reader_fields, jacpy_csv_reader_line, jacpy_csv_registry, jacpy_csv_write }
    modules.functools --> bindings.functools { jacpy_cmp_key, jacpy_lru_call, jacpy_lru_init, jacpy_partial_call, jacpy_partial_clear, jacpy_partial_field, jacpy_partial_init, jacpy_partial_repr, jacpy_partial_restore, lru_state, partial_state }
    modules.iterators --> modules.combinatorics { reusable_tuple }
    modules.json --> bindings.json { jacpy_json_encode, jacpy_json_escape, jacpy_json_scan, jacpy_json_scanstring }
    modules.math --> bindings.math { jacpy_math_binary, jacpy_math_log, jacpy_math_unary }
    modules.numeric --> modules.cmath { asinh, atan2, copysign, cos, cosh, exp, fabs, hypot, isfinite, isinf, isnan, log, log1p, scaled, sin, sinh, sqrt, tan, tanh }
    modules.numeric --> modules.math { acos, acosh, asin, asinh, atan, atan2, atanh, cbrt, ceil, copysign, cos, cosh, erf, erfc, exp, exp2, expm1, fabs, floor, fma, fmod, infinity, isfinite, isinf, isnan, log, log10, log1p, log2, nan, nextafter, pow, remainder, scaled, sin, sinh, sqrt, tan, tanh }
    modules.numeric --> modules.statistics { fabs, log, sqrt }
    modules.object_ring --> modules.collections { object_ring }
    modules.object_ring --> modules.queue { object_ring }
    modules.operator --> bindings.operator { jacpy_operator_apply, jacpy_operator_call, jacpy_operator_prepare, jacpy_operator_reduce, jacpy_operator_repr }
    modules.pickle --> bindings.pickle { jacpy_pickler_memo_set, jacpy_pickler_new, jacpy_unpickler_memo_set, jacpy_unpickler_new }
    modules.pickle_decode --> modules.pickle { unpickle_state }
    modules.pickle_encode --> modules.pickle { pickle_state }
    modules.pickle_objects --> modules.pickle { find_global }
    modules.pickle_objects --> modules.pickle_encode { global_names, mapped_names }
    modules.pickle_opcodes --> modules.pickle_decode { opcode }
    modules.pickle_opcodes --> modules.pickle_encode { opcode }
    modules.pickle_stream --> modules.pickle { builtin_stream_error }
    modules.pickle_stream --> modules.pickle_decode { builtin_stream_error, pickle_reader, stream_error }
    modules.pickle_stream --> modules.pickle_encode { builtin_stream_error, pickle_writer, stream_error }
    modules.pickle_stream --> modules.pickle_objects { builtin_stream_error, stream_error }
    modules.random --> bindings.random { jacpy_random_new }
    modules.struct --> bindings.struct { jacpy_struct_cached, jacpy_struct_items, jacpy_struct_memory, jacpy_struct_next, jacpy_struct_offset, jacpy_struct_pack, jacpy_struct_remaining, jacpy_struct_size }
    modules.bz2 --> bindings.bz2 { BZ2Compressor_token, BZ2Decompressor_token }
    modules.bz2 --> bindings.clinic.bz2 { _bz2_BZ2Compressor_compress_impl, _bz2_BZ2Compressor_flush_impl, _bz2_BZ2Compressor_impl, _bz2_BZ2Decompressor_decompress_impl, _bz2_BZ2Decompressor_impl }
    modules.errno_constants --> bindings.errno { CONSTANTS, PLATFORM }
    modules.grp --> bindings.clinic.grp { grp_getgrall_impl, grp_getgrgid_impl, grp_getgrnam_impl }
    modules.opcode --> bindings.clinic.opcode { _opcode_get_executor_impl, _opcode_get_intrinsic1_descs_impl, _opcode_get_intrinsic2_descs_impl, _opcode_get_nb_ops_impl, _opcode_get_special_method_names_impl, _opcode_get_specialization_stats_impl, _opcode_has_arg_impl, _opcode_has_const_impl, _opcode_has_exc_impl, _opcode_has_free_impl, _opcode_has_jump_impl, _opcode_has_local_impl, _opcode_has_name_impl, _opcode_is_valid_impl, _opcode_stack_effect_impl }
    modules.opcode --> bindings.opcode { ENABLE_SPECIALIZATION, ENABLE_SPECIALIZATION_FT }
    modules.output_buffer --> modules.bz2 { BlocksOutputBuffer, Cursor }
    modules.output_buffer --> modules.zlib { BlocksOutputBuffer, Cursor }
    modules.pwd --> bindings.clinic.pwd { pwd_getpwall_impl, pwd_getpwnam_impl, pwd_getpwuid_impl }
    modules.resource --> bindings.clinic.resource { resource_getpagesize_impl, resource_getrlimit_impl, resource_getrusage_impl, resource_prlimit_impl, resource_setrlimit_impl }
    modules.resource_constants --> bindings.resource { CONSTANTS, RLIM_INFINITY }
    modules.resource_constants --> modules.resource { RLIM_INFINITY, RLIM_NLIMITS }
    modules.resource_records --> bindings.resource { HAS_PRLIMIT, PLATFORM }
    modules.resource_records --> modules.resource { prlimit, rlimit, rusage, timeval }
    modules.stat --> bindings.stat { S_IFBLK, S_IFCHR, S_IFDIR, S_IFDOOR, S_IFIFO, S_IFLNK, S_IFMT, S_IFPORT, S_IFREG, S_IFSOCK, S_IMODE, S_IRGRP, S_IROTH, S_IRUSR, S_IRWXG, S_IRWXO, S_IRWXU, S_ISGID, S_ISUID, S_ISVTX, S_IWGRP, S_IWOTH, S_IWUSR, S_IXGRP, S_IXOTH, S_IXUSR, filemode_text, is_type, mode_value }
    modules.stat_platform --> bindings.stat { HAS_SF_SUPPORTED, PLATFORM, SF_APPEND, SF_ARCHIVED, SF_DATALESS, SF_FIRMLINK, SF_IMMUTABLE, SF_NOUNLINK, SF_SETTABLE, SF_SNAPSHOT, SF_SUPPORTED, SF_SYNTHETIC, S_IFWHT, UF_APPEND, UF_COMPRESSED, UF_DATAVAULT, UF_HIDDEN, UF_IMMUTABLE, UF_NODUMP, UF_NOUNLINK, UF_OPAQUE, UF_SETTABLE, UF_TRACKED }
    modules.suggestions --> bindings.clinic.suggestions { _suggestions__generate_suggestions_impl }
    modules.sysconfig --> bindings.clinic.sysconfig { _sysconfig_config_vars_impl }
    modules.syslog --> bindings.clinic.syslog { LOG_USER, syslog_LOG_MASK_impl, syslog_LOG_UPTO_impl, syslog_closelog_impl, syslog_openlog_impl, syslog_setlogmask_impl }
    modules.syslog --> bindings.syslog { default_priority, syslog_syslog_impl }
    modules.syslog_constants --> bindings.syslog { CONSTANTS, PLATFORM }
    modules.syslog_constants --> modules.syslog { LOG_INFO, LOG_USER }
    modules.tracemalloc --> bindings.clinic.tracemalloc { _tracemalloc__get_object_traceback_impl, _tracemalloc__get_traces_impl, _tracemalloc_clear_traces_impl, _tracemalloc_get_traceback_limit_impl, _tracemalloc_get_traced_memory_impl, _tracemalloc_get_tracemalloc_memory_impl, _tracemalloc_is_tracing_impl, _tracemalloc_reset_peak_impl, _tracemalloc_start_impl, _tracemalloc_stop_impl }
    modules.typing --> bindings.clinic.typing { _typing__idfunc_impl }
    modules.user_records --> bindings.grp { PLATFORM }
    modules.user_records --> bindings.pwd { PLATFORM }
    modules.user_records --> modules.grp { SC_GETGR_R_SIZE_MAX }
    modules.user_records --> modules.pwd { SC_GETPW_R_SIZE_MAX, passwd }
    modules.weakref --> bindings.clinic.weakref { _weakref__remove_dead_weakref_impl, _weakref_getweakrefcount_impl, _weakref_getweakrefs_impl, _weakref_proxy_impl }
    modules.zlib --> bindings.clinic.zlib { Compress_token, DEFLATED, DEF_BUF_SIZE, DEF_MEM_LEVEL, Decompress_token, MAX_WBITS, Z_DEFAULT_COMPRESSION, Z_DEFAULT_STRATEGY, Z_FINISH, zlib_Compress___copy___impl, zlib_Compress___deepcopy___impl, zlib_Compress_compress_impl, zlib_Compress_copy_impl, zlib_Compress_flush_impl, zlib_Decompress___copy___impl, zlib_Decompress___deepcopy___impl, zlib_Decompress_copy_impl, zlib_Decompress_decompress_impl, zlib_Decompress_flush_impl, zlib_ZlibDecompressor_decompress_impl, zlib_adler32_impl, zlib_compress_impl, zlib_compressobj_impl, zlib_crc32_impl, zlib_decompress_impl, zlib_decompressobj_impl }
    modules.zlib --> bindings.zlib { COMPRESS_TYPE, Compress_token, DECOMPRESSOR_TYPE, DECOMPRESS_TYPE, DEFLATED, DEF_BUF_SIZE, DEF_MEM_LEVEL, Decompress_token, MAX_WBITS, ZLIB_ERROR, ZLIB_VERSION, Z_BEST_COMPRESSION, Z_BEST_SPEED, Z_BLOCK, Z_DEFAULT_COMPRESSION, Z_DEFAULT_STRATEGY, Z_FILTERED, Z_FINISH, Z_FIXED, Z_FULL_FLUSH, Z_HUFFMAN_ONLY, Z_NO_COMPRESSION, Z_NO_FLUSH, Z_PARTIAL_FLUSH, Z_RLE, Z_SYNC_FLUSH, Z_TREES, ZlibDecompressorState, ZlibDecompressor_token, ZlibStream, runtime_version, zlib_decompressor_new }
    modules.atexit --> bindings.atexit { atexit_clear, atexit_ncallbacks, atexit_register, atexit_run_exitfuncs, atexit_unregister }
    modules.blake2 --> bindings.blake2 { Blake2_token, HACL_HASH_BLAKE2B_KEY_BYTES, HACL_HASH_BLAKE2B_OUT_BYTES, HACL_HASH_BLAKE2B_PERSONAL_BYTES, HACL_HASH_BLAKE2B_SALT_BYTES, HACL_HASH_BLAKE2S_KEY_BYTES, HACL_HASH_BLAKE2S_OUT_BYTES, HACL_HASH_BLAKE2S_PERSONAL_BYTES, HACL_HASH_BLAKE2S_SALT_BYTES, get_block_size, get_digest_size, get_name }
    modules.blake2 --> bindings.clinic.blake2 { HACL_HASH_BLAKE2B_OUT_BYTES, HACL_HASH_BLAKE2S_OUT_BYTES, _blake2_blake2b_copy_impl, _blake2_blake2b_digest_impl, _blake2_blake2b_hexdigest_impl, _blake2_blake2b_update_impl, py_blake2b_new_impl, py_blake2s_new_impl }
    modules.blake2_simd --> modules.blake2 { Hacl_Hash_Blake2b_blake2_params, simd128_copy, simd128_digest, simd128_free, simd128_malloc, simd128_update, simd256_copy, simd256_digest, simd256_free, simd256_malloc, simd256_update }
    modules.hashlib --> bindings.blake2 | bindings.hmac | bindings.md5 | bindings.sha1 | bindings.sha2 | bindings.sha3 { HASHLIB_GIL_MINSIZE }
    modules.hashlib --> modules.blake2 | modules.md5 | modules.sha1 | modules.sha2 | modules.sha3 { HashLock, UINT32_MAX, data_argument, hash_digest, hash_initial_data, hash_object_new, hash_state_of, hash_update }
    modules.hashlib --> modules.hmac { HashLock, UINT32_MAX, hash_buffer, hash_initial_data, hash_object_new, hash_state_of, hash_update }
    modules.hmac --> bindings.clinic.hmac { HMAC_token, _hmac_HMAC_block_size_get_impl, _hmac_HMAC_copy_impl, _hmac_HMAC_digest_impl, _hmac_HMAC_digest_size_get_impl, _hmac_HMAC_hexdigest_impl, _hmac_HMAC_name_get_impl, _hmac_HMAC_update_impl, _hmac_compute_blake2b_32_impl, _hmac_compute_blake2s_32_impl, _hmac_compute_digest_impl, _hmac_compute_md5_impl, _hmac_compute_sha1_impl, _hmac_compute_sha2_224_impl, _hmac_compute_sha2_256_impl, _hmac_compute_sha2_384_impl, _hmac_compute_sha2_512_impl, _hmac_compute_sha3_224_impl, _hmac_compute_sha3_256_impl, _hmac_compute_sha3_384_impl, _hmac_compute_sha3_512_impl, _hmac_new_impl }
    modules.hmac --> bindings.hmac { HMAC_TYPE, HMAC_token, UNKNOWN_HASH_ERROR, hmac_repr }
    modules.md5 --> bindings.clinic.md5 { MD5Type_copy_impl, MD5Type_digest_impl, MD5Type_hexdigest_impl, MD5Type_token, MD5Type_update_impl, _md5_md5_impl }
    modules.md5 --> bindings.md5 { MD5Type_token, MD5_BLOCKSIZE, MD5_DIGESTSIZE }
    modules.numeric --> modules.math { round }
    modules.sha1 --> bindings.clinic.sha1 { SHA1Type_copy_impl, SHA1Type_digest_impl, SHA1Type_hexdigest_impl, SHA1Type_token, SHA1Type_update_impl, _sha1_sha1_impl }
    modules.sha1 --> bindings.sha1 { SHA1Type_token, SHA1_BLOCKSIZE, SHA1_DIGESTSIZE }
    modules.sha2 --> bindings.clinic.sha2 { SHA256Type_copy_impl, SHA256Type_digest_impl, SHA256Type_hexdigest_impl, SHA256Type_token, SHA256Type_update_impl, SHA512Type_copy_impl, SHA512Type_digest_impl, SHA512Type_hexdigest_impl, SHA512Type_token, SHA512Type_update_impl, _sha2_sha224_impl, _sha2_sha256_impl, _sha2_sha384_impl, _sha2_sha512_impl }
    modules.sha2 --> bindings.sha2 { SHA256Type_token, SHA256_BLOCKSIZE, SHA512Type_token, SHA512_BLOCKSIZE, sha2_of }
    modules.sha3 --> bindings.clinic.sha3 { _sha3_sha3_224_copy_impl, _sha3_sha3_224_digest_impl, _sha3_sha3_224_hexdigest_impl, _sha3_sha3_224_update_impl, _sha3_shake_128_digest_impl, _sha3_shake_128_hexdigest_impl, py_sha3_new_impl }
    modules.sha3 --> bindings.sha3 { SHA3_TYPES, SHA3_token, get_block_size, get_capacity_bits, get_digest_size, get_name, get_rate_bits, get_shake_digest_size, get_shake_suffix, get_suffix }
    modules.abc --> bindings.abc { AbcModuleState, DATA_TYPE, STATE_NAMES, abc_data_new, abc_data_token }
    modules.abc --> bindings.clinic.abc { _abc__abc_init_impl, _abc__abc_instancecheck_impl, _abc__abc_register_impl, _abc__abc_subclasscheck_impl, _abc__get_dump_impl, _abc__reset_caches_impl, _abc__reset_registry_impl, _abc_get_cache_token_impl }
    modules.array --> bindings.array { ArrayIteratorState, ArrayState, allocate, append_buffer, array_array___copy___impl, array_module_token, array_token, arrayiterator_token, iterator_state, module_for, state_for }
    modules.array --> bindings.clinic.array { array__array_reconstructor_impl, array_array___copy___impl, array_array___deepcopy___impl, array_array___reduce_ex___impl, array_array___sizeof___impl, array_array_append_impl, array_array_buffer_info_impl, array_array_byteswap_impl, array_array_clear_impl, array_array_count_impl, array_array_extend_impl, array_array_frombytes_impl, array_array_fromfile_impl, array_array_fromlist_impl, array_array_fromunicode_impl, array_array_index_impl, array_array_insert_impl, array_array_pop_impl, array_array_remove_impl, array_array_reverse_impl, array_array_tobytes_impl, array_array_tofile_impl, array_array_tolist_impl, array_array_tounicode_impl, array_arrayiterator___reduce___impl, array_arrayiterator___setstate___impl, array_token, arrayiterator_token }
    modules.asyncio --> bindings.asyncio { Future_token, Task_token, _asyncio_Future___init___impl, _asyncio_Future_add_done_callback_impl, _asyncio_Future_cancelled_impl, _asyncio_Future_done_impl, _asyncio_Future_exception_impl, _asyncio_Future_get_loop_impl, _asyncio_Future_result_impl, _asyncio_Future_set_result_impl, _asyncio_Task___init___impl, _asyncio_future_add_to_awaited_by_impl, _asyncio_future_discard_from_awaited_by_impl, future_clear, future_dealloc, future_finalize, future_new_iter, future_repr, future_traverse, futureiter_am_send, futureiter_clear, futureiter_close, futureiter_dealloc, futureiter_iternext, futureiter_send, futureiter_throw, futureiter_traverse, stepwrapper_call, stepwrapper_clear, stepwrapper_dealloc, stepwrapper_self, stepwrapper_traverse, task_clear, task_dealloc, task_finalize, task_repr, task_traverse }
    modules.asyncio --> bindings.clinic.asyncio { Future_token, Task_token, _asyncio_Future___init___impl, _asyncio_Future__asyncio_awaited_by_get_impl, _asyncio_Future__asyncio_future_blocking_get_impl, _asyncio_Future__asyncio_future_blocking_set_impl, _asyncio_Future__callbacks_get_impl, _asyncio_Future__cancel_message_get_impl, _asyncio_Future__cancel_message_set_impl, _asyncio_Future__exception_get_impl, _asyncio_Future__log_traceback_get_impl, _asyncio_Future__log_traceback_set_impl, _asyncio_Future__loop_get_impl, _asyncio_Future__make_cancelled_error_impl, _asyncio_Future__result_get_impl, _asyncio_Future__source_traceback_get_impl, _asyncio_Future__state_get_impl, _asyncio_Future_add_done_callback_impl, _asyncio_Future_cancel_impl, _asyncio_Future_cancelled_impl, _asyncio_Future_done_impl, _asyncio_Future_exception_impl, _asyncio_Future_get_loop_impl, _asyncio_Future_remove_done_callback_impl, _asyncio_Future_result_impl, _asyncio_Future_set_exception_impl, _asyncio_Future_set_result_impl, _asyncio_Task___init___impl, _asyncio_Task__coro_get_impl, _asyncio_Task__fut_waiter_get_impl, _asyncio_Task__log_destroy_pending_get_impl, _asyncio_Task__log_destroy_pending_set_impl, _asyncio_Task__make_cancelled_error_impl, _asyncio_Task__must_cancel_get_impl, _asyncio_Task_cancel_impl, _asyncio_Task_cancelling_impl, _asyncio_Task_get_context_impl, _asyncio_Task_get_coro_impl, _asyncio_Task_get_name_impl, _asyncio_Task_get_stack_impl, _asyncio_Task_print_stack_impl, _asyncio_Task_set_exception_impl, _asyncio_Task_set_name_impl, _asyncio_Task_set_result_impl, _asyncio_Task_uncancel_impl, _asyncio__enter_task_impl, _asyncio__get_running_loop_impl, _asyncio__leave_task_impl, _asyncio__register_eager_task_impl, _asyncio__register_task_impl, _asyncio__set_running_loop_impl, _asyncio__swap_current_task_impl, _asyncio__unregister_eager_task_impl, _asyncio__unregister_task_impl, _asyncio_all_tasks_impl, _asyncio_current_task_impl, _asyncio_future_add_to_awaited_by_impl, _asyncio_future_discard_from_awaited_by_impl, _asyncio_get_event_loop_impl, _asyncio_get_running_loop_impl }
    modules.asyncio_core --> bindings.asyncio { AsyncioState, FUTURE_ITER_SIZE, FUTURE_OBJECT_SIZE, STATE_ASYNCIO_MOD, STATE_CANCELLED_ERROR, STATE_CONTEXT_KWNAME, STATE_COUNT, STATE_FUTURE_ITER_TYPE, STATE_FUTURE_REPR_FUNC, STATE_FUTURE_TYPE, STATE_GET_EVENT_LOOP_POLICY, STATE_INVALID_STATE_ERROR, STATE_ISCOROUTINE_FUNC, STATE_ISCOROUTINE_TYPECACHE, STATE_NON_ASYNCIO_EAGER_TASKS, STATE_NON_ASYNCIO_TASKS, STATE_TASK_GET_STACK_FUNC, STATE_TASK_PRINT_STACK_FUNC, STATE_TASK_REPR_FUNC, STATE_TASK_STEP_WRAPPER_TYPE, STATE_TASK_TYPE, STATE_TRACEBACK_EXTRACT_STACK, TASK_OBJECT_SIZE, TASK_STEP_WRAPPER_SIZE, asyncio_module_token, ids, intern_identifiers, release, running_loop_slot, running_task_slot }
    modules.asyncio_core --> modules.asyncio { BIT_BLOCKING, BIT_LOG_DESTROY_PENDING, BIT_LOG_TB, BIT_MUST_CANCEL, FutureIterObject, STATE_CANCELLED, STATE_CANCELLED_ERROR, STATE_CONTEXT_KWNAME, STATE_FINISHED, STATE_FUTURE_ITER_TYPE, STATE_FUTURE_REPR_FUNC, STATE_INVALID_STATE_ERROR, STATE_NON_ASYNCIO_EAGER_TASKS, STATE_NON_ASYNCIO_TASKS, STATE_PENDING, STATE_TASK_GET_STACK_FUNC, STATE_TASK_PRINT_STACK_FUNC, STATE_TASK_REPR_FUNC, STATE_TASK_STEP_WRAPPER_TYPE, TASK_NODE_OFFSET, TaskStepMethWrapper, call_soon, create_cancelled_error, enter_task, exception_class_check, exception_instance_check, fut_of, future_add_done_callback, future_awaited_by_add, future_awaited_by_discard, future_cancel, future_check_exact, future_ensure_alive, future_get_result, future_init, future_is_alive, future_set_cancelled_error, future_set_exception, future_set_result, get_event_loop, get_future_loop, has_bit, ids, is_coroutine, leave_task, module_of, module_of_type, native_state, register_task, release, running_loop, running_loop_slot, running_task_slot, set_bit, state_ref, swap_current_task, task_check, task_check_exact, task_of, task_or_future_check, unregister_task }
    modules.asyncio_core --> modules.asyncio.call_with_context { CallStack }
    modules.asyncio_core --> modules.asyncio.future_clear { clear_future_fields }
    modules.binascii --> bindings.clinic.binascii { binascii_a2b_base64_impl, binascii_a2b_hex_impl, binascii_a2b_qp_impl, binascii_a2b_uu_impl, binascii_b2a_base64_impl, binascii_b2a_hex_impl, binascii_b2a_qp_impl, binascii_b2a_uu_impl, binascii_crc32_impl, binascii_crc_hqx_impl, binascii_hexlify_impl, binascii_unhexlify_impl, convert_ascii_buffer_converter }
    modules.bisect --> bindings.clinic.bisect { _bisect_bisect_left_impl, _bisect_bisect_right_impl, _bisect_insort_left_impl, _bisect_insort_right_impl }
    modules.bz2 --> bindings.clinic.bz2 { BZ2Compressor_token, BZ2Decompressor_token }
    modules.cjkcodecs --> modules.cjkcodecs_mappings_cn { DbcsMap, Gb18030Range }
    modules.cjkcodecs --> modules.cjkcodecs_mappings_hk { DbcsMap }
    modules.cjkcodecs --> modules.cjkcodecs_mappings_jp { DbcsMap, PairEncodeMap }
    modules.cjkcodecs --> modules.cjkcodecs_mappings_kr { DbcsMap }
    modules.cjkcodecs --> modules.cjkcodecs_mappings_tw { DbcsMap }
    modules.cjkcodecs --> modules.codecs_cn { DecodeWriter, Gb18030Range, MBERR_EXCEPTION, MBERR_TOOFEW, MBERR_TOOSMALL, MultibyteCodec, MultibyteCodec_State, NOCHAR, UNIINV, getcodec, inbyte, inchar, map_decode, map_encode, next_in, next_inchar, next_out, no_codec_init, no_decode_reset, no_encode_reset, no_state_init, outbyte, outchar, register_maps, set_state_byte, state_byte }
    modules.cjkcodecs --> modules.codecs_hk { DbcsMap, DecodeWriter, MBENC_FLUSH, MBERR_EXCEPTION, MBERR_INTERNAL, MBERR_TOOFEW, MBERR_TOOSMALL, MULTIC, MultibyteCodec, MultibyteCodec_State, NOCHAR, UNIINV, getcodec, importmap, inbyte, inchar, map_decode, map_encode, next_in, next_inchar, next_out, no_decode_reset, no_encode_reset, no_state_init, outbyte, outchar, outchar2, register_maps }
    modules.cjkcodecs --> modules.codecs_iso2022 { DBCINV, DbcsMap, DecodeWriter, MBENC_FLUSH, MBERR_EXCEPTION, MBERR_INTERNAL, MBERR_TOOFEW, MBERR_TOOSMALL, MULTIC, MultibyteCodec, MultibyteCodec_State, NOCHAR, PairEncodeMap, UNIINV, find_pairencmap, getcodec, importmap, inbyte, inchar, map_decode, map_decode_wide, map_encode, next_in, next_inchar, next_out, no_codec_init, outbyte, outchar, outchar2, set_state_byte, state_byte }
    modules.cjkcodecs --> modules.codecs_jp { DBCINV, DecodeWriter, MBENC_FLUSH, MBERR_EXCEPTION, MBERR_TOOFEW, MBERR_TOOSMALL, MULTIC, MultibyteCodec, MultibyteCodec_State, NOCHAR, UNIINV, find_pairencmap, getcodec, inbyte, inchar, map_decode, map_decode_wide, map_encode, next_in, next_inchar, next_out, no_codec_init, no_decode_reset, no_encode_reset, no_state_init, outbyte, outchar, outchar2, register_maps }
    modules.cjkcodecs --> modules.codecs_kr { DecodeWriter, MBERR_EXCEPTION, MBERR_TOOFEW, MBERR_TOOSMALL, MultibyteCodec, MultibyteCodec_State, NOCHAR, UNIINV, getcodec, inbyte, inchar, map_decode, map_encode, next_in, next_inchar, next_out, no_codec_init, no_decode_reset, no_encode_reset, no_state_init, outbyte, outchar, register_maps }
    modules.cjkcodecs --> modules.codecs_tw { DecodeWriter, MBERR_EXCEPTION, MBERR_TOOFEW, MBERR_TOOSMALL, MultibyteCodec, MultibyteCodec_State, NOCHAR, UNIINV, getcodec, inbyte, inchar, map_decode, map_encode, next_in, next_inchar, next_out, no_codec_init, no_decode_reset, no_encode_reset, no_state_init, outbyte, outchar, register_maps }
    modules.cjkcodecs --> modules.multibytecodec { CodecCapsule, DecodeWriter, MBENC_FLUSH, MBENC_MAX, MBERR_EXCEPTION, MBERR_INTERNAL, MBERR_TOOFEW, MBERR_TOOSMALL, MultibyteCodec, MultibyteCodec_State }
    modules.cjkcodecs_jis --> modules.codecs_iso2022 { emulate_2000_decode_plane1, emulate_2000_decode_plane2, emulate_2000_encode_bmp, emulate_2000_encode_emp, jisx0201_k_decode, jisx0201_k_encode, jisx0201_r_decode, jisx0201_r_encode }
    modules.cjkcodecs_jis --> modules.codecs_jp { EMPBASE, EMULATE_JISX0213_2000_DECODE_INVALID, EMULATE_JISX0213_2000_ENCODE_INVALID, emulate_2000_decode_plane1, emulate_2000_decode_plane2, emulate_2000_encode_bmp, emulate_2000_encode_emp, jisx0201_k_decode, jisx0201_k_encode, jisx0201_r_decode, jisx0201_r_encode }
    modules.cjkcodecs_mappings_cn --> modules.codecs_cn { CJK_CN_MAPPINGS, cjk_cn_mappings, cjk_gb18030_to_unibmp_ranges, cjk_gb18030ext_map, cjk_gb2312_map, cjk_gbcommon_map, cjk_gbkext_map }
    modules.cjkcodecs_mappings_hk --> modules.codecs_hk { CJK_HK_MAPPINGS, cjk_big5hkscs_bmp_map, cjk_big5hkscs_map, cjk_big5hkscs_nonbmp_map, cjk_big5hkscs_phint_0, cjk_big5hkscs_phint_12130, cjk_big5hkscs_phint_21924, cjk_hk_mappings }
    modules.cjkcodecs_mappings_jp --> modules.codecs_iso2022 { JISX0213_ENCPAIRS }
    modules.cjkcodecs_mappings_jp --> modules.codecs_jp { CJK_JP_MAPPINGS, JISX0213_ENCPAIRS, cjk_cp932ext_map, cjk_jisx0208_map, cjk_jisx0212_map, cjk_jisx0213_1_bmp_map, cjk_jisx0213_1_emp_map, cjk_jisx0213_2_bmp_map, cjk_jisx0213_2_emp_map, cjk_jisx0213_bmp_map, cjk_jisx0213_emp_map, cjk_jisx0213_pair_encmap, cjk_jisx0213_pair_map, cjk_jisxcommon_map, cjk_jp_mappings }
    modules.cjkcodecs_mappings_kr --> modules.codecs_kr { CJK_KR_MAPPINGS, cjk_cp949_map, cjk_cp949ext_map, cjk_kr_mappings, cjk_ksx1001_map }
    modules.cjkcodecs_mappings_tw --> modules.codecs_tw { CJK_TW_MAPPINGS, cjk_big5_map, cjk_cp950ext_map, cjk_tw_mappings }
    modules.cmath --> bindings.clinic.cmath { cmath_acos_impl, cmath_acosh_impl, cmath_asin_impl, cmath_asinh_impl, cmath_atan_impl, cmath_atanh_impl, cmath_cos_impl, cmath_cosh_impl, cmath_exp_impl, cmath_isclose_impl, cmath_isfinite_impl, cmath_isinf_impl, cmath_isnan_impl, cmath_log10_impl, cmath_log_impl, cmath_phase_impl, cmath_polar_impl, cmath_rect_impl, cmath_sin_impl, cmath_sinh_impl, cmath_sqrt_impl, cmath_tan_impl, cmath_tanh_impl, convert_Py_complex, convert_Py_complex_protected, return_Py_complex_protected }
    modules.codecs --> bindings.clinic.codecs { _codecs__unregister_error_impl, _codecs_ascii_decode_impl, _codecs_ascii_encode_impl, _codecs_charmap_build_impl, _codecs_charmap_decode_impl, _codecs_charmap_encode_impl, _codecs_decode_impl, _codecs_encode_impl, _codecs_escape_decode_impl, _codecs_escape_encode_impl, _codecs_latin_1_decode_impl, _codecs_latin_1_encode_impl, _codecs_lookup_error_impl, _codecs_lookup_impl, _codecs_raw_unicode_escape_decode_impl, _codecs_raw_unicode_escape_encode_impl, _codecs_readbuffer_encode_impl, _codecs_register_error_impl, _codecs_register_impl, _codecs_unicode_escape_decode_impl, _codecs_unicode_escape_encode_impl, _codecs_unregister_impl, _codecs_utf_16_be_decode_impl, _codecs_utf_16_be_encode_impl, _codecs_utf_16_decode_impl, _codecs_utf_16_encode_impl, _codecs_utf_16_ex_decode_impl, _codecs_utf_16_le_decode_impl, _codecs_utf_16_le_encode_impl, _codecs_utf_32_be_decode_impl, _codecs_utf_32_be_encode_impl, _codecs_utf_32_decode_impl, _codecs_utf_32_encode_impl, _codecs_utf_32_ex_decode_impl, _codecs_utf_32_le_decode_impl, _codecs_utf_32_le_encode_impl, _codecs_utf_7_decode_impl, _codecs_utf_7_encode_impl, _codecs_utf_8_decode_impl, _codecs_utf_8_encode_impl }
    modules.codecs_cn --> bindings.codecs_cn { codecs_cn_exec, codecs_cn_getcodec }
    modules.codecs_hk --> bindings.codecs_hk { codecs_hk_exec, codecs_hk_getcodec }
    modules.codecs_iso2022 --> bindings.codecs_iso2022 { codecs_iso2022_exec, codecs_iso2022_getcodec }
    modules.codecs_jp --> bindings.codecs_jp { codecs_jp_exec, codecs_jp_getcodec }
    modules.codecs_kr --> bindings.codecs_kr { codecs_kr_exec, codecs_kr_getcodec }
    modules.codecs_tw --> bindings.codecs_tw { codecs_tw_exec, codecs_tw_getcodec }
    modules.collections --> bindings.clinic.collections { _collections__count_elements_impl, _tuplegetter_token, deque___copy___impl, deque___reduce___impl, deque___reversed___impl, deque___sizeof___impl, deque_append_impl, deque_appendleft_impl, deque_clearmethod_impl, deque_copy_impl, deque_count_impl, deque_extend_impl, deque_extendleft_impl, deque_index_impl, deque_init_impl, deque_insert_impl, deque_pop_impl, deque_popleft_impl, deque_remove_impl, deque_reverse_impl, deque_rotate_impl, tuplegetter_new_impl }
    modules.collections --> bindings.collections { DequeIteratorState, DequeState, TupleGetterState, _tuplegetter_token, allocate, collections_module_token, defdict_token, deque_copy_impl, deque_token, deque_value, dequeiter_token, dequereviter_token, iterator_create, module_for, search }
    modules.combinatorics --> modules.itertools { combinatorial_state, jacpy_combinatorial_clear, jacpy_combinatorial_field, jacpy_combinatorial_init, jacpy_combinatorial_memory, jacpy_combinatorial_new, jacpy_combinatorial_next }
    modules.csv --> bindings.clinic.csv { _csv_field_size_limit_impl, _csv_get_dialect_impl, _csv_list_dialects_impl, _csv_unregister_dialect_impl }
    modules.datetime --> bindings.clinic.datetime { datetime_date_fromtimestamp_impl, datetime_date_replace_impl, datetime_datetime_now_impl, datetime_datetime_replace_impl, datetime_time_replace_impl, iso_calendar_date_new_impl }
    modules.datetime --> bindings.datetime { capi_date_from_date, capi_datetime_from_date_and_time, capi_datetime_from_date_and_time_and_fold, capi_delta_from_delta, capi_time_from_time, capi_time_from_time_and_fold, datetime_date_fromtimestamp_capi, datetime_date_replace_impl, datetime_datetime_replace_impl, datetime_time_replace_impl }
    modules.datetime_calendar --> bindings.datetime { MAXYEAR, MAX_DELTA_DAYS, MINYEAR }
    modules.datetime_calendar --> modules.datetime_date { DateTimeFields, MAXYEAR, MINYEAR, YearMonthDay, iso_to_ymd, iso_week1_monday, ord_to_ymd, parse_isoformat_date, weekday, ymd_to_ord }
    modules.datetime_calendar --> modules.datetime_datetime { IsoTime, MAXYEAR, MINYEAR, YearMonthDay, days_in_month, find_isoformat_datetime_separator, parse_isoformat_date, parse_isoformat_time, ymd_to_ord }
    modules.datetime_calendar --> modules.datetime_format { days_before_month, weekday }
    modules.datetime_calendar --> modules.datetime_objects { DateTimeFields, MAXYEAR, MAX_DELTA_DAYS, MINYEAR, days_in_month, normalize_d_s_us, normalize_datetime, normalize_y_m_d }
    modules.datetime_calendar --> modules.datetime_time { IsoTime, parse_isoformat_time }
    modules.datetime_date --> bindings.datetime { PyDateTime_DateType, date_ctime, date_format, date_fromisocalendar, date_fromisoformat, date_fromordinal, date_isocalendar, date_isoformat, date_isoweekday, date_reduce, date_strftime, date_strptime, date_timetuple, date_today, date_toordinal, date_weekday, iso_calendar_date_dealloc, iso_calendar_date_reduce, iso_calendar_date_repr, iso_calendar_date_traverse, iso_calendar_date_week, iso_calendar_date_weekday, iso_calendar_date_year }
    modules.datetime_date --> modules.datetime { date_fromtimestamp, new_iso_calendar_date }
    modules.datetime_date --> modules.datetime_datetime { PyDateTime_DateType, compare_data, generic_hash, month_is_sane, strptime_via }
    modules.datetime_date --> modules.datetime_time { compare_data, generic_hash, strptime_via }
    modules.datetime_datetime --> bindings.datetime { PyDateTime_DateTimeType, datetime_astimezone, datetime_combine, datetime_ctime, datetime_fromisoformat, datetime_fromtimestamp, datetime_getdate, datetime_gettime, datetime_gettimetz, datetime_isoformat, datetime_reduce, datetime_reduce_ex, datetime_strptime, datetime_timestamp, datetime_timetuple, datetime_tzname, datetime_utcfromtimestamp, datetime_utcnow, datetime_utctimetuple }
    modules.datetime_datetime --> modules.datetime { datetime_now }
    modules.datetime_delta --> bindings.datetime { PyDateTime_DeltaType, delta_reduce, delta_total_seconds }
    modules.datetime_delta --> modules.datetime_datetime { delta_total_seconds }
    modules.datetime_delta --> modules.datetime_tzinfo { delta_hash, delta_richcompare, zero_delta }
    modules.datetime_format --> modules.datetime_date { build_struct_time, format_ctime, time_time, wrap_strftime }
    modules.datetime_format --> modules.datetime_datetime { build_struct_time, format_ctime, format_utcoffset }
    modules.datetime_format --> modules.datetime_time { format_utcoffset, wrap_strftime }
    modules.datetime_objects --> bindings.datetime { STATE_COUNT, STATE_EPOCH, STATE_ISOCALENDAR_DATE_TYPE, STATE_SECONDS_PER_DAY, STATE_US_PER_DAY, STATE_US_PER_HOUR, STATE_US_PER_MINUTE, STATE_US_PER_MS, STATE_US_PER_SECOND, STATE_US_PER_WEEK, clear_current_module, create_timezone, date_get_fold, date_get_hour, date_get_microsecond, date_get_minute, date_get_second, datetime_dst, datetime_tzinfo_of, datetime_utcoffset, get_current_module, get_day, get_month, get_year, new_date, new_datetime, new_delta, new_time, new_timezone, set_current_module, time_get_fold, time_get_hour, time_get_microsecond, time_get_minute, time_get_second, time_tzinfo_of, utc, utc_timezone }
    modules.datetime_objects --> modules.datetime { STATE_ISOCALENDAR_DATE_TYPE, new_date_ex, new_date_subclass_ex, new_datetime_ex, new_datetime_ex2, new_datetime_subclass_fold_ex, new_delta_ex, new_time_ex, new_time_ex2, new_time_subclass_fold_ex, type_of }
    modules.datetime_objects --> modules.datetime_date { STATE_ISOCALENDAR_DATE_TYPE, data_address, data_bytes, date_check, datetime_check, delta_check, diff_to_bool, get_current_state, get_day, get_month, get_year, new_date_ex, new_date_subclass_ex, new_delta, normalize_date, not_implemented, state_value, td_days, type_alloc, type_name_of, type_of }
    modules.datetime_objects --> modules.datetime_datetime { Py_EQ, Py_NE, STATE_EPOCH, add_datetime_timedelta, append_keyword_fold, append_keyword_tzinfo, call_dst, call_tzname, call_utcoffset, check_tzinfo_subclass, data_address, data_bytes, date_get_fold, date_get_hour, date_get_microsecond, date_get_minute, date_get_second, date_type, datetime_check, datetime_dst, datetime_tzinfo_of, datetime_utcoffset, delta_bool, delta_check, delta_cmp, delta_subtract, diff_to_bool, divide_timedelta_timedelta, get_current_state, get_day, get_month, get_year, has_tzinfo, new_date, new_datetime, new_datetime_ex2, new_datetime_subclass_ex, new_datetime_subclass_fold_ex, new_delta, new_time, new_timezone, not_implemented, state_value, td_days, td_microseconds, td_seconds, time_get_fold, time_get_hour, time_get_microsecond, time_get_minute, time_get_second, time_type, time_tzinfo_of, type_alloc, type_free, type_name_of, type_object, type_of, tzinfo_from_isoformat_results, utc }
    modules.datetime_objects --> modules.datetime_delta { STATE_SECONDS_PER_DAY, STATE_US_PER_DAY, STATE_US_PER_HOUR, STATE_US_PER_MINUTE, STATE_US_PER_MS, STATE_US_PER_SECOND, STATE_US_PER_WEEK, checked_divmod, delta_bool, delta_check, delta_cmp, delta_negative, delta_subtract, delta_to_microseconds, diff_to_bool, divide_timedelta_timedelta, get_current_state, microseconds_to_delta, microseconds_to_delta_ex, new_delta, not_implemented, state_value, td_days, td_microseconds, td_seconds, type_name_of, type_of }
    modules.datetime_objects --> modules.datetime_format { call_tzname, call_utcoffset, date_get_microsecond, datetime_check, delta_negative, get_day, get_month, get_tzinfo_member, get_year, td_days, td_microseconds, td_seconds, time_check, time_get_microsecond }
    modules.datetime_objects --> modules.datetime_time { Py_EQ, Py_NE, append_keyword_fold, append_keyword_tzinfo, call_dst, call_tzname, call_utcoffset, check_tzinfo_subclass, data_address, data_bytes, delta_check, delta_cmp, delta_subtract, diff_to_bool, has_tzinfo, new_delta, new_time, new_time_ex2, not_implemented, td_days, td_seconds, time_check, time_get_fold, time_get_hour, time_get_microsecond, time_get_minute, time_get_second, time_type, time_tzinfo_of, type_alloc, type_free, type_name_of, type_object, type_of, tzinfo_from_isoformat_results }
    modules.datetime_objects --> modules.datetime_tzinfo { PyDateTime_TimeZone, Py_EQ, Py_NE, add_datetime_timedelta, call_dst, datetime_check, datetime_dst, datetime_tzinfo_of, datetime_utcoffset, delta_bool, delta_negative, delta_subtract, delta_type, has_tzinfo, new_timezone, not_implemented, td_days, td_microseconds, td_seconds, timezone_check, type_free, type_name_of, type_object, type_of, utc }
    modules.datetime_time --> bindings.datetime { PyDateTime_TimeType, time_dst, time_fromisoformat, time_isoformat, time_reduce, time_reduce_ex, time_strftime, time_strptime, time_tzname, time_utcoffset }
    modules.datetime_time --> modules.datetime_datetime { append_utcoffset, timespec_index }
    modules.datetime_tzinfo --> bindings.datetime { PyDateTime_TZInfoType, PyDateTime_TimeZoneType, timezone_dst, timezone_fromutc, timezone_getinitargs, timezone_tzname, timezone_utcoffset, tzinfo_dst, tzinfo_fromutc, tzinfo_reduce, tzinfo_tzname, tzinfo_utcoffset }
    modules.decimal_context --> bindings.decimal { context_clear, context_clear_flags, context_clear_traps, context_dealloc, context_getattr, context_getcapitals, context_getclamp, context_getemax, context_getemin, context_getetiny, context_getetop, context_getprec, context_getround, context_init, context_new, context_reduce, context_repr, context_setattr, context_setcapitals, context_setclamp, context_setemax, context_setemin, context_setprec, context_setround, context_traverse, ctx_apply, ctx_binary, ctx_bool, ctx_canonical, ctx_copy_decimal, ctx_create_decimal, ctx_from_float, ctx_iscanonical, ctx_mpd_class, ctx_mpd_qcopy_abs, ctx_mpd_qcopy_negate, ctx_mpd_qcopy_sign, ctx_mpd_qdivmod, ctx_mpd_qfma, ctx_mpd_qpow, ctx_mpd_radix, ctx_mpd_same_quantum, ctx_mpd_to_eng, ctx_mpd_to_sci, ctx_total, ctx_unary, ctxmanager_clear, ctxmanager_dealloc, ctxmanager_new, ctxmanager_restore_global, ctxmanager_set_local, ctxmanager_traverse, dec_getcontext, dec_setcontext, ieee_context, init_basic_context, init_extended_context, signaldict_copy, signaldict_dealloc, signaldict_getitem, signaldict_init, signaldict_iter, signaldict_len, signaldict_repr, signaldict_richcompare, signaldict_setitem, signaldict_traverse }
    modules.decimal_convert --> modules.decimal_context { convert_op, dec_apply, dec_from_object, dec_type_from_float }
    modules.decimal_convert --> modules.decimal_number { convert_op, convert_op_cmp, dec_settriple, dec_type_from_float_exact, dec_type_from_number_exact, dec_type_from_object_exact, failed_operand }
    modules.decimal_number --> bindings.decimal { dec_as_float, dec_as_integer_ratio, dec_as_tuple, dec_binary_va, dec_bool, dec_bool_va, dec_canonical, dec_ceil, dec_complex, dec_conjugate, dec_copy, dec_dealloc, dec_floor, dec_format, dec_from_float, dec_from_number, dec_hash, dec_imag, dec_mpd_adjexp, dec_mpd_class, dec_mpd_qcopy_abs, dec_mpd_qcopy_negate, dec_mpd_qcopy_sign, dec_mpd_qfma, dec_mpd_qquantize, dec_mpd_radix, dec_mpd_same_quantum, dec_mpd_to_eng, dec_new, dec_real, dec_reduce, dec_repr, dec_richcompare, dec_round, dec_sizeof, dec_str, dec_to_integral_exact, dec_to_integral_value, dec_total_va, dec_traverse, dec_trunc, dec_unary_va, nm_dec_as_long, nm_mpd_qabs, nm_mpd_qadd, nm_mpd_qdiv, nm_mpd_qdivint, nm_mpd_qdivmod, nm_mpd_qminus, nm_mpd_qmul, nm_mpd_qplus, nm_mpd_qpow, nm_mpd_qrem, nm_mpd_qsub, nm_nonzero }
    modules.decimal_number --> modules.decimal_context { dec_mpd_radix_of, divmod_operands, parse_keywords, parse_tuple, power_operands, unicode_fromascii }
    modules.decimal_objects --> bindings.decimal { CONDITION_FLAGS, CONDITION_NAMES, CONTEXT_MANAGER_OBJECT_SIZE, CONTEXT_OBJECT_SIZE, DEC_OBJECT_SIZE, INEXACT, MPD_Float_operation, PY_DEC_MINALLOC, PY_DEC_ROUND_GUARD, PyFloat_Type, PyLong_Type, PyType_Type, ROUNDED, SIGNAL_DICT_OBJECT_SIZE, SIGNAL_FLAGS, SIGNAL_MAP_LEN, SIGNAL_NAMES, STATE_BASIC_CONTEXT_TEMPLATE, STATE_CONDITION_EXCEPTIONS, STATE_CONTEXT_MANAGER_TYPE, STATE_CONTEXT_TYPE, STATE_COUNT, STATE_CURRENT_CONTEXT_VAR, STATE_DECIMAL_EXCEPTION, STATE_DECIMAL_TUPLE, STATE_DEC_TYPE, STATE_DEFAULT_CONTEXT_TEMPLATE, STATE_EXTENDED_CONTEXT_TEMPLATE, STATE_RATIONAL, STATE_ROUND_MAP, STATE_SIGNAL_DICT_MIXIN_TYPE, STATE_SIGNAL_DICT_TYPE, STATE_SIGNAL_EXCEPTIONS, STATE_SIGNAL_TUPLE, SUBNORMAL, builtin_methods, context_copy, decimal_module_token, hash_context, max_context, signal_exception }
    modules.decimal_objects --> modules.decimal_context { CONTEXT_STATUS_OFFSET, CONTEXT_TRAPS_OFFSET, DEC_ERRORS, INVALID_SIGNALDICT_ERROR_MSG, PyDecContextManagerObject, PyDecContextObject, PyDecSignalDictObject, Py_EQ_OP, Py_NE_OP, SIGNAL_FLAGS, SIGNAL_MAP_LEN, SIGNAL_NAMES, STATE_CONTEXT_MANAGER_TYPE, STATE_DEFAULT_CONTEXT_TEMPLATE, STATE_ROUND_MAP, STATE_SIGNAL_DICT_TYPE, STATE_SIGNAL_TUPLE, bool_object, context_check, context_copy, context_record, context_type, copy_mpd_context, ctx_caps, ctx_of, current_context, current_context_borrowed, dec_addstatus, dec_alloc, dec_check, dec_type, dict_as_flags, exception_as_flag, flags_as_dict, getround, internal_error_int, internal_error_ptr, list_as_flags, module_of_context, module_of_type, mpd, set_current_context, signal_dict_check, signal_dict_flags, signals_as_list, state_value, value_error_int, value_error_ptr }
    modules.decimal_objects --> modules.decimal_convert { MPD_Float_operation, PyComplex_Type, PyFloat_Type, Py_EQ_OP, Py_NE_OP, STATE_RATIONAL, builtin_methods, context_or_current, ctx_of, current_context_borrowed, dec_addstatus, dec_alloc, dec_check, dec_check_exact, dec_type, dec_type_new, max_context, module_of_context, module_of_type, mpd, state_value, type_check }
    modules.decimal_objects --> modules.decimal_number { PyDecObject, PyFloat_Type, PyLong_Type, Py_EQ_OP, Py_GE_OP, Py_GT_OP, Py_LE_OP, Py_LT_OP, Py_NE_OP, STATE_DECIMAL_TUPLE, STATE_PYDECIMAL, bool_object, context_or_current, ctx_caps, ctx_of, current_context_borrowed, dec_addstatus, dec_alloc, dec_type, free_work_context, getround, hash_context, internal_error_ptr, max_context, module_of, module_of_left_or_right, module_of_ternary, module_of_type, mpd, state_value, work_context }
    modules.decimal_ops --> bindings.decimal { OP_ABS, OP_ADD, OP_AND, OP_COMPARE, OP_COMPARE_SIGNAL, OP_COMPARE_TOTAL, OP_COMPARE_TOTAL_MAG, OP_DIV, OP_DIVINT, OP_EXP, OP_INVERT, OP_IS_CANONICAL, OP_IS_FINITE, OP_IS_INFINITE, OP_IS_NAN, OP_IS_NORMAL, OP_IS_QNAN, OP_IS_SIGNED, OP_IS_SNAN, OP_IS_SUBNORMAL, OP_IS_ZERO, OP_LN, OP_LOG10, OP_LOGB, OP_MAX, OP_MAX_MAG, OP_MIN, OP_MINUS, OP_MIN_MAG, OP_MUL, OP_NEXT_MINUS, OP_NEXT_PLUS, OP_NEXT_TOWARD, OP_OR, OP_PLUS, OP_QUANTIZE, OP_REDUCE, OP_REM, OP_REM_NEAR, OP_ROTATE, OP_ROUND_TO_INT, OP_ROUND_TO_INTX, OP_SCALEB, OP_SHIFT, OP_SQRT, OP_SUB, OP_XOR }
    modules.decimal_ops --> modules.decimal_context { binary_op, bool_op, fma_op, total_op, unary_op }
    modules.decimal_ops --> modules.decimal_number { OP_ABS, OP_ADD, OP_DIV, OP_DIVINT, OP_MINUS, OP_MUL, OP_PLUS, OP_REM, OP_SUB, binary_op, bool_op, fma_op, total_op, unary_op }
    modules.elementtree --> bindings.clinic.elementtree { Element_token, _elementtree_Element___copy___impl, _elementtree_Element___deepcopy___impl, _elementtree_Element___getstate___impl, _elementtree_Element___setstate___impl, _elementtree_Element___sizeof___impl, _elementtree_Element_append_impl, _elementtree_Element_clear_impl, _elementtree_Element_extend_impl, _elementtree_Element_find_impl, _elementtree_Element_findall_impl, _elementtree_Element_findtext_impl, _elementtree_Element_get_impl, _elementtree_Element_insert_impl, _elementtree_Element_items_impl, _elementtree_Element_iter_impl, _elementtree_Element_iterfind_impl, _elementtree_Element_itertext_impl, _elementtree_Element_keys_impl, _elementtree_Element_makeelement_impl, _elementtree_Element_remove_impl, _elementtree_Element_set_impl, _elementtree_TreeBuilder___init___impl, _elementtree_TreeBuilder_close_impl, _elementtree_TreeBuilder_comment_impl, _elementtree_TreeBuilder_data_impl, _elementtree_TreeBuilder_end_impl, _elementtree_TreeBuilder_pi_impl, _elementtree_TreeBuilder_start_impl, _elementtree_XMLParser___init___impl, _elementtree_XMLParser__parse_whole_impl, _elementtree_XMLParser__setevents_impl, _elementtree_XMLParser_close_impl, _elementtree_XMLParser_feed_impl, _elementtree_XMLParser_flush_impl, _elementtree__set_factories_impl, subclass_clinic_state_Element_Type }
    modules.elementtree --> bindings.elementtree { ELEMENT_ITER_RECORD_SIZE, ELEMENT_RECORD_SIZE, ELEMENT_TYPE_NAME, ElementIter_token, ElementTreeState, Element_token, TREEBUILDER_RECORD_SIZE, TreeBuilder_token, XMLPARSER_MEMBERS, XMLPARSER_RECORD_SIZE, XMLParser_token, element_ass_subscr, element_attrib_getter, element_attrib_setter, element_bool, element_dealloc, element_gc_clear, element_gc_traverse, element_getitem, element_init, element_length, element_new, element_repr, element_setitem, element_subscr, element_tag_getter, element_tag_setter, element_tail_getter, element_tail_setter, element_text_getter, element_text_setter, elementiter_dealloc, elementiter_next, elementiter_self, elementiter_traverse, import_expat_capi, module_definition, subelement, treebuilder_dealloc, treebuilder_gc_clear, treebuilder_gc_traverse, treebuilder_new, xmlparser_dealloc, xmlparser_gc_clear, xmlparser_gc_traverse, xmlparser_new, xmlparser_version_getter }
    modules.errno_constants --> modules.locale { ERANGE }
    modules.errno_constants --> modules.multiprocessing { EAGAIN, EINTR, ETIMEDOUT }
    modules.errno_constants --> modules.posixshmem { EINTR }
    modules.errno_constants --> modules.select { EINTR, EINVAL, ENOENT }
    modules.errno_constants --> modules.socket { EAFNOSUPPORT, ECONNRESET, EINVAL, ENODEV, ENXIO }
    modules.errno_constants --> modules.socket_core { EAGAIN, EINTR, EWOULDBLOCK }
    modules.errno_constants --> modules.socket_object { EBADF, ECONNRESET, EINPROGRESS, EINTR, EINVAL, EISCONN, ENOSYS, ENOTSOCK }
    modules.errno_constants --> modules.time { EINTR }
    modules.errno_constants --> object_model.complex { EDOM, ERANGE }
    modules.errno_constants --> object_model.file { EAGAIN, ENXIO }
    modules.expat --> bindings.pyexpat { XML_PARAM_ENTITY_PARSING_ALWAYS, XML_PARAM_ENTITY_PARSING_NEVER, XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE }
    modules.expat --> modules.elementtree { PyExpat_CAPI, XML_ERROR_UNDEFINED_ENTITY, XML_FALSE, XML_TRUE, expat_memory_suite, expat_version }
    modules.expat --> modules.pyexpat { PYEXPAT_CAPI_MAGIC, PYEXPAT_CAPI_SIZE, PYEXPAT_CAPSULE_NAME, PyExpat_CAPI, XML_Content, XML_ERROR_INVALID_ARGUMENT, XML_ERROR_NONE, XML_ErrorString, XML_ExpatVersion, XML_ExternalEntityParserCreate, XML_FALSE, XML_FEATURE_END, XML_FreeContentModel, XML_GetBase, XML_GetBuffer, XML_GetCurrentByteIndex, XML_GetCurrentColumnNumber, XML_GetCurrentLineNumber, XML_GetErrorCode, XML_GetFeatureList, XML_GetInputContext, XML_GetSpecifiedAttributeCount, XML_Memory_Handling_Suite, XML_Parse, XML_ParseBuffer, XML_ParserCreate_MM, XML_ParserFree, XML_STATUS_ERROR, XML_STATUS_OK, XML_SetAllocTrackerActivationThreshold, XML_SetAllocTrackerMaximumAmplification, XML_SetAttlistDeclHandler, XML_SetBase, XML_SetBillionLaughsAttackProtectionActivationThreshold, XML_SetBillionLaughsAttackProtectionMaximumAmplification, XML_SetCharacterDataHandler, XML_SetCommentHandler, XML_SetDefaultHandler, XML_SetDefaultHandlerExpand, XML_SetElementDeclHandler, XML_SetElementHandler, XML_SetEncoding, XML_SetEndCdataSectionHandler, XML_SetEndDoctypeDeclHandler, XML_SetEndElementHandler, XML_SetEndNamespaceDeclHandler, XML_SetEntityDeclHandler, XML_SetExternalEntityRefHandler, XML_SetHashSalt, XML_SetNamespaceDeclHandler, XML_SetNotStandaloneHandler, XML_SetNotationDeclHandler, XML_SetParamEntityParsing, XML_SetProcessingInstructionHandler, XML_SetReparseDeferralEnabled, XML_SetReturnNSTriplet, XML_SetSkippedEntityHandler, XML_SetStartCdataSectionHandler, XML_SetStartDoctypeDeclHandler, XML_SetStartElementHandler, XML_SetStartNamespaceDeclHandler, XML_SetUnknownEncodingHandler, XML_SetUnparsedEntityDeclHandler, XML_SetUserData, XML_SetXmlDeclHandler, XML_StopParser, XML_TRUE, XML_UseForeignDTD, expat_memory_suite, expat_version }
    modules.fcntl --> bindings.clinic.fcntl { fcntl_fcntl_impl, fcntl_flock_impl, fcntl_ioctl_impl, fcntl_lockf_impl }
    modules.fcntl_constants --> bindings.fcntl { CONSTANTS }
    modules.fcntl_constants --> modules.fcntl { F_RDLCK, F_SETLK, F_SETLKW, F_UNLCK, F_WRLCK, LOCK_EX, LOCK_NB, LOCK_SH, LOCK_UN }
    modules.fcntl_records --> bindings.fcntl { PLATFORM }
    modules.fcntl_records --> modules.fcntl { flock_record }
    modules.functools --> bindings.clinic.functools { _functools__lru_cache_wrapper_cache_clear_impl, _functools__lru_cache_wrapper_cache_info_impl, _functools_cmp_to_key_impl, _functools_reduce_impl }
    modules.functools --> bindings.functools { KeyWrapper_token, LruState, _lru_cache_wrapper_token }
    modules.grouping --> modules.itertools { group_state, jacpy_group_activate, jacpy_group_clear, jacpy_group_field, jacpy_group_init, jacpy_group_next, jacpy_grouper_next }
    modules.hashlib --> bindings.hashopenssl { HASHLIB_GIL_MINSIZE }
    modules.hashlib --> modules.hashopenssl { HASHLIB_GIL_MINSIZE, HashLock, compare_digest, data_argument, hash_buffer, hash_object_new, hash_state_of }
    modules.hashlib --> modules.operator { compare_digest }
    modules.hashopenssl --> bindings.clinic.hashopenssl { EVPXOF_digest_impl, EVPXOF_hexdigest_impl, EVP_copy_impl, EVP_digest_impl, EVP_hexdigest_impl, EVP_update_impl, _hashlib_HMAC_copy_impl, _hashlib_HMAC_digest_impl, _hashlib_HMAC_hexdigest_impl, _hashlib_HMAC_update_impl, _hashlib_compare_digest_impl, _hashlib_get_fips_mode_impl, _hashlib_hmac_new_impl, _hashlib_hmac_singleshot_impl, _hashlib_new_impl, _hashlib_openssl_md5_impl, _hashlib_openssl_sha1_impl, _hashlib_openssl_sha224_impl, _hashlib_openssl_sha256_impl, _hashlib_openssl_sha384_impl, _hashlib_openssl_sha3_224_impl, _hashlib_openssl_sha3_256_impl, _hashlib_openssl_sha3_384_impl, _hashlib_openssl_sha3_512_impl, _hashlib_openssl_sha512_impl, _hashlib_openssl_shake_128_impl, _hashlib_openssl_shake_256_impl, _hashlib_scrypt_impl, pbkdf2_hmac_impl }
    modules.hashopenssl --> bindings.hashopenssl { HASH_token, HMAC_token, STATE_CONSTRUCTS, STATE_COUNT, STATE_EVPXOF_TYPE, STATE_EVP_TYPE, STATE_HMAC_TYPE, STATE_UNSUPPORTED_DIGESTMOD_ERROR, add_object, dict_proxy, evp_block_size, evp_digest_size, evp_name, evp_repr, hashlib_exception, hashlib_init_constructors, hashlib_md_meth_names, hashlib_state_new, hmac_get_block_size, hmac_get_digest_size, hmac_get_name, hmac_repr }
    modules.heapq --> bindings.clinic.heapq { _heapq_heapify_impl, _heapq_heapify_max_impl, _heapq_heappop_impl, _heapq_heappop_max_impl, _heapq_heappush_impl, _heapq_heappush_max_impl, _heapq_heappushpop_impl, _heapq_heappushpop_max_impl, _heapq_heapreplace_impl, _heapq_heapreplace_max_impl }
    modules.iterators --> modules.itertools { jacpy_pipeline_clear, jacpy_pipeline_field, jacpy_pipeline_init, jacpy_pipeline_length, jacpy_pipeline_new, jacpy_pipeline_next, jacpy_pipeline_repr, pipeline_state }
    modules.itertools --> bindings.clinic.itertools { _grouper_token, _tee_token, batched_new_impl, cycle_token, dropwhile_token, filterfalse_token, itertools__grouper_impl, itertools__tee_impl, itertools_accumulate_impl, itertools_chain_from_iterable_impl, itertools_combinations_impl, itertools_combinations_with_replacement_impl, itertools_compress_impl, itertools_count_impl, itertools_cycle_impl, itertools_dropwhile_impl, itertools_filterfalse_impl, itertools_groupby_impl, itertools_permutations_impl, itertools_starmap_impl, itertools_takewhile_impl, itertools_tee_impl, itertools_teedataobject_impl, pairwise_new_impl, pairwise_token, starmap_token, subclass_clinic_state_by_cls_groupby_type, takewhile_token, teedataobject_token }
    modules.itertools --> bindings.itertools { Kind, combination_size, data_dealloc, iterator_clear, iterator_dealloc, iterator_new, iterator_next, iterator_repr, iterator_self, iterator_traverse, itertools_module_token, kind_tokens, names, pipeline_iterator_next, repeat_length, tee_copy }
    modules.locale --> bindings.clinic.locale { _locale_bind_textdomain_codeset_impl, _locale_bindtextdomain_impl, _locale_dcgettext_impl, _locale_dgettext_impl, _locale_getencoding_impl, _locale_gettext_impl, _locale_localeconv_impl, _locale_nl_langinfo_impl, _locale_setlocale_impl, _locale_strcoll_impl, _locale_strxfrm_impl, _locale_textdomain_impl }
    modules.locale --> bindings.locale { ERROR }
    modules.locale_constants --> bindings.locale { CONSTANTS, PLATFORM }
    modules.locale_constants --> modules.locale { ALT_DIGITS, CONSTANTS, ERA, LC_CTYPE, LC_MESSAGES, LC_MONETARY, LC_NUMERIC, LC_TIME }
    modules.locale_platform --> bindings.locale { HAS_LIBINTL }
    modules.locale_platform --> modules.locale { GLIBC, bind_textdomain_codeset, bindtextdomain, dcgettext, dgettext, gettext, textdomain }
    modules.lsprof --> bindings.clinic.lsprof { Profiler_token, _lsprof_Profiler__ccall_callback_impl, _lsprof_Profiler__creturn_callback_impl, _lsprof_Profiler__pyreturn_callback_impl, _lsprof_Profiler__pystart_callback_impl, _lsprof_Profiler__pythrow_callback_impl, _lsprof_Profiler_clear_impl, _lsprof_Profiler_disable_impl, _lsprof_Profiler_enable_impl, _lsprof_Profiler_getstats_impl, profiler_init_impl }
    modules.lsprof --> bindings.lsprof { Profiler_token, profiler_finalize }
    modules.lzma --> bindings.clinic.lzma { FORMAT_AUTO, _lzma_LZMACompressor_compress_impl, _lzma_LZMACompressor_flush_impl, _lzma_LZMADecompressor_decompress_impl, _lzma_LZMADecompressor_impl, _lzma__decode_filter_properties_impl, _lzma_is_check_supported_impl, convert_lzma_vli_converter }
    modules.lzma --> bindings.lzma { COMPRESSOR_TYPE, DECOMPRESSOR_TYPE, EMPTY_TUPLE, FORMAT_ALONE, FORMAT_AUTO, FORMAT_RAW, FORMAT_XZ, LZMACompressor_token, LZMADecompressor_token, LZMA_CHECK_CRC32, LZMA_CHECK_CRC64, LZMA_CHECK_ID_MAX, LZMA_CHECK_NONE, LZMA_CHECK_SHA256, LZMA_CHECK_UNKNOWN, LZMA_ERROR, LZMA_FILTER_ARM, LZMA_FILTER_ARMTHUMB, LZMA_FILTER_DELTA, LZMA_FILTER_IA64, LZMA_FILTER_LZMA1, LZMA_FILTER_LZMA2, LZMA_FILTER_POWERPC, LZMA_FILTER_SPARC, LZMA_FILTER_X86, LZMA_MF_BT2, LZMA_MF_BT3, LZMA_MF_BT4, LZMA_MF_HC3, LZMA_MF_HC4, LZMA_MODE_FAST, LZMA_MODE_NORMAL, LZMA_PRESET_DEFAULT, LZMA_PRESET_EXTREME, lzma_compressor_new, lzma_encode_filter_properties }
    modules.math --> bindings.clinic.math { math_ceil_impl, math_comb_impl, math_degrees_impl, math_dist_impl, math_factorial_impl, math_floor_impl, math_fma_impl, math_fmod_impl, math_frexp_impl, math_fsum_impl, math_gcd_impl, math_hypot_impl, math_isclose_impl, math_isfinite_impl, math_isinf_impl, math_isnan_impl, math_isqrt_impl, math_lcm_impl, math_ldexp_impl, math_log10_impl, math_log2_impl, math_modf_impl, math_nextafter_impl, math_perm_impl, math_pow_impl, math_prod_impl, math_radians_impl, math_sumprod_impl, math_trunc_impl, math_ulp_impl }
    modules.mmap --> bindings.clinic.mmap { mmap_mmap___enter___impl, mmap_mmap___exit___impl, mmap_mmap_close_impl, mmap_mmap_find_impl, mmap_mmap_flush_impl, mmap_mmap_madvise_impl, mmap_mmap_move_impl, mmap_mmap_read_byte_impl, mmap_mmap_read_impl, mmap_mmap_readline_impl, mmap_mmap_resize_impl, mmap_mmap_rfind_impl, mmap_mmap_seek_impl, mmap_mmap_seekable_impl, mmap_mmap_size_impl, mmap_mmap_tell_impl, mmap_mmap_write_byte_impl, mmap_mmap_write_impl }
    modules.mmap --> bindings.mmap { mmap_ass_item, mmap_ass_subscript, mmap_closed_get, mmap_getbuffer, mmap_item, mmap_length, mmap_new, mmap_release, mmap_releasebuffer, mmap_repr, mmap_subscript, mmap_token, page_size }
    modules.mmap_constants --> bindings.mmap { CONSTANTS, PLATFORM }
    modules.mmap_constants --> modules.mmap { F_FULLFSYNC, MAP_ANONYMOUS, MAP_PRIVATE, MAP_SHARED, MREMAP_MAYMOVE, MS_SYNC, PROT_READ, PROT_WRITE, _SC_PAGESIZE }
    modules.mmap_platform --> modules.mmap { FULLFSYNC_BEFORE_MAP, HAS_MREMAP, REFUSES_SHARED_ANONYMOUS_GROWTH, mremap }
    modules.mpdecimal --> bindings.decimal { MPD_Division_by_zero, MPD_Division_undefined, MPD_IEEE_CONTEXT_MAX_BITS, MPD_MAX_EMAX, MPD_MAX_PREC, MPD_MIN_EMIN, MPD_MIN_ETINY, MPD_Overflow, MPD_Underflow, mpd_callocfunc, mpd_callocfunc_em, mpd_context_t, mpd_free, mpd_mallocfunc, mpd_maxcontext, mpd_reallocfunc, mpd_round_string, mpd_setminalloc, mpd_traphandler, mpd_version }
    modules.mpdecimal --> modules.decimal_context { MPD_Clamped, MPD_Division_by_zero, MPD_IEEE_CONTEXT_MAX_BITS, MPD_IEEE_Invalid_operation, MPD_MAX_SIGNAL_LIST, MPD_Malloc_error, MPD_Overflow, MPD_ROUND_HALF_EVEN, MPD_ROUND_HALF_UP, MPD_Underflow, mpd_class, mpd_context_t, mpd_etiny, mpd_etop, mpd_free_memory, mpd_getclamp, mpd_getemax, mpd_getemin, mpd_getprec, mpd_getround, mpd_ieee_context, mpd_iscanonical, mpd_lsnprint_signals, mpd_qcopy_abs, mpd_qcopy_negate, mpd_qcopy_sign, mpd_qsetclamp, mpd_qsetemax, mpd_qsetemin, mpd_qsetprec, mpd_qsetround, mpd_qsetstatus, mpd_qsettraps, mpd_round_string, mpd_same_quantum, mpd_to_eng_size, mpd_to_sci_size }
    modules.mpdecimal --> modules.decimal_convert { MPD_Clamped, MPD_Conversion_syntax, MPD_Errors, MPD_INF, MPD_Inexact, MPD_Invalid_operation, MPD_NAN, MPD_NEG, MPD_POS, MPD_Rounded, mpd_context_t, mpd_del, mpd_isnan, mpd_isspecial, mpd_qcopy, mpd_qfinalize, mpd_qimport_u16, mpd_qimport_u32, mpd_qmul, mpd_qncopy, mpd_qnew, mpd_qpow, mpd_qset_i64, mpd_qset_ssize, mpd_qset_string, mpd_qset_uint, mpd_set_flags, mpd_set_sign, mpd_setdigits, mpd_seterror, mpd_setspecial, mpd_t }
    modules.mpdecimal --> modules.decimal_number { MPD_CONST_DATA, MPD_Malloc_error, MPD_POS, MPD_ROUND_CEILING, MPD_ROUND_DOWN, MPD_ROUND_FLOOR, MPD_ROUND_HALF_EVEN, MPD_SSIZE_MAX, MPD_SSIZE_MIN, MPD_STATIC, MPD_UINT_SIZE, mpd_adjexp, mpd_arith_sign, mpd_class, mpd_clear_flags, mpd_context_t, mpd_del, mpd_free_memory, mpd_isdynamic_data, mpd_isinfinite, mpd_isnan, mpd_isnegative, mpd_ispositive, mpd_isqnan, mpd_issnan, mpd_isspecial, mpd_iszero, mpd_parse_fmt_str, mpd_qcmp, mpd_qcopy, mpd_qcopy_abs, mpd_qcopy_negate, mpd_qcopy_sign, mpd_qdivmod, mpd_qexport_u16, mpd_qexport_u32, mpd_qformat_spec, mpd_qget_i64, mpd_qget_ssize, mpd_qmul, mpd_qncopy, mpd_qnew, mpd_qpow, mpd_qpowmod, mpd_qquantize, mpd_qrem, mpd_qround_to_int, mpd_qround_to_intx, mpd_qset_uint, mpd_qsetround, mpd_qsset_ssize, mpd_same_quantum, mpd_set_positive, mpd_sign, mpd_spec_t, mpd_t, mpd_to_eng_size, mpd_to_sci, mpd_to_sci_size, mpd_validate_lconv }
    modules.mpdecimal --> modules.decimal_objects { MPD_CONTEXT_SIZE, MPD_Clamped, MPD_Conversion_syntax, MPD_Division_by_zero, MPD_Division_impossible, MPD_Division_undefined, MPD_IEEE_Invalid_operation, MPD_Inexact, MPD_Invalid_context, MPD_Invalid_operation, MPD_Malloc_error, MPD_Max_status, MPD_Not_implemented, MPD_Overflow, MPD_ROUND_GUARD, MPD_Rounded, MPD_STATIC, MPD_STATIC_DATA, MPD_Subnormal, MPD_Underflow, mpd_context_t, mpd_t }
    modules.mpdecimal --> modules.decimal_ops { mpd_compare_total, mpd_compare_total_mag, mpd_context_t, mpd_iscanonical, mpd_isfinite, mpd_isinfinite, mpd_isnan, mpd_isnormal, mpd_isqnan, mpd_issigned, mpd_issnan, mpd_issubnormal, mpd_iszero, mpd_qabs, mpd_qadd, mpd_qand, mpd_qcompare, mpd_qcompare_signal, mpd_qdiv, mpd_qdivint, mpd_qexp, mpd_qfma, mpd_qinvert, mpd_qln, mpd_qlog10, mpd_qlogb, mpd_qmax, mpd_qmax_mag, mpd_qmin, mpd_qmin_mag, mpd_qminus, mpd_qmul, mpd_qnext_minus, mpd_qnext_plus, mpd_qnext_toward, mpd_qor, mpd_qplus, mpd_qpow, mpd_qquantize, mpd_qreduce, mpd_qrem, mpd_qrem_near, mpd_qrotate, mpd_qround_to_int, mpd_qround_to_intx, mpd_qscaleb, mpd_qshift, mpd_qsqrt, mpd_qsub, mpd_qxor, mpd_t }
    modules.multibytecodec --> bindings.clinic.multibytecodec { MultibyteStreamWriter_token, _multibytecodec_MultibyteCodec_decode_impl, _multibytecodec_MultibyteCodec_encode_impl, _multibytecodec_MultibyteIncrementalDecoder_decode_impl, _multibytecodec_MultibyteIncrementalDecoder_getstate_impl, _multibytecodec_MultibyteIncrementalDecoder_reset_impl, _multibytecodec_MultibyteIncrementalDecoder_setstate_impl, _multibytecodec_MultibyteIncrementalEncoder_encode_impl, _multibytecodec_MultibyteIncrementalEncoder_getstate_impl, _multibytecodec_MultibyteIncrementalEncoder_reset_impl, _multibytecodec_MultibyteIncrementalEncoder_setstate_impl, _multibytecodec_MultibyteStreamReader_read_impl, _multibytecodec_MultibyteStreamReader_readline_impl, _multibytecodec_MultibyteStreamReader_readlines_impl, _multibytecodec_MultibyteStreamReader_reset_impl, _multibytecodec_MultibyteStreamWriter_reset_impl, _multibytecodec_MultibyteStreamWriter_write_impl, _multibytecodec_MultibyteStreamWriter_writelines_impl, _multibytecodec___create_codec_impl }
    modules.multibytecodec --> bindings.multibytecodec { MultibyteCodec_token, MultibyteIncrementalDecoder_token, MultibyteIncrementalEncoder_token, MultibyteStreamReader_token, MultibyteStreamWriter_token, STATE_CODEC_TYPE, STATE_COUNT, STATE_DECODER_TYPE, STATE_ENCODER_TYPE, STATE_READER_TYPE, STATE_STR_WRITE, STATE_WRITER_TYPE, StatefulState, codecctx_errors_get, codecctx_errors_set, parse_new_arguments, stateful_new }
    modules.multiprocessing --> bindings.clinic.multiprocessing { _multiprocessing_SemLock___enter___impl, _multiprocessing_SemLock___exit___impl, _multiprocessing_SemLock__after_fork_impl, _multiprocessing_SemLock__count_impl, _multiprocessing_SemLock__get_value_impl, _multiprocessing_SemLock__is_mine_impl, _multiprocessing_SemLock__is_zero_impl, _multiprocessing_SemLock__rebuild_impl, _multiprocessing_SemLock_acquire_impl, _multiprocessing_SemLock_impl, _multiprocessing_SemLock_release_impl, _multiprocessing_sem_unlink_impl, convert_SEM_HANDLE }
    modules.multiprocessing --> bindings.multiprocessing { SEMLOCK_FIELDS_SIZE, SemLock_token, semlock_members }
    modules.multiprocessing_constants --> bindings.multiprocessing { SEM_VALUE_MAX }
    modules.multiprocessing_constants --> modules.multiprocessing { O_CREAT, O_EXCL }
    modules.numeric --> modules.datetime_delta { fabs, modf, round }
    modules.numeric --> modules.decimal_convert { copysign, isinf, isnan }
    modules.numeric --> modules.math { frexp, modf }
    modules.numeric --> object_model.complex { atan2, copysign, cos, exp, fabs, floor, hypot, infinity, isfinite, isinf, isnan, log, nan, pow, sin }
    modules.openssl --> modules.hashopenssl { ERR_clear_error, ERR_func_error_string, ERR_lib_error_string, ERR_peek_last_error, ERR_reason_error_string, EVP_DigestFinal, EVP_DigestFinalXOF, EVP_DigestInit_ex, EVP_DigestUpdate, EVP_MD_CTX_copy, EVP_MD_CTX_free, EVP_MD_CTX_get0_md, EVP_MD_CTX_get_size_ex, EVP_MD_CTX_new, EVP_MD_do_all_provided, EVP_MD_fetch, EVP_MD_free, EVP_MD_get_block_size, EVP_MD_get_flags, EVP_MD_get_size, EVP_MD_get_type, EVP_MD_up_ref, EVP_PBE_scrypt, EVP_default_properties_is_fips_enabled, HMAC, HMAC_CTX_copy, HMAC_CTX_free, HMAC_CTX_get_md, HMAC_CTX_new, HMAC_Final, HMAC_Init_ex, HMAC_Update, OBJ_nid2ln, OBJ_nid2sn, PKCS5_PBKDF2_HMAC }
    modules.openssl --> modules.ssl { ASN1_OBJECT_free, ASN1_STRING_get0_data, ASN1_STRING_length, BIO_clear_flags, BIO_ctrl, BIO_ctrl_pending, BIO_free, BIO_free_all, BIO_new, BIO_new_fp, BIO_new_mem_buf, BIO_printf, BIO_puts, BIO_read, BIO_s_file, BIO_s_mem, BIO_set_flags, BIO_up_ref, BIO_write, COMP_get_type, DH_free, ERR_clear_error, ERR_get_error, ERR_peek_last_error, ERR_reason_error_string, OBJ_nid2ln, OBJ_nid2obj, OBJ_nid2sn, OBJ_obj2nid, OBJ_sn2nid, OBJ_txt2obj, OPENSSL_sk_find, OPENSSL_sk_free, OPENSSL_sk_num, OPENSSL_sk_value, OpenSSL_version, OpenSSL_version_num, PEM_read_DHparams, PEM_read_bio_X509, PEM_write_bio_X509, PEM_write_bio_X509_AUX, RAND_add, RAND_bytes, RAND_status, SSL_CIPHER_description, SSL_CIPHER_get_auth_nid, SSL_CIPHER_get_bits, SSL_CIPHER_get_cipher_nid, SSL_CIPHER_get_digest_nid, SSL_CIPHER_get_id, SSL_CIPHER_get_kx_nid, SSL_CIPHER_get_name, SSL_CIPHER_get_version, SSL_CIPHER_is_aead, SSL_CTX_callback_ctrl, SSL_CTX_check_private_key, SSL_CTX_clear_options, SSL_CTX_ctrl, SSL_CTX_free, SSL_CTX_get0_param, SSL_CTX_get_cert_store, SSL_CTX_get_default_passwd_cb, SSL_CTX_get_default_passwd_cb_userdata, SSL_CTX_get_num_tickets, SSL_CTX_get_options, SSL_CTX_get_security_level, SSL_CTX_get_verify_mode, SSL_CTX_load_verify_locations, SSL_CTX_new, SSL_CTX_set_alpn_protos, SSL_CTX_set_alpn_select_cb, SSL_CTX_set_cipher_list, SSL_CTX_set_default_passwd_cb, SSL_CTX_set_default_passwd_cb_userdata, SSL_CTX_set_default_verify_paths, SSL_CTX_set_keylog_callback, SSL_CTX_set_msg_callback, SSL_CTX_set_num_tickets, SSL_CTX_set_options, SSL_CTX_set_post_handshake_auth, SSL_CTX_set_psk_client_callback, SSL_CTX_set_psk_server_callback, SSL_CTX_set_verify, SSL_CTX_use_PrivateKey_file, SSL_CTX_use_certificate_chain_file, SSL_CTX_use_psk_identity_hint, SSL_SESSION_free, SSL_SESSION_get_id, SSL_SESSION_get_ticket_lifetime_hint, SSL_SESSION_get_time_ex, SSL_SESSION_get_timeout, SSL_SESSION_has_ticket, SSL_ctrl, SSL_do_handshake, SSL_free, SSL_get0_alpn_selected, SSL_get0_param, SSL_get0_verified_chain, SSL_get1_peer_certificate, SSL_get1_session, SSL_get_SSL_CTX, SSL_get_ciphers, SSL_get_client_ciphers, SSL_get_current_cipher, SSL_get_current_compression, SSL_get_error, SSL_get_ex_data, SSL_get_finished, SSL_get_peer_cert_chain, SSL_get_peer_finished, SSL_get_rbio, SSL_get_servername, SSL_get_shutdown, SSL_get_verify_mode, SSL_get_version, SSL_get_wbio, SSL_is_init_finished, SSL_new, SSL_pending, SSL_read_ex, SSL_select_next_proto, SSL_session_reused, SSL_set_SSL_CTX, SSL_set_accept_state, SSL_set_bio, SSL_set_connect_state, SSL_set_ex_data, SSL_set_fd, SSL_set_msg_callback, SSL_set_post_handshake_auth, SSL_set_read_ahead, SSL_set_session, SSL_set_session_id_context, SSL_set_verify, SSL_shutdown, SSL_verify_client_post_handshake, SSL_write_ex, TLS_client_method, TLS_method, TLS_server_method, TLSv1_1_method, TLSv1_2_method, TLSv1_method, X509_OBJECT_free, X509_OBJECT_get0_X509, X509_OBJECT_get_type, X509_STORE_add_cert, X509_STORE_get1_objects, X509_VERIFY_PARAM_clear_flags, X509_VERIFY_PARAM_get_flags, X509_VERIFY_PARAM_get_hostflags, X509_VERIFY_PARAM_set1_host, X509_VERIFY_PARAM_set1_ip, X509_VERIFY_PARAM_set_flags, X509_VERIFY_PARAM_set_hostflags, X509_check_ca, X509_cmp, X509_free, X509_get_default_cert_dir, X509_get_default_cert_dir_env, X509_get_default_cert_file, X509_get_default_cert_file_env, X509_get_subject_name, X509_subject_name_hash, a2i_IPADDRESS, d2i_X509_bio, err_get_lib, err_get_reason, fclose, i2d_X509_bio }
    modules.openssl --> modules.ssl_cert { ASN1_STRING_get0_data, ASN1_STRING_length, ASN1_STRING_to_UTF8, ASN1_STRING_type, ASN1_TIME_print, AUTHORITY_INFO_ACCESS_free, BIO_ctrl, BIO_free, BIO_gets, BIO_new, BIO_s_mem, CRL_DIST_POINTS_free, GENERAL_NAMES_free, GENERAL_NAME_print, OBJ_obj2nid, OBJ_obj2txt, OPENSSL_sk_num, OPENSSL_sk_value, X509_NAME_ENTRY_get_data, X509_NAME_ENTRY_get_object, X509_NAME_ENTRY_set, X509_NAME_entry_count, X509_NAME_get_entry, X509_NAME_print_ex, X509_free, X509_get0_notAfter, X509_get0_notBefore, X509_get_ext_d2i, X509_get_issuer_name, X509_get_serialNumber, X509_get_subject_name, X509_get_version, X509_up_ref, i2a_ASN1_INTEGER, i2d_X509, i2t_ASN1_OBJECT, openssl_free }
    modules.openssl --> modules.ssl_core { ASN1_OCTET_STRING_free, BIO_free_all, ERR_clear_error, ERR_peek_last_error, ERR_reason_error_string, SSL_CTX_free, SSL_SESSION_free, SSL_free, SSL_get_error, SSL_get_shutdown, SSL_get_verify_result, SSL_set_shutdown, X509_free, X509_verify_cert_error_string, err_get_lib, err_get_reason }
    modules.openssl_constants --> bindings.ssl { OPENSSL_NO_PSK, SSL_AD_ACCESS_DENIED, SSL_AD_BAD_CERTIFICATE, SSL_AD_BAD_CERTIFICATE_HASH_VALUE, SSL_AD_BAD_CERTIFICATE_STATUS_RESPONSE, SSL_AD_BAD_RECORD_MAC, SSL_AD_CERTIFICATE_EXPIRED, SSL_AD_CERTIFICATE_REVOKED, SSL_AD_CERTIFICATE_UNKNOWN, SSL_AD_CERTIFICATE_UNOBTAINABLE, SSL_AD_CLOSE_NOTIFY, SSL_AD_DECODE_ERROR, SSL_AD_DECOMPRESSION_FAILURE, SSL_AD_DECRYPT_ERROR, SSL_AD_HANDSHAKE_FAILURE, SSL_AD_ILLEGAL_PARAMETER, SSL_AD_INSUFFICIENT_SECURITY, SSL_AD_INTERNAL_ERROR, SSL_AD_NO_RENEGOTIATION, SSL_AD_PROTOCOL_VERSION, SSL_AD_RECORD_OVERFLOW, SSL_AD_UNEXPECTED_MESSAGE, SSL_AD_UNKNOWN_CA, SSL_AD_UNKNOWN_PSK_IDENTITY, SSL_AD_UNRECOGNIZED_NAME, SSL_AD_UNSUPPORTED_CERTIFICATE, SSL_AD_UNSUPPORTED_EXTENSION, SSL_AD_USER_CANCELLED, SSL_OP_ALL, SSL_OP_CIPHER_SERVER_PREFERENCE, SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS, SSL_OP_ENABLE_KTLS, SSL_OP_ENABLE_MIDDLEBOX_COMPAT, SSL_OP_IGNORE_UNEXPECTED_EOF, SSL_OP_LEGACY_SERVER_CONNECT, SSL_OP_NO_COMPRESSION, SSL_OP_NO_RENEGOTIATION, SSL_OP_NO_SSLv2, SSL_OP_NO_SSLv3, SSL_OP_NO_TICKET, SSL_OP_NO_TLSv1, SSL_OP_NO_TLSv1_1, SSL_OP_NO_TLSv1_2, SSL_OP_NO_TLSv1_3, SSL_OP_SINGLE_DH_USE, SSL_OP_SINGLE_ECDH_USE, UNDEFINED, X509_CHECK_FLAG_ALWAYS_CHECK_SUBJECT, X509_CHECK_FLAG_MULTI_LABEL_WILDCARDS, X509_CHECK_FLAG_NEVER_CHECK_SUBJECT, X509_CHECK_FLAG_NO_PARTIAL_WILDCARDS, X509_CHECK_FLAG_NO_WILDCARDS, X509_CHECK_FLAG_SINGLE_LABEL_SUBDOMAINS, X509_V_FLAG_ALLOW_PROXY_CERTS, X509_V_FLAG_CRL_CHECK, X509_V_FLAG_CRL_CHECK_ALL, X509_V_FLAG_PARTIAL_CHAIN, X509_V_FLAG_TRUSTED_FIRST, X509_V_FLAG_X509_STRICT }
    modules.openssl_constants --> modules.hashopenssl { EVP_MAX_MD_SIZE, EVP_MD_FLAG_XOF, NID_blake2b512, NID_blake2s256, NID_md5, NID_sha1, NID_sha224, NID_sha256, NID_sha384, NID_sha3_224, NID_sha3_256, NID_sha3_384, NID_sha3_512, NID_sha512, NID_sha512_224, NID_sha512_256, NID_shake128, NID_shake256, NID_undef, SN_blake2b512, SN_blake2s256, SN_md5, SN_sha1, SN_sha224, SN_sha256, SN_sha384, SN_sha3_224, SN_sha3_256, SN_sha3_384, SN_sha3_512, SN_sha512, SN_sha512_224, SN_sha512_256, SN_shake128, SN_shake256, UNDEFINED }
    modules.openssl_constants --> modules.openssl { ERR_LIB_MASK, ERR_LIB_OFFSET, ERR_LIB_SYS, ERR_REASON_MASK, ERR_SYSTEM_FLAG, ERR_SYSTEM_MASK }
    modules.openssl_constants --> modules.ssl { BIO_CLOSE, BIO_CTRL_EOF, BIO_CTRL_FLUSH, BIO_C_FILE_TELL, BIO_C_SET_BUF_MEM_EOF_RETURN, BIO_C_SET_FILENAME, BIO_C_SET_NBIO, BIO_FLAGS_READ, BIO_FLAGS_RWS, BIO_FLAGS_SHOULD_RETRY, BIO_FP_READ, BIO_FP_TEXT, ERR_LIB_PEM, ERR_LIB_X509, NID_undef, OPENSSL_NO_COMP, OPENSSL_NO_PSK, OPENSSL_NO_TLS1_1_METHOD, OPENSSL_NO_TLS1_2_METHOD, OPENSSL_NO_TLS1_METHOD, OPENSSL_NPN_NEGOTIATED, OPENSSL_VERSION, OPENSSL_VERSION_NUMBER, PEM_R_NO_START_LINE, SSL3_MT_CHANGE_CIPHER_SPEC, SSL3_RT_ALERT, SSL3_RT_CHANGE_CIPHER_SPEC, SSL3_RT_HANDSHAKE, SSL3_RT_HEADER, SSL3_RT_INNER_CONTENT_TYPE, SSL_AD_HANDSHAKE_FAILURE, SSL_AD_INTERNAL_ERROR, SSL_CTRL_GET_MAX_PROTO_VERSION, SSL_CTRL_GET_MIN_PROTO_VERSION, SSL_CTRL_MODE, SSL_CTRL_SESS_ACCEPT, SSL_CTRL_SESS_ACCEPT_GOOD, SSL_CTRL_SESS_ACCEPT_RENEGOTIATE, SSL_CTRL_SESS_CACHE_FULL, SSL_CTRL_SESS_CONNECT, SSL_CTRL_SESS_CONNECT_GOOD, SSL_CTRL_SESS_CONNECT_RENEGOTIATE, SSL_CTRL_SESS_HIT, SSL_CTRL_SESS_MISSES, SSL_CTRL_SESS_NUMBER, SSL_CTRL_SESS_TIMEOUTS, SSL_CTRL_SET_GROUPS, SSL_CTRL_SET_MAX_PROTO_VERSION, SSL_CTRL_SET_MIN_PROTO_VERSION, SSL_CTRL_SET_TLSEXT_HOSTNAME, SSL_CTRL_SET_TLSEXT_SERVERNAME_ARG, SSL_CTRL_SET_TLSEXT_SERVERNAME_CB, SSL_CTRL_SET_TMP_DH, SSL_ERROR_WANT_READ, SSL_ERROR_WANT_WRITE, SSL_ERROR_ZERO_RETURN, SSL_FILETYPE_ASN1, SSL_FILETYPE_PEM, SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER, SSL_MODE_AUTO_RETRY, SSL_MODE_RELEASE_BUFFERS, SSL_OP_ALL, SSL_OP_CIPHER_SERVER_PREFERENCE, SSL_OP_DONT_INSERT_EMPTY_FRAGMENTS, SSL_OP_NO_COMPRESSION, SSL_OP_NO_SSLv2, SSL_OP_NO_SSLv3, SSL_OP_NO_TLSv1, SSL_OP_NO_TLSv1_1, SSL_OP_NO_TLSv1_2, SSL_OP_NO_TLSv1_3, SSL_OP_SINGLE_DH_USE, SSL_OP_SINGLE_ECDH_USE, SSL_RECEIVED_SHUTDOWN, SSL_TLSEXT_ERR_ALERT_FATAL, SSL_TLSEXT_ERR_NOACK, SSL_TLSEXT_ERR_OK, SSL_VERIFY_FAIL_IF_NO_PEER_CERT, SSL_VERIFY_NONE, SSL_VERIFY_PEER, SSL_VERIFY_POST_HANDSHAKE, TLSEXT_NAMETYPE_host_name, UNDEFINED, X509_CHECK_FLAG_NO_PARTIAL_WILDCARDS, X509_FILETYPE_ASN1, X509_FILETYPE_PEM, X509_LU_CRL, X509_LU_X509, X509_R_CERT_ALREADY_IN_HASH_TABLE, X509_V_FLAG_TRUSTED_FIRST, XN_FLAG_RFC2253 }
    modules.openssl_constants --> modules.ssl_cert { ACCESS_DESCRIPTION_LOCATION_OFFSET, ACCESS_DESCRIPTION_METHOD_OFFSET, BIO_CTRL_INFO, BIO_CTRL_RESET, DIST_POINT_DISTPOINT_OFFSET, DIST_POINT_NAME_NAME_OFFSET, GENERAL_NAME_D_OFFSET, GENERAL_NAME_TYPE_OFFSET, GEN_DIRNAME, GEN_DNS, GEN_EDIPARTY, GEN_EMAIL, GEN_IPADD, GEN_OTHERNAME, GEN_RID, GEN_URI, GEN_X400, NID_ad_OCSP, NID_ad_ca_issuers, NID_crl_distribution_points, NID_info_access, NID_subject_alt_name, V_ASN1_BIT_STRING }
    modules.openssl_constants --> modules.ssl_core { ERR_LIB_SSL, ERR_LIB_SYS, OPENSSL_NO_SSL3, OPENSSL_NO_TLS1, OPENSSL_NO_TLS1_1, OPENSSL_NO_TLS1_2, OPENSSL_NO_TLS1_3, SSL3_VERSION, SSL_ERROR_SSL, SSL_ERROR_SYSCALL, SSL_ERROR_WANT_CONNECT, SSL_ERROR_WANT_READ, SSL_ERROR_WANT_WRITE, SSL_ERROR_WANT_X509_LOOKUP, SSL_ERROR_ZERO_RETURN, SSL_R_CERTIFICATE_VERIFY_FAILED, SSL_R_UNEXPECTED_EOF_WHILE_READING, SSL_SENT_SHUTDOWN, SSL_VERIFY_POST_HANDSHAKE, TLS1_1_VERSION, TLS1_2_VERSION, TLS1_3_VERSION, TLS1_VERSION, UNDEFINED, X509_V_ERR_HOSTNAME_MISMATCH, X509_V_ERR_IP_ADDRESS_MISMATCH }
    modules.operator --> bindings.clinic.operator { _operator__compare_digest_impl, _operator_abs_impl, _operator_add_impl, _operator_and__impl, _operator_concat_impl, _operator_contains_impl, _operator_countOf_impl, _operator_delitem_impl, _operator_eq_impl, _operator_floordiv_impl, _operator_ge_impl, _operator_getitem_impl, _operator_gt_impl, _operator_iadd_impl, _operator_iand_impl, _operator_iconcat_impl, _operator_ifloordiv_impl, _operator_ilshift_impl, _operator_imatmul_impl, _operator_imod_impl, _operator_imul_impl, _operator_indexOf_impl, _operator_index_impl, _operator_inv_impl, _operator_invert_impl, _operator_ior_impl, _operator_ipow_impl, _operator_irshift_impl, _operator_is__impl, _operator_is_none_impl, _operator_is_not_impl, _operator_is_not_none_impl, _operator_isub_impl, _operator_itruediv_impl, _operator_ixor_impl, _operator_le_impl, _operator_length_hint_impl, _operator_lshift_impl, _operator_lt_impl, _operator_matmul_impl, _operator_mod_impl, _operator_mul_impl, _operator_ne_impl, _operator_neg_impl, _operator_not__impl, _operator_or__impl, _operator_pos_impl, _operator_pow_impl, _operator_rshift_impl, _operator_setitem_impl, _operator_sub_impl, _operator_truediv_impl, _operator_truth_impl, _operator_xor_impl }
    modules.output_buffer --> modules.lzma { BlocksOutputBuffer, Cursor }
    modules.output_buffer --> modules.zstd { BlocksOutputBuffer, Cursor }
    modules.pickle --> bindings.clinic.pickle { Pickler_token, Unpickler_token, _pickle_PicklerMemoProxy___reduce___impl, _pickle_PicklerMemoProxy_clear_impl, _pickle_PicklerMemoProxy_copy_impl, _pickle_Pickler___init___impl, _pickle_Pickler___sizeof___impl, _pickle_Pickler_clear_memo_impl, _pickle_Pickler_dump_impl, _pickle_UnpicklerMemoProxy___reduce___impl, _pickle_UnpicklerMemoProxy_clear_impl, _pickle_UnpicklerMemoProxy_copy_impl, _pickle_Unpickler___init___impl, _pickle_Unpickler___sizeof___impl, _pickle_Unpickler_find_class_impl, _pickle_Unpickler_load_impl, _pickle_Unpickler_persistent_load_impl, _pickle_dump_impl, _pickle_dumps_impl, _pickle_load_impl, _pickle_loads_impl }
    modules.pickle --> bindings.pickle { MemoState, PICKLER_DISPATCH, PICKLER_RECORD, PicklerMemoProxy_token, PicklerState, Pickler_token, Slot, UnpicklerMemoProxy_token, UnpicklerState, Unpickler_token, memo_proxy_copy, module_for, pickle_module_token, pickler_record, state_for, type_definition, wrap }
    modules.posix --> bindings.clinic.posix { CHMOD_DEFAULT_FOLLOW_SYMLINKS, DEFAULT_DIR_FD, DirEntry_token, EFD_CLOEXEC, MFD_CLOEXEC, PATH_HAVE_FCHDIR, PATH_HAVE_FCHMOD, PATH_HAVE_FCHOWN, PATH_HAVE_FDOPENDIR, PATH_HAVE_FEXECVE, PATH_HAVE_FPATHCONF, PATH_HAVE_FSTATVFS, PATH_HAVE_FTRUNCATE, PATH_T_INITIALIZE, PATH_T_INITIALIZE_P, PATH_UTIME_HAVE_FD, convert_FACCESSAT_DIR_FD_CONVERTER, convert_FCHMODAT_DIR_FD_CONVERTER, convert_FCHOWNAT_DIR_FD_CONVERTER, convert_FSTATAT_DIR_FD_CONVERTER, convert_FUTIMENSAT_DIR_FD_CONVERTER, convert_MKDIRAT_DIR_FD_CONVERTER, convert_MKFIFOAT_DIR_FD_CONVERTER, convert_MKNODAT_DIR_FD_CONVERTER, convert_OPENAT_DIR_FD_CONVERTER, convert_Py_off_t_converter, convert_READLINKAT_DIR_FD_CONVERTER, convert_SYMLINKAT_DIR_FD_CONVERTER, convert_UNLINKAT_DIR_FD_CONVERTER, convert__Py_Dev_Converter, convert__Py_Gid_Converter, convert__Py_Uid_Converter, convert_conv_confname, convert_dir_fd_converter, convert_id_t, convert_idtype_t_converter, convert_path_converter, fileno, os_DirEntry___fspath___impl, os_DirEntry_inode_impl, os_DirEntry_is_dir_impl, os_DirEntry_is_file_impl, os_DirEntry_is_junction_impl, os_DirEntry_is_symlink_impl, os_DirEntry_stat_impl, os_WCOREDUMP_impl, os_WEXITSTATUS_impl, os_WIFCONTINUED_impl, os_WIFEXITED_impl, os_WIFSIGNALED_impl, os_WIFSTOPPED_impl, os_WSTOPSIG_impl, os_WTERMSIG_impl, os__create_environ_impl, os__exit_impl, os__fcopyfile_impl, os__inputhook_impl, os__is_inputhook_installed_impl, os__path_normpath_impl, os__path_splitroot_ex_impl, os_abort_impl, os_access_impl, os_chdir_impl, os_chflags_impl, os_chmod_impl, os_chown_impl, os_chroot_impl, os_close_impl, os_closerange_impl, os_confstr_impl, os_copy_file_range_impl, os_cpu_count_impl, os_ctermid_impl, os_device_encoding_impl, os_dup2_impl, os_dup_impl, os_eventfd_impl, os_eventfd_read_impl, os_eventfd_write_impl, os_execv_impl, os_execve_impl, os_fchdir_impl, os_fchmod_impl, os_fchown_impl, os_fdatasync_impl, os_fork1_impl, os_fork_impl, os_forkpty_impl, os_fpathconf_impl, os_fspath_impl, os_fstat_impl, os_fstatvfs_impl, os_fsync_impl, os_ftruncate_impl, os_get_blocking_impl, os_get_inheritable_impl, os_get_terminal_size_impl, os_getcwd_impl, os_getcwdb_impl, os_getegid_impl, os_geteuid_impl, os_getgid_impl, os_getgrouplist_darwin_impl, os_getgrouplist_linux_impl, os_getgroups_impl, os_getloadavg_impl, os_getlogin_impl, os_getpgid_impl, os_getpgrp_impl, os_getpid_impl, os_getppid_impl, os_getpriority_impl, os_getrandom_impl, os_getresgid_impl, os_getresuid_impl, os_getsid_impl, os_getuid_impl, os_getxattr_impl, os_grantpt_impl, os_initgroups_darwin_impl, os_initgroups_linux_impl, os_isatty_impl, os_kill_impl, os_killpg_impl, os_lchflags_impl, os_lchmod_impl, os_lchown_impl, os_link_impl, os_listdir_impl, os_listxattr_impl, os_lockf_impl, os_login_tty_impl, os_lseek_impl, os_lstat_impl, os_major_impl, os_makedev_impl, os_memfd_create_impl, os_minor_impl, os_mkdir_impl, os_mkfifo_impl, os_mknod_impl, os_nice_impl, os_open_impl, os_openpty_impl, os_pathconf_impl, os_pidfd_open_impl, os_pipe2_impl, os_pipe_impl, os_posix_fadvise_impl, os_posix_fallocate_impl, os_posix_openpt_impl, os_posix_spawn_impl, os_posix_spawnp_impl, os_pread_impl, os_preadv_impl, os_ptsname_impl, os_putenv_impl, os_pwrite_impl, os_pwritev_impl, os_read_impl, os_readinto_impl, os_readlink_impl, os_readv_impl, os_register_at_fork_impl, os_remove_impl, os_removexattr_impl, os_rename_impl, os_replace_impl, os_rmdir_impl, os_scandir_impl, os_sched_get_priority_max_impl, os_sched_get_priority_min_impl, os_sched_getaffinity_impl, os_sched_getparam_impl, os_sched_getscheduler_impl, os_sched_param_impl, os_sched_rr_get_interval_impl, os_sched_setaffinity_impl, os_sched_setparam_impl, os_sched_setscheduler_impl, os_sched_yield_impl, os_sendfile_darwin_impl, os_sendfile_linux_impl, os_set_blocking_impl, os_set_inheritable_impl, os_setegid_impl, os_seteuid_impl, os_setgid_impl, os_setgroups_impl, os_setns_impl, os_setpgid_impl, os_setpgrp_impl, os_setpriority_impl, os_setregid_impl, os_setresgid_impl, os_setresuid_impl, os_setreuid_impl, os_setsid_impl, os_setuid_impl, os_setxattr_impl, os_splice_impl, os_stat_impl, os_statvfs_impl, os_strerror_impl, os_symlink_impl, os_sync_impl, os_sysconf_impl, os_system_impl, os_tcgetpgrp_impl, os_tcsetpgrp_impl, os_timerfd_create_impl, os_timerfd_gettime_impl, os_timerfd_gettime_ns_impl, os_timerfd_settime_impl, os_timerfd_settime_ns_impl, os_times_impl, os_truncate_impl, os_ttyname_impl, os_umask_impl, os_uname_impl, os_unlink_impl, os_unlockpt_impl, os_unsetenv_impl, os_unshare_impl, os_urandom_impl, os_utime_impl, os_wait3_impl, os_wait4_impl, os_wait_impl, os_waitid_impl, os_waitpid_impl, os_waitstatus_to_exitcode_impl, os_write_impl, os_writev_impl, return_Py_off_t, return_dev_t, stdout }
    modules.posix_constants --> bindings.posix { CONFSTR_TABLE, CONSTANTS, HAVE_CONFSTR, HAVE_EVENTFD, HAVE_FACCESSAT, HAVE_FCHDIR, HAVE_FCHMOD, HAVE_FCHMODAT, HAVE_FCHOWN, HAVE_FCHOWNAT, HAVE_FDOPENDIR, HAVE_FEXECVE, HAVE_FPATHCONF, HAVE_FSTATAT, HAVE_FSTATVFS, HAVE_FTRUNCATE, HAVE_FUTIMENS, HAVE_FUTIMES, HAVE_FUTIMESAT, HAVE_LCHFLAGS, HAVE_LCHMOD, HAVE_LCHOWN, HAVE_LINKAT, HAVE_LSTAT, HAVE_LUTIMES, HAVE_MEMFD_CREATE, HAVE_MKDIRAT, HAVE_MKFIFOAT, HAVE_MKNODAT, HAVE_OPENAT, HAVE_PATHCONF, HAVE_PTSNAME_R, HAVE_READLINKAT, HAVE_RENAMEAT, HAVE_SYMLINKAT, HAVE_SYSCONF, HAVE_TIMERFD_CREATE, HAVE_UNLINKAT, HAVE_UTIMENSAT, METHODS, PATHCONF_TABLE, SYSCONF_TABLE }
    modules.posix_constants --> modules.posix_core { AT_FDCWD, EFD_CLOEXEC as EFD_CLOEXEC_VALUE, EINTR, EINVAL, HAVE_FACCESSAT, HAVE_FCHDIR, HAVE_FCHMOD, HAVE_FCHMODAT, HAVE_FCHOWN, HAVE_FCHOWNAT, HAVE_FDOPENDIR, HAVE_FEXECVE, HAVE_FPATHCONF, HAVE_FSTATAT, HAVE_FSTATVFS, HAVE_FTRUNCATE, HAVE_FUTIMENS, HAVE_FUTIMES, HAVE_FUTIMESAT, HAVE_MKDIRAT, HAVE_MKFIFOAT, HAVE_MKNODAT, HAVE_OPENAT, HAVE_READLINKAT, HAVE_SYMLINKAT, HAVE_UNLINKAT, HAVE_UTIMENSAT, MFD_CLOEXEC as MFD_CLOEXEC_VALUE, NODEV, NSIG }
    modules.posix_constants --> modules.posix_fileio { EAGAIN, EBUSY, EINTR, EINVAL, ENOSYS, HAVE_DUP3, HAVE_LOGIN_TTY, HAVE_OPENAT, HAVE_PIPE2, HAVE_PREADV2, HAVE_PTSNAME_R, HAVE_PWRITEV2, L_ctermid, MAXPATHLEN, O_CLOEXEC, SEEK_CUR, SEEK_END, SEEK_SET, SIGCHLD, TFD_CLOEXEC, TIOCGWINSZ, TIOCSCTTY, _SC_TTY_NAME_MAX }
    modules.posix_constants --> modules.posix_fileio_platform { ENOSYS }
    modules.posix_constants --> modules.posix_files { AT_EACCESS, AT_REMOVEDIR, AT_SYMLINK_FOLLOW, AT_SYMLINK_NOFOLLOW, EINTR, EINVAL, ENOENT, ENOSYS, ENOTSUP, EOPNOTSUPP, ERANGE, HAVE_FACCESSAT, HAVE_FCHDIR, HAVE_FCHMOD, HAVE_FCHMODAT, HAVE_FCHOWN, HAVE_FCHOWNAT, HAVE_FPATHCONF, HAVE_FUTIMENS, HAVE_FUTIMES, HAVE_FUTIMESAT, HAVE_LCHFLAGS, HAVE_LCHMOD, HAVE_LCHOWN, HAVE_LINKAT, HAVE_LUTIMES, HAVE_MKDIRAT, HAVE_MKFIFOAT, HAVE_MKNODAT, HAVE_READLINKAT, HAVE_RENAMEAT, HAVE_SYMLINKAT, HAVE_UNLINKAT, HAVE_UTIMENSAT, MAXPATHLEN, NODEV, XATTR_LIST_MAX, XATTR_SIZE_MAX }
    modules.posix_constants --> modules.posix_ids { EINTR, EINVAL, HAVE_BROKEN_UNSETENV, NGROUPS_MAX, _SC_NPROCESSORS_ONLN }
    modules.posix_constants --> modules.posix_process { EINTR, EINVAL, HAVE_BROKEN_NICE, HAVE_FEXECVE, HAVE_GETPRIORITY, HAVE_SCHED_SETPARAM, HAVE_SCHED_SETSCHEDULER, HAVE_WAIT3, HAVE_WAIT4, HAVE_WAITID, POSIX_SPAWN_CLOSE, POSIX_SPAWN_DUP2, POSIX_SPAWN_OPEN, POSIX_SPAWN_RESETIDS, POSIX_SPAWN_SETPGROUP, POSIX_SPAWN_SETSCHEDPARAM, POSIX_SPAWN_SETSCHEDULER, POSIX_SPAWN_SETSID, POSIX_SPAWN_SETSID_NP, POSIX_SPAWN_SETSIGDEF, POSIX_SPAWN_SETSIGMASK, PRIO_PROCESS }
    modules.posix_constants --> modules.posix_stat { AT_SYMLINK_NOFOLLOW, DT_DIR, DT_LNK, DT_REG, DT_UNKNOWN, EINTR, HAVE_FDOPENDIR, HAVE_FSTATAT, HAVE_FSTATVFS }
    modules.posix_core --> bindings.posix { PosixState, STATE_BILLION, STATE_COUNT, STATE_DIR_ENTRY_TYPE, STATE_SCANDIR_ITERATOR_TYPE, STATE_SCHED_PARAM_TYPE, STATE_ST_MODE, convertenviron, state_object }
    modules.posix_core --> modules.grp { _PyLong_FromGid, _Py_Gid_Converter }
    modules.posix_core --> modules.posix { CHMOD_DEFAULT_FOLLOW_SYMLINKS, DEFAULT_DIR_FD, EFD_CLOEXEC, MFD_CLOEXEC, PATH_HAVE_FCHDIR, PATH_HAVE_FCHMOD, PATH_HAVE_FCHOWN, PATH_HAVE_FDOPENDIR, PATH_HAVE_FEXECVE, PATH_HAVE_FPATHCONF, PATH_HAVE_FSTATVFS, PATH_HAVE_FTRUNCATE, PATH_T_INITIALIZE, PATH_T_INITIALIZE_P, PATH_UTIME_HAVE_FD, convert_FACCESSAT_DIR_FD_CONVERTER, convert_FCHMODAT_DIR_FD_CONVERTER, convert_FCHOWNAT_DIR_FD_CONVERTER, convert_FSTATAT_DIR_FD_CONVERTER, convert_FUTIMENSAT_DIR_FD_CONVERTER, convert_MKDIRAT_DIR_FD_CONVERTER, convert_MKFIFOAT_DIR_FD_CONVERTER, convert_MKNODAT_DIR_FD_CONVERTER, convert_OPENAT_DIR_FD_CONVERTER, convert_Py_off_t_converter, convert_READLINKAT_DIR_FD_CONVERTER, convert_SYMLINKAT_DIR_FD_CONVERTER, convert_UNLINKAT_DIR_FD_CONVERTER, convert__Py_Dev_Converter, convert__Py_Gid_Converter, convert__Py_Uid_Converter, convert_conv_confname, convert_dir_fd_converter, convert_id_t, convert_idtype_t_converter, convert_path_converter, fileno, return_Py_off_t, return_dev_t, stdout }
    modules.posix_core --> modules.posix_fileio { DEFAULT_DIR_FD, INT_MAX, STATE_TERMINAL_SIZE_TYPE, argument_unavailable_error, path_t, posix_error, state_object }
    modules.posix_core --> modules.posix_files { DEFAULT_DIR_FD, STATE_BILLION, argument_unavailable_error, dev_value, dir_fd_and_fd_invalid, dir_fd_and_follow_symlinks_invalid, fd_and_follow_symlinks_invalid, follow_symlinks_specified, path_and_dir_fd_invalid, path_error, path_error2, path_object_error, path_t, posix_error, posix_fildes_fd, posix_path_error, state_object }
    modules.posix_core --> modules.posix_ids { INT_MAX, PyOS_FSPath, STATE_UNAME_RESULT_TYPE, _PyLong_FromGid, _PyLong_FromUid, _Py_Gid_Converter, convertenviron, posix_error, state_object }
    modules.posix_core --> modules.posix_process { AFTER_FORKERS_CHILD, AFTER_FORKERS_PARENT, BEFORE_FORKERS, INT_MAX, INT_MIN, PyOS_AfterFork_Child, PyOS_AfterFork_Parent, PyOS_BeforeFork, STATE_SCHED_PARAM_TYPE, STATE_STRUCT_RUSAGE, STATE_TIMES_RESULT_TYPE, STATE_WAITID_RESULT_TYPE, _PyLong_FromUid, _Py_Sigset_Converter, argument_unavailable_error, interned, path_object_error, path_t, posix_error, posix_path_error, posix_state, register_at_forker, state_object }
    modules.posix_core --> modules.posix_stat { DEFAULT_DIR_FD, PosixState, STATE_BILLION, STATE_DIR_ENTRY_TYPE, STATE_SCANDIR_ITERATOR_TYPE, STATE_STATVFS_RESULT_TYPE, STATE_STAT_RESULT_TYPE, STATE_ST_MODE, _PyLong_FromDev, _PyLong_FromGid, _PyLong_FromUid, argument_unavailable_error, dir_fd_and_fd_invalid, fd_and_follow_symlinks_invalid, interned, path_and_dir_fd_invalid, path_error, path_object_error, path_t, posix_error, posix_module, posix_state, state_object }
    modules.posix_core --> modules.posixsubprocess { PyOS_AfterFork_Child, PyOS_AfterFork_Parent, PyOS_BeforeFork, _Py_Gid_Converter, _Py_Uid_Converter }
    modules.posix_core --> modules.pwd { _PyLong_FromUid, _Py_Uid_Converter }
    modules.posix_fileio --> bindings.posix { posix_fileio_exec }
    modules.posix_fileio --> modules.posix { os__fcopyfile_impl, os_close_impl, os_closerange_impl, os_copy_file_range_impl, os_ctermid_impl, os_device_encoding_impl, os_dup2_impl, os_dup_impl, os_eventfd_impl, os_eventfd_read_impl, os_eventfd_write_impl, os_get_blocking_impl, os_get_inheritable_impl, os_get_terminal_size_impl, os_grantpt_impl, os_isatty_impl, os_login_tty_impl, os_lseek_impl, os_memfd_create_impl, os_open_impl, os_openpty_impl, os_pipe2_impl, os_pipe_impl, os_posix_openpt_impl, os_pread_impl, os_preadv_impl, os_ptsname_impl, os_pwrite_impl, os_pwritev_impl, os_read_impl, os_readinto_impl, os_readv_impl, os_sendfile_darwin_impl, os_sendfile_linux_impl, os_set_blocking_impl, os_set_inheritable_impl, os_splice_impl, os_timerfd_create_impl, os_timerfd_gettime_impl, os_timerfd_gettime_ns_impl, os_timerfd_settime_impl, os_timerfd_settime_ns_impl, os_ttyname_impl, os_unlockpt_impl, os_write_impl, os_writev_impl }
    modules.posix_fileio_platform --> modules.posix_fileio { PY_READ_MAX, copy_file_range_call, ctermid_call, dup3_call, eventfd_call, eventfd_read_call, eventfd_write_call, fcopyfile_call, fd_pair, iovec, itimerspec, memfd_create_call, pipe2_call, preadv2_call, pwritev2_call, sendfile_darwin_call, sendfile_linux_call, splice_call, timerfd_create_call, timerfd_gettime_call, timerfd_settime_call }
    modules.posix_files --> bindings.posix { posix_files_exec }
    modules.posix_files --> modules.posix { os__path_normpath_impl, os__path_splitroot_ex_impl, os_access_impl, os_chdir_impl, os_chflags_impl, os_chmod_impl, os_chown_impl, os_chroot_impl, os_fchdir_impl, os_fchmod_impl, os_fchown_impl, os_fdatasync_impl, os_fpathconf_impl, os_fsync_impl, os_ftruncate_impl, os_getcwd_impl, os_getcwdb_impl, os_getxattr_impl, os_lchflags_impl, os_lchmod_impl, os_lchown_impl, os_link_impl, os_listxattr_impl, os_lockf_impl, os_major_impl, os_makedev_impl, os_minor_impl, os_mkdir_impl, os_mkfifo_impl, os_mknod_impl, os_pathconf_impl, os_posix_fadvise_impl, os_posix_fallocate_impl, os_readlink_impl, os_remove_impl, os_removexattr_impl, os_rename_impl, os_replace_impl, os_rmdir_impl, os_setxattr_impl, os_symlink_impl, os_sync_impl, os_truncate_impl, os_umask_impl, os_unlink_impl, os_utime_impl }
    modules.posix_files_platform --> modules.posix_files { MODE_T_MASK, PLATFORM, chflags_call, dev_major, dev_makedev, dev_minor, lchflags_call, lchmod_call, mkfifoat_available, mkfifoat_call, mknod_call, mknodat_available, mknodat_call, posix_fadvise_call, posix_fallocate_call, umask_call, xattr_get, xattr_list, xattr_remove, xattr_set }
    modules.posix_ids --> bindings.posix { posix_ids_exec }
    modules.posix_ids --> modules.posix { os__create_environ_impl, os__inputhook_impl, os__is_inputhook_installed_impl, os_confstr_impl, os_cpu_count_impl, os_fspath_impl, os_getegid_impl, os_geteuid_impl, os_getgid_impl, os_getgrouplist_darwin_impl, os_getgrouplist_linux_impl, os_getgroups_impl, os_getlogin_impl, os_getpgid_impl, os_getpgrp_impl, os_getpid_impl, os_getppid_impl, os_getrandom_impl, os_getresgid_impl, os_getresuid_impl, os_getsid_impl, os_getuid_impl, os_initgroups_darwin_impl, os_initgroups_linux_impl, os_putenv_impl, os_setegid_impl, os_seteuid_impl, os_setgid_impl, os_setgroups_impl, os_setpgid_impl, os_setpgrp_impl, os_setregid_impl, os_setresgid_impl, os_setresuid_impl, os_setreuid_impl, os_setsid_impl, os_setuid_impl, os_strerror_impl, os_sysconf_impl, os_tcgetpgrp_impl, os_tcsetpgrp_impl, os_uname_impl, os_unsetenv_impl, os_urandom_impl }
    modules.posix_ids_platform --> modules.posix_ids { LOGIN_NAME_SIZE, UTSNAME_FIELD_SIZE, UTSNAME_SIZE, get_res_gid, get_res_uid, getgrouplist_darwin, getgrouplist_linux, getrandom_syscall, initgroups_darwin, initgroups_linux, set_groups, setresgid, setresuid }
    modules.posix_platform --> bindings.posix { PLATFORM, runtime_function }
    modules.posix_platform --> modules.posix_core { DEV_T_SIGNED_32, environment_table, fildes_call }
    modules.posix_platform --> modules.posix_files { DEV_T_SIGNED_32 }
    modules.posix_platform --> modules.posix_process { environment_table }
    modules.posix_process --> bindings.posix { posix_process_exec, sched_param_reduce }
    modules.posix_process --> modules.posix { os_WCOREDUMP_impl, os_WEXITSTATUS_impl, os_WIFCONTINUED_impl, os_WIFEXITED_impl, os_WIFSIGNALED_impl, os_WIFSTOPPED_impl, os_WSTOPSIG_impl, os_WTERMSIG_impl, os__exit_impl, os_abort_impl, os_execv_impl, os_execve_impl, os_fork1_impl, os_fork_impl, os_forkpty_impl, os_getloadavg_impl, os_getpriority_impl, os_kill_impl, os_killpg_impl, os_nice_impl, os_pidfd_open_impl, os_posix_spawn_impl, os_posix_spawnp_impl, os_register_at_fork_impl, os_sched_get_priority_max_impl, os_sched_get_priority_min_impl, os_sched_getaffinity_impl, os_sched_getparam_impl, os_sched_getscheduler_impl, os_sched_param_impl, os_sched_rr_get_interval_impl, os_sched_setaffinity_impl, os_sched_setparam_impl, os_sched_setscheduler_impl, os_sched_yield_impl, os_setns_impl, os_setpriority_impl, os_system_impl, os_times_impl, os_unshare_impl, os_wait3_impl, os_wait4_impl, os_wait_impl, os_waitid_impl, os_waitpid_impl, os_waitstatus_to_exitcode_impl }
    modules.posix_process_platform --> modules.posix_process { FILE_ACTIONS_SIZE, SIGSET_SIZE, SPAWNATTR_SIZE, WCOREDUMP, WEXITSTATUS, WIFCONTINUED, WIFEXITED, WIFSIGNALED, WIFSTOPPED, WSTOPSIG, WTERMSIG, cpu_alloc, cpu_alloc_size, cpu_count_s, cpu_free, cpu_isset_s, cpu_set_s, cpu_zero_s, fexecve_call, fork_one, get_number_of_os_threads, mode_bits, pidfd_open_call, process_times, sched_getaffinity_call, sched_getparam_call, sched_getscheduler_call, sched_rr_get_interval_call, sched_setaffinity_call, sched_setparam_call, sched_setscheduler_call, setns_call, siginfo_t, spawnattr_setschedparam, spawnattr_setschedpolicy, unshare_call }
    modules.posix_stat --> bindings.posix { DIR_ENTRY_MEMBERS, DIR_ENTRY_RECORD_SIZE, DirEntry_dealloc, DirEntry_repr, DirEntry_token, ScandirIterator_close, ScandirIterator_dealloc, ScandirIterator_enter, ScandirIterator_exit, ScandirIterator_finalize, ScandirIterator_iternext, ScandirIterator_token, posix_stat_exec }
    modules.posix_stat --> modules.posix { DirEntry_token, os_DirEntry___fspath___impl, os_DirEntry_inode_impl, os_DirEntry_is_dir_impl, os_DirEntry_is_file_impl, os_DirEntry_is_junction_impl, os_DirEntry_is_symlink_impl, os_DirEntry_stat_impl, os_fstat_impl, os_fstatvfs_impl, os_listdir_impl, os_lstat_impl, os_scandir_impl, os_stat_impl, os_statvfs_impl }
    modules.posix_stat_platform --> modules.posix_stat { STATVFS_RECORD_SIZE, STAT_EXTRA_FIELDS, set_stat_extra, stat_blksize, stat_device, stat_mode, stat_nlink, stat_rdev, statvfs_fd, statvfs_path, statvfs_result }
    modules.posixshmem --> bindings.clinic.posixshmem { _posixshmem_shm_open_impl, _posixshmem_shm_unlink_impl }
    modules.posixsubprocess --> bindings.clinic.posixsubprocess { subprocess_fork_exec_impl }
    modules.posixsubprocess_constants --> bindings.posixsubprocess { CONSTANTS }
    modules.posixsubprocess_constants --> modules.posixsubprocess { ENOENT, ENOTDIR, NGROUPS_MAX }
    modules.posixsubprocess_constants --> modules.posixsubprocess_fds { _SC_OPEN_MAX }
    modules.posixsubprocess_platform --> bindings.posixsubprocess { PLATFORM }
    modules.posixsubprocess_platform --> modules.posixsubprocess { DIRENT_BUFFER_SIZE, FD_DIR, SIGACTION_SIZE, SIGSET_SIZE, VFORK_USABLE, block_signals, close_open_fds, reset_signal_handlers, set_groups, set_signal_mask, set_umask }
    modules.pyexpat --> bindings.clinic.pyexpat { pyexpat_ErrorString_impl, pyexpat_ParserCreate_impl, pyexpat_xmlparser_ExternalEntityParserCreate_impl, pyexpat_xmlparser_GetBase_impl, pyexpat_xmlparser_GetInputContext_impl, pyexpat_xmlparser_GetReparseDeferralEnabled_impl, pyexpat_xmlparser_ParseFile_impl, pyexpat_xmlparser_Parse_impl, pyexpat_xmlparser_SetAllocTrackerActivationThreshold_impl, pyexpat_xmlparser_SetAllocTrackerMaximumAmplification_impl, pyexpat_xmlparser_SetBase_impl, pyexpat_xmlparser_SetBillionLaughsAttackProtectionActivationThreshold_impl, pyexpat_xmlparser_SetBillionLaughsAttackProtectionMaximumAmplification_impl, pyexpat_xmlparser_SetParamEntityParsing_impl, pyexpat_xmlparser_SetReparseDeferralEnabled_impl, pyexpat_xmlparser_UseForeignDTD_impl, xmlparser_token }
    modules.pyexpat --> bindings.pyexpat { HANDLER_NAMES, PyexpatState, XMLPARSER_MEMBERS, XMLPARSER_RECORD_SIZE, add_errors_module, add_features, add_model_module, add_version, module_definition, new_capsule, xmlparse_ErrorByteIndex_getter, xmlparse_ErrorCode_getter, xmlparse_ErrorColumnNumber_getter, xmlparse_ErrorLineNumber_getter, xmlparse_buffer_size_getter, xmlparse_buffer_size_setter, xmlparse_buffer_text_getter, xmlparse_buffer_text_setter, xmlparse_buffer_used_getter, xmlparse_clear, xmlparse_dealloc, xmlparse_handler_getter, xmlparse_handler_setter, xmlparse_namespace_prefixes_getter, xmlparse_namespace_prefixes_setter, xmlparse_ordered_attributes_getter, xmlparse_ordered_attributes_setter, xmlparse_specified_attributes_getter, xmlparse_specified_attributes_setter, xmlparse_traverse, xmlparser_token }
    modules.queue --> bindings.clinic.queue { SimpleQueue_token, _queue_SimpleQueue_empty_impl, _queue_SimpleQueue_get_impl, _queue_SimpleQueue_get_nowait_impl, _queue_SimpleQueue_put_impl, _queue_SimpleQueue_put_nowait_impl, _queue_SimpleQueue_qsize_impl, simplequeue_new_impl }
    modules.queue --> bindings.queue { SimpleQueue_token }
    modules.random --> bindings.clinic.random { Random_token, _random_Random_getrandbits_impl, _random_Random_getstate_impl, _random_Random_random_impl, _random_Random_seed_impl, _random_Random_setstate_impl, random_init_impl }
    modules.random --> bindings.random { Random_token }
    modules.resource_records --> modules.posix_process { rusage, timeval }
    modules.resource_records --> modules.time { rusage }
    modules.select --> bindings.clinic.select { EPOLLIN, EPOLLOUT, EPOLLPRI, POLLIN, POLLOUT, POLLPRI, kqueue_token, select_devpoll_close_impl, select_devpoll_fileno_impl, select_devpoll_impl, select_devpoll_modify_impl, select_devpoll_poll_impl, select_devpoll_register_impl, select_devpoll_unregister_impl, select_epoll___enter___impl, select_epoll___exit___impl, select_epoll_close_impl, select_epoll_fileno_impl, select_epoll_fromfd_impl, select_epoll_impl, select_epoll_modify_impl, select_epoll_poll_impl, select_epoll_register_impl, select_epoll_unregister_impl, select_kqueue_close_impl, select_kqueue_control_impl, select_kqueue_fileno_impl, select_kqueue_fromfd_impl, select_kqueue_impl, select_poll_impl, select_poll_modify_impl, select_poll_poll_impl, select_poll_register_impl, select_poll_unregister_impl, select_select_impl }
    modules.select --> bindings.select { SelectState, epoll_closed_get, epoll_internal_close, epoll_of, epoll_token, have_broken_poll, kevent_token, kqueue_closed_get, kqueue_event_init, kqueue_event_new, kqueue_event_repr, kqueue_event_richcompare, kqueue_finalize, kqueue_token, module_definition, poll_token }
    modules.select_constants --> bindings.select { CONSTANTS, PLATFORM }
    modules.select_constants --> modules.select { EPOLLIN, EPOLLOUT, EPOLLPRI, EPOLL_CLOEXEC, EPOLL_CTL_ADD, EPOLL_CTL_DEL, EPOLL_CTL_MOD, FD_SETSIZE, KQ_EV_ADD, KQ_FILTER_READ, POLLIN, POLLNVAL, POLLOUT, POLLPRI }
    modules.select_platform --> bindings.select { HAS_EPOLL, HAS_KQUEUE, KEVENT_MEMBERS, KEVENT_SIZE, PROBE_BROKEN_POLL }
    modules.select_platform --> modules.select { EPOLL_DATA_OFFSET, EPOLL_EVENT_SIZE, KEVENT_MEMBERS, KEVENT_SIZE, epoll_create1, epoll_ctl, epoll_wait, kevent, kevent_record, kqueue, poll_fds, pollfd, select }
    modules.semaphore_platform --> bindings.multiprocessing { HAVE_BROKEN_SEM_GETVALUE, HAVE_BROKEN_SEM_UNLINK, HAVE_SEM_OPEN, HAVE_SEM_TIMEDWAIT }
    modules.semaphore_platform --> modules.multiprocessing { HAVE_BROKEN_SEM_GETVALUE, HAVE_SEM_TIMEDWAIT, SEM_FAILED, timed_wait, timespec, timeval, timeval_from, timeval_usec }
    modules.socket --> bindings.clinic.socket { _socket_htonl_impl, _socket_htons_impl, _socket_if_indextoname_impl, _socket_if_nametoindex_impl, _socket_inet_aton_impl, _socket_inet_ntoa_impl, _socket_ntohl_impl, _socket_ntohs_impl, _socket_socket_close_impl, convert__PyLong_NetIfindex_Converter, sock_initobj_impl }
    modules.socket --> bindings.socket { netdb_lock, socket_CMSG_LEN, socket_CMSG_SPACE, socket_close, socket_dup, socket_getaddrinfo, socket_getdefaulttimeout, socket_gethostbyaddr, socket_gethostbyname, socket_gethostbyname_ex, socket_gethostname, socket_getnameinfo, socket_getprotobyname, socket_getservbyname, socket_getservbyport, socket_if_nameindex, socket_inet_ntop, socket_inet_pton, socket_setdefaulttimeout, socket_sethostname, socket_socketpair }
    modules.socket_address --> bindings.ssl { new_view }
    modules.socket_address --> modules.socket { free_addrbuf, freeaddrinfo, get_u16, getaddrinfo, make_ipv4_addr, make_ipv6_addr, makesockaddr, new_addrbuf, new_view, put_u32, setipaddr }
    modules.socket_address --> modules.socket_object { free_addrbuf, get_u32, getsockaddrarg, getsockaddrlen, makesockaddr, new_addrbuf, new_view, put_u32 }
    modules.socket_address --> modules.ssl { new_view }
    modules.socket_constants --> bindings.socket { CONSTANTS }
    modules.socket_constants --> modules.socket { AF_INET, AF_INET6, AF_UNIX, AF_UNSPEC, AI_NUMERICHOST, AI_NUMERICSERV, IF_NAMESIZE, INET6_ADDRSTRLEN, NI_MAXHOST, NI_MAXSERV, SOCK_CLOEXEC, SOCK_DGRAM, SOCK_STREAM }
    modules.socket_constants --> modules.socket_address { AF_ALG, AF_CAN, AF_INET, AF_INET6, AF_NETLINK, AF_PACKET, AF_QIPCRTR, AF_RDS, AF_SYSTEM, AF_SYS_CONTROL, AF_TIPC, AF_UNIX, AF_UNSPEC, AF_VSOCK, AI_PASSIVE, CAN_BCM, CAN_ISOTP, CAN_J1939, CAN_RAW, CTLIOCGINFO, INADDR_BROADCAST, INET6_ADDRSTRLEN, INET_ADDRSTRLEN, PACKET_HOST, PF_SYSTEM, SIOCGIFINDEX, SIOCGIFNAME, SOCK_DGRAM, SYSPROTO_CONTROL, TIPC_ADDR_ID, TIPC_ADDR_NAME, TIPC_ADDR_NAMESEQ, TIPC_CLUSTER_SCOPE }
    modules.socket_constants --> modules.socket_core { EAI_SYSTEM, FIONBIO, POLLERR, POLLIN, POLLOUT, SOCK_CLOEXEC, SOCK_NONBLOCK }
    modules.socket_constants --> modules.socket_object { AF_ALG, AF_INET, AF_UNSPEC, AF_VSOCK, ALG_SET_AEAD_ASSOCLEN, ALG_SET_IV, ALG_SET_OP, SCM_RIGHTS, SOCK_CLOEXEC, SOCK_STREAM, SOL_ALG, SOL_SOCKET, SOMAXCONN, SO_ERROR, SO_PROTOCOL, SO_TYPE }
    modules.socket_constants --> modules.ssl_core { POLLIN, POLLOUT }
    modules.socket_core --> bindings.socket { STATE_COUNT, STATE_GAIERROR, STATE_HERROR, STATE_SOCK_TYPE, SocketState, socket_module_token }
    modules.socket_core --> modules.socket { INT_MAX, INVALID_SOCKET, SOCKADDR_IN6_SIZE, SOCKADDR_IN_SIZE, SOCK_ADDR_SIZE, TIMEOUT_ERROR, close, hostent, htonl, htons, if_nameindex_record, new_sockobject, ntohl, ntohs, set_error, set_gaierror, set_herror, sock_cloexec_works, socket_error, socket_parse_timeout, socket_state, timeout_object }
    modules.socket_core --> modules.socket_address { SOCKADDR_IN6_SIZE, SOCKADDR_IN_SIZE, SOCK_ADDR_SIZE, get_sock_fd, htonl, htons, ioctl, module_of, ntohl, ntohs, set_error, set_gaierror, sock_family, sock_proto, socket_error }
    modules.socket_core --> modules.socket_object { INT_MAX, INVALID_SOCKET, SEC_TO_NS, SOCKLEN_T_LIMIT, SOCK_ADDR_SIZE, SocketCall, TIMEOUT_ERROR, accept4_works, close, get_sock_fd, init_sockobject, internal_setblocking, module_of_type, set_error, set_sock_fd, set_sock_timeout, sock_call, sock_call_ex, sock_cloexec_works, sock_family, sock_of, sock_proto, sock_timeout, socket_error, socket_parse_timeout, timeout_object }
    modules.socket_core --> modules.ssl_core { poll, pollfd }
    modules.socket_object --> bindings.socket { sock_accept, sock_bind, sock_connect, sock_connect_ex, sock_dealloc, sock_detach, sock_fileno, sock_finalize, sock_getblocking, sock_getpeername, sock_getsockname, sock_getsockopt, sock_gettimeout_getter, sock_gettimeout_method, sock_listen, sock_new, sock_recv, sock_recv_into, sock_recvfrom, sock_recvfrom_into, sock_recvmsg, sock_recvmsg_into, sock_repr, sock_send, sock_sendall, sock_sendmsg, sock_sendmsg_afalg, sock_sendto, sock_setblocking, sock_setsockopt, sock_settimeout, sock_shutdown, sock_traverse }
    modules.socket_object --> modules.socket { c_int, get_CMSG_LEN, get_CMSG_SPACE, set_inheritable_new, sock_close, sock_init }
    modules.socket_platform --> bindings.socket { HAS_ALG, HAS_GETHOSTBYNAME_R, HAS_VSOCK, PLATFORM }
    modules.socket_platform --> modules.socket { HAS_GETHOSTBYNAME_R, HAS_SA_LEN, HAS_SOCK_CLOEXEC, PLATFORM, addrinfo, host_by_addr, host_by_name, host_error, set_host_name, sockaddr_family, store_sa_family, store_sa_len }
    modules.socket_platform --> modules.socket_address { HAS_ABSTRACT_UNIX, HAS_ALG, HAS_CAN, HAS_CAN_BCM, HAS_CAN_ISOTP, HAS_CAN_J1939, HAS_CAN_RAW, HAS_NETLINK, HAS_PACKET, HAS_QIPCRTR, HAS_RDS, HAS_SA_LEN, HAS_SYSTEM, HAS_TIPC, HAS_VSOCK, SOCKADDR_UN_SIZE, SUN_PATH_SIZE, addrinfo, sockaddr_family, store_sa_family, store_sa_len }
    modules.socket_platform --> modules.socket_core { HAS_SOCK_CLOEXEC, HAS_SOCK_NONBLOCK }
    modules.socket_platform --> modules.socket_object { CMSGHDR_SIZE, HAS_ACCEPT4, HAS_ALG, HAS_SOCK_CLOEXEC, HAS_SO_PROTOCOL, HAS_VSOCK, MSGHDR_SIZE, accept_cloexec, cmsg_align, cmsg_length, cmsg_nxthdr, cmsghdr, msg_controllen, msghdr, set_cmsg_length, set_msg_control, set_msg_iov, set_msg_name, sockaddr_family, store_sa_family }
    modules.sqlite3 --> bindings.clinic.sqlite3 { Connection_token, Cursor_token, LEGACY_TRANSACTION_CONTROL, Row_token, _sqlite3_Cursor_arraysize_get_impl, _sqlite3_Cursor_arraysize_set_impl, blob_close_impl, blob_enter_impl, blob_exit_impl, blob_read_impl, blob_seek_impl, blob_tell_impl, blob_write_impl, blobopen_impl, clinic_state_ConnectionType, clinic_state_PrepareProtocolType, convert_autocommit_converter, convert_isolation_level_converter, convert_sqlite3_int64_converter, create_window_function_impl, deserialize_impl, getconfig_impl, getlimit_impl, pysqlite_adapt_impl, pysqlite_complete_statement_impl, pysqlite_connection_backup_impl, pysqlite_connection_close_impl, pysqlite_connection_commit_impl, pysqlite_connection_create_aggregate_impl, pysqlite_connection_create_collation_impl, pysqlite_connection_create_function_impl, pysqlite_connection_cursor_impl, pysqlite_connection_enable_load_extension_impl, pysqlite_connection_enter_impl, pysqlite_connection_execute_impl, pysqlite_connection_executemany_impl, pysqlite_connection_executescript_impl, pysqlite_connection_exit_impl, pysqlite_connection_init_impl, pysqlite_connection_interrupt_impl, pysqlite_connection_iterdump_impl, pysqlite_connection_load_extension_impl, pysqlite_connection_rollback_impl, pysqlite_connection_set_authorizer_impl, pysqlite_connection_set_progress_handler_impl, pysqlite_connection_set_trace_callback_impl, pysqlite_cursor_close_impl, pysqlite_cursor_execute_impl, pysqlite_cursor_executemany_impl, pysqlite_cursor_executescript_impl, pysqlite_cursor_fetchall_impl, pysqlite_cursor_fetchmany_impl, pysqlite_cursor_fetchone_impl, pysqlite_cursor_init_impl, pysqlite_cursor_setinputsizes_impl, pysqlite_cursor_setoutputsize_impl, pysqlite_enable_callback_trace_impl, pysqlite_register_adapter_impl, pysqlite_register_converter_impl, pysqlite_row_keys_impl, pysqlite_row_new_impl, self_arraysize, serialize_impl, setconfig_impl, setlimit_impl, subclass_clinic_state_ConnectionType, subclass_clinic_state_CursorType }
    modules.sqlite3 --> bindings.sqlite3 { Blob_token, CONNECTION_MEMBERS, CONNECTION_RECORD_SIZE, CURSOR_MEMBERS, CURSOR_RECORD_SIZE, Connection_token, Cursor_token, ENABLE_LOAD_EXTENSION, ERROR_CODES, INTEGER_CONSTANTS, LEGACY_TRANSACTION_CONTROL, PrepareProtocol_token, Row_token, SqliteState, Statement_token, blob_ass_subscript, blob_close_on_dealloc, blob_length, blob_subscript, connection_call, connection_finalize, connection_get_autocommit, connection_get_in_transaction, connection_get_isolation_level, connection_get_row_factory, connection_get_sig, connection_get_text_factory, connection_get_total_changes, connection_set_autocommit, connection_set_isolation_level, connection_set_row_factory, connection_set_text_factory, cursor_iternext, cursor_of, cursor_self_iter, initialize_library, library_version, module_definition, prepare_protocol_init, pysqlite_connect, row_hash, row_item, row_iter, row_length, row_richcompare, row_subscript, statement_finalize, threadsafety }
    modules.sre --> bindings.clinic.sre { SRE_Pattern_token, SRE_Scanner_token, _sre_SRE_Match___copy___impl, _sre_SRE_Match___deepcopy___impl, _sre_SRE_Match_end_impl, _sre_SRE_Match_expand_impl, _sre_SRE_Match_groupdict_impl, _sre_SRE_Match_groups_impl, _sre_SRE_Match_span_impl, _sre_SRE_Match_start_impl, _sre_SRE_Pattern___copy___impl, _sre_SRE_Pattern___deepcopy___impl, _sre_SRE_Pattern_findall_impl, _sre_SRE_Pattern_finditer_impl, _sre_SRE_Pattern_fullmatch_impl, _sre_SRE_Pattern_match_impl, _sre_SRE_Pattern_scanner_impl, _sre_SRE_Pattern_search_impl, _sre_SRE_Pattern_split_impl, _sre_SRE_Pattern_sub_impl, _sre_SRE_Pattern_subn_impl, _sre_SRE_Scanner_match_impl, _sre_SRE_Scanner_search_impl, _sre_ascii_iscased_impl, _sre_ascii_tolower_impl, _sre_compile_impl, _sre_getcodesize_impl, _sre_template_impl, _sre_unicode_iscased_impl, _sre_unicode_tolower_impl }
    modules.sre --> bindings.sre { COPYRIGHT, MATCH_ENDPOS, MATCH_PATTERN, MATCH_POS, MATCH_SIZE, MATCH_STRING, PATTERN_FLAGS, PATTERN_GROUPS, PATTERN_PATTERN, PATTERN_SIZE, PATTERN_WEAKREFLIST, SCANNER_PATTERN, SCANNER_SIZE, SRE_CODE_SIZE, SRE_MAXGROUPS, SRE_Pattern_token, SRE_Scanner_token, STATE_COUNT, STATE_MATCH_TYPE, STATE_PATTERN_TYPE, STATE_SCANNER_TYPE, STATE_TEMPLATE_TYPE, TEMPLATE_ITEM_SIZE, TEMPLATE_SIZE, match_clear, match_dealloc, match_getitem, match_group, match_lastgroup_get, match_lastindex_get, match_regs_get, match_repr, match_traverse, pattern_clear, pattern_dealloc, pattern_groupindex, pattern_hash, pattern_repr, pattern_richcompare, pattern_traverse, scanner_clear, scanner_dealloc, scanner_traverse, template_clear, template_dealloc, template_traverse }
    modules.sre_constants --> bindings.sre { SRE_MAGIC }
    modules.sre_constants --> modules.sre { SRE_AT_BEGINNING, SRE_AT_BEGINNING_LINE, SRE_AT_BEGINNING_STRING, SRE_AT_BOUNDARY, SRE_AT_END, SRE_AT_END_LINE, SRE_AT_END_STRING, SRE_AT_LOC_BOUNDARY, SRE_AT_LOC_NON_BOUNDARY, SRE_AT_NON_BOUNDARY, SRE_AT_UNI_BOUNDARY, SRE_AT_UNI_NON_BOUNDARY, SRE_FLAG_ASCII, SRE_FLAG_DEBUG, SRE_FLAG_DOTALL, SRE_FLAG_IGNORECASE, SRE_FLAG_LOCALE, SRE_FLAG_MULTILINE, SRE_FLAG_UNICODE, SRE_FLAG_VERBOSE, SRE_INFO_CHARSET, SRE_INFO_LITERAL, SRE_INFO_PREFIX, SRE_OP_ANY, SRE_OP_ANY_ALL, SRE_OP_ASSERT, SRE_OP_ASSERT_NOT, SRE_OP_AT, SRE_OP_ATOMIC_GROUP, SRE_OP_BIGCHARSET, SRE_OP_BRANCH, SRE_OP_CATEGORY, SRE_OP_CHARSET, SRE_OP_FAILURE, SRE_OP_GROUPREF, SRE_OP_GROUPREF_EXISTS, SRE_OP_GROUPREF_IGNORE, SRE_OP_GROUPREF_LOC_IGNORE, SRE_OP_GROUPREF_UNI_IGNORE, SRE_OP_IN, SRE_OP_INFO, SRE_OP_IN_IGNORE, SRE_OP_IN_LOC_IGNORE, SRE_OP_IN_UNI_IGNORE, SRE_OP_JUMP, SRE_OP_LITERAL, SRE_OP_LITERAL_IGNORE, SRE_OP_LITERAL_LOC_IGNORE, SRE_OP_LITERAL_UNI_IGNORE, SRE_OP_MARK, SRE_OP_MAX_UNTIL, SRE_OP_MIN_REPEAT_ONE, SRE_OP_MIN_UNTIL, SRE_OP_NEGATE, SRE_OP_NOT_LITERAL, SRE_OP_NOT_LITERAL_IGNORE, SRE_OP_NOT_LITERAL_LOC_IGNORE, SRE_OP_NOT_LITERAL_UNI_IGNORE, SRE_OP_POSSESSIVE_REPEAT, SRE_OP_POSSESSIVE_REPEAT_ONE, SRE_OP_RANGE, SRE_OP_RANGE_UNI_IGNORE, SRE_OP_REPEAT, SRE_OP_REPEAT_ONE, SRE_OP_SUCCESS }
    modules.sre_constants --> modules.sre_ucs1 { SRE_AT_BEGINNING, SRE_AT_BEGINNING_STRING, SRE_INFO_CHARSET, SRE_INFO_LITERAL, SRE_INFO_PREFIX, SRE_OP_AT, SRE_OP_IN, SRE_OP_INFO, SRE_OP_LITERAL, SRE_OP_SUCCESS }
    modules.sre_constants --> modules.sre_ucs2 { SRE_AT_BEGINNING, SRE_AT_BEGINNING_STRING, SRE_INFO_CHARSET, SRE_INFO_LITERAL, SRE_INFO_PREFIX, SRE_OP_AT, SRE_OP_IN, SRE_OP_INFO, SRE_OP_LITERAL, SRE_OP_SUCCESS }
    modules.sre_constants --> modules.sre_ucs4 { SRE_AT_BEGINNING, SRE_AT_BEGINNING_STRING, SRE_INFO_CHARSET, SRE_INFO_LITERAL, SRE_INFO_PREFIX, SRE_OP_AT, SRE_OP_IN, SRE_OP_INFO, SRE_OP_LITERAL, SRE_OP_SUCCESS }
    modules.sre_engine --> bindings.sre { SRE_MAXREPEAT }
    modules.sre_engine --> modules.sre { SRE_ERROR_INTERRUPTED, SRE_ERROR_MEMORY, SRE_ERROR_RECURSION_LIMIT, SRE_MAXREPEAT, SRE_STATE_SIZE, SreRepeat, SreState, ascii_is_alpha, data_stack_dealloc, repeat_pool_clear, sre_lower_ascii, sre_lower_unicode, sre_upper_unicode }
    modules.sre_engine --> modules.sre_ucs1 { JUMP_ASSERT, JUMP_ASSERT_NOT, JUMP_ATOMIC_GROUP, JUMP_BRANCH, JUMP_MAX_UNTIL_1, JUMP_MAX_UNTIL_2, JUMP_MAX_UNTIL_3, JUMP_MIN_REPEAT_ONE, JUMP_MIN_UNTIL_1, JUMP_MIN_UNTIL_2, JUMP_MIN_UNTIL_3, JUMP_NONE, JUMP_POSS_REPEAT_1, JUMP_POSS_REPEAT_2, JUMP_REPEAT, JUMP_REPEAT_ONE_1, JUMP_REPEAT_ONE_2, SRE_CONTEXT_SIZE, SRE_ERROR_ILLEGAL, SRE_ERROR_INTERRUPTED, SRE_ERROR_MEMORY, SRE_ERROR_STATE, SRE_MAXREPEAT, SRE_REPEAT_LAST_PTR, SRE_REPEAT_SIZE, SreContext, SreRepeat, SreState, char_loc_ignore, data_stack_grow, sre_is_digit, sre_is_linebreak, sre_is_space, sre_is_word, sre_loc_is_word, sre_lower_ascii, sre_lower_locale, sre_lower_unicode, sre_uni_is_digit, sre_uni_is_linebreak, sre_uni_is_space, sre_uni_is_word, sre_upper_locale, sre_upper_unicode }
    modules.sre_engine --> modules.sre_ucs2 { JUMP_ASSERT, JUMP_ASSERT_NOT, JUMP_ATOMIC_GROUP, JUMP_BRANCH, JUMP_MAX_UNTIL_1, JUMP_MAX_UNTIL_2, JUMP_MAX_UNTIL_3, JUMP_MIN_REPEAT_ONE, JUMP_MIN_UNTIL_1, JUMP_MIN_UNTIL_2, JUMP_MIN_UNTIL_3, JUMP_NONE, JUMP_POSS_REPEAT_1, JUMP_POSS_REPEAT_2, JUMP_REPEAT, JUMP_REPEAT_ONE_1, JUMP_REPEAT_ONE_2, SRE_CONTEXT_SIZE, SRE_ERROR_ILLEGAL, SRE_ERROR_INTERRUPTED, SRE_ERROR_MEMORY, SRE_ERROR_STATE, SRE_MAXREPEAT, SRE_REPEAT_LAST_PTR, SRE_REPEAT_SIZE, SreContext, SreRepeat, SreState, char_loc_ignore, data_stack_grow, sre_is_digit, sre_is_linebreak, sre_is_space, sre_is_word, sre_loc_is_word, sre_lower_ascii, sre_lower_locale, sre_lower_unicode, sre_uni_is_digit, sre_uni_is_linebreak, sre_uni_is_space, sre_uni_is_word, sre_upper_locale, sre_upper_unicode }
    modules.sre_engine --> modules.sre_ucs4 { JUMP_ASSERT, JUMP_ASSERT_NOT, JUMP_ATOMIC_GROUP, JUMP_BRANCH, JUMP_MAX_UNTIL_1, JUMP_MAX_UNTIL_2, JUMP_MAX_UNTIL_3, JUMP_MIN_REPEAT_ONE, JUMP_MIN_UNTIL_1, JUMP_MIN_UNTIL_2, JUMP_MIN_UNTIL_3, JUMP_NONE, JUMP_POSS_REPEAT_1, JUMP_POSS_REPEAT_2, JUMP_REPEAT, JUMP_REPEAT_ONE_1, JUMP_REPEAT_ONE_2, SRE_CONTEXT_SIZE, SRE_ERROR_ILLEGAL, SRE_ERROR_INTERRUPTED, SRE_ERROR_MEMORY, SRE_ERROR_STATE, SRE_MAXREPEAT, SRE_REPEAT_LAST_PTR, SRE_REPEAT_SIZE, SreContext, SreRepeat, SreState, char_loc_ignore, data_stack_grow, sre_is_digit, sre_is_linebreak, sre_is_space, sre_is_word, sre_loc_is_word, sre_lower_ascii, sre_lower_locale, sre_lower_unicode, sre_uni_is_digit, sre_uni_is_linebreak, sre_uni_is_space, sre_uni_is_word, sre_upper_locale, sre_upper_unicode }
    modules.sre_locale --> modules.sre_engine { sre_isalnum, sre_tolower, sre_toupper }
    modules.sre_ucs1 --> modules.sre { sre_match as ucs1_match, sre_search as ucs1_search }
    modules.sre_ucs2 --> modules.sre { sre_match as ucs2_match, sre_search as ucs2_search }
    modules.sre_ucs4 --> modules.sre { sre_match as ucs4_match, sre_search as ucs4_search }
    modules.ssl --> bindings.clinic.ssl { MemoryBIO_token, PY_SSL_ENCODING_PEM, _SSLContext_token, _ssl_Certificate_get_info_impl, _ssl_Certificate_public_bytes_impl, _ssl_MemoryBIO_eof_get_impl, _ssl_MemoryBIO_impl, _ssl_MemoryBIO_pending_get_impl, _ssl_MemoryBIO_read_impl, _ssl_MemoryBIO_write_eof_impl, _ssl_MemoryBIO_write_impl, _ssl_RAND_add_impl, _ssl_RAND_bytes_impl, _ssl_RAND_status_impl, _ssl_SSLSession_has_ticket_get_impl, _ssl_SSLSession_id_get_impl, _ssl_SSLSession_ticket_lifetime_hint_get_impl, _ssl_SSLSession_time_get_impl, _ssl_SSLSession_timeout_get_impl, _ssl__SSLContext__host_flags_get_impl, _ssl__SSLContext__host_flags_set_impl, _ssl__SSLContext__set_alpn_protocols_impl, _ssl__SSLContext__wrap_bio_impl, _ssl__SSLContext__wrap_socket_impl, _ssl__SSLContext_cert_store_stats_impl, _ssl__SSLContext_check_hostname_get_impl, _ssl__SSLContext_check_hostname_set_impl, _ssl__SSLContext_get_ca_certs_impl, _ssl__SSLContext_get_ciphers_impl, _ssl__SSLContext_impl, _ssl__SSLContext_load_cert_chain_impl, _ssl__SSLContext_load_dh_params_impl, _ssl__SSLContext_load_verify_locations_impl, _ssl__SSLContext_maximum_version_get_impl, _ssl__SSLContext_maximum_version_set_impl, _ssl__SSLContext_minimum_version_get_impl, _ssl__SSLContext_minimum_version_set_impl, _ssl__SSLContext_num_tickets_get_impl, _ssl__SSLContext_num_tickets_set_impl, _ssl__SSLContext_options_get_impl, _ssl__SSLContext_options_set_impl, _ssl__SSLContext_protocol_get_impl, _ssl__SSLContext_security_level_get_impl, _ssl__SSLContext_session_stats_impl, _ssl__SSLContext_set_ciphers_impl, _ssl__SSLContext_set_default_verify_paths_impl, _ssl__SSLContext_set_ecdh_curve_impl, _ssl__SSLContext_set_psk_client_callback_impl, _ssl__SSLContext_set_psk_server_callback_impl, _ssl__SSLContext_sni_callback_get_impl, _ssl__SSLContext_sni_callback_set_impl, _ssl__SSLContext_verify_flags_get_impl, _ssl__SSLContext_verify_flags_set_impl, _ssl__SSLContext_verify_mode_get_impl, _ssl__SSLContext_verify_mode_set_impl, _ssl__SSLSocket_cipher_impl, _ssl__SSLSocket_compression_impl, _ssl__SSLSocket_context_get_impl, _ssl__SSLSocket_context_set_impl, _ssl__SSLSocket_do_handshake_impl, _ssl__SSLSocket_get_channel_binding_impl, _ssl__SSLSocket_get_unverified_chain_impl, _ssl__SSLSocket_get_verified_chain_impl, _ssl__SSLSocket_getpeercert_impl, _ssl__SSLSocket_owner_get_impl, _ssl__SSLSocket_owner_set_impl, _ssl__SSLSocket_pending_impl, _ssl__SSLSocket_selected_alpn_protocol_impl, _ssl__SSLSocket_server_hostname_get_impl, _ssl__SSLSocket_server_side_get_impl, _ssl__SSLSocket_session_get_impl, _ssl__SSLSocket_session_reused_get_impl, _ssl__SSLSocket_session_set_impl, _ssl__SSLSocket_shared_ciphers_impl, _ssl__SSLSocket_shutdown_impl, _ssl__SSLSocket_verify_client_post_handshake_impl, _ssl__SSLSocket_version_impl, _ssl__SSLSocket_write_impl, _ssl__test_decode_cert_impl, _ssl_get_default_verify_paths_impl, _ssl_nid2obj_impl, _ssl_txt2obj_impl, subclass_get_state_ctx_self_PySSLMemoryBIO_Type, subclass_get_state_ctx_self_Sock_Type }
    modules.ssl --> bindings.ssl { PY_SSL_ENCODING_DER, PY_SSL_ENCODING_PEM, certificate_hash, certificate_repr, certificate_richcompare, context_get_keylog_filename, context_get_msg_callback, context_get_post_handshake_auth, context_set_keylog_filename, context_set_msg_callback, context_set_post_handshake_auth, session_richcompare, ssl_socket_read, version_constants }
    modules.ssl_cert --> modules.ssl { asn1obj2py, bytes_from_bio, certificate_from_x509, certificate_to_der, certificates_from_stack, decode_certificate, pem_errors, type_name_address, unicode_from_bio, x509name_print }
    modules.ssl_core --> bindings.ssl { Certificate_token, HAS_SSLv3, HAS_TLSv1, HAS_TLSv1_1, HAS_TLSv1_2, HAS_TLSv1_3, HAVE_POST_HS_AUTH, MemoryBIO_token, PY_PROTO_MAXIMUM_SUPPORTED, PY_PROTO_MINIMUM_SUPPORTED, PY_PROTO_SSLv3, PY_PROTO_TLSv1, PY_PROTO_TLSv1_1, PY_PROTO_TLSv1_2, PY_PROTO_TLSv1_3, PY_SSL_CERT_NONE, PY_SSL_CERT_OPTIONAL, PY_SSL_CERT_REQUIRED, PY_SSL_DEFAULT_CIPHER_STRING, PY_SSL_ERROR_EOF, PY_SSL_ERROR_INVALID_ERROR_CODE, PY_SSL_ERROR_SSL, PY_SSL_ERROR_SYSCALL, PY_SSL_ERROR_WANT_CONNECT, PY_SSL_ERROR_WANT_READ, PY_SSL_ERROR_WANT_WRITE, PY_SSL_ERROR_WANT_X509_LOOKUP, PY_SSL_ERROR_ZERO_RETURN, PY_SSL_VERSION_SSL3, PY_SSL_VERSION_TLS, PY_SSL_VERSION_TLS1, PY_SSL_VERSION_TLS1_1, PY_SSL_VERSION_TLS1_2, PY_SSL_VERSION_TLS_CLIENT, PY_SSL_VERSION_TLS_SERVER, SSLModuleState, SSLSession_token, STATE_CERTIFICATE_TYPE, STATE_CERT_VERIFICATION_ERROR, STATE_CONTEXT_TYPE, STATE_COUNT, STATE_EOF_ERROR, STATE_ERR_CODES_TO_NAMES, STATE_LIB_CODES_TO_NAMES, STATE_MEMORY_BIO_TYPE, STATE_SESSION_TYPE, STATE_SOCKET_TYPE, STATE_SOCK_TYPE, STATE_SSL_ERROR, STATE_STR_LIBRARY, STATE_STR_REASON, STATE_STR_VERIFY_CODE, STATE_STR_VERIFY_MESSAGE, STATE_SYSCALL_ERROR, STATE_WANT_READ_ERROR, STATE_WANT_WRITE_ERROR, STATE_ZERO_RETURN_ERROR, _SSLContext_token, _SSLSocket_token, socket_of, ssl_module_token }
    modules.ssl_core --> modules.ssl { AlpnProtocols, CertificateState, HAS_SSLv3, HAS_TLSv1, HAS_TLSv1_1, HAS_TLSv1_2, HAVE_POST_HS_AUTH, INT_MAX, MemoryBIOState, MemoryBIO_token, PY_PROTO_MAXIMUM_AVAILABLE, PY_PROTO_MAXIMUM_SUPPORTED, PY_PROTO_MINIMUM_AVAILABLE, PY_PROTO_MINIMUM_SUPPORTED, PY_PROTO_SSLv3, PY_PROTO_TLSv1, PY_PROTO_TLSv1_1, PY_PROTO_TLSv1_2, PY_PROTO_TLSv1_3, PY_SSL_CERT_NONE, PY_SSL_CERT_OPTIONAL, PY_SSL_CERT_REQUIRED, PY_SSL_CLIENT, PY_SSL_DEFAULT_CIPHER_STRING, PY_SSL_ERROR_NO_SOCKET, PY_SSL_MIN_PROTOCOL, PY_SSL_SERVER, PY_SSL_VERSION_SSL2, PY_SSL_VERSION_SSL3, PY_SSL_VERSION_TLS, PY_SSL_VERSION_TLS1, PY_SSL_VERSION_TLS1_1, PY_SSL_VERSION_TLS1_2, PY_SSL_VERSION_TLS_CLIENT, PY_SSL_VERSION_TLS_SERVER, PySSL_CB_MAXLEN, SOCKET_HAS_BEEN_CLOSED, SOCKET_HAS_TIMED_OUT, SOCKET_IS_NONBLOCKING, SOCKET_OPERATION_OK, SOCKET_TOO_LARGE_FOR_SELECT, SSLContextState, SSLSessionState, SSLSession_token, SSLSocketState, STATE_CERTIFICATE_TYPE, STATE_CONTEXT_TYPE, STATE_MEMORY_BIO_TYPE, STATE_SESSION_TYPE, STATE_SOCKET_TYPE, STATE_SOCK_TYPE, STATE_SSL_ERROR, UINT_MAX, _SSLContext_token, _SSLSocket_token, certificate_of, chain_exceptions, context_of, free_octet_string, get_socket, memory_bio_of, module_native, module_of_object, module_of_socket, module_of_type, mutex_new, session_of, set_ssl_error, socket_fd, socket_of, socket_timeout, ssl_select, ssl_set_error, state_ref, type_check }
    modules.ssl_core --> modules.ssl_cert { CertificateState, Certificate_token, STATE_CERTIFICATE_TYPE, STATE_SSL_ERROR, X509_NAME_MAXLEN, set_ssl_error, state_ref }
    modules.ssl_errors --> bindings.ssl { ERROR_CODES, LIBRARY_CODES }
    modules.stat --> modules.posix_stat { S_IFDIR, S_IFLNK, S_IFMT, S_IFREG }
    modules.stat_records --> cpython_api { _Py_stat_struct }
    modules.stat_records --> modules.mmap { _Py_stat_struct }
    modules.stat_records --> modules.posix_stat { _Py_stat_struct }
    modules.stat_records --> modules.posix_stat_platform { _Py_stat_struct }
    modules.statistics --> bindings.clinic.statistics { _statistics__normal_dist_inv_cdf_impl }
    modules.struct --> bindings.clinic.struct { Struct___init___impl, Struct_iter_unpack_impl, Struct_unpack_from_impl, Struct_unpack_impl, _clearcache_impl, calcsize_impl, convert_cache_struct_converter, iter_unpack_impl, unpack_from_impl, unpack_impl }
    modules.struct --> bindings.struct { StructState, Struct_token, iterator_state, module_error, module_for, state_for, struct_module_token, unpack_iterator_token }
    modules.tee --> modules.itertools { TeeBindings, jacpy_tee_block_clear, jacpy_tee_block_count, jacpy_tee_block_field, jacpy_tee_block_init, jacpy_tee_construct, jacpy_tee_cursor_clear, jacpy_tee_cursor_field, jacpy_tee_next, jacpy_tee_split, tee_block, tee_cursor }
    modules.termios --> bindings.clinic.termios { termios_tcdrain_impl, termios_tcflow_impl, termios_tcflush_impl, termios_tcgetattr_impl, termios_tcgetwinsize_impl, termios_tcsendbreak_impl, termios_tcsetattr_impl, termios_tcsetwinsize_impl }
    modules.termios_constants --> bindings.termios { CONSTANTS }
    modules.termios_constants --> modules.termios { ICANON, NCCS, TIOCGWINSZ, TIOCSWINSZ, VMIN, VTIME }
    modules.termios_records --> bindings.termios { PLATFORM }
    modules.termios_records --> modules.termios { CC_OFFSET, TERMIOS_SIZE, flags_of, input_speed, output_speed, set_flags, set_input_speed, set_output_speed }
    modules.time --> bindings.clinic.time { convert_time_clockid_converter, time_clock_gettime_impl, time_clock_gettime_ns_impl }
    modules.time --> bindings.time { init_clock_bases, init_timezone, time_asctime, time_clock_getres, time_clock_settime, time_clock_settime_ns, time_ctime, time_get_clock_info, time_gmtime, time_localtime, time_mktime, time_monotonic, time_monotonic_ns, time_perf_counter, time_perf_counter_ns, time_process_time, time_process_time_ns, time_pthread_getcpuclockid, time_sleep, time_strftime, time_strptime, time_thread_time, time_thread_time_ns, time_time, time_time_ns, time_tzset }
    modules.time_constants --> bindings.time { CONSTANTS, PLATFORM }
    modules.time_constants --> modules.time { CLOCKS_PER_SEC, CLOCK_MONOTONIC, CLOCK_PROCESS_CPUTIME_ID, CLOCK_THREAD_CPUTIME_ID, TIMER_ABSTIME }
    modules.time_platform --> bindings.time { HAS_PTHREAD_GETCPUCLOCKID }
    modules.time_platform --> modules.time { HAS_CLOCK_NANOSLEEP, clock_nanosleep, pthread_getcpuclockid }
    modules.time_records --> cpython_api { timespec, timeval, tm }
    modules.time_records --> modules.datetime_date { tm }
    modules.time_records --> modules.datetime_datetime { tm }
    modules.time_records --> modules.datetime_format { tm }
    modules.time_records --> modules.posix_fileio { timespec }
    modules.time_records --> modules.posix_fileio_platform { timespec }
    modules.time_records --> modules.posix_files { timespec }
    modules.time_records --> modules.select { timespec, timeval }
    modules.time_records --> modules.time { timespec, timeval, tm, tms }
    modules.time_records --> modules.time_platform { timespec }
    modules.unicodedata --> bindings.clinic.unicodedata { unicodedata_UCD_bidirectional_impl, unicodedata_UCD_category_impl, unicodedata_UCD_combining_impl, unicodedata_UCD_decimal_impl, unicodedata_UCD_decomposition_impl, unicodedata_UCD_digit_impl, unicodedata_UCD_east_asian_width_impl, unicodedata_UCD_is_normalized_impl, unicodedata_UCD_lookup_impl, unicodedata_UCD_mirrored_impl, unicodedata_UCD_name_impl, unicodedata_UCD_normalize_impl, unicodedata_UCD_numeric_impl }
    modules.unicodedata --> bindings.unicodedata { UCD_token, new_previous_version, ucd_3_2_0_version, unicodedata_create_capi }
    modules.unicodedata_db --> bindings.unicodedata { UNIDATA_VERSION }
    modules.unicodedata_db --> modules.unicodedata { CHANGES_3_2_0_SHIFT, COMP_SHIFT, ChangeRecord, DECOMP_SHIFT, DatabaseRecord, NORMALIZATION_3_2_0_LENGTH, Reindex, SHIFT, TOTAL_LAST, _PyUnicode_BidirectionalNames, _PyUnicode_CategoryNames, _PyUnicode_Database_Records, _PyUnicode_EastAsianWidthNames, ucd_change_records_3_2_0, ucd_changes_3_2_0_data, ucd_changes_3_2_0_index, ucd_comp_data, ucd_comp_index, ucd_decomp_data, ucd_decomp_index1, ucd_decomp_index2, ucd_decomp_prefix, ucd_index1, ucd_index2, ucd_nfc_first, ucd_nfc_last, ucd_normalization_3_2_0 }
    modules.unicodename_db --> modules.unicodedata { DAWG_CODEPOINT_TO_POS_NOTFOUND, DAWG_CODEPOINT_TO_POS_SHIFT, DERIVED_NAME_PREFIXES_LENGTH, DERIVED_NAME_RANGES_LENGTH, NAME_MAXLEN, aliases_end, aliases_start, named_sequences_end, named_sequences_start, ucn_dawg_codepoint_to_pos_index1, ucn_dawg_codepoint_to_pos_index2, ucn_dawg_pos_to_codepoint, ucn_derived_name_prefixes, ucn_derived_name_ranges, ucn_name_aliases, ucn_named_sequence_chars, ucn_named_sequence_lengths, ucn_packed_name_dawg }
    modules.uuid --> bindings.uuid { py_uuid_generate_time_safe }
    modules.uuid_library --> bindings.uuid { HAVE_GENERATE_TIME_SAFE, HAVE_GENERATE_TIME_SAFE_STABLE_MAC, HAVE_UUID_HEADER }
    modules.uuid_library --> modules.uuid { HAVE_GENERATE_TIME_SAFE, generate_time }
    modules.zoneinfo --> bindings.clinic.zoneinfo { ZoneInfo_token, zoneinfo_ZoneInfo__unpickle_impl, zoneinfo_ZoneInfo_clear_cache_impl, zoneinfo_ZoneInfo_dst_impl, zoneinfo_ZoneInfo_from_file_impl, zoneinfo_ZoneInfo_impl, zoneinfo_ZoneInfo_no_cache_impl, zoneinfo_ZoneInfo_tzname_impl, zoneinfo_ZoneInfo_utcoffset_impl }
    modules.zoneinfo --> bindings.zoneinfo { ZoneInfoModuleState, ZoneInfo_token, datetime_import, module_definition, populate_module_state, zoneinfo_fromutc, zoneinfo_init_subclass, zoneinfo_reduce, zoneinfo_repr, zoneinfo_str }
    modules.zstd --> bindings.clinic.zstd { ZSTD_e_continue, ZSTD_e_end, _zstd_ZstdCompressor_compress_impl, _zstd_ZstdCompressor_flush_impl, _zstd_ZstdCompressor_new_impl, _zstd_ZstdCompressor_set_pledged_input_size_impl, _zstd_ZstdDecompressor_decompress_impl, _zstd_ZstdDecompressor_new_impl, _zstd_ZstdDecompressor_unused_data_get_impl, _zstd_ZstdDict_as_digested_dict_get_impl, _zstd_ZstdDict_as_prefix_get_impl, _zstd_ZstdDict_as_undigested_dict_get_impl, _zstd_ZstdDict_dict_content_get_impl, _zstd_ZstdDict_new_impl, _zstd_finalize_dict_impl, _zstd_get_frame_info_impl, _zstd_get_frame_size_impl, _zstd_get_param_bounds_impl, _zstd_set_parameter_types_impl, _zstd_train_dict_impl, convert_zstd_contentsize_converter }
    modules.zstd --> bindings.zstd { STATE_SLOTS, ZSTD_COMPRESSOR_TYPE, ZSTD_DECOMPRESSOR_TYPE, ZSTD_DICT_TYPE, ZSTD_ERROR, ZSTD_btlazy2, ZSTD_btopt, ZSTD_btultra, ZSTD_btultra2, ZSTD_c_chainLog, ZSTD_c_checksumFlag, ZSTD_c_compressionLevel, ZSTD_c_contentSizeFlag, ZSTD_c_dictIDFlag, ZSTD_c_enableLongDistanceMatching, ZSTD_c_hashLog, ZSTD_c_jobSize, ZSTD_c_ldmBucketSizeLog, ZSTD_c_ldmHashLog, ZSTD_c_ldmHashRateLog, ZSTD_c_ldmMinMatch, ZSTD_c_minMatch, ZSTD_c_nbWorkers, ZSTD_c_overlapLog, ZSTD_c_searchLog, ZSTD_c_strategy, ZSTD_c_targetLength, ZSTD_c_windowLog, ZSTD_d_windowLogMax, ZSTD_dfast, ZSTD_e_continue, ZSTD_e_end, ZSTD_e_flush, ZSTD_fast, ZSTD_greedy, ZSTD_lazy, ZSTD_lazy2, ZstdCompressor_token, ZstdDecompressor_token, ZstdDict_token, compressor_of, decompressor_of, release_compressor_context, release_decompressor_context, zstd_default_level, zstd_dict_id, zstd_dict_length, zstd_dict_repr, zstd_dstream_out_size, zstd_version, zstd_version_number }
    bindings.clinic.bz2 --> bindings.bz2 { BZ2Compressor_doc, BZ2Compressor_methods, BZ2Decompressor_doc, BZ2Decompressor_methods, _bz2_BZ2Compressor_new, _bz2_BZ2Decompressor_new }
    bindings.clinic.grp --> bindings.grp { module_methods }
    bindings.clinic.opcode --> bindings.opcode { module_methods }
    bindings.clinic.pwd --> bindings.pwd { module_methods }
    bindings.clinic.resource --> bindings.resource { module_methods }
    bindings.clinic.suggestions --> bindings.suggestions { module_methods }
    bindings.clinic.sysconfig --> bindings.sysconfig { module_methods }
    bindings.clinic.syslog --> bindings.syslog { module_methods }
    bindings.clinic.tracemalloc --> bindings.tracemalloc { module_methods }
    bindings.clinic.typing --> bindings.typing { module_methods }
    bindings.clinic.weakref --> bindings.weakref { module_methods }
    bindings.clinic.zlib --> bindings.zlib { Compress_methods, Decompress_methods, ZlibDecompressor_methods, module_methods }
    bindings.clinic.blake2 --> bindings.blake2 { blake2b_doc, blake2b_methods, blake2s_doc, py_blake2b_new_new, py_blake2s_new_new }
    bindings.clinic.hmac --> bindings.hmac { HMAC_getset, HMAC_methods, module_methods }
    bindings.clinic.md5 --> bindings.md5 { MD5Type_methods, module_methods }
    bindings.clinic.sha1 --> bindings.sha1 { SHA1Type_methods, module_methods }
    bindings.clinic.sha2 --> bindings.sha2 { SHA256Type_methods, SHA512Type_methods, module_methods }
    bindings.clinic.sha3 --> bindings.sha3 { py_sha3_new_new, sha3_224_methods, shake_128_methods }
    bindings.clinic.abc --> bindings.abc { module_methods }
    bindings.clinic.array --> bindings.array { array_getsets_itemsize_doc, array_getsets_typecode_doc, array_methods, array_methods___class_getitem___doc, arrayiterator_methods, arraytype_doc, module_doc, module_methods }
    bindings.clinic.asyncio --> bindings.asyncio { FutureType_methods___class_getitem___doc, Future_doc, Future_getset, Future_methods, TaskType_methods___class_getitem___doc, Task_doc, Task_getset, Task_methods, _asyncio_Future___init___init, _asyncio_Task___init___init, module_methods }
    bindings.clinic.binascii --> bindings.binascii { doc_binascii, module_methods }
    bindings.clinic.bisect --> bindings.bisect { module_doc, module_methods }
    bindings.clinic.bz2 --> bindings.bz2 { BZ2Decompressor_eof__doc__, BZ2Decompressor_needs_input_doc, BZ2Decompressor_unused_data__doc__ }
    bindings.clinic.cmath --> bindings.cmath { module_doc, module_methods }
    bindings.clinic.codecs --> bindings.codecs { module_methods }
    bindings.clinic.collections --> bindings.collections { collections_doc, defdict_class_getitem_doc, defdict_copy_doc, defdict_doc, defdict_members_default_factory_doc, defdict_missing_doc, deque_doc, deque_getset_maxlen_doc, deque_init_init, deque_methods, deque_methods___class_getitem___doc, length_hint_doc, module_methods, reduce_doc, tuplegetter_new_new }
    bindings.clinic.csv --> bindings.csv { Dialect_Type_doc, Reader_Type_doc, Writer_Type_doc, csv_module_doc, csv_reader_doc, csv_register_dialect_doc, csv_writer_doc, csv_writerow_doc, csv_writerows_doc, dialect_reduce_doc, module_methods }
    bindings.clinic.datetime --> bindings.datetime { date_methods, datetime_methods, iso_calendar_date_new_new }
    bindings.clinic.elementtree --> bindings.elementtree { Element_methods, TreeBuilder_methods, XMLParser_methods, _elementtree_TreeBuilder___init___init, _elementtree_XMLParser___init___init, module_methods }
    bindings.clinic.fcntl --> bindings.fcntl { module_methods }
    bindings.clinic.functools --> bindings.functools { _functools_doc, _lru_cache_wrapper_methods, keyobject_members_obj_doc, lru_cache_doc, module_methods, partial_doc, partial_memberlist_args_doc, partial_memberlist_func_doc, partial_memberlist_keywords_doc, partial_methods___class_getitem___doc, placeholder_doc }
    bindings.clinic.hashopenssl --> bindings.hashopenssl { HASHXOF_methods, HASH_methods, HMAC_methods, module_methods }
    bindings.clinic.heapq --> bindings.heapq { __about__, module_doc, module_methods }
    bindings.clinic.itertools --> bindings.itertools { _tee_doc, accumulate_doc, batched_doc, batched_new_new, chain_class_getitem_doc, chain_doc, chain_methods, combinations_doc, combinations_with_replacement_doc, compress_doc, count_doc, cycle_doc, dropwhile_doc, filterfalse_doc, groupby_doc, islice_doc, itertools__grouper_new, itertools__tee_new, itertools_accumulate_new, itertools_combinations_new, itertools_combinations_with_replacement_new, itertools_compress_new, itertools_count_new, itertools_cycle_new, itertools_dropwhile_new, itertools_filterfalse_new, itertools_groupby_new, itertools_permutations_new, itertools_starmap_new, itertools_takewhile_new, itertools_teedataobject_new, length_hint_doc, module_doc, module_methods, pairwise_doc, pairwise_new_new, permutations_doc, product_doc, repeat_doc, sizeof_doc, starmap_doc, takewhile_doc, teecopy_doc, teedataobject_doc, zip_longest_doc }
    bindings.clinic.json --> bindings.json { encoder_doc, encoder_members_default_doc, encoder_members_encoder_doc, encoder_members_indent_doc, encoder_members_item_separator_doc, encoder_members_key_separator_doc, encoder_members_markers_doc, encoder_members_skipkeys_doc, encoder_members_sort_keys_doc, module_doc, pydoc_encode_basestring, pydoc_encode_basestring_ascii, pydoc_scanstring, scanner_doc, scanner_members_object_hook_doc, scanner_members_parse_constant_doc, scanner_members_parse_float_doc, scanner_members_parse_int_doc, scanner_members_strict_doc }
    bindings.clinic.locale --> bindings.locale { module_methods }
    bindings.clinic.lsprof --> bindings.lsprof { Profiler_doc, Profiler_methods, profiler_init_init }
    bindings.clinic.lzma --> bindings.lzma { LZMACompressor_methods, LZMADecompressor_doc, LZMADecompressor_methods, _lzma_LZMADecompressor_new, module_methods }
    bindings.clinic.math --> bindings.math { math_acos_doc, math_acosh_doc, math_asin_doc, math_asinh_doc, math_atan2_doc, math_atan_doc, math_atanh_doc, math_cbrt_doc, math_copysign_doc, math_cos_doc, math_cosh_doc, math_erf_doc, math_erfc_doc, math_exp2_doc, math_exp_doc, math_expm1_doc, math_fabs_doc, math_gamma_doc, math_lgamma_doc, math_log1p_doc, math_log_doc, math_remainder_doc, math_sin_doc, math_sinh_doc, math_sqrt_doc, math_tan_doc, math_tanh_doc, module_doc, module_methods }
    bindings.clinic.mmap --> bindings.mmap { mmap_methods }
    bindings.clinic.multibytecodec --> bindings.multibytecodec { MultibyteCodec_methods, MultibyteIncrementalDecoder_methods, MultibyteIncrementalEncoder_methods, MultibyteStreamReader_methods, MultibyteStreamWriter_methods, module_methods }
    bindings.clinic.multiprocessing --> bindings.multiprocessing { SemLock_methods, _multiprocessing_SemLock_new, module_methods }
    bindings.clinic.operator --> bindings.operator { _operator_call__doc__, attrgetter_doc, itemgetter_doc, methodcaller_doc, module_methods, operator_doc, reduce_doc }
    bindings.clinic.pickle --> bindings.pickle { PicklerMemoProxy_methods, Pickler_doc, Pickler_methods, Pickler_methods_persistent_id_doc, UnpicklerMemoProxy_methods, Unpickler_doc, Unpickler_methods, _pickle_Pickler___init___init, _pickle_Unpickler___init___init, module_methods, pickle_module_doc }
    bindings.clinic.posix --> bindings.posix { DirEntry_methods, module_methods, module_methods_darwin, module_methods_linux, os_sched_param_new }
    bindings.clinic.posixshmem --> bindings.posixshmem { module_methods }
    bindings.clinic.posixsubprocess --> bindings.posixsubprocess { module_methods }
    bindings.clinic.pyexpat --> bindings.pyexpat { module_methods, xmlparser_methods }
    bindings.clinic.queue --> bindings.queue { SimpleQueue_doc, SimpleQueue_methods, queue_module_doc, simplequeue_methods___class_getitem___doc, simplequeue_new_new }
    bindings.clinic.random --> bindings.random { Random_methods, module_doc, random_doc, random_init_init }
    bindings.clinic.select --> bindings.select { epoll_methods, kqueue_doc, kqueue_methods, module_methods, poll_methods, select_epoll_new, select_kqueue_new }
    bindings.clinic.socket --> bindings.socket { module_methods, sock_initobj_init, socket_methods }
    bindings.clinic.sqlite3 --> bindings.sqlite3 { Blob_methods, Connection_methods, Cursor_getset, Cursor_methods, Row_methods, module_methods, pysqlite_connect_doc, pysqlite_connection_init_init, pysqlite_cursor_init_init, pysqlite_row_new_new }
    bindings.clinic.sre --> bindings.sre { SRE_Match_methods, SRE_Pattern_methods, SRE_Scanner_methods, module_methods }
    bindings.clinic.ssl --> bindings.ssl { Certificate_methods, MemoryBIO_getset, MemoryBIO_methods, SSLSession_getset, _SSLContext_getset, _SSLContext_methods, _SSLSocket_getset, _SSLSocket_methods, _ssl_MemoryBIO_new, _ssl__SSLContext_new, module_methods }
    bindings.clinic.statistics --> bindings.statistics { module_methods, statistics_doc }
    bindings.clinic.struct --> bindings.struct { Struct___init___init, Struct_methods, module_doc, module_methods, pack_doc, pack_into_doc, s__doc__, s_getsetlist_format_doc, s_getsetlist_size_doc, s_pack__doc__, s_pack_into__doc__, s_sizeof__doc__ }
    bindings.clinic.termios --> bindings.termios { module_methods }
    bindings.clinic.time --> bindings.time { module_methods }
    bindings.clinic.unicodedata --> bindings.unicodedata { UCD_methods }
    bindings.clinic.zlib --> bindings.zlib { ZlibDecompressor__new____doc__, ZlibDecompressor_eof__doc__, ZlibDecompressor_needs_input_doc, ZlibDecompressor_unused_data__doc__ }
    bindings.clinic.zoneinfo --> bindings.zoneinfo { ZoneInfo_methods, zoneinfo_ZoneInfo_new }
    bindings.clinic.zstd --> bindings.zstd { ZstdCompressor_doc, ZstdCompressor_methods, ZstdDecompressor_doc, ZstdDecompressor_getset, ZstdDecompressor_methods, ZstdDict_doc, ZstdDict_getset, _zstd_ZstdCompressor_new_new, _zstd_ZstdDecompressor_new_new, _zstd_ZstdDict_new_new, module_methods }
    object_model.bool --> bindings.converters { PyBool_FromLong }
    object_model.bool --> bindings.decimal { py_true }
    object_model.bool --> bindings.socket { py_true }
    object_model.bool --> bindings.ssl { py_false, py_true }
    object_model.bool --> bindings.stat { PyBool_FromLong }
    object_model.bool --> bindings.zlib { PyBool_FromLong }
    object_model.bool --> bindings.zstd { PyBool_FromLong }
    object_model.bool --> modules.array { PyBool_FromLong }
    object_model.bool --> modules.asyncio { py_false, py_true }
    object_model.bool --> modules.asyncio_core { py_false, py_true }
    object_model.bool --> modules.cmath { PyBool_FromLong }
    object_model.bool --> modules.collections { PyBool_FromLong }
    object_model.bool --> modules.csv { PyBool_FromLong }
    object_model.bool --> modules.datetime_datetime { PyBool_FromLong }
    object_model.bool --> modules.datetime_objects { PyBool_FromLong }
    object_model.bool --> modules.datetime_time { PyBool_FromLong }
    object_model.bool --> modules.decimal_number { PyBool_FromLong }
    object_model.bool --> modules.decimal_objects { PyBool_FromLong }
    object_model.bool --> modules.functools { PyBool_FromLong }
    object_model.bool --> modules.hashlib { PyBool_FromLong }
    object_model.bool --> modules.json { PyBool_FromLong }
    object_model.bool --> modules.lzma { PyBool_FromLong }
    object_model.bool --> modules.math { PyBool_FromLong }
    object_model.bool --> modules.multiprocessing { PyBool_FromLong }
    object_model.bool --> modules.operator { PyBool_FromLong }
    object_model.bool --> modules.pickle { PyBool_FromLong }
    object_model.bool --> modules.pickle_decode { PyBool_FromLong }
    object_model.bool --> modules.posix_ids { PyBool_FromLong }
    object_model.bool --> modules.pyexpat { PyBool_FromLong }
    object_model.bool --> modules.socket_object { py_false, py_true }
    object_model.bool --> modules.sqlite3 { PyBool_FromLong }
    object_model.bool --> modules.sre { PyBool_FromLong }
    object_model.bool --> modules.ssl { PyBool_FromLong }
    object_model.bool --> modules.struct { PyBool_FromLong }
    object_model.bool --> modules.time { PyBool_FromLong }
    object_model.bool --> modules.tracemalloc { PyBool_FromLong }
    object_model.bool --> modules.unicodedata { PyBool_FromLong }
    object_model.bool --> object_model.file { PyBool_FromLong, bool_check }
    object_model.bool --> object_model.range { bool_check }
    object_model.capsule --> bindings.datetime { PyCapsule_New }
    object_model.capsule --> bindings.socket { PyCapsule_GetPointer, PyCapsule_New, _PyCapsule_SetTraverse }
    object_model.capsule --> bindings.ssl { PyCapsule_Import }
    object_model.capsule --> modules.cjkcodecs { PyCapsule_GetPointer, PyCapsule_IsValid, PyCapsule_New }
    object_model.capsule --> modules.elementtree { PyCapsule_GetPointer }
    object_model.capsule --> modules.multibytecodec { PyCapsule_GetPointer, PyCapsule_IsValid }
    object_model.capsule --> modules.pyexpat { PyCapsule_GetPointer, PyCapsule_New }
    object_model.capsule --> modules.unicodedata { PyCapsule_New }
    object_model.capsule --> modules.zoneinfo { PyCapsule_Import }
    object_model.complex --> bindings.cmath { PyComplex_FromDoubles }
    object_model.complex --> constant_input { PyComplex_ImagAsDouble, PyComplex_RealAsDouble }
    object_model.complex --> modules.cmath { PyComplex_FromDoubles, PyComplex_ImagAsDouble, PyComplex_RealAsDouble, _Py_c_abs }
    object_model.complex --> modules.decimal_convert { PyComplex_AsCComplex }
    object_model.complex --> modules.decimal_number { PyComplex_FromDoubles }
    object_model.complex --> modules.struct { PyComplex_FromDoubles, PyComplex_ImagAsDouble, PyComplex_RealAsDouble }
    object_model.file --> bindings.converters { PyObject_AsFileDescriptor }
    object_model.file --> modules.select { PyObject_AsFileDescriptor }
    object_model.genericalias --> bindings.array { Py_GenericAlias }
    object_model.genericalias --> bindings.asyncio { Py_GenericAlias }
    object_model.genericalias --> bindings.collections { Py_GenericAlias }
    object_model.genericalias --> bindings.functools { Py_GenericAlias }
    object_model.genericalias --> bindings.itertools { Py_GenericAlias }
    object_model.genericalias --> bindings.posix { Py_GenericAlias }
    object_model.genericalias --> bindings.queue { Py_GenericAlias }
    object_model.genericalias --> bindings.sre { Py_GenericAlias }
    object_model.genericalias --> object_model.enumerate { Py_GenericAlias }
    object_model.genericalias --> object_model.interpolation { Py_GenericAlias }
    object_model.genericalias --> object_model.template { Py_GenericAlias }
    object_model.header --> modules.asyncio { freelist_pop, freelist_push }
    object_model.header --> modules.datetime_objects { object_type, object_type_check }
    object_model.header --> modules.decimal_context { object_type }
    object_model.header --> modules.decimal_convert { object_type }
    object_model.header --> modules.decimal_number { object_type }
    object_model.header --> modules.decimal_objects { object_type }
    object_model.header --> modules.socket_address { object_type }
    object_model.header --> modules.socket_core { object_type }
    object_model.header --> modules.socket_object { object_type }
    object_model.header --> modules.sqlite3 { object_type }
    object_model.header --> modules.sre { object_size, object_type, tuple_get_item, tuple_set_item }
    object_model.header --> object_model.bool { object_is_type }
    object_model.header --> object_model.capsule { PyType_Type, object_gc_track, object_gc_untrack, object_is_type }
    object_model.header --> object_model.cell { PyType_Type, object_gc_track, object_gc_untrack, object_is_type, object_type, rich_compare_values }
    object_model.header --> object_model.complex { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, object_is_type, object_size, object_type, object_type_check, tuple_get_item }
    object_model.header --> object_model.enumerate { PyType_Type, object_gc_untrack, object_refcount, object_size, object_type, tuple_get_item, tuple_recycle, tuple_set_item }
    object_model.header --> object_model.file { PyType_Type, _Py_FalseStruct, _Py_TrueStruct }
    object_model.header --> object_model.genericalias { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, eval_builtin, object_gc_track, object_gc_untrack, object_size, object_type, object_type_check, tuple_get_item, tuple_set_item }
    object_model.header --> object_model.interpolation { object_gc_track, object_gc_untrack, object_type }
    object_model.header --> object_model.iterator { PyType_Type, eval_builtin, object_gc_track, object_gc_untrack, object_type }
    object_model.header --> object_model.method { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, current_interp, eval_builtin, freelist_pop_in, freelist_push_in, gc_track_in, gc_untrack_in, object_decref, object_gc_is_tracked, object_gc_track, object_gc_untrack, object_is_type, object_new_ref, object_size, object_type, tuple_get_item }
    object_model.header --> object_model.namespace { PyType_Type, object_gc_untrack, object_is_type, object_type, object_type_check }
    object_model.header --> object_model.picklebuffer { object_gc_untrack, object_is_type, object_type }
    object_model.header --> object_model.range { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, eval_builtin, freelist_pop, freelist_push, object_is_type, object_size, object_type, tuple_items, tuple_set_item }
    object_model.header --> object_model.slice { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, freelist_pop, freelist_push, object_gc_track, object_gc_untrack, object_is_type, object_size, object_type }
    object_model.header --> object_model.structseq { PyType_Type, fast_items, object_decref, object_gc_track, object_gc_untrack, object_new_ref, object_size, object_type, object_xdecref, tuple_get_item, tuple_items, type_has_feature }
    object_model.header --> object_model.template { object_gc_track, object_gc_untrack, object_size, object_type, tuple_get_item, tuple_set_item }
    object_model.header --> object_model.union { PyType_Type, _Py_FalseStruct, _Py_TrueStruct, object_gc_track, object_gc_untrack, object_is_type, object_size, object_type, object_type_check, tuple_get_item }
    object_model.interpolation --> object_model.template { _PyInterpolation_GetValueRef, interpolation_check_exact }
    object_model.iterator --> modules.sre { PyCallIter_New }
    object_model.method --> bindings.functools { PyMethod_New }
    object_model.namespace --> modules.time { _PyNamespace_New }
    object_model.slice --> modules.elementtree { PySlice_AdjustIndices, PySlice_Unpack }
    object_model.slice --> modules.sqlite3 { PySlice_AdjustIndices, PySlice_Unpack }
    object_model.slice --> object_model.range { slice_check, slice_get_long_indices }
    object_model.structseq --> bindings.type { PyStructSequence_NewType, PyStructSequence_UnnamedField }
    object_model.structseq --> modules.grp { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.lsprof { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.posix_fileio { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.posix_ids { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.posix_process { PyStructSequence_GetItem, PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.posix_stat { PyStructSequence_GetItem, PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.pwd { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.resource { PyStructSequence_New, PyStructSequence_SetItem }
    object_model.structseq --> modules.time { PyStructSequence_GetItem, PyStructSequence_New, PyStructSequence_SetItem }
    object_model.union --> object_model.genericalias { _Py_union_type_or }
}
