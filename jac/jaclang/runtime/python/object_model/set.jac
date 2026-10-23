"""The set and frozenset types and their iterator: Objects/setobject.c in
native Jac.

`PySet_Type`, `PyFrozenSet_Type` and `PySetIter_Type` are C data Jac defines
under their C names, and the set C API (`PySet_New`, `PySet_Add`,
`_PySet_AddTakeRef`, `_PySet_NextEntry`, ...) is defined here under its C
names, so the evaluator and every C caller use them unchanged. The hash table
is setobject.c's: open addressing over `setentry` slots, a run of linear
probes before each perturbed jump, a static dummy key marking deleted slots,
and the eight-slot table embedded in the object for small sets.
See ../LICENSE.cpython.
"""

import from c {
    glob PyType_Type: PyTypeObject; def _PyDict_Next(
        op: ptr[PyObject],
        pos: &mut i64,
        key: &mut ptr[PyObject],
        value: &mut ptr[PyObject],
        hash: &mut i64
    ) -> i32;  def _PyDict_Contains_KnownHash(
        op: ptr[PyObject], key: ptr[PyObject], hash: i64
    ) -> i32;  def _PyErr_SetKeyError(key: ptr[PyObject]);  def Py_FatalError(
        message: str
    );  def memcmp(left: ptr, right: ptr, size: u64) -> i32;
    # setobject.c's setiterobject.
    obj setiterobject {
        has ob_base: _object,
            si_set: ptr[PyObject],
            si_used: i64,
            si_pos: i64,
            len: i64;
    }  glob:priv set_as_sequence: PySequenceMethods = PySequenceMethods(
             sq_length=set_len, sq_contains=set_contains
         ),
         set_as_number: PyNumberMethods = PyNumberMethods(
             nb_subtract=set_sub,
             nb_and=set_and,
             nb_xor=set_xor,
             nb_or=set_or,
             nb_inplace_subtract=set_isub,
             nb_inplace_and=set_iand,
             nb_inplace_xor=set_ixor,
             nb_inplace_or=set_ior
         ),
         frozenset_as_number: PyNumberMethods = PyNumberMethods(
             nb_subtract=set_sub, nb_and=set_and, nb_xor=set_xor, nb_or=set_or
         ),
         set_methods: list[PyMethodDef] = [
             PyMethodDef(
                 ml_name=ptr[u8]("add"),
                 ml_meth=ptr(set_add),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "add($self, object, /)\n--\n\n"
                     "Add an element to a set.\n\n"
                     "This has no effect if the element is already present."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("clear"),
                 ml_meth=ptr(set_clear),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "clear($self, /)\n--\n\nRemove all elements from this set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__contains__"),
                 ml_meth=ptr(set___contains__),
                 ml_flags=METH_O | METH_COEXIST,
                 ml_doc=ptr[u8](
                     "__contains__($self, object, /)\n--\n\nx.__contains__(y) <==> y in x."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("copy"),
                 ml_meth=ptr(set_copy),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8]("copy($self, /)\n--\n\nReturn a shallow copy of a set.")
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("discard"),
                 ml_meth=ptr(set_discard),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "discard($self, object, /)\n--\n\n"
                     "Remove an element from a set if it is a member.\n\n"
                     "Unlike set.remove(), the discard() method does not raise\n"
                     "an exception when an element is missing from the set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("difference"),
                 ml_meth=ptr(set_difference_multi),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "difference($self, /, *others)\n--\n\n"
                     "Return a new set with elements in the set that are not in the others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("difference_update"),
                 ml_meth=ptr(set_difference_update),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "difference_update($self, /, *others)\n--\n\n"
                     "Update the set, removing elements found in others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("intersection"),
                 ml_meth=ptr(set_intersection_multi),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "intersection($self, /, *others)\n--\n\n"
                     "Return a new set with elements common to the set and all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("intersection_update"),
                 ml_meth=ptr(set_intersection_update_multi),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "intersection_update($self, /, *others)\n--\n\n"
                     "Update the set, keeping only elements found in it and all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isdisjoint"),
                 ml_meth=ptr(set_isdisjoint),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "isdisjoint($self, other, /)\n--\n\n"
                     "Return True if two sets have a null intersection."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("issubset"),
                 ml_meth=ptr(set_issubset),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "issubset($self, other, /)\n--\n\n"
                     "Report whether another set contains this set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("issuperset"),
                 ml_meth=ptr(set_issuperset),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "issuperset($self, other, /)\n--\n\n"
                     "Report whether this set contains another set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("pop"),
                 ml_meth=ptr(set_pop),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "pop($self, /)\n--\n\n"
                     "Remove and return an arbitrary set element.\n\n"
                     "Raises KeyError if the set is empty."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce__"),
                 ml_meth=ptr(set___reduce__),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__reduce__($self, /)\n--\n\nReturn state information for pickling."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("remove"),
                 ml_meth=ptr(set_remove),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "remove($self, object, /)\n--\n\n"
                     "Remove an element from a set; it must be a member.\n\n"
                     "If the element is not a member, raise a KeyError."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__sizeof__"),
                 ml_meth=ptr(set___sizeof__),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__sizeof__($self, /)\n--\n\nS.__sizeof__() -> size of S in memory, in bytes."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("symmetric_difference"),
                 ml_meth=ptr(set_symmetric_difference),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "symmetric_difference($self, other, /)\n--\n\n"
                     "Return a new set with elements in either the set or other but not both."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("symmetric_difference_update"),
                 ml_meth=ptr(set_symmetric_difference_update),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "symmetric_difference_update($self, other, /)\n--\n\n"
                     "Update the set, keeping only elements found in either set, but not in both."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("union"),
                 ml_meth=ptr(set_union),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "union($self, /, *others)\n--\n\n"
                     "Return a new set with elements from the set and all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("update"),
                 ml_meth=ptr(set_update),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "update($self, /, *others)\n--\n\n"
                     "Update the set, adding elements from all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__class_getitem__"),
                 ml_meth=ptr(Py_GenericAlias),
                 ml_flags=METH_O | METH_CLASS,
                 ml_doc=ptr[u8]("sets are generic over the type of their elements")
             ),
             PyMethodDef(ml_name=ptr[u8](), ml_meth=ptr(), ml_flags=0, ml_doc=ptr[u8]())
         ],
         frozenset_methods: list[PyMethodDef] = [
             PyMethodDef(
                 ml_name=ptr[u8]("__contains__"),
                 ml_meth=ptr(frozenset___contains__),
                 ml_flags=METH_O | METH_COEXIST,
                 ml_doc=ptr[u8](
                     "__contains__($self, object, /)\n--\n\nx.__contains__(y) <==> y in x."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("copy"),
                 ml_meth=ptr(frozenset_copy),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8]("copy($self, /)\n--\n\nReturn a shallow copy of a set.")
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("difference"),
                 ml_meth=ptr(set_difference_multi),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "difference($self, /, *others)\n--\n\n"
                     "Return a new set with elements in the set that are not in the others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("intersection"),
                 ml_meth=ptr(set_intersection_multi),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "intersection($self, /, *others)\n--\n\n"
                     "Return a new set with elements common to the set and all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isdisjoint"),
                 ml_meth=ptr(set_isdisjoint),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "isdisjoint($self, other, /)\n--\n\n"
                     "Return True if two sets have a null intersection."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("issubset"),
                 ml_meth=ptr(set_issubset),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "issubset($self, other, /)\n--\n\n"
                     "Report whether another set contains this set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("issuperset"),
                 ml_meth=ptr(set_issuperset),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "issuperset($self, other, /)\n--\n\n"
                     "Report whether this set contains another set."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce__"),
                 ml_meth=ptr(set___reduce__),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__reduce__($self, /)\n--\n\nReturn state information for pickling."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__sizeof__"),
                 ml_meth=ptr(set___sizeof__),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__sizeof__($self, /)\n--\n\nS.__sizeof__() -> size of S in memory, in bytes."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("symmetric_difference"),
                 ml_meth=ptr(set_symmetric_difference),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "symmetric_difference($self, other, /)\n--\n\n"
                     "Return a new set with elements in either the set or other but not both."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("union"),
                 ml_meth=ptr(set_union),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "union($self, /, *others)\n--\n\n"
                     "Return a new set with elements from the set and all others."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__class_getitem__"),
                 ml_meth=ptr(Py_GenericAlias),
                 ml_flags=METH_O | METH_CLASS,
                 ml_doc=ptr[u8](
                     "frozensets are generic over the type of their elements"
                 )
             ),
             PyMethodDef(ml_name=ptr[u8](), ml_meth=ptr(), ml_flags=0, ml_doc=ptr[u8]())
         ],
         setiter_methods: list[PyMethodDef] = [
             PyMethodDef(
                 ml_name=ptr[u8]("__length_hint__"),
                 ml_meth=ptr(setiter_len),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "Private method returning an estimate of len(list(it))."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce__"),
                 ml_meth=ptr(setiter_reduce),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8]("Return state information for pickling.")
             ),
             PyMethodDef(ml_name=ptr[u8](), ml_meth=ptr(), ml_flags=0, ml_doc=ptr[u8]())
         ],
         # The type of the dummy key that marks a deleted slot.
         _PySetDummy_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("<dummy key> type"),
             tp_dealloc=dummy_dealloc,
             tp_repr=dummy_repr,
             tp_flags=Py_TPFLAGS_DEFAULT
         ),
         dummy_struct: _object = _object(
             ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
             ob_type=addressof(_PySetDummy_Type)
         ); glob PySetIter_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("set_iterator"),
             # sizeof(setiterobject): its header and four words.
             tp_basicsize=48,
             tp_dealloc=setiter_dealloc,
             tp_getattro=PyObject_GenericGetAttr,
             tp_flags=Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
             tp_traverse=setiter_traverse,
             tp_iter=PyObject_SelfIter,
             tp_iternext=setiter_iternext,
             tp_methods=addressof(setiter_methods)
         ),
         PySet_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("set"),
             tp_basicsize=PySetObject_SIZE,
             tp_dealloc=set_dealloc,
             tp_repr=set_repr,
             tp_as_number=addressof(set_as_number),
             tp_as_sequence=addressof(set_as_sequence),
             tp_hash=PyObject_HashNotImplemented,
             tp_getattro=PyObject_GenericGetAttr,
             tp_flags=Py_TPFLAGS_DEFAULT
                 | Py_TPFLAGS_HAVE_GC
                 | Py_TPFLAGS_BASETYPE
                 | _Py_TPFLAGS_MATCH_SELF,
             tp_doc=ptr[u8](
                 "set(iterable=(), /)\n--\n\n"
                 "Build an unordered collection of unique elements."
             ),
             tp_traverse=set_traverse,
             tp_clear=set_clear_internal,
             tp_richcompare=set_richcompare,
             tp_weaklistoffset=PySetObject_WEAKREFLIST,
             tp_iter=set_iter,
             tp_methods=addressof(set_methods),
             tp_init=set_init,
             tp_alloc=PyType_GenericAlloc,
             tp_new=set_new,
             tp_free=PyObject_GC_Del,
             tp_vectorcall=set_vectorcall,
             tp_version_tag=_Py_TYPE_VERSION_SET
         ),
         PyFrozenSet_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("frozenset"),
             tp_basicsize=PySetObject_SIZE,
             tp_dealloc=set_dealloc,
             tp_repr=set_repr,
             tp_as_number=addressof(frozenset_as_number),
             tp_as_sequence=addressof(set_as_sequence),
             tp_hash=frozenset_hash,
             tp_getattro=PyObject_GenericGetAttr,
             tp_flags=Py_TPFLAGS_DEFAULT
                 | Py_TPFLAGS_HAVE_GC
                 | Py_TPFLAGS_BASETYPE
                 | _Py_TPFLAGS_MATCH_SELF,
             tp_doc=ptr[u8](
                 "frozenset(iterable=(), /)\n--\n\n"
                 "Build an immutable unordered collection of unique elements."
             ),
             tp_traverse=set_traverse,
             tp_clear=set_clear_internal,
             tp_richcompare=set_richcompare,
             tp_weaklistoffset=PySetObject_WEAKREFLIST,
             tp_iter=set_iter,
             tp_methods=addressof(frozenset_methods),
             tp_alloc=PyType_GenericAlloc,
             tp_new=frozenset_new,
             tp_free=PyObject_GC_Del,
             tp_vectorcall=frozenset_vectorcall,
             tp_version_tag=_Py_TYPE_VERSION_FROZEN_SET
         ),
         # The dummy key, exported for the gdb plugin.
         _PySet_Dummy: ptr[_object] = addressof(dummy_struct);
}

glob:priv PY_SSIZE_T_MAX: i64 = 0x7FFFFFFFFFFFFFFF,
     # Probe this many consecutive slots before a perturbed jump.
     LINEAR_PROBES: u64 = u64(9),
     PERTURB_SHIFT: u64 = u64(5),
     SETENTRY_SIZE: i64 = 16,
     DISCARD_NOTFOUND: i32 = 0,
     DISCARD_FOUND: i32 = 1;

def set_of(op: ptr[PyObject]) -> ptr[PySetObject] {
    return ptr[PySetObject](op);
}

def setiter_of(op: ptr[PyObject]) -> ptr[setiterobject] {
    return ptr[setiterobject](op);
}

def no_entry -> ptr[setentry] {
    return ptr[setentry]();
}

"""The object used as the key of deleted slots."""
def dummy -> ptr[PyObject] {
    return ptr[PyObject](addressof(dummy_struct));
}

def type_of_object(type: ptr[PyObject]) -> ptr[PyTypeObject] {
    return ptr[PyTypeObject](type);
}

def set_type -> ptr[PyTypeObject] {
    return addressof(PySet_Type);
}

def frozenset_type -> ptr[PyTypeObject] {
    return addressof(PyFrozenSet_Type);
}

"""The table embedded in the set object."""
def smalltable(so: ptr[PyObject]) -> ptr[setentry] {
    return ptr[setentry](ptr[u8](so) + PySetObject_SMALLTABLE);
}

def set_table(so: ptr[PyObject]) -> ptr[setentry] {
    return set_of(so).view(1)[0].table;
}

def set_mask(so: ptr[PyObject]) -> i64 {
    return set_of(so).view(1)[0].mask;
}

"""PySet_GET_SIZE."""
def set_used(so: ptr[PyObject]) -> i64 {
    return set_of(so).view(1)[0].used;
}

def set_fill(so: ptr[PyObject]) -> i64 {
    return set_of(so).view(1)[0].fill;
}

def entry_key(slot: ptr[setentry]) -> ptr[PyObject] {
    return slot.view(1)[0].key;
}

def entry_hash(slot: ptr[setentry]) -> i64 {
    return slot.view(1)[0].hash;
}

def set_entry(slot: ptr[setentry], key: ptr[PyObject], hash: i64) {
    slot.view(1)[0].key = key;
    slot.view(1)[0].hash = hash;
}

"""PySet_Check."""
def set_check(op: ptr[PyObject]) -> bool {
    return object_is_type(op, set_type())
        or PyType_IsSubtype(ptr[PyObject](object_type(op)), ptr[PyObject](set_type()))
            != 0;
}

"""PyFrozenSet_CheckExact."""
def frozenset_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, frozenset_type());
}

"""PyFrozenSet_Check."""
def frozenset_check(op: ptr[PyObject]) -> bool {
    return frozenset_check_exact(op)
        or PyType_IsSubtype(
            ptr[PyObject](object_type(op)), ptr[PyObject](frozenset_type())
        )
            != 0;
}

"""PyAnySet_CheckExact."""
def anyset_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, set_type()) or frozenset_check_exact(op);
}

"""PyAnySet_Check."""
def anyset_check(op: ptr[PyObject]) -> bool {
    return anyset_check_exact(op) or set_check(op) or frozenset_check(op);
}

def dict_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, type_of_object(addressof(PyDict_Type)));
}

def unicode_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, type_of_object(addressof(PyUnicode_Type)));
}

"""PyDict_GET_SIZE."""
def dict_used(dict: ptr[PyObject]) -> i64 {
    return ptr[i64](ptr[u8](dict) + PyDictObject_USED).view(1)[0];
}

"""_PyObject_HashFast: an exact str's cached hash, else PyObject_Hash."""
def hash_fast(op: ptr[PyObject]) -> i64 {
    if unicode_check_exact(op) {
        hash = ptr[i64](ptr[u8](op) + PyASCIIObject_HASH).view(1)[0];
        if hash != -1 {
            return hash;
        }
    }
    return PyObject_Hash(op);
}

"""stringlib's unicode_eq, for two exact str with equal hashes."""
def unicode_eq(str1: ptr[PyObject], str2: ptr[PyObject]) -> bool {
    length = ptr[i64](ptr[u8](str1) + PyASCIIObject_LENGTH).view(1)[0];
    if ptr[i64](ptr[u8](str2) + PyASCIIObject_LENGTH).view(1)[0] != length {
        return False;
    }
    kind = jacpy_unicode_kind(str1);
    if jacpy_unicode_kind(str2) != kind {
        return False;
    }
    return memcmp(
        jacpy_unicode_data(str1), jacpy_unicode_data(str2), u64(length * kind)
    )
        == 0;
}

"""The next probe index after `i`, mixing in the hash's higher bits."""
def next_probe(i: u64, perturb: u64, mask: u64) -> u64 {
    return wrapping_add(wrapping_add(wrapping_mul(i, u64(5)), u64(1)), perturb) & mask;
}

"""The slot holding `key`, or the empty slot that ends its probe sequence;
NULL with an error set when a compare fails. A compare that changes a
mutable set restarts the search."""
def set_lookkey(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> ptr[setentry] {
    frozenset = frozenset_check_exact(so);
    while True {
        restart = False;
        mask = u64.wrap(set_mask(so));
        perturb = u64.wrap(hash);
        i = perturb & mask;
        while not restart {
            slot = set_table(so) + i64.wrap(i);
            probes = LINEAR_PROBES if i + LINEAR_PROBES <= mask else u64(0);
            while True {
                ekey = entry_key(slot);
                ehash = entry_hash(slot);
                if ehash == 0 and not ekey {
                    return slot;
                }
                if ehash == hash {
                    startkey = ekey;
                    if startkey == key {
                        return slot;
                    }
                    if unicode_check_exact(startkey)
                        and unicode_check_exact(key)
                        and unicode_eq(startkey, key) {
                        return slot;
                    }
                    table = set_table(so);
                    cmp = i32(0);
                    if frozenset {
                        cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                        if cmp < 0 {
                            return no_entry();
                        }
                    } else {
                        # The compare can remove startkey from the set.
                        object_incref(startkey);
                        cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                        object_decref(startkey);
                        if cmp < 0 {
                            return no_entry();
                        }
                        if table != set_table(so) or entry_key(slot) != startkey {
                            restart = True;
                            break;
                        }
                    }
                    if cmp > 0 {
                        return slot;
                    }
                    mask = u64.wrap(set_mask(so));
                }
                if probes == u64(0) {
                    break;
                }
                probes -= u64(1);
                slot = slot + 1;
            }
            perturb = perturb >> PERTURB_SHIFT;
            i = next_probe(i, perturb, mask);
        }
    }
    return no_entry();
}

glob:priv ADD_PROBING: i64 = 0,
     ADD_UNUSED_OR_DUMMY: i64 = 1,
     ADD_ACTIVE: i64 = 2,
     ADD_ERROR: i64 = 3,
     ADD_RESTART: i64 = 4;

"""Add `key` (stealing it) with its hash. A dummy slot found on the way is
reused; a compare that changes the set restarts the insertion."""
def set_add_entry_takeref(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> i32 {
    while True {
        mask = u64.wrap(set_mask(so));
        i = u64.wrap(hash) & mask;
        freeslot = no_entry();
        perturb = u64.wrap(hash);
        slot = no_entry();
        outcome = ADD_PROBING;
        while outcome == ADD_PROBING {
            slot = set_table(so) + i64.wrap(i);
            probes = LINEAR_PROBES if i + LINEAR_PROBES <= mask else u64(0);
            while True {
                ekey = entry_key(slot);
                ehash = entry_hash(slot);
                if ehash == 0 and not ekey {
                    outcome = ADD_UNUSED_OR_DUMMY;
                    break;
                }
                if ehash == hash {
                    startkey = ekey;
                    if startkey == key
                        or (
                            unicode_check_exact(startkey)
                            and unicode_check_exact(key)
                            and unicode_eq(startkey, key)
                        ) {
                        outcome = ADD_ACTIVE;
                        break;
                    }
                    table = set_table(so);
                    object_incref(startkey);
                    cmp = PyObject_RichCompareBool(startkey, key, Py_EQ);
                    object_decref(startkey);
                    if cmp > 0 {
                        outcome = ADD_ACTIVE;
                        break;
                    }
                    if cmp < 0 {
                        outcome = ADD_ERROR;
                        break;
                    }
                    if table != set_table(so) or entry_key(slot) != startkey {
                        outcome = ADD_RESTART;
                        break;
                    }
                    mask = u64.wrap(set_mask(so));
                } elif ehash == -1 {
                    freeslot = slot;
                }
                if probes == u64(0) {
                    break;
                }
                probes -= u64(1);
                slot = slot + 1;
            }
            if outcome == ADD_PROBING {
                perturb = perturb >> PERTURB_SHIFT;
                i = next_probe(i, perturb, mask);
            }
        }
        if outcome == ADD_RESTART {
            continue;
        }
        if outcome == ADD_ACTIVE {
            object_decref(key);
            return i32(0);
        }
        if outcome == ADD_ERROR {
            object_decref(key);
            return i32(-1);
        }
        s = set_of(so);
        if freeslot {
            # A compare may have refilled the dummy slot.
            if entry_hash(freeslot) != -1 {
                continue;
            }
            s.view(1)[0].used += 1;
            set_entry(freeslot, key, hash);
            return i32(0);
        }
        s.view(1)[0].fill += 1;
        s.view(1)[0].used += 1;
        set_entry(slot, key, hash);
        if u64.wrap(set_fill(so)) * u64(5) < mask * u64(3) {
            return i32(0);
        }
        used = set_used(so);
        return set_table_resize(so, used * 2 if used > 50000 else used * 4);
    }
    return i32(-1);
}

def set_add_entry(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> i32 {
    return set_add_entry_takeref(so, object_new_ref(key), hash);
}

"""Reword a TypeError from hashing `key` as one about a set element."""
def set_unhashable_type(key: ptr[PyObject]) {
    exc = PyErr_GetRaisedException();
    if not object_is_type(exc, type_of_object(PyExc_TypeError)) {
        PyErr_SetRaisedException(exc);
        return;
    }
    PyErr_Format(PyExc_TypeError, "cannot use '%T' as a set element (%S)", key, exc);
    object_decref(exc);
}

"""Insert a key known to be absent into a table with room and no dummies,
without compares: set_table_resize must not call back into Python
(issue 1456209). The caller counts it in fill and used."""
def set_insert_clean(table: ptr[setentry], mask: u64, key: ptr[PyObject], hash: i64) {
    perturb = u64.wrap(hash);
    i = perturb & mask;
    while True {
        slot = table + i64.wrap(i);
        if not entry_key(slot) {
            set_entry(slot, key, hash);
            return;
        }
        if i + LINEAR_PROBES <= mask {
            for j in range(9) {
                slot = slot + 1;
                if not entry_key(slot) {
                    set_entry(slot, key, hash);
                    return;
                }
            }
        }
        perturb = perturb >> PERTURB_SHIFT;
        i = next_probe(i, perturb, mask);
    }
}

"""Rebuild the table with room for more than `minused` keys, dropping the
dummies; the new table may be smaller than the old."""
def set_table_resize(so: ptr[PyObject], minused: i64) -> i32 {
    s = set_of(so);
    oldmask = set_mask(so);
    newsize = u64(PySet_MINSIZE);
    while newsize <= u64.wrap(minused) {
        newsize = newsize << u64(1);
    }
    oldtable = set_table(so);
    is_oldtable_malloced = oldtable != smalltable(so);
    small_copy = no_entry();
    newtable = no_entry();
    if newsize == u64(PySet_MINSIZE) {
        # A large table is shrinking, or the small table is rebuilt.
        newtable = smalltable(so);
        if newtable == oldtable {
            if set_fill(so) == set_used(so) {
                # No dummies to purge.
                return i32(0);
            }
            # Rebuild in place to purge dummies (required when the table is
            # full of them, since a failing search needs an empty slot).
            small_copy = ptr[setentry](
                PyMem_Malloc(u64(PySet_MINSIZE * SETENTRY_SIZE))
            );
            if not small_copy {
                PyErr_NoMemory();
                return i32(-1);
            }
            jacpy_memory_copy(
                ptr(small_copy), ptr(oldtable), PySet_MINSIZE * SETENTRY_SIZE
            );
            oldtable = small_copy;
        }
    } else {
        if newsize > u64(PY_SSIZE_T_MAX // SETENTRY_SIZE) {
            PyErr_NoMemory();
            return i32(-1);
        }
        newtable = ptr[setentry](PyMem_Malloc(newsize * u64(SETENTRY_SIZE)));
        if not newtable {
            PyErr_NoMemory();
            return i32(-1);
        }
    }
    jacpy_memory_zero(ptr(newtable), i64.wrap(newsize) * SETENTRY_SIZE);
    s.view(1)[0].mask = i64.wrap(newsize) - 1;
    s.view(1)[0].table = newtable;
    newmask = newsize - u64(1);
    # Moving active entries is refcount-neutral; dummies are dropped.
    if set_fill(so) == set_used(so) {
        for j in range(oldmask + 1) {
            slot = oldtable + j;
            if entry_key(slot) {
                set_insert_clean(newtable, newmask, entry_key(slot), entry_hash(slot));
            }
        }
    } else {
        s.view(1)[0].fill = set_used(so);
        for j in range(oldmask + 1) {
            slot = oldtable + j;
            key = entry_key(slot);
            if key and key != dummy() {
                set_insert_clean(newtable, newmask, key, entry_hash(slot));
            }
        }
    }
    if is_oldtable_malloced {
        PyMem_Free(ptr(oldtable));
    }
    if small_copy {
        PyMem_Free(ptr(small_copy));
    }
    return i32(0);
}

def set_contains_entry(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> i32 {
    slot = set_lookkey(so, key, hash);
    if slot {
        return i32(1) if entry_key(slot) else i32(0);
    }
    return i32(-1);
}

def set_discard_entry(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> i32 {
    slot = set_lookkey(so, key, hash);
    if not slot {
        return i32(-1);
    }
    old_key = entry_key(slot);
    if not old_key {
        return DISCARD_NOTFOUND;
    }
    set_entry(slot, dummy(), -1);
    set_of(so).view(1)[0].used -= 1;
    object_decref(old_key);
    return DISCARD_FOUND;
}

def set_add_key(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    hash = hash_fast(key);
    if hash == -1 {
        set_unhashable_type(key);
        return i32(-1);
    }
    return set_add_entry(so, key, hash);
}

def set_contains_key(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    hash = hash_fast(key);
    if hash == -1 {
        set_unhashable_type(key);
        return i32(-1);
    }
    return set_contains_entry(so, key, hash);
}

def set_discard_key(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    hash = hash_fast(key);
    if hash == -1 {
        set_unhashable_type(key);
        return i32(-1);
    }
    return set_discard_entry(so, key, hash);
}

def set_empty_to_minsize(so: ptr[PyObject]) {
    s = set_of(so);
    jacpy_memory_zero(ptr(smalltable(so)), PySet_MINSIZE * SETENTRY_SIZE);
    s.view(1)[0].fill = 0;
    s.view(1)[0].used = 0;
    s.view(1)[0].mask = PySet_MINSIZE - 1;
    s.view(1)[0].table = smalltable(so);
    s.view(1)[0].hash = -1;
}

"""Empty the set. Releasing a key can mutate the set, so the set is made
empty first and the old entries are released from a detached table."""
def set_clear_internal(so: ptr[PyObject]) -> i32 {
    table = set_table(so);
    fill = set_fill(so);
    used = set_used(so);
    table_is_malloced = table != smalltable(so);
    small_copy = no_entry();
    if table_is_malloced {
        set_empty_to_minsize(so);
    } elif fill > 0 {
        # A small table with something to clear: copy it out first.
        small_copy = ptr[setentry](PyMem_Malloc(u64(PySet_MINSIZE * SETENTRY_SIZE)));
        if not small_copy {
            PyErr_NoMemory();
            return i32(-1);
        }
        jacpy_memory_copy(ptr(small_copy), ptr(table), PySet_MINSIZE * SETENTRY_SIZE);
        table = small_copy;
        set_empty_to_minsize(so);
    }
    slot = table;
    while used > 0 {
        key = entry_key(slot);
        if key and key != dummy() {
            used -= 1;
            object_decref(key);
        }
        slot = slot + 1;
    }
    if table_is_malloced {
        PyMem_Free(ptr(table));
    }
    if small_copy {
        PyMem_Free(ptr(small_copy));
    }
    return i32(0);
}

"""set_next: the index of the first active slot at or after `pos`, or -1.
Not safe in a loop that mutates the table."""
def set_next(so: ptr[PyObject], pos: i64) -> i64 {
    mask = set_mask(so);
    table = set_table(so);
    i = pos;
    while i <= mask {
        key = entry_key(table + i);
        if key and key != dummy() {
            return i;
        }
        i += 1;
    }
    return -1;
}

def set_dealloc(so: ptr[PyObject]) {
    used = set_used(so);
    # bpo-31095: untrack before any callback.
    object_gc_untrack(so);
    if set_of(so).view(1)[0].weakreflist {
        PyObject_ClearWeakRefs(so);
    }
    slot = set_table(so);
    while used > 0 {
        key = entry_key(slot);
        if key and key != dummy() {
            used -= 1;
            object_decref(key);
        }
        slot = slot + 1;
    }
    if set_table(so) != smalltable(so) {
        PyMem_Free(ptr(set_table(so)));
    }
    object_type(so).view(1)[0].tp_free(ptr(so));
}

def set_repr(so: ptr[PyObject]) -> ptr[PyObject] {
    tp_name = object_type(so).view(1)[0].tp_name;
    status = Py_ReprEnter(so);
    if status != 0 {
        if status < 0 {
            return NULL;
        }
        return PyUnicode_FromFormat("%s(...)", tp_name);
    }
    if set_used(so) == 0 {
        Py_ReprLeave(so);
        return PyUnicode_FromFormat("%s()", tp_name);
    }
    # gh-129967: build the key list directly rather than through
    # PySequence_List, which could let the set be cleared meanwhile.
    result = NULL;
    keys = PyList_New(set_used(so));
    if keys {
        items = ptr[PyListObject](keys).view(1)[0].ob_item;
        pos = 0;
        idx = 0;
        while True {
            i = set_next(so, pos);
            if i < 0 {
                break;
            }
            pos = i + 1;
            (items + idx).view(1)[0] = object_new_ref(entry_key(set_table(so) + i));
            idx += 1;
        }
        # repr(keys)[1:-1]
        listrepr = PyObject_Repr(keys);
        object_decref(keys);
        if listrepr {
            inner = PyUnicode_Substring(
                listrepr,
                1,
                ptr[i64](ptr[u8](listrepr) + PyASCIIObject_LENGTH).view(1)[0] - 1
            );
            object_decref(listrepr);
            if inner {
                if not object_is_type(so, set_type()) {
                    result = PyUnicode_FromFormat("%s({%U})", tp_name, inner);
                } else {
                    result = PyUnicode_FromFormat("{%U}", inner);
                }
                object_decref(inner);
            }
        }
    }
    Py_ReprLeave(so);
    return result;
}

def set_len(so: ptr[PyObject]) -> i64 {
    return set_used(so);
}

"""Add every key of the set or frozenset `other`."""
def set_merge(so: ptr[PyObject], other: ptr[PyObject]) -> i32 {
    s = set_of(so);
    if other == so or set_used(other) == 0 {
        # a.update(a) or a.update(set()): nothing to do.
        return i32(0);
    }
    # One big resize up front, expecting few overlapping keys.
    if (set_fill(so) + set_used(other)) * 5 >= set_mask(so) * 3 {
        if set_table_resize(so, (set_used(so) + set_used(other)) * 2) != 0 {
            return i32(-1);
        }
    }
    so_table = set_table(so);
    other_table = set_table(other);
    other_mask = set_mask(other);
    # An empty table of the same size, from a table without dummies: copy
    # the slots.
    if set_fill(so) == 0
        and set_mask(so) == other_mask
        and set_fill(other) == set_used(other) {
        for i in range(other_mask + 1) {
            key = entry_key(other_table + i);
            if key {
                set_entry(
                    so_table + i, object_new_ref(key), entry_hash(other_table + i)
                );
            }
        }
        s.view(1)[0].fill = set_fill(other);
        s.view(1)[0].used = set_used(other);
        return i32(0);
    }
    # An empty table takes the keys without compares.
    if set_fill(so) == 0 {
        newmask = u64.wrap(set_mask(so));
        s.view(1)[0].fill = set_used(other);
        s.view(1)[0].used = set_used(other);
        for i in range(other_mask + 1) {
            key = entry_key(other_table + i);
            if key and key != dummy() {
                set_insert_clean(
                    so_table, newmask, object_new_ref(key), entry_hash(other_table + i)
                );
            }
        }
        return i32(0);
    }
    # Duplicates are possible: insert normally. A compare can change other,
    # so its table and mask are read again for every slot.
    i = 0;
    while i <= set_mask(other) {
        slot = set_table(other) + i;
        key = entry_key(slot);
        if key and key != dummy() {
            if set_add_entry(so, key, entry_hash(slot)) != 0 {
                return i32(-1);
            }
        }
        i += 1;
    }
    return i32(0);
}

def set_pop(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    s = set_of(so);
    if set_used(so) == 0 {
        PyErr_SetString(PyExc_KeyError, "pop from an empty set");
        return NULL;
    }
    table = set_table(so);
    mask = set_mask(so);
    # Start at the search finger, kept in bounds.
    i = s.view(1)[0].finger & mask;
    while True {
        key = entry_key(table + i);
        if key and key != dummy() {
            break;
        }
        i += 1;
        if i > mask {
            i = 0;
        }
    }
    key = entry_key(table + i);
    set_entry(table + i, dummy(), -1);
    s.view(1)[0].used -= 1;
    # The next place to start.
    s.view(1)[0].finger = i + 1;
    return key;
}

def set_traverse(so: ptr[PyObject], visitor: ptr, arg: ptr) -> i32 {
    pos = 0;
    while True {
        i = set_next(so, pos);
        if i < 0 {
            return i32(0);
        }
        pos = i + 1;
        status = visit_reference(entry_key(set_table(so) + i), visitor, arg);
        if status != 0 {
            return status;
        }
    }
    return i32(0);
}

"""Spread the bits of closely spaced hashes, so combinations of few elements
with nearby hashes do not collapse to few frozenset hashes."""
def shuffle_bits(h: u64) -> u64 {
    return wrapping_mul(
        (h ^ u64(89869747)) ^ wrapping_shl(h, u64(16)), u64(3644798167)
    );
}

"""The hash of a set's contents as a frozenset: the xor of every slot's
shuffled hash, with the empty and dummy slots' effect removed, then mixed."""
def frozenset_hash_impl(so: ptr[PyObject]) -> i64 {
    hash = u64(0);
    table = set_table(so);
    mask = set_mask(so);
    # Every slot, empty and dummy ones included, for speed.
    for i in range(mask + 1) {
        hash = hash ^ shuffle_bits(u64.wrap(entry_hash(table + i)));
    }
    # Remove the effect of an odd number of empty slots.
    if ((mask + 1 - set_fill(so)) & 1) != 0 {
        hash = hash ^ shuffle_bits(u64(0));
    }
    # Remove the effect of an odd number of dummy slots.
    if ((set_fill(so) - set_used(so)) & 1) != 0 {
        hash = hash ^ shuffle_bits(u64(0xFFFFFFFFFFFFFFFF));
    }
    # Factor in the number of active entries.
    hash = hash ^ wrapping_mul(u64.wrap(set_used(so)) + u64(1), u64(1927868237));
    # Disperse patterns arising in nested frozensets.
    hash = hash ^ ((hash >> u64(11)) ^ (hash >> u64(25)));
    hash = wrapping_add(wrapping_mul(hash, u64(69069)), u64(907133923));
    # -1 is reserved as an error code.
    if hash == u64(0xFFFFFFFFFFFFFFFF) {
        hash = u64(590923713);
    }
    return i64.wrap(hash);
}

def frozenset_hash(so: ptr[PyObject]) -> i64 {
    s = set_of(so);
    if s.view(1)[0].hash != -1 {
        return s.view(1)[0].hash;
    }
    hash = frozenset_hash_impl(so);
    s.view(1)[0].hash = hash;
    return hash;
}

# ------------------------------------------------------------------ iterator

def setiter_dealloc(op: ptr[PyObject]) {
    # bpo-31095: untrack before any callback.
    object_gc_untrack(op);
    object_xdecref(setiter_of(op).view(1)[0].si_set);
    PyObject_GC_Del(ptr(op));
}

def setiter_traverse(op: ptr[PyObject], visitor: ptr, arg: ptr) -> i32 {
    return visit_reference(setiter_of(op).view(1)[0].si_set, visitor, arg);
}

def setiter_len(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    si = setiter_of(op);
    length: i64 = 0;
    so = si.view(1)[0].si_set;
    if so and si.view(1)[0].si_used == set_used(so) {
        length = si.view(1)[0].len;
    }
    return PyLong_FromSsize_t(length);
}

"""Pickle as iter(list): the keys the iterator has left, read from a copy of
its state so the iterator itself does not advance."""
def setiter_reduce(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    si = setiter_of(op);
    copy = _PyObject_GC_New(ptr[PyObject](addressof(PySetIter_Type)));
    if not copy {
        return NULL;
    }
    state = setiter_of(copy);
    state.view(1)[0].si_set = object_xnew_ref(si.view(1)[0].si_set);
    state.view(1)[0].si_used = si.view(1)[0].si_used;
    state.view(1)[0].si_pos = si.view(1)[0].si_pos;
    state.view(1)[0].len = si.view(1)[0].len;
    keys = PySequence_List(copy);
    object_decref(copy);
    if not keys {
        return NULL;
    }
    return Py_BuildValue("N(N)", eval_builtin("iter"), keys);
}

def setiter_iternext(op: ptr[PyObject]) -> ptr[PyObject] {
    si = setiter_of(op);
    so = si.view(1)[0].si_set;
    if not so {
        return NULL;
    }
    if si.view(1)[0].si_used != set_used(so) {
        PyErr_SetString(PyExc_RuntimeError, "Set changed size during iteration");
        # Make this state sticky.
        si.view(1)[0].si_used = -1;
        return NULL;
    }
    i = si.view(1)[0].si_pos;
    table = set_table(so);
    mask = set_mask(so);
    key = NULL;
    while i <= mask {
        candidate = entry_key(table + i);
        if candidate and candidate != dummy() {
            key = object_new_ref(candidate);
            break;
        }
        i += 1;
    }
    si.view(1)[0].si_pos = i + 1;
    if not key {
        si.view(1)[0].si_set = NULL;
        object_decref(so);
        return NULL;
    }
    si.view(1)[0].len -= 1;
    return key;
}

def set_iter(so: ptr[PyObject]) -> ptr[PyObject] {
    size = set_used(so);
    op = _PyObject_GC_New(ptr[PyObject](addressof(PySetIter_Type)));
    if not op {
        return NULL;
    }
    si = setiter_of(op);
    si.view(1)[0].si_set = object_new_ref(so);
    si.view(1)[0].si_used = size;
    si.view(1)[0].si_pos = 0;
    si.view(1)[0].len = size;
    object_gc_track(op);
    return op;
}

# ---------------------------------------------------------------- updating

def object_xnew_ref(op: ptr[PyObject]) -> ptr[PyObject] {
    if op {
        object_incref(op);
    }
    return op;
}

"""Add a dict's keys, with their known hashes."""
def set_update_dict(so: ptr[PyObject], other: ptr[PyObject]) -> i32 {
    # One big resize up front, expecting few overlapping keys.
    dictsize = dict_used(other);
    if (set_fill(so) + dictsize) * 5 >= set_mask(so) * 3 {
        if set_table_resize(so, (set_used(so) + dictsize) * 2) != 0 {
            return i32(-1);
        }
    }
    pos: i64 = 0;
    key: ptr[PyObject] = NULL;
    value: ptr[PyObject] = NULL;
    hash: i64 = 0;
    while _PyDict_Next(other, &mut pos, &mut key, &mut value, &mut hash) != 0 {
        if set_add_entry(so, key, hash) != 0 {
            return i32(-1);
        }
    }
    return i32(0);
}

def set_update_iterable(so: ptr[PyObject], other: ptr[PyObject]) -> i32 {
    it = PyObject_GetIter(other);
    if not it {
        return i32(-1);
    }
    while True {
        key = PyIter_Next(it);
        if not key {
            break;
        }
        if set_add_key(so, key) != 0 {
            object_decref(it);
            object_decref(key);
            return i32(-1);
        }
        object_decref(key);
    }
    object_decref(it);
    if PyErr_Occurred() {
        return i32(-1);
    }
    return i32(0);
}

"""set_update_local / set_update_lock_held: add the keys of `other`, a set,
a dict or any iterable."""
def set_update_local(so: ptr[PyObject], other: ptr[PyObject]) -> i32 {
    if anyset_check(other) {
        return set_merge(so, other);
    }
    if dict_check_exact(other) {
        return set_update_dict(so, other);
    }
    return set_update_iterable(so, other);
}

def set_update_internal(so: ptr[PyObject], other: ptr[PyObject]) -> i32 {
    if anyset_check(other) and other == so {
        return i32(0);
    }
    return set_update_local(so, other);
}

def set_update(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    for i in range(nothers) {
        if set_update_internal(so, (others + i).view(1)[0]) != 0 {
            return NULL;
        }
    }
    return object_new_ref(Py_None);
}

def make_new_set(type: ptr[PyTypeObject], iterable: ptr[PyObject]) -> ptr[PyObject] {
    so = type.view(1)[0].tp_alloc(type, 0);
    if not so {
        return NULL;
    }
    s = set_of(so);
    s.view(1)[0].fill = 0;
    s.view(1)[0].used = 0;
    s.view(1)[0].mask = PySet_MINSIZE - 1;
    s.view(1)[0].table = smalltable(so);
    s.view(1)[0].hash = -1;
    s.view(1)[0].finger = 0;
    s.view(1)[0].weakreflist = NULL;
    if iterable and set_update_local(so, iterable) != 0 {
        object_decref(so);
        return NULL;
    }
    return so;
}

def make_new_set_basetype(
    type: ptr[PyTypeObject], iterable: ptr[PyObject]
) -> ptr[PyObject] {
    base = type;
    if base != set_type() and base != frozenset_type() {
        if PyType_IsSubtype(ptr[PyObject](base), ptr[PyObject](set_type())) != 0 {
            base = set_type();
        } else {
            base = frozenset_type();
        }
    }
    return make_new_set(base, iterable);
}

def make_new_frozenset(
    type: ptr[PyTypeObject], iterable: ptr[PyObject]
) -> ptr[PyObject] {
    if type != frozenset_type() {
        return make_new_set(type, iterable);
    }
    if iterable and frozenset_check_exact(iterable) {
        # frozenset(f) is idempotent.
        return object_new_ref(iterable);
    }
    return make_new_set(type, iterable);
}

"""PyArg_UnpackTuple(args, name, 0, 1, ...)'s check: False with a TypeError
set for more than one argument."""
def at_most_one_argument(args: ptr[PyObject], name: ptr[u8]) -> bool {
    nargs = object_size(args);
    if nargs > 1 {
        PyErr_Format(
            PyExc_TypeError, "%.200s expected at most 1 argument, got %zd", name, nargs
        );
        return False;
    }
    return True;
}

"""The optional iterable argument of an args tuple (NULL when absent)."""
def optional_iterable(args: ptr[PyObject]) -> ptr[PyObject] {
    return tuple_get_item(args, 0) if object_size(args) == 1 else NULL;
}

def frozenset_new(
    type: ptr[PyTypeObject], args: ptr[PyObject], kwds: ptr[PyObject]
) -> ptr[PyObject] {
    base = frozenset_type();
    if (type == base or int(type.view(1)[0].tp_init) == int(base.view(1)[0].tp_init))
        and kwds
        and _PyArg_NoKeywords("frozenset", kwds) == 0 {
        return NULL;
    }
    if not at_most_one_argument(args, type.view(1)[0].tp_name) {
        return NULL;
    }
    return make_new_frozenset(type, optional_iterable(args));
}

def frozenset_vectorcall(
    type: ptr[PyObject], args: ptr[ptr[PyObject]], nargsf: u64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if kwnames and _PyArg_NoKwnames("frozenset", kwnames) == 0 {
        return NULL;
    }
    nargs = PyVectorcall_NARGS(nargsf);
    if nargs > 1 and _PyArg_CheckPositional("frozenset", nargs, 0, 1) == 0 {
        return NULL;
    }
    iterable = args.view(1)[0] if nargs != 0 else NULL;
    return make_new_frozenset(type_of_object(type), iterable);
}

def set_new(
    type: ptr[PyTypeObject], args: ptr[PyObject], kwds: ptr[PyObject]
) -> ptr[PyObject] {
    return make_new_set(type, NULL);
}

"""Exchange the contents of two sets, moving table pointers and swapping the
embedded tables; frozenset hashes go along, other hashes are reset. Like
t=set(a); a.clear(); a.update(b); b.clear(); b.update(t), but it cannot
fail."""
def set_swap_bodies(a: ptr[PyObject], b: ptr[PyObject]) {
    sa = set_of(a);
    sb = set_of(b);
    t = sa.view(1)[0].fill;
    sa.view(1)[0].fill = sb.view(1)[0].fill;
    sb.view(1)[0].fill = t;
    t = sa.view(1)[0].used;
    sa.view(1)[0].used = sb.view(1)[0].used;
    sb.view(1)[0].used = t;
    t = sa.view(1)[0].mask;
    sa.view(1)[0].mask = sb.view(1)[0].mask;
    sb.view(1)[0].mask = t;
    u = set_table(a);
    if set_table(a) == smalltable(a) {
        u = smalltable(b);
    }
    newa = set_table(b);
    if set_table(b) == smalltable(b) {
        newa = smalltable(a);
    }
    sa.view(1)[0].table = newa;
    sb.view(1)[0].table = u;
    if newa == smalltable(a) or u == smalltable(b) {
        small_a = smalltable(a);
        small_b = smalltable(b);
        for i in range(PySet_MINSIZE) {
            key = entry_key(small_a + i);
            hash = entry_hash(small_a + i);
            set_entry(small_a + i, entry_key(small_b + i), entry_hash(small_b + i));
            set_entry(small_b + i, key, hash);
        }
    }
    frozen = ptr[PyObject](frozenset_type());
    if PyType_IsSubtype(ptr[PyObject](object_type(a)), frozen) != 0
        and PyType_IsSubtype(ptr[PyObject](object_type(b)), frozen) != 0 {
        h = sa.view(1)[0].hash;
        sa.view(1)[0].hash = sb.view(1)[0].hash;
        sb.view(1)[0].hash = h;
    } else {
        sa.view(1)[0].hash = -1;
        sb.view(1)[0].hash = -1;
    }
}

def set_copy_impl(so: ptr[PyObject]) -> ptr[PyObject] {
    copy = make_new_set_basetype(object_type(so), NULL);
    if not copy {
        return NULL;
    }
    if set_merge(copy, so) < 0 {
        object_decref(copy);
        return NULL;
    }
    return copy;
}

def set_copy(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    return set_copy_impl(so);
}

def frozenset_copy(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    if frozenset_check_exact(so) {
        return object_new_ref(so);
    }
    return set_copy_impl(so);
}

def set_clear(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    set_clear_internal(so);
    return object_new_ref(Py_None);
}

def set_union(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    result = set_copy_impl(so);
    if not result {
        return NULL;
    }
    for i in range(nothers) {
        other = (others + i).view(1)[0];
        if so == other {
            continue;
        }
        if set_update_local(result, other) != 0 {
            object_decref(result);
            return NULL;
        }
    }
    return result;
}

def set_or(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(so) or not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    result = set_copy_impl(so);
    if not result {
        return NULL;
    }
    if so == other {
        return result;
    }
    if set_update_local(result, other) != 0 {
        object_decref(result);
        return NULL;
    }
    return result;
}

def set_ior(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    if set_update_internal(so, other) != 0 {
        return NULL;
    }
    return object_new_ref(so);
}

def set_intersection(so_in: ptr[PyObject], other_in: ptr[PyObject]) -> ptr[PyObject] {
    so = so_in;
    other = other_in;
    if so == other {
        return set_copy_impl(so);
    }
    result = make_new_set_basetype(object_type(so), NULL);
    if not result {
        return NULL;
    }
    if anyset_check(other) {
        # Iterate over the smaller set.
        if set_used(other) > set_used(so) {
            tmp = so;
            so = other;
            other = tmp;
        }
        pos = 0;
        while True {
            i = set_next(other, pos);
            if i < 0 {
                break;
            }
            pos = i + 1;
            slot = set_table(other) + i;
            key = object_new_ref(entry_key(slot));
            hash = entry_hash(slot);
            rv = set_contains_entry(so, key, hash);
            if rv < 0 or (rv != 0 and set_add_entry(result, key, hash) != 0) {
                object_decref(result);
                object_decref(key);
                return NULL;
            }
            object_decref(key);
        }
        return result;
    }
    it = PyObject_GetIter(other);
    if not it {
        object_decref(result);
        return NULL;
    }
    while True {
        key = PyIter_Next(it);
        if not key {
            break;
        }
        hash = PyObject_Hash(key);
        failed = hash == -1;
        rv = i32(0);
        if not failed {
            rv = set_contains_entry(so, key, hash);
            failed = rv < 0;
        }
        if not failed and rv != 0 {
            failed = set_add_entry(result, key, hash) != 0;
            if not failed and set_used(result) >= set_used(so) {
                object_decref(key);
                break;
            }
        }
        if failed {
            object_decref(it);
            object_decref(result);
            object_decref(key);
            return NULL;
        }
        object_decref(key);
    }
    object_decref(it);
    if PyErr_Occurred() {
        object_decref(result);
        return NULL;
    }
    return result;
}

def set_intersection_multi(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    if nothers == 0 {
        return set_copy_impl(so);
    }
    result = object_new_ref(so);
    for i in range(nothers) {
        newresult = set_intersection(result, (others + i).view(1)[0]);
        if not newresult {
            object_decref(result);
            return NULL;
        }
        object_decref(result);
        result = newresult;
    }
    return result;
}

def set_intersection_update(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    tmp = set_intersection(so, other);
    if not tmp {
        return NULL;
    }
    set_swap_bodies(so, tmp);
    object_decref(tmp);
    return object_new_ref(Py_None);
}

def set_intersection_update_multi(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    tmp = set_intersection_multi(so, others, nothers);
    if not tmp {
        return NULL;
    }
    set_swap_bodies(so, tmp);
    object_decref(tmp);
    return object_new_ref(Py_None);
}

def set_and(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(so) or not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    return set_intersection(so, other);
}

def set_iand(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    result = set_intersection_update(so, other);
    if not result {
        return NULL;
    }
    object_decref(result);
    return object_new_ref(so);
}

def set_isdisjoint(so_in: ptr[PyObject], other_in: ptr[PyObject]) -> ptr[PyObject] {
    so = so_in;
    other = other_in;
    if so == other {
        return PyBool_FromLong(1 if set_used(so) == 0 else 0);
    }
    if anyset_check_exact(other) {
        # Iterate over the smaller set.
        if set_used(other) > set_used(so) {
            tmp = so;
            so = other;
            other = tmp;
        }
        pos = 0;
        while True {
            i = set_next(other, pos);
            if i < 0 {
                break;
            }
            pos = i + 1;
            slot = set_table(other) + i;
            key = object_new_ref(entry_key(slot));
            rv = set_contains_entry(so, key, entry_hash(slot));
            object_decref(key);
            if rv < 0 {
                return NULL;
            }
            if rv != 0 {
                return PyBool_FromLong(0);
            }
        }
        return PyBool_FromLong(1);
    }
    it = PyObject_GetIter(other);
    if not it {
        return NULL;
    }
    while True {
        key = PyIter_Next(it);
        if not key {
            break;
        }
        rv = set_contains_key(so, key);
        object_decref(key);
        if rv < 0 {
            object_decref(it);
            return NULL;
        }
        if rv != 0 {
            object_decref(it);
            return PyBool_FromLong(0);
        }
    }
    object_decref(it);
    if PyErr_Occurred() {
        return NULL;
    }
    return PyBool_FromLong(1);
}

def set_difference_update_internal(so: ptr[PyObject], other_in: ptr[PyObject]) -> i32 {
    if so == other_in {
        return set_clear_internal(so);
    }
    if anyset_check(other_in) {
        other = other_in;
        # When the other set is more than 8 times larger, discard its
        # intersection with this one instead.
        if (set_used(other) >> 3) > set_used(so) {
            other = set_intersection(so, other);
            if not other {
                return i32(-1);
            }
        } else {
            object_incref(other);
        }
        pos = 0;
        while True {
            i = set_next(other, pos);
            if i < 0 {
                break;
            }
            pos = i + 1;
            slot = set_table(other) + i;
            key = object_new_ref(entry_key(slot));
            if set_discard_entry(so, key, entry_hash(slot)) < 0 {
                object_decref(other);
                object_decref(key);
                return i32(-1);
            }
            object_decref(key);
        }
        object_decref(other);
    } else {
        it = PyObject_GetIter(other_in);
        if not it {
            return i32(-1);
        }
        while True {
            key = PyIter_Next(it);
            if not key {
                break;
            }
            if set_discard_key(so, key) < 0 {
                object_decref(it);
                object_decref(key);
                return i32(-1);
            }
            object_decref(key);
        }
        object_decref(it);
        if PyErr_Occurred() {
            return i32(-1);
        }
    }
    # More than a quarter dummies: resize them away.
    if u64.wrap(set_fill(so) - set_used(so)) <= u64.wrap(set_mask(so)) / u64(4) {
        return i32(0);
    }
    used = set_used(so);
    return set_table_resize(so, used * 2 if used > 50000 else used * 4);
}

def set_difference_update(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    for i in range(nothers) {
        if set_difference_update_internal(so, (others + i).view(1)[0]) != 0 {
            return NULL;
        }
    }
    return object_new_ref(Py_None);
}

def set_copy_and_difference(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    result = set_copy_impl(so);
    if not result {
        return NULL;
    }
    if set_difference_update_internal(result, other) == 0 {
        return result;
    }
    object_decref(result);
    return NULL;
}

def set_difference(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    other_size: i64 = 0;
    other_is_dict = False;
    if anyset_check(other) {
        other_size = set_used(other);
    } elif dict_check_exact(other) {
        other_size = dict_used(other);
        other_is_dict = True;
    } else {
        return set_copy_and_difference(so, other);
    }
    # Much larger than other: copy, then discard other's elements.
    if (set_used(so) >> 2) > other_size {
        return set_copy_and_difference(so, other);
    }
    result = make_new_set_basetype(object_type(so), NULL);
    if not result {
        return NULL;
    }
    # Keep the elements of so that other lacks.
    pos = 0;
    while True {
        i = set_next(so, pos);
        if i < 0 {
            break;
        }
        pos = i + 1;
        slot = set_table(so) + i;
        key = object_new_ref(entry_key(slot));
        hash = entry_hash(slot);
        rv = i32(0);
        if other_is_dict {
            rv = _PyDict_Contains_KnownHash(other, key, hash);
        } else {
            rv = set_contains_entry(other, key, hash);
        }
        if rv < 0 or (rv == 0 and set_add_entry(result, key, hash) != 0) {
            object_decref(result);
            object_decref(key);
            return NULL;
        }
        object_decref(key);
    }
    return result;
}

def set_difference_multi(
    so: ptr[PyObject], others: ptr[ptr[PyObject]], nothers: i64
) -> ptr[PyObject] {
    if nothers == 0 {
        return set_copy_impl(so);
    }
    result = set_difference(so, others.view(1)[0]);
    if not result {
        return NULL;
    }
    for i in range(1, nothers) {
        if set_difference_update_internal(result, (others + i).view(1)[0]) != 0 {
            object_decref(result);
            return NULL;
        }
    }
    return result;
}

def set_sub(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(so) or not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    return set_difference(so, other);
}

def set_isub(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    if set_difference_update_internal(so, other) < 0 {
        return NULL;
    }
    return object_new_ref(so);
}

"""Toggle `key`: discard it if present, else add it."""
def toggle_entry(so: ptr[PyObject], key: ptr[PyObject], hash: i64) -> i32 {
    rv = set_discard_entry(so, key, hash);
    if rv < 0 {
        return i32(-1);
    }
    if rv == DISCARD_NOTFOUND and set_add_entry(so, key, hash) != 0 {
        return i32(-1);
    }
    return i32(0);
}

def set_symmetric_difference_update_dict(
    so: ptr[PyObject], other: ptr[PyObject]
) -> i32 {
    pos: i64 = 0;
    key: ptr[PyObject] = NULL;
    value: ptr[PyObject] = NULL;
    hash: i64 = 0;
    while _PyDict_Next(other, &mut pos, &mut key, &mut value, &mut hash) != 0 {
        held = object_new_ref(key);
        rv = toggle_entry(so, held, hash);
        object_decref(held);
        if rv < 0 {
            return i32(-1);
        }
    }
    return i32(0);
}

def set_symmetric_difference_update_set(
    so: ptr[PyObject], other: ptr[PyObject]
) -> i32 {
    pos = 0;
    while True {
        i = set_next(other, pos);
        if i < 0 {
            break;
        }
        pos = i + 1;
        slot = set_table(other) + i;
        key = object_new_ref(entry_key(slot));
        rv = toggle_entry(so, key, entry_hash(slot));
        object_decref(key);
        if rv < 0 {
            return i32(-1);
        }
    }
    return i32(0);
}

def set_symmetric_difference_update(
    so: ptr[PyObject], other: ptr[PyObject]
) -> ptr[PyObject] {
    if so == other {
        return set_clear(so, NULL);
    }
    rv = i32(0);
    if dict_check_exact(other) {
        rv = set_symmetric_difference_update_dict(so, other);
    } elif anyset_check(other) {
        rv = set_symmetric_difference_update_set(so, other);
    } else {
        otherset = make_new_set_basetype(object_type(so), other);
        if not otherset {
            return NULL;
        }
        rv = set_symmetric_difference_update_set(so, otherset);
        object_decref(otherset);
    }
    if rv < 0 {
        return NULL;
    }
    return object_new_ref(Py_None);
}

def set_symmetric_difference(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    result = make_new_set_basetype(object_type(so), NULL);
    if not result {
        return NULL;
    }
    if set_update_local(result, other) < 0
        or set_symmetric_difference_update_set(result, so) < 0 {
        object_decref(result);
        return NULL;
    }
    return result;
}

def set_xor(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(so) or not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    return set_symmetric_difference(so, other);
}

def set_ixor(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(other) {
        return object_new_ref(Py_NotImplemented);
    }
    result = set_symmetric_difference_update(so, other);
    if not result {
        return NULL;
    }
    object_decref(result);
    return object_new_ref(so);
}

def set_issubset(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if not anyset_check(other) {
        tmp = set_intersection(so, other);
        if not tmp {
            return NULL;
        }
        result = set_used(tmp) == set_used(so);
        object_decref(tmp);
        return PyBool_FromLong(1 if result else 0);
    }
    if set_used(so) > set_used(other) {
        return PyBool_FromLong(0);
    }
    pos = 0;
    while True {
        i = set_next(so, pos);
        if i < 0 {
            break;
        }
        pos = i + 1;
        slot = set_table(so) + i;
        key = object_new_ref(entry_key(slot));
        rv = set_contains_entry(other, key, entry_hash(slot));
        object_decref(key);
        if rv < 0 {
            return NULL;
        }
        if rv == 0 {
            return PyBool_FromLong(0);
        }
    }
    return PyBool_FromLong(1);
}

def set_issuperset(so: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    if anyset_check(other) {
        return set_issubset(other, so);
    }
    it = PyObject_GetIter(other);
    if not it {
        return NULL;
    }
    while True {
        key = PyIter_Next(it);
        if not key {
            break;
        }
        rv = set_contains_key(so, key);
        object_decref(key);
        if rv < 0 {
            object_decref(it);
            return NULL;
        }
        if rv == 0 {
            object_decref(it);
            return PyBool_FromLong(0);
        }
    }
    object_decref(it);
    if PyErr_Occurred() {
        return NULL;
    }
    return PyBool_FromLong(1);
}

def set_richcompare(v: ptr[PyObject], w: ptr[PyObject], op: i32) -> ptr[PyObject] {
    if not anyset_check(w) {
        return object_new_ref(Py_NotImplemented);
    }
    if op == Py_EQ {
        if set_used(v) != set_used(w) {
            return PyBool_FromLong(0);
        }
        v_hash = set_of(v).view(1)[0].hash;
        w_hash = set_of(w).view(1)[0].hash;
        if v_hash != -1 and w_hash != -1 and v_hash != w_hash {
            return PyBool_FromLong(0);
        }
        return set_issubset(v, w);
    }
    if op == Py_NE {
        r1 = set_richcompare(v, w, Py_EQ);
        if not r1 {
            return NULL;
        }
        r2 = PyObject_IsTrue(r1);
        object_decref(r1);
        if r2 < 0 {
            return NULL;
        }
        return PyBool_FromLong(1 if r2 == 0 else 0);
    }
    if op == Py_LE {
        return set_issubset(v, w);
    }
    if op == Py_GE {
        return set_issuperset(v, w);
    }
    if op == Py_LT {
        if set_used(v) >= set_used(w) {
            return PyBool_FromLong(0);
        }
        return set_issubset(v, w);
    }
    if op == Py_GT {
        if set_used(v) <= set_used(w) {
            return PyBool_FromLong(0);
        }
        return set_issuperset(v, w);
    }
    return object_new_ref(Py_NotImplemented);
}

def set_add(so: ptr[PyObject], key: ptr[PyObject]) -> ptr[PyObject] {
    if set_add_key(so, key) != 0 {
        return NULL;
    }
    return object_new_ref(Py_None);
}

"""After a lookup of `key` failed: whether to retry it as the frozenset with
the same contents, which a set key (unhashable) stands for. True clears the
TypeError."""
def retry_as_frozenset(key: ptr[PyObject]) -> bool {
    if not set_check(key) or PyErr_ExceptionMatches(PyExc_TypeError) == 0 {
        return False;
    }
    PyErr_Clear();
    return True;
}

def set_contains_lock_held(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    rv = set_contains_key(so, key);
    if rv < 0 {
        if not retry_as_frozenset(key) {
            return i32(-1);
        }
        rv = set_contains_entry(so, key, frozenset_hash_impl(key));
    }
    return rv;
}

def set_contains(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    return set_contains_lock_held(so, key);
}

def set___contains__(so: ptr[PyObject], key: ptr[PyObject]) -> ptr[PyObject] {
    result = set_contains_lock_held(so, key);
    if result < 0 {
        return NULL;
    }
    return PyBool_FromLong(i64(result));
}

def frozenset___contains__(so: ptr[PyObject], key: ptr[PyObject]) -> ptr[PyObject] {
    return set___contains__(so, key);
}

"""Discard `key` (or the frozenset of a set key); -1 with an error set."""
def discard_any(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
    rv = set_discard_key(so, key);
    if rv < 0 {
        if not retry_as_frozenset(key) {
            return i32(-1);
        }
        rv = set_discard_entry(so, key, frozenset_hash_impl(key));
    }
    return rv;
}

def set_remove(so: ptr[PyObject], key: ptr[PyObject]) -> ptr[PyObject] {
    rv = discard_any(so, key);
    if rv < 0 {
        return NULL;
    }
    if rv == DISCARD_NOTFOUND {
        _PyErr_SetKeyError(key);
        return NULL;
    }
    return object_new_ref(Py_None);
}

def set_discard(so: ptr[PyObject], key: ptr[PyObject]) -> ptr[PyObject] {
    if discard_any(so, key) < 0 {
        return NULL;
    }
    return object_new_ref(Py_None);
}

def set___reduce__(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    result = NULL;
    args = NULL;
    state = NULL;
    keys = PySequence_List(so);
    if keys {
        args = PyTuple_Pack(1, keys);
        if args {
            state = _PyObject_GetState(so);
            if state {
                result = PyTuple_Pack(3, ptr[PyObject](object_type(so)), args, state);
            }
        }
    }
    object_xdecref(args);
    object_xdecref(keys);
    object_xdecref(state);
    return result;
}

def set___sizeof__(so: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    res = object_type(so).view(1)[0].tp_basicsize;
    if set_table(so) != smalltable(so) {
        res += (set_mask(so) + 1) * SETENTRY_SIZE;
    }
    return PyLong_FromSize_t(u64(res));
}

def set_init(so: ptr[PyObject], args: ptr[PyObject], kwds: ptr[PyObject]) -> i32 {
    if kwds and _PyArg_NoKeywords("set", kwds) == 0 {
        return i32(-1);
    }
    if not at_most_one_argument(args, object_type(so).view(1)[0].tp_name) {
        return i32(-1);
    }
    iterable = optional_iterable(args);
    if object_refcount(so) == 1 and set_fill(so) == 0 {
        set_of(so).view(1)[0].hash = -1;
        if not iterable {
            return i32(0);
        }
        return set_update_local(so, iterable);
    }
    if set_fill(so) != 0 {
        set_clear_internal(so);
    }
    set_of(so).view(1)[0].hash = -1;
    if not iterable {
        return i32(0);
    }
    return set_update_internal(so, iterable);
}

def set_vectorcall(
    type: ptr[PyObject], args: ptr[ptr[PyObject]], nargsf: u64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if kwnames and _PyArg_NoKwnames("set", kwnames) == 0 {
        return NULL;
    }
    nargs = PyVectorcall_NARGS(nargsf);
    if nargs > 1 and _PyArg_CheckPositional("set", nargs, 0, 1) == 0 {
        return NULL;
    }
    if nargs != 0 {
        return make_new_set(type_of_object(type), args.view(1)[0]);
    }
    return make_new_set(type_of_object(type), NULL);
}

def dummy_repr(op: ptr[PyObject]) -> ptr[PyObject] {
    return PyUnicode_FromString("<dummy key>");
}

def dummy_dealloc(op: ptr[PyObject]) {
    Py_FatalError("deallocating <dummy key>");
}

import from c {
    def PySet_New(iterable: ptr[PyObject]) -> ptr[PyObject] {
        return make_new_set(set_type(), iterable);
    }  def PyFrozenSet_New(iterable: ptr[PyObject]) -> ptr[PyObject] {
        return make_new_set(frozenset_type(), iterable);
    }  def PySet_Size(anyset: ptr[PyObject]) -> i64 {
        if not anyset_check(anyset) {
            PyErr_BadInternalCall();
            return -1;
        }
        return set_used(anyset);
    }  def PySet_Clear(set: ptr[PyObject]) -> i32 {
        if not set_check(set) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        set_clear_internal(set);
        return i32(0);
    }  def _PySet_Contains(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
        return set_contains_lock_held(so, key);
    }  def _PySet_ClearInternal(so: ptr[PyObject]) {
        set_clear_internal(so);
    }  def PySet_Contains(anyset: ptr[PyObject], key: ptr[PyObject]) -> i32 {
        if not anyset_check(anyset) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        return set_contains_key(anyset, key);
    }  def PySet_Discard(set: ptr[PyObject], key: ptr[PyObject]) -> i32 {
        if not set_check(set) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        return set_discard_key(set, key);
    }
    # A frozenset only while it is being built (its sole reference).
    def PySet_Add(anyset: ptr[PyObject], key: ptr[PyObject]) -> i32 {
        if not set_check(anyset)
            and (not frozenset_check(anyset) or object_refcount(anyset) != 1) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        return set_add_key(anyset, key);
    }
    # Add `key`, stealing it.
    def _PySet_AddTakeRef(so: ptr[PyObject], key: ptr[PyObject]) -> i32 {
        hash = hash_fast(key);
        if hash == -1 {
            set_unhashable_type(key);
            object_decref(key);
            return i32(-1);
        }
        return set_add_entry_takeref(so, key, hash);
    }  def _PySet_NextEntry(
        set: ptr[PyObject], pos: ptr[i64], key: ptr[ptr[PyObject]], hash: ptr[i64]
    ) -> i32 {
        if not anyset_check(set) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        i = set_next(set, pos.view(1)[0]);
        if i < 0 {
            pos.view(1)[0] = set_mask(set) + 2;
            return i32(0);
        }
        pos.view(1)[0] = i + 1;
        slot = set_table(set) + i;
        key.view(1)[0] = entry_key(slot);
        hash.view(1)[0] = entry_hash(slot);
        return i32(1);
    }  def _PySet_NextEntryRef(
        set: ptr[PyObject], pos: ptr[i64], key: ptr[ptr[PyObject]], hash: ptr[i64]
    ) -> i32 {
        if not anyset_check(set) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        i = set_next(set, pos.view(1)[0]);
        if i < 0 {
            pos.view(1)[0] = set_mask(set) + 2;
            return i32(0);
        }
        pos.view(1)[0] = i + 1;
        slot = set_table(set) + i;
        key.view(1)[0] = object_new_ref(entry_key(slot));
        hash.view(1)[0] = entry_hash(slot);
        return i32(1);
    }  def PySet_Pop(set: ptr[PyObject]) -> ptr[PyObject] {
        if not set_check(set) {
            PyErr_BadInternalCall();
            return NULL;
        }
        return set_pop(set, NULL);
    }  def _PySet_Update(set: ptr[PyObject], iterable: ptr[PyObject]) -> i32 {
        if not set_check(set) {
            PyErr_BadInternalCall();
            return i32(-1);
        }
        return set_update_internal(set, iterable);
    }
}
