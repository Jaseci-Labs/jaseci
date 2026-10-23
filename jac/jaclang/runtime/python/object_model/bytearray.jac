"""The bytearray type and its iterator: Objects/bytearrayobject.c in native Jac.

`PyByteArray_Type`, `PyByteArrayIter_Type` and `_PyByteArray_empty_string` are
C data Jac defines under their C names, and the bytearray C API
(`PyByteArray_FromObject`, `PyByteArray_FromStringAndSize`, `PyByteArray_Size`,
`PyByteArray_AsString`, `PyByteArray_Resize`, `PyByteArray_Concat`) is defined
here under its C names, so the evaluator, the bytes writer and every C caller,
including the static inline `PyByteArray_AS_STRING` that reads `ob_start` and
`_PyByteArray_empty_string` directly, use them unchanged. A bytearray keeps
its bytes in a separate buffer whose logical start `ob_start` may lie past
`ob_bytes`, so deleting from the front only advances the start; the buffer
grows and shrinks by bytearrayobject.c's overallocation rules and cannot move
while `ob_exports` is nonzero, which buffer exports and the methods that call
back into Python keep raised. The methods bytearray shares with bytes are the
byte stringlib of bytes_methods.jac, and `%` formatting, `fromhex` and
repetition are bytes.jac's `_PyBytes_FormatEx`, `_PyBytes_FromHex` and
`_PyBytes_Repeat`. Methods parse their arguments as
Objects/clinic/bytearrayobject.c.h does. The critical sections of the
free-threaded build are not reproduced. See ../LICENSE.cpython.
"""

import from c {
    glob PyType_Type: PyTypeObject,
         PyExc_BytesWarning: ptr[PyObject]; def memcpy(
        target: ptr, source: ptr, size: u64
    ) -> ptr;  def memmove(target: ptr, source: ptr, size: u64) -> ptr;  def memset(
        target: ptr, value: i32, size: u64
    ) -> ptr;  def memchr(source: ptr, value: i32, size: u64) -> ptr;  def memcmp(
        left: ptr, right: ptr, size: u64
    ) -> i32;  def strlen(s: ptr[u8]) -> u64;  def _Py_GetConfig -> ptr[u8];  def PyBuffer_FillInfo(
        view: ptr[Py_buffer],
        o: ptr[PyObject],
        buf: ptr,
        len_: i64,
        readonly: i32,
        flags: i32
    ) -> i32;  def PyUnicode_FromStringAndSize(
        u: ptr[u8], size: i64
    ) -> ptr[PyObject];  def PyUnicode_AsEncodedString(
        unicode: ptr[PyObject], encoding: ptr[u8], errors: ptr[u8]
    ) -> ptr[PyObject];  def PyUnicode_FromEncodedObject(
        obj_: ptr[PyObject], encoding: ptr[u8], errors: ptr[u8]
    ) -> ptr[PyObject];  def _Py_strhex_with_sep(
        argbuf: ptr, arglen: i64, sep: ptr[PyObject], bytes_per_group: i32
    ) -> ptr[PyObject];
    # Defined in Jac by memory.jac.
    def PyBuffer_ToContiguous(
        buf: ptr, src: ptr[Py_buffer], length: i64, order: i8
    ) -> i32;
    # Defined in Jac by bytes.jac.
    def _PyBytes_FromHex(string: ptr[PyObject], use_bytearray: i32) -> ptr[PyObject];  def _PyBytes_FormatEx(
        format: ptr[u8], format_len: i64, args_in: ptr[PyObject], use_bytearray: i32
    ) -> ptr[PyObject];  def _PyBytes_Repeat(
        dest: ptr[u8], len_dest: i64, src: ptr[u8], len_src: i64
    );  glob:priv bytearray_as_number: PyNumberMethods = PyNumberMethods(
             nb_remainder=bytearray_mod
         ),
         bytearray_as_sequence: PySequenceMethods = PySequenceMethods(
             sq_length=bytearray_length,
             sq_concat=bytearray_concat,
             sq_repeat=bytearray_repeat,
             sq_item=bytearray_getitem,
             sq_ass_item=bytearray_setitem,
             sq_contains=bytearray_contains,
             sq_inplace_concat=bytearray_iconcat,
             sq_inplace_repeat=bytearray_irepeat
         ),
         bytearray_as_mapping: PyMappingMethods = PyMappingMethods(
             mp_length=bytearray_length,
             mp_subscript=bytearray_subscript,
             mp_ass_subscript=bytearray_ass_subscript
         ),
         bytearray_as_buffer: PyBufferProcs = PyBufferProcs(
             bf_getbuffer=bytearray_getbuffer, bf_releasebuffer=bytearray_releasebuffer
         ),
         bytearray_methods: list[PyMethodDef] = [
             PyMethodDef(
                 ml_name=ptr[u8]("__alloc__"),
                 ml_meth=ptr(bytearray_alloc),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.__alloc__() -> int\n\n"
                     "Return the number of bytes actually allocated."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce__"),
                 ml_meth=ptr(bytearray_reduce),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__reduce__($self, /)\n--\n\n"
                     "Return state information for pickling."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce_ex__"),
                 ml_meth=ptr(bytearray_reduce_ex),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "__reduce_ex__($self, proto=0, /)\n--\n\n"
                     "Return state information for pickling."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__sizeof__"),
                 ml_meth=ptr(bytearray_sizeof),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__sizeof__($self, /)\n--\n\n"
                     "Returns the size of the bytearray object in memory, in bytes."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("append"),
                 ml_meth=ptr(bytearray_append),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "append($self, item, /)\n--\n\n"
                     "Append a single item to the end of the bytearray.\n\n"
                     "  item\n"
                     "    The item to be appended."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("capitalize"),
                 ml_meth=ptr(bytearray_capitalize),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.capitalize() -> copy of B\n\n"
                     "Return a copy of B with only its first character capitalized (ASCII)\n"
                     "and the rest lower-cased."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("center"),
                 ml_meth=ptr(bytearray_center),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "center($self, width, fillchar=b' ', /)\n--\n\n"
                     "Return a centered string of length width.\n\n"
                     "Padding is done using the specified fill character."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("clear"),
                 ml_meth=ptr(bytearray_clear),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "clear($self, /)\n--\n\n" "Remove all items from the bytearray."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("copy"),
                 ml_meth=ptr(bytearray_copy),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8]("copy($self, /)\n--\n\nReturn a copy of B.")
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("count"),
                 ml_meth=ptr(bytearray_count),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "count($self, sub[, start[, end]], /)\n--\n\n"
                     "Return the number of non-overlapping occurrences of subsection 'sub' in bytes B[start:end].\n\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytes.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytes."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("decode"),
                 ml_meth=ptr(bytearray_decode),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "decode($self, /, encoding='utf-8', errors='strict')\n--\n\n"
                     "Decode the bytearray using the codec registered for encoding.\n\n"
                     "  encoding\n"
                     "    The encoding with which to decode the bytearray.\n"
                     "  errors\n"
                     "    The error handling scheme to use for the handling of decoding\n"
                     "    errors.  The default is 'strict' meaning that decoding errors\n"
                     "    raise a UnicodeDecodeError.  Other possible values are 'ignore'\n"
                     "    and 'replace' as well as any other name registered with\n"
                     "    codecs.register_error that can handle UnicodeDecodeErrors."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("endswith"),
                 ml_meth=ptr(bytearray_endswith),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "endswith($self, suffix[, start[, end]], /)\n--\n\n"
                     "Return True if the bytearray ends with the specified suffix, False otherwise.\n\n"
                     "  suffix\n"
                     "    A bytes or a tuple of bytes to try.\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytearray.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytearray."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("expandtabs"),
                 ml_meth=ptr(bytearray_expandtabs),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "expandtabs($self, /, tabsize=8)\n--\n\n"
                     "Return a copy where all tab characters are expanded using spaces.\n\n"
                     "If tabsize is not given, a tab size of 8 characters is assumed."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("extend"),
                 ml_meth=ptr(bytearray_extend),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "extend($self, iterable_of_ints, /)\n--\n\n"
                     "Append all the items from the iterator or sequence to the end of the bytearray.\n\n"
                     "  iterable_of_ints\n"
                     "    The iterable of items to append."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("find"),
                 ml_meth=ptr(bytearray_find),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "find($self, sub[, start[, end]], /)\n--\n\n"
                     "Return the lowest index in B where subsection 'sub' is found, such that 'sub' is contained within B[start:end].\n\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytes.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytes.\n\n"
                     "Return -1 on failure."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("fromhex"),
                 ml_meth=ptr(bytearray_fromhex),
                 ml_flags=METH_O | METH_CLASS,
                 ml_doc=ptr[u8](
                     "fromhex($type, string, /)\n--\n\n"
                     "Create a bytearray object from a string of hexadecimal numbers.\n\n"
                     "Spaces between two numbers are accepted.\n"
                     "Example:\n"
                     "    bytearray.fromhex('B9 01EF') -> bytearray(b'\\\\xb9\\\\x01\\\\xef')"
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("hex"),
                 ml_meth=ptr(bytearray_hex),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "hex($self, /, sep=<unrepresentable>, bytes_per_sep=1)\n--\n\n"
                     "Create a string of hexadecimal numbers from a bytearray object.\n\n"
                     "  sep\n"
                     "    An optional single character or byte to separate hex bytes.\n"
                     "  bytes_per_sep\n"
                     "    How many bytes between separators.  Positive values count from\n"
                     "    the right, negative values count from the left.\n\n"
                     "Example:\n"
                     ">>> value = bytearray([0xb9, 0x01, 0xef])\n"
                     ">>> value.hex()\n"
                     "'b901ef'\n"
                     ">>> value.hex(':')\n"
                     "'b9:01:ef'\n"
                     ">>> value.hex(':', 2)\n"
                     "'b9:01ef'\n"
                     ">>> value.hex(':', -2)\n"
                     "'b901:ef'"
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("index"),
                 ml_meth=ptr(bytearray_index),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "index($self, sub[, start[, end]], /)\n--\n\n"
                     "Return the lowest index in B where subsection 'sub' is found, such that 'sub' is contained within B[start:end].\n\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytes.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytes.\n\n"
                     "Raise ValueError if the subsection is not found."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("insert"),
                 ml_meth=ptr(bytearray_insert),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "insert($self, index, item, /)\n--\n\n"
                     "Insert a single item into the bytearray before the given index.\n\n"
                     "  index\n"
                     "    The index where the value is to be inserted.\n"
                     "  item\n"
                     "    The item to be inserted."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isalnum"),
                 ml_meth=ptr(bytearray_isalnum),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isalnum() -> bool\n\n"
                     "Return True if all characters in B are alphanumeric\n"
                     "and there is at least one character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isalpha"),
                 ml_meth=ptr(bytearray_isalpha),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isalpha() -> bool\n\n"
                     "Return True if all characters in B are alphabetic\n"
                     "and there is at least one character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isascii"),
                 ml_meth=ptr(bytearray_isascii),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isascii() -> bool\n\n"
                     "Return True if B is empty or all characters in B are ASCII,\n"
                     "False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isdigit"),
                 ml_meth=ptr(bytearray_isdigit),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isdigit() -> bool\n\n"
                     "Return True if all characters in B are digits\n"
                     "and there is at least one character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("islower"),
                 ml_meth=ptr(bytearray_islower),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.islower() -> bool\n\n"
                     "Return True if all cased characters in B are lowercase and there is\n"
                     "at least one cased character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isspace"),
                 ml_meth=ptr(bytearray_isspace),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isspace() -> bool\n\n"
                     "Return True if all characters in B are whitespace\n"
                     "and there is at least one character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("istitle"),
                 ml_meth=ptr(bytearray_istitle),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.istitle() -> bool\n\n"
                     "Return True if B is a titlecased string and there is at least one\n"
                     "character in B, i.e. uppercase characters may only follow uncased\n"
                     "characters and lowercase characters only cased ones. Return False\n"
                     "otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("isupper"),
                 ml_meth=ptr(bytearray_isupper),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.isupper() -> bool\n\n"
                     "Return True if all cased characters in B are uppercase and there is\n"
                     "at least one cased character in B, False otherwise."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("join"),
                 ml_meth=ptr(bytearray_join),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "join($self, iterable_of_bytes, /)\n--\n\n"
                     "Concatenate any number of bytes/bytearray objects.\n\n"
                     "The bytearray whose method is called is inserted in between each\n"
                     "pair.\n\n"
                     "The result is returned as a new bytearray object."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("ljust"),
                 ml_meth=ptr(bytearray_ljust),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "ljust($self, width, fillchar=b' ', /)\n--\n\n"
                     "Return a left-justified string of length width.\n\n"
                     "Padding is done using the specified fill character."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("lower"),
                 ml_meth=ptr(bytearray_lower),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.lower() -> copy of B\n\n"
                     "Return a copy of B with all ASCII characters converted to lowercase."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("lstrip"),
                 ml_meth=ptr(bytearray_lstrip),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "lstrip($self, bytes=None, /)\n--\n\n"
                     "Strip leading bytes contained in the argument.\n\n"
                     "If the argument is omitted or None, strip leading ASCII whitespace."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("maketrans"),
                 ml_meth=ptr(bytearray_maketrans),
                 ml_flags=METH_FASTCALL | METH_STATIC,
                 ml_doc=ptr[u8](
                     "maketrans(frm, to, /)\n--\n\n"
                     "Return a translation table usable for the bytes or bytearray translate method.\n\n"
                     "The returned table will be one where each byte in frm is mapped to\n"
                     "the byte at the same position in to.\n\n"
                     "The bytes objects frm and to must be of the same length."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("partition"),
                 ml_meth=ptr(bytearray_partition),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "partition($self, sep, /)\n--\n\n"
                     "Partition the bytearray into three parts using the given separator.\n\n"
                     "This will search for the separator sep in the bytearray.  If the\n"
                     "separator is found, returns a 3-tuple containing the part before the\n"
                     "separator, the separator itself, and the part after it as new\n"
                     "bytearray objects.\n\n"
                     "If the separator is not found, returns a 3-tuple containing the copy\n"
                     "of the original bytearray object and two empty bytearray objects."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("pop"),
                 ml_meth=ptr(bytearray_pop),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "pop($self, index=-1, /)\n--\n\n"
                     "Remove and return a single item from B.\n\n"
                     "  index\n"
                     "    The index from where to remove the item.\n"
                     "    -1 (the default value) means remove the last item.\n\n"
                     "If no index argument is given, will pop the last item."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("remove"),
                 ml_meth=ptr(bytearray_remove),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "remove($self, value, /)\n--\n\n"
                     "Remove the first occurrence of a value in the bytearray.\n\n"
                     "  value\n"
                     "    The value to remove."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("replace"),
                 ml_meth=ptr(bytearray_replace),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "replace($self, old, new, count=-1, /)\n--\n\n"
                     "Return a copy with all occurrences of substring old replaced by new.\n\n"
                     "  count\n"
                     "    Maximum number of occurrences to replace.\n"
                     "    -1 (the default value) means replace all occurrences.\n\n"
                     "If the optional argument count is given, only the first count occurrences are\n"
                     "replaced."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("removeprefix"),
                 ml_meth=ptr(bytearray_removeprefix),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "removeprefix($self, prefix, /)\n--\n\n"
                     "Return a bytearray with the given prefix string removed if present.\n\n"
                     "If the bytearray starts with the prefix string, return\n"
                     "bytearray[len(prefix):].  Otherwise, return a copy of the original\n"
                     "bytearray."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("removesuffix"),
                 ml_meth=ptr(bytearray_removesuffix),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "removesuffix($self, suffix, /)\n--\n\n"
                     "Return a bytearray with the given suffix string removed if present.\n\n"
                     "If the bytearray ends with the suffix string and that suffix is not\n"
                     "empty, return bytearray[:-len(suffix)].  Otherwise, return a copy of\n"
                     "the original bytearray."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("resize"),
                 ml_meth=ptr(bytearray_resize_method),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "resize($self, size, /)\n--\n\n"
                     "Resize the internal buffer of bytearray to len.\n\n"
                     "  size\n"
                     "    New size to resize to."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("reverse"),
                 ml_meth=ptr(bytearray_reverse),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "reverse($self, /)\n--\n\n"
                     "Reverse the order of the values in B in place."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rfind"),
                 ml_meth=ptr(bytearray_rfind),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "rfind($self, sub[, start[, end]], /)\n--\n\n"
                     "Return the highest index in B where subsection 'sub' is found, such that 'sub' is contained within B[start:end].\n\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytes.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytes.\n\n"
                     "Return -1 on failure."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rindex"),
                 ml_meth=ptr(bytearray_rindex),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "rindex($self, sub[, start[, end]], /)\n--\n\n"
                     "Return the highest index in B where subsection 'sub' is found, such that 'sub' is contained within B[start:end].\n\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytes.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytes.\n\n"
                     "Raise ValueError if the subsection is not found."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rjust"),
                 ml_meth=ptr(bytearray_rjust),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "rjust($self, width, fillchar=b' ', /)\n--\n\n"
                     "Return a right-justified string of length width.\n\n"
                     "Padding is done using the specified fill character."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rpartition"),
                 ml_meth=ptr(bytearray_rpartition),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "rpartition($self, sep, /)\n--\n\n"
                     "Partition the bytearray into three parts using the given separator.\n\n"
                     "This will search for the separator sep in the bytearray, starting at\n"
                     "the end.  If the separator is found, returns a 3-tuple containing\n"
                     "the part before the separator, the separator itself, and the part\n"
                     "after it as new bytearray objects.\n\n"
                     "If the separator is not found, returns a 3-tuple containing two\n"
                     "empty bytearray objects and the copy of the original bytearray\n"
                     "object."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rsplit"),
                 ml_meth=ptr(bytearray_rsplit),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "rsplit($self, /, sep=None, maxsplit=-1)\n--\n\n"
                     "Return a list of the sections in the bytearray, using sep as the delimiter.\n\n"
                     "  sep\n"
                     "    The delimiter according which to split the bytearray.\n"
                     "    None (the default value) means split on ASCII whitespace\n"
                     "    characters (space, tab, return, newline, formfeed, vertical tab).\n"
                     "  maxsplit\n"
                     "    Maximum number of splits to do.\n"
                     "    -1 (the default value) means no limit.\n\n"
                     "Splitting is done starting at the end of the bytearray and working\n"
                     "to the front."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("rstrip"),
                 ml_meth=ptr(bytearray_rstrip),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "rstrip($self, bytes=None, /)\n--\n\n"
                     "Strip trailing bytes contained in the argument.\n\n"
                     "If the argument is omitted or None, strip trailing ASCII whitespace."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("split"),
                 ml_meth=ptr(bytearray_split),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "split($self, /, sep=None, maxsplit=-1)\n--\n\n"
                     "Return a list of the sections in the bytearray, using sep as the delimiter.\n\n"
                     "  sep\n"
                     "    The delimiter according which to split the bytearray.\n"
                     "    None (the default value) means split on ASCII whitespace\n"
                     "    characters (space, tab, return, newline, formfeed, vertical tab).\n"
                     "  maxsplit\n"
                     "    Maximum number of splits to do.\n"
                     "    -1 (the default value) means no limit."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("splitlines"),
                 ml_meth=ptr(bytearray_splitlines),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "splitlines($self, /, keepends=False)\n--\n\n"
                     "Return a list of the lines in the bytearray, breaking at line boundaries.\n\n"
                     "Line breaks are not included in the resulting list unless keepends\n"
                     "is given and true."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("startswith"),
                 ml_meth=ptr(bytearray_startswith),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "startswith($self, prefix[, start[, end]], /)\n--\n\n"
                     "Return True if the bytearray starts with the specified prefix, False otherwise.\n\n"
                     "  prefix\n"
                     "    A bytes or a tuple of bytes to try.\n"
                     "  start\n"
                     "    Optional start position. Default: start of the bytearray.\n"
                     "  end\n"
                     "    Optional stop position. Default: end of the bytearray."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("strip"),
                 ml_meth=ptr(bytearray_strip),
                 ml_flags=METH_FASTCALL,
                 ml_doc=ptr[u8](
                     "strip($self, bytes=None, /)\n--\n\n"
                     "Strip leading and trailing bytes contained in the argument.\n\n"
                     "If the argument is omitted or None, strip leading and trailing ASCII\n"
                     "whitespace."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("swapcase"),
                 ml_meth=ptr(bytearray_swapcase),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.swapcase() -> copy of B\n\n"
                     "Return a copy of B with uppercase ASCII characters converted\n"
                     "to lowercase ASCII and vice versa."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("title"),
                 ml_meth=ptr(bytearray_title),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.title() -> copy of B\n\n"
                     "Return a titlecased version of B, i.e. ASCII words start with\n"
                     "uppercase characters, all remaining cased characters have lowercase."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("translate"),
                 ml_meth=ptr(bytearray_translate),
                 ml_flags=METH_FASTCALL | METH_KEYWORDS,
                 ml_doc=ptr[u8](
                     "translate($self, table, /, delete=b'')\n--\n\n"
                     "Return a copy with each character mapped by the given translation table.\n\n"
                     "  table\n"
                     "    Translation table, which must be a bytes object of length 256.\n\n"
                     "All characters occurring in the optional argument delete are\n"
                     "removed.  The remaining characters are mapped through the given\n"
                     "translation table."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("upper"),
                 ml_meth=ptr(bytearray_upper),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "B.upper() -> copy of B\n\n"
                     "Return a copy of B with all ASCII characters converted to uppercase."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("zfill"),
                 ml_meth=ptr(bytearray_zfill),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8](
                     "zfill($self, width, /)\n--\n\n"
                     "Pad a numeric string with zeros on the left, to fill a field of the given width.\n\n"
                     "The original string is never truncated."
                 )
             ),
             PyMethodDef(ml_name=ptr[u8](), ml_meth=ptr(), ml_flags=0, ml_doc=ptr[u8]())
         ],
         bytearrayiter_methods: list[PyMethodDef] = [
             PyMethodDef(
                 ml_name=ptr[u8]("__length_hint__"),
                 ml_meth=ptr(bytearrayiter_length_hint),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "Private method returning an estimate of len(list(it))."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__reduce__"),
                 ml_meth=ptr(bytearrayiter_reduce),
                 ml_flags=METH_NOARGS,
                 ml_doc=ptr[u8](
                     "__reduce__($self, /)\n--\n\n"
                     "Return state information for pickling."
                 )
             ),
             PyMethodDef(
                 ml_name=ptr[u8]("__setstate__"),
                 ml_meth=ptr(bytearrayiter_setstate),
                 ml_flags=METH_O,
                 ml_doc=ptr[u8]("Set state information for unpickling.")
             ),
             PyMethodDef(ml_name=ptr[u8](), ml_meth=ptr(), ml_flags=0, ml_doc=ptr[u8]())
         ];
    # For PyByteArray_AS_STRING(): the bytes of every empty bytearray. A
    # minor downsize to zero stores its NUL here, so it is writable.
    glob _PyByteArray_empty_string: list[u8] = [u8(0)],
         PyByteArray_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("bytearray"),
             tp_basicsize=PyByteArrayObject_SIZE,
             tp_dealloc=bytearray_dealloc,
             tp_repr=bytearray_repr,
             tp_as_number=addressof(bytearray_as_number),
             tp_as_sequence=addressof(bytearray_as_sequence),
             tp_as_mapping=addressof(bytearray_as_mapping),
             tp_str=bytearray_str,
             tp_getattro=PyObject_GenericGetAttr,
             tp_as_buffer=addressof(bytearray_as_buffer),
             tp_flags=Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | _Py_TPFLAGS_MATCH_SELF,
             tp_doc=ptr[u8](
                 "bytearray(iterable_of_ints) -> bytearray\n"
                 "bytearray(string, encoding[, errors]) -> bytearray\n"
                 "bytearray(bytes_or_buffer) -> mutable copy of bytes_or_buffer\n"
                 "bytearray(int) -> bytes array of size given by the parameter initialized with null bytes\n"
                 "bytearray() -> empty bytes array\n\n"
                 "Construct a mutable bytearray object from:\n"
                 "  - an iterable yielding integers in range(256)\n"
                 "  - a text string encoded using the specified encoding\n"
                 "  - a bytes or a buffer object\n"
                 "  - any object implementing the buffer API.\n"
                 "  - an integer"
             ),
             tp_richcompare=bytearray_richcompare,
             tp_iter=bytearray_iter,
             tp_methods=addressof(bytearray_methods),
             tp_init=bytearray___init__,
             tp_alloc=PyType_GenericAlloc,
             tp_new=PyType_GenericNew,
             tp_free=PyObject_Free,
             tp_version_tag=_Py_TYPE_VERSION_BYTEARRAY
         ),
         PyByteArrayIter_Type: PyTypeObject = PyTypeObject(
             ob_base=PyVarObject(
                 ob_base=_object(
                     ob_refcnt_full=_Py_STATIC_IMMORTAL_INITIAL_REFCNT,
                     ob_type=addressof(PyType_Type)
                 ),
                 ob_size=0
             ),
             tp_name=ptr[u8]("bytearray_iterator"),
             tp_basicsize=bytesiterobject_SIZE,
             tp_dealloc=bytearrayiter_dealloc,
             tp_getattro=PyObject_GenericGetAttr,
             tp_flags=Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,
             tp_traverse=bytearrayiter_traverse,
             tp_iter=PyObject_SelfIter,
             tp_iternext=bytearrayiter_next,
             tp_methods=addressof(bytearrayiter_methods)
         );
}

glob:priv PY_SSIZE_T_MAX: i64 = 0x7FFFFFFFFFFFFFFF,
     # sizeof(Py_buffer) on every supported (LP64) target.
     PY_BUFFER_SIZE: i64 = 80,
     # bytearray_strip_impl_helper's striptype.
     LEFTSTRIP: i64 = 0,
     RIGHTSTRIP: i64 = 1,
     BOTHSTRIP: i64 = 2,
     # The _Py_bytes_* search bytearray_with_buffer runs (C passes the
     # function itself).
     OP_FIND: i64 = 0,
     OP_COUNT: i64 = 1,
     OP_INDEX: i64 = 2,
     OP_RFIND: i64 = 3,
     OP_RINDEX: i64 = 4,
     OP_STARTSWITH: i64 = 5,
     OP_ENDSWITH: i64 = 6,
     # The str arguments text_arg converts, which name the argument in its
     # TypeError.
     ARG_DECODE_ENCODING: i64 = 0,
     ARG_DECODE_ERRORS: i64 = 1,
     ARG_INIT_ENCODING: i64 = 2,
     ARG_INIT_ERRORS: i64 = 3,
     # PyBuffer_ToContiguous's order 'C'.
     ORDER_C: i64 = 67,
     # Character codes.
     CH_TAB: i64 = 9,
     CH_NEWLINE: i64 = 10,
     CH_RETURN: i64 = 13,
     CH_SPACE: i64 = 32,
     CH_DQUOTE: i64 = 34,
     CH_QUOTE: i64 = 39,
     CH_LPAREN: i64 = 40,
     CH_RPAREN: i64 = 41,
     CH_ZERO: i64 = 48,
     CH_BACKSLASH: i64 = 92,
     CH_LOWER_B: i64 = 98,
     CH_LOWER_N: i64 = 110,
     CH_LOWER_R: i64 = 114,
     CH_LOWER_T: i64 = 116,
     CH_LOWER_X: i64 = 120,
     CH_DEL: i64 = 127;

glob:priv bytearray_init_signature = CallSignature(
         "bytearray", ["source", "encoding", "errors"], 0, 3, 0, parser=PARSE_KEYWORDS
     ),
     split_signature = CallSignature(
         "split", ["sep", "maxsplit"], 0, 2, 0, parser=PARSE_KEYWORDS
     ),
     rsplit_signature = CallSignature(
         "rsplit", ["sep", "maxsplit"], 0, 2, 0, parser=PARSE_KEYWORDS
     ),
     translate_signature = CallSignature(
         "translate", ["table", "delete"], 1, 2, 1, parser=PARSE_KEYWORDS
     ),
     decode_signature = CallSignature(
         "decode", ["encoding", "errors"], 0, 2, 0, parser=PARSE_KEYWORDS
     ),
     splitlines_signature = CallSignature(
         "splitlines", ["keepends"], 0, 1, 0, parser=PARSE_KEYWORDS
     ),
     hex_signature = CallSignature(
         "hex", ["sep", "bytes_per_sep"], 0, 2, 0, parser=PARSE_KEYWORDS
     );

# ------------------------------------------------------------ object access
def bytearray_type -> ptr[PyTypeObject] {
    return addressof(PyByteArray_Type);
}

def ba_of(op: ptr[PyObject]) -> ptr[PyByteArrayObject] {
    return ptr[PyByteArrayObject](op);
}

"""ob_alloc: how many bytes are allocated in ob_bytes."""
def ba_alloc(op: ptr[PyObject]) -> i64 {
    return ba_of(op).view(1)[0].ob_alloc;
}

"""ob_bytes: the physical backing buffer, NULL for a bytearray that never
held a byte."""
def ba_bytes(op: ptr[PyObject]) -> ptr[u8] {
    return ba_of(op).view(1)[0].ob_bytes;
}

"""ob_start: the logical start inside ob_bytes."""
def ba_start(op: ptr[PyObject]) -> ptr[u8] {
    return ba_of(op).view(1)[0].ob_start;
}

def set_start(op: ptr[PyObject], start: ptr[u8]) {
    ba_of(op).view(1)[0].ob_start = start;
}

"""ob_exports: how many buffer exports (and running methods) pin the
storage."""
def ba_exports(op: ptr[PyObject]) -> i64 {
    return ba_of(op).view(1)[0].ob_exports;
}

def add_exports(op: ptr[PyObject], delta: i64) {
    ba = ba_of(op);
    ba.view(1)[0].ob_exports = ba.view(1)[0].ob_exports + delta;
}

def set_size(op: ptr[PyObject], size: i64) {
    ptr[PyVarObject](op).view(1)[0].ob_size = size;
}

"""PyByteArray_AS_STRING: the logical start, or the shared empty string for
an empty bytearray."""
def ba_as_string(op: ptr[PyObject]) -> ptr[u8] {
    if object_size(op) != 0 {
        return ba_start(op);
    }
    return addressof(_PyByteArray_empty_string);
}

"""PyByteArray_Check."""
def bytearray_check(op: ptr[PyObject]) -> bool {
    return object_type_check(op, bytearray_type());
}

"""PyUnicode_Check."""
def unicode_check(op: ptr[PyObject]) -> bool {
    return type_has_feature(object_type(op), Py_TPFLAGS_UNICODE_SUBCLASS);
}

"""PyLong_CheckExact."""
def long_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, ptr[PyTypeObject](addressof(PyLong_Type)));
}

"""PyList_CheckExact."""
def list_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, ptr[PyTypeObject](addressof(PyList_Type)));
}

"""PyTuple_CheckExact."""
def tuple_check_exact(op: ptr[PyObject]) -> bool {
    return object_is_type(op, ptr[PyTypeObject](addressof(PyTuple_Type)));
}

"""PySlice_Check: the exact slice type."""
def slice_check(op: ptr[PyObject]) -> bool {
    return object_is_type(op, ptr[PyTypeObject](addressof(PySlice_Type)));
}

"""The byte at p."""
def peek(p: ptr[u8]) -> u8 {
    return p.view(1)[0];
}

def poke(p: ptr[u8], c: u8) {
    p.view(1)[0] = c;
}

"""The distance in bytes from `start` to `stop`."""
def span(start: ptr[u8], stop: ptr[u8]) -> i64 {
    return i64(int(stop) - int(start));
}

"""Py_hexdigits[x]: the lowercase hexadecimal digit of 0 <= x < 16."""
def hex_char(x: i64) -> u8 {
    return u8(48 + x) if x < 10 else u8(87 + x);
}

"""_Py_GetConfig()->bytes_warning: the -b option's level."""
def config_bytes_warning -> i32 {
    return ptr[i32](_Py_GetConfig() + PyConfig_BYTES_WARNING).view(1)[0];
}

"""A zeroed Py_buffer on the heap (C keeps it on the stack), or NULL with
MemoryError set. Releasing it before it was filled does nothing, as for C's
`{NULL, NULL}` initializer and its `len = -1` marker."""
def buffer_slot -> ptr[Py_buffer] {
    view = ptr[Py_buffer](PyMem_Calloc(1, u64(PY_BUFFER_SIZE)));
    if not view {
        PyErr_NoMemory();
    }
    return view;
}

"""Release the buffer a slot holds, if any, and free the slot."""
def buffer_free(view: ptr[Py_buffer]) {
    PyBuffer_Release(view);
    PyMem_Free(ptr(view));
}

"""A Py_ssize_t argument as clinic converts it (through __index__): (True,
value), or (False, -1) with an error set."""
def ssize_arg(value: ptr[PyObject]) -> tuple[bool, i64] {
    ival: i64 = -1;
    iobj = _PyNumber_Index(value);
    if iobj {
        ival = PyLong_AsSsize_t(iobj);
        object_decref(iobj);
    }
    if ival == -1 and PyErr_Occurred() {
        return (False, ival);
    }
    return (True, ival);
}

"""_getbytevalue (clinic's bytesvalue converter): an int as one byte,
(True, value), or (False, -1) with an error set."""
def getbytevalue(arg: ptr[PyObject]) -> tuple[bool, i64] {
    overflow = i32(0);
    face_value = PyLong_AsLongAndOverflow(arg, &mut overflow);
    if face_value == -1 and PyErr_Occurred() {
        return (False, i64(-1));
    }
    if face_value < 0 or face_value >= 256 {
        # this includes an overflow in converting to C long
        PyErr_SetString(PyExc_ValueError, "byte must be in range(0, 256)");
        return (False, i64(-1));
    }
    return (True, face_value);
}

"""_canresize: False with BufferError set while buffers are exported."""
def can_resize(op: ptr[PyObject]) -> bool {
    if ba_exports(op) > 0 {
        PyErr_SetString(
            PyExc_BufferError, "Existing exports of data: object cannot be re-sized"
        );
        return False;
    }
    return True;
}

"""_bytearray_with_buffer: run the _Py_bytes_* search `which` over the
bytes, which may not move meanwhile."""
def bytearray_with_buffer(
    op: ptr[PyObject], which: i64, sub: ptr[PyObject], start: i64, end: i64
) -> ptr[PyObject] {
    # Increase exports to prevent bytearray storage from changing during op.
    add_exports(op, 1);
    s = ba_as_string(op);
    n = object_size(op);
    res = NULL;
    if which == OP_FIND {
        res = _Py_bytes_find(s, n, sub, start, end);
    } elif which == OP_COUNT {
        res = _Py_bytes_count(s, n, sub, start, end);
    } elif which == OP_INDEX {
        res = _Py_bytes_index(s, n, sub, start, end);
    } elif which == OP_RFIND {
        res = _Py_bytes_rfind(s, n, sub, start, end);
    } elif which == OP_RINDEX {
        res = _Py_bytes_rindex(s, n, sub, start, end);
    } elif which == OP_STARTSWITH {
        res = _Py_bytes_startswith(s, n, sub, start, end);
    } else {
        res = _Py_bytes_endswith(s, n, sub, start, end);
    }
    add_exports(op, -1);
    return res;
}

# ------------------------------------------------------------ resizing
"""bytearray_resize_lock_held: set the size to `requested_size`, moving or
reallocating the buffer as needed; -1 with an error set."""
def bytearray_resize(op: ptr[PyObject], requested_size: i64) -> i32 {
    ba = ba_of(op);
    # All computations are done unsigned to avoid integer overflows (see
    # issue #22335).
    alloc = u64(ba.view(1)[0].ob_alloc);
    logical_offset = u64(span(ba.view(1)[0].ob_bytes, ba.view(1)[0].ob_start));
    if requested_size < 0 {
        PyErr_Format(
            PyExc_ValueError,
            "Can only resize to positive sizes, got %zd",
            requested_size
        );
        return i32(-1);
    }
    size = u64(requested_size);
    if requested_size == object_size(op) {
        return i32(0);
    }
    if not can_resize(op) {
        return i32(-1);
    }
    if size + logical_offset + u64(1) <= alloc {
        # Current buffer is large enough to host the requested size, decide
        # on a strategy.
        if size < alloc // u64(2) {
            # Major downsize; resize down to exact size
            alloc = size + u64(1);
        } else {
            # Minor downsize; quick exit
            set_size(op, requested_size);
            # Trailing null
            poke(ba_as_string(op) + requested_size, u8(0));
            return i32(0);
        }
    } elif f64(requested_size) <= f64(ba.view(1)[0].ob_alloc) * 1.125 {
        # Need growing: a moderate upsize; overallocate similar to
        # list_resize()
        alloc = size + (size >> u64(3)) + (u64(3) if size < u64(9) else u64(6));
    } else {
        # Major upsize; resize up to exact size
        alloc = size + u64(1);
    }
    if alloc > u64(PY_SSIZE_T_MAX) {
        PyErr_NoMemory();
        return i32(-1);
    }
    sval = ptr();
    if logical_offset > u64(0) {
        sval = PyMem_Malloc(alloc);
        if not sval {
            PyErr_NoMemory();
            return i32(-1);
        }
        memcpy(sval, ptr(ba_as_string(op)), u64(min(requested_size, object_size(op))));
        PyMem_Free(ptr(ba.view(1)[0].ob_bytes));
    } else {
        sval = PyMem_Realloc(ptr(ba.view(1)[0].ob_bytes), alloc);
        if not sval {
            PyErr_NoMemory();
            return i32(-1);
        }
    }
    ba.view(1)[0].ob_bytes = ptr[u8](sval);
    ba.view(1)[0].ob_start = ptr[u8](sval);
    set_size(op, requested_size);
    ba.view(1)[0].ob_alloc = i64(alloc);
    # Trailing null byte
    poke(ptr[u8](sval) + requested_size, u8(0));
    return i32(0);
}

"""_PyByteArray_FromBufferObject: a bytearray copy of obj's buffer."""
def bytearray_from_buffer_object(source: ptr[PyObject]) -> ptr[PyObject] {
    view = buffer_slot();
    if not view {
        return NULL;
    }
    if PyObject_GetBuffer(source, view, PyBUF_FULL_RO) < i32(0) {
        buffer_free(view);
        return NULL;
    }
    result = PyByteArray_FromStringAndSize(ptr[u8](), view.view(1)[0].length);
    if result
        and PyBuffer_ToContiguous(
            ptr(ba_as_string(result)), view, view.view(1)[0].length, i8(ORDER_C)
        )
            < i32(0) {
        object_decref(result);
        result = NULL;
    }
    buffer_free(view);
    return result;
}

# --------------------------------------------------------- direct API
import from c {
    def PyByteArray_FromObject(input: ptr[PyObject]) -> ptr[PyObject] {
        return PyObject_CallOneArg(ptr[PyObject](bytearray_type()), input);
    }  def PyByteArray_FromStringAndSize(data: ptr[u8], size: i64) -> ptr[PyObject] {
        if size < 0 {
            PyErr_SetString(
                PyExc_SystemError,
                "Negative size passed to PyByteArray_FromStringAndSize"
            );
            return NULL;
        }
        # Prevent buffer overflow when setting alloc to size+1.
        if size == PY_SSIZE_T_MAX {
            return PyErr_NoMemory();
        }
        op = _PyObject_New(ptr[PyObject](bytearray_type()));
        if not op {
            return NULL;
        }
        ba = ba_of(op);
        alloc: i64 = 0;
        if size == 0 {
            ba.view(1)[0].ob_bytes = ptr[u8]();
        } else {
            alloc = size + 1;
            raw = ptr[u8](PyMem_Malloc(u64(alloc)));
            ba.view(1)[0].ob_bytes = raw;
            if not raw {
                object_decref(op);
                return PyErr_NoMemory();
            }
            if data and size > 0 {
                memcpy(ptr(raw), ptr(data), u64(size));
            }
            # Trailing null byte
            poke(raw + size, u8(0));
        }
        set_size(op, size);
        ba.view(1)[0].ob_alloc = alloc;
        ba.view(1)[0].ob_start = ba.view(1)[0].ob_bytes;
        ba.view(1)[0].ob_exports = 0;
        return op;
    }  def PyByteArray_Size(op: ptr[PyObject]) -> i64 {
        return object_size(op);
    }  def PyByteArray_AsString(op: ptr[PyObject]) -> ptr[u8] {
        return ba_as_string(op);
    }  def PyByteArray_Resize(op: ptr[PyObject], requested_size: i64) -> i32 {
        return bytearray_resize(op, requested_size);
    }  def PyByteArray_Concat(a: ptr[PyObject], b: ptr[PyObject]) -> ptr[PyObject] {
        va = buffer_slot();
        if not va {
            return NULL;
        }
        vb = buffer_slot();
        if not vb {
            PyMem_Free(ptr(va));
            return NULL;
        }
        result = NULL;
        if PyObject_GetBuffer(a, va, PyBUF_SIMPLE) != i32(0)
            or PyObject_GetBuffer(b, vb, PyBUF_SIMPLE) != i32(0) {
            PyErr_Format(
                PyExc_TypeError,
                "can't concat %.100s to %.100s",
                object_type(b).view(1)[0].tp_name,
                object_type(a).view(1)[0].tp_name
            );
        } elif va.view(1)[0].length > PY_SSIZE_T_MAX - vb.view(1)[0].length {
            PyErr_NoMemory();
        } else {
            result = PyByteArray_FromStringAndSize(
                ptr[u8](), va.view(1)[0].length + vb.view(1)[0].length
            );
            # result->ob_bytes is NULL if result is an empty bytearray: if
            # va.len + vb.len equals zero.
            if result and ba_bytes(result) {
                memcpy(
                    ptr(ba_bytes(result)), va.view(1)[0].buf, u64(va.view(1)[0].length)
                );
                memcpy(
                    ptr(ba_bytes(result) + va.view(1)[0].length),
                    vb.view(1)[0].buf,
                    u64(vb.view(1)[0].length)
                );
            }
        }
        buffer_free(va);
        buffer_free(vb);
        return result;
    }
}

# ------------------------------------------------------- buffer protocol
def bytearray_getbuffer(op: ptr[PyObject], view: ptr[Py_buffer], flags: i32) -> i32 {
    if not view {
        PyErr_SetString(
            PyExc_BufferError, "bytearray_getbuffer: view==NULL argument is obsolete"
        );
        return i32(-1);
    }
    if PyBuffer_FillInfo(
        view, op, ptr(ba_as_string(op)), object_size(op), i32(0), flags
    )
        < i32(0) {
        return i32(-1);
    }
    add_exports(op, 1);
    return i32(0);
}

def bytearray_releasebuffer(op: ptr[PyObject], view: ptr[Py_buffer]) {
    add_exports(op, -1);
}

# ------------------------------------------------------- sequence slots
def bytearray_length(op: ptr[PyObject]) -> i64 {
    return object_size(op);
}

"""sq_concat: PyByteArray_Concat."""
def bytearray_concat(a: ptr[PyObject], b: ptr[PyObject]) -> ptr[PyObject] {
    return PyByteArray_Concat(a, b);
}

def bytearray_iconcat(op: ptr[PyObject], other: ptr[PyObject]) -> ptr[PyObject] {
    vo = buffer_slot();
    if not vo {
        return NULL;
    }
    if PyObject_GetBuffer(other, vo, PyBUF_SIMPLE) != i32(0) {
        PyErr_Format(
            PyExc_TypeError,
            "can't concat %.100s to %.100s",
            object_type(other).view(1)[0].tp_name,
            object_type(op).view(1)[0].tp_name
        );
        buffer_free(vo);
        return NULL;
    }
    size = object_size(op);
    added = vo.view(1)[0].length;
    if size > PY_SSIZE_T_MAX - added {
        buffer_free(vo);
        return PyErr_NoMemory();
    }
    if bytearray_resize(op, size + added) < i32(0) {
        buffer_free(vo);
        return NULL;
    }
    memcpy(ptr(ba_as_string(op) + size), vo.view(1)[0].buf, u64(added));
    buffer_free(vo);
    return object_new_ref(op);
}

def bytearray_repeat(op: ptr[PyObject], count_in: i64) -> ptr[PyObject] {
    count = count_in;
    if count < 0 {
        count = 0;
    }
    mysize = object_size(op);
    if count > 0 and mysize > PY_SSIZE_T_MAX // count {
        return PyErr_NoMemory();
    }
    size = mysize * count;
    result = PyByteArray_FromStringAndSize(ptr[u8](), size);
    buf = ba_as_string(op);
    if result and size != 0 {
        _PyBytes_Repeat(ba_bytes(result), size, buf, mysize);
    }
    return result;
}

def bytearray_irepeat(op: ptr[PyObject], count_in: i64) -> ptr[PyObject] {
    count = count_in;
    if count < 0 {
        count = 0;
    } elif count == 1 {
        return object_new_ref(op);
    }
    mysize = object_size(op);
    if count > 0 and mysize > PY_SSIZE_T_MAX // count {
        return PyErr_NoMemory();
    }
    size = mysize * count;
    if bytearray_resize(op, size) < i32(0) {
        return NULL;
    }
    buf = ba_as_string(op);
    _PyBytes_Repeat(buf, size, buf, mysize);
    return object_new_ref(op);
}

def bytearray_getitem(op: ptr[PyObject], i: i64) -> ptr[PyObject] {
    if i < 0 or i >= object_size(op) {
        PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
        return NULL;
    }
    return get_small_int(i64(peek(ba_start(op) + i)));
}

def bytearray_subscript(op: ptr[PyObject], index: ptr[PyObject]) -> ptr[PyObject] {
    if PyIndex_Check(index) != i32(0) {
        i = PyNumber_AsSsize_t(index, PyExc_IndexError);
        if i == -1 and PyErr_Occurred() {
            return NULL;
        }
        if i < 0 {
            i += object_size(op);
        }
        if i < 0 or i >= object_size(op) {
            PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
            return NULL;
        }
        return get_small_int(i64(peek(ba_start(op) + i)));
    }
    if not slice_check(index) {
        PyErr_Format(
            PyExc_TypeError,
            "bytearray indices must be integers or slices, not %.200s",
            object_type(index).view(1)[0].tp_name
        );
        return NULL;
    }
    start: i64 = 0;
    stop: i64 = 0;
    step: i64 = 0;
    if PySlice_Unpack(index, &mut start, &mut stop, &mut step) < i32(0) {
        return NULL;
    }
    slicelength = PySlice_AdjustIndices(object_size(op), &mut start, &mut stop, step);
    if slicelength <= 0 {
        return PyByteArray_FromStringAndSize(ptr[u8](), 0);
    }
    if step == 1 {
        return PyByteArray_FromStringAndSize(ba_as_string(op) + start, slicelength);
    }
    source_buf = ba_as_string(op);
    result = PyByteArray_FromStringAndSize(ptr[u8](), slicelength);
    if not result {
        return NULL;
    }
    result_buf = ba_as_string(result);
    cur = start;
    for k in range(slicelength) {
        poke(result_buf + k, peek(source_buf + cur));
        cur = wrapping_add(cur, step);
    }
    return result;
}

"""bytearray_setslice_linear: replace bytes lo:hi with `bytes_len` bytes at
`data`, growing or shrinking the storage."""
def bytearray_setslice_linear(
    op: ptr[PyObject], lo: i64, hi: i64, data: ptr[u8], bytes_len: i64
) -> i32 {
    avail = hi - lo;
    buf = ba_as_string(op);
    growth = bytes_len - avail;
    res = i32(0);
    if growth < 0 {
        if not can_resize(op) {
            return i32(-1);
        }
        if lo == 0 {
            # Shrink the buffer by advancing its logical start
            set_start(op, ba_start(op) + (0 - growth));
            #   0   lo               hi             old_size
            #   |   |<----avail----->|<-----tail------>|
            #   |      |<-bytes_len->|<-----tail------>|
            #   0    new_lo         new_hi          new_size
        } else {
            #   0   lo               hi               old_size
            #   |   |<----avail----->|<-----tomove------>|
            #   |   |<-bytes_len->|<-----tomove------>|
            #   0   lo         new_hi              new_size
            memmove(
                ptr(buf + lo + bytes_len), ptr(buf + hi), u64(object_size(op) - hi)
            );
        }
        if bytearray_resize(op, object_size(op) + growth) < i32(0) {
            # Issue #19578: Handling the memory allocation failure here is
            # tricky here because the bytearray object has already been
            # modified. Depending on growth and lo, the behaviour is
            # different.
            #
            # If growth < 0 and lo != 0, the operation is completed, but a
            # MemoryError is still raised and the memory block is not
            # shrunk. Otherwise, the bytearray is restored in its previous
            # state and a MemoryError is raised.
            if lo == 0 {
                set_start(op, ba_start(op) + growth);
                return i32(-1);
            }
            # memmove() removed bytes, the bytearray object cannot be
            # restored in its previous state.
            set_size(op, object_size(op) + growth);
            res = i32(-1);
        }
        buf = ba_as_string(op);
    } elif growth > 0 {
        if object_size(op) > PY_SSIZE_T_MAX - growth {
            PyErr_NoMemory();
            return i32(-1);
        }
        if bytearray_resize(op, object_size(op) + growth) < i32(0) {
            return i32(-1);
        }
        buf = ba_as_string(op);
        # Make the place for the additional bytes
        #   0   lo        hi               old_size
        #   |   |<-avail->|<-----tomove------>|
        #   |   |<---bytes_len-->|<-----tomove------>|
        #   0   lo            new_hi              new_size
        memmove(
            ptr(buf + lo + bytes_len),
            ptr(buf + hi),
            u64(object_size(op) - lo - bytes_len)
        );
    }
    if bytes_len > 0 {
        memcpy(ptr(buf + lo), ptr(data), u64(bytes_len));
    }
    return res;
}

"""bytearray_setslice: b[lo:hi] = values, or del b[lo:hi] when `values` is
NULL; `values` is any object with a buffer."""
def bytearray_setslice(
    op: ptr[PyObject], lo_in: i64, hi_in: i64, values: ptr[PyObject]
) -> i32 {
    if values == op {
        # Make a copy and call this function recursively
        copy = PyByteArray_FromStringAndSize(ba_as_string(values), object_size(values));
        if not copy {
            return i32(-1);
        }
        err = bytearray_setslice(op, lo_in, hi_in, copy);
        object_decref(copy);
        return err;
    }
    vbytes = ptr[Py_buffer]();
    data = ptr[u8]();
    needed: i64 = 0;
    if values {
        vbytes = buffer_slot();
        if not vbytes {
            return i32(-1);
        }
        if PyObject_GetBuffer(values, vbytes, PyBUF_SIMPLE) != i32(0) {
            PyErr_Format(
                PyExc_TypeError,
                "can't set bytearray slice from %.100s",
                object_type(values).view(1)[0].tp_name
            );
            buffer_free(vbytes);
            return i32(-1);
        }
        needed = vbytes.view(1)[0].length;
        data = ptr[u8](vbytes.view(1)[0].buf);
    }
    # del b[lo:hi] leaves bytes NULL and needed 0.
    lo = lo_in;
    hi = hi_in;
    if lo < 0 {
        lo = 0;
    }
    if hi < lo {
        hi = lo;
    }
    if hi > object_size(op) {
        hi = object_size(op);
    }
    res = bytearray_setslice_linear(op, lo, hi, data, needed);
    if vbytes {
        buffer_free(vbytes);
    }
    return res;
}

def bytearray_setitem(op: ptr[PyObject], index: i64, value: ptr[PyObject]) -> i32 {
    # GH-91153: We need to do this *before* the size check, in case value
    # has a nasty __index__ method that changes the size of the bytearray:
    ival: i64 = -1;
    if value {
        (ok, ival) = getbytevalue(value);
        if not ok {
            return i32(-1);
        }
    }
    i = index;
    if i < 0 {
        i += object_size(op);
    }
    if i < 0 or i >= object_size(op) {
        PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
        return i32(-1);
    }
    if not value {
        return bytearray_setslice(op, i, i + 1, NULL);
    }
    poke(ba_as_string(op) + i, u8(ival));
    return i32(0);
}

"""Delete the extended slice of `slicelen` bytes from `start` by `step`
(not 1), moving the kept bytes down in place."""
def bytearray_delete_extended(
    op: ptr[PyObject], start_in: i64, step_in: i64, slicelen: i64
) -> i32 {
    buf = ba_as_string(op);
    if not can_resize(op) {
        return i32(-1);
    }
    if slicelen == 0 {
        # Nothing to do here.
        return i32(0);
    }
    start = start_in;
    step = step_in;
    if step < 0 {
        stop = start + 1;
        start = stop + step * (slicelen - 1) - 1;
        step = -step;
    }
    size = object_size(op);
    # cur is a size_t in C: past the last byte it must not overflow.
    cur = u64(start);
    for i in range(slicelen) {
        lim = step - 1;
        if cur + u64(step) >= u64(size) {
            lim = size - i64(cur) - 1;
        }
        memmove(ptr(buf + (i64(cur) - i)), ptr(buf + i64(cur) + 1), u64(lim));
        cur = cur + u64(step);
    }
    # Move the tail of the bytes, in one chunk
    cur = u64(start) + u64(slicelen) * u64(step);
    if cur < u64(size) {
        memmove(
            ptr(buf + (i64(cur) - slicelen)), ptr(buf + i64(cur)), u64(size - i64(cur))
        );
    }
    if bytearray_resize(op, size - slicelen) < i32(0) {
        return i32(-1);
    }
    return i32(0);
}

def bytearray_ass_subscript(
    op: ptr[PyObject], index: ptr[PyObject], values: ptr[PyObject]
) -> i32 {
    start: i64 = 0;
    stop: i64 = 0;
    step: i64 = 0;
    slicelen: i64 = 0;
    # Do not store a reference to the internal buffer since
    # index.__index__() or _getbytevalue() may alter 'self'.
    # See https://github.com/python/cpython/issues/91153.
    if PyIndex_Check(index) != i32(0) {
        i = PyNumber_AsSsize_t(index, PyExc_IndexError);
        if i == -1 and PyErr_Occurred() {
            return i32(-1);
        }
        # GH-91153: We need to do this *before* the size check, in case
        # values has a nasty __index__ method that changes the size of the
        # bytearray:
        ival: i64 = -1;
        if values {
            (ok, ival) = getbytevalue(values);
            if not ok {
                return i32(-1);
            }
        }
        if i < 0 {
            i += object_size(op);
        }
        if i < 0 or i >= object_size(op) {
            PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
            return i32(-1);
        }
        if values {
            poke(ba_as_string(op) + i, u8(ival));
            return i32(0);
        }
        # Fall through to slice assignment
        start = i;
        stop = i + 1;
        step = 1;
        slicelen = 1;
    } elif slice_check(index) {
        if PySlice_Unpack(index, &mut start, &mut stop, &mut step) < i32(0) {
            return i32(-1);
        }
        slicelen = PySlice_AdjustIndices(object_size(op), &mut start, &mut stop, step);
    } else {
        PyErr_Format(
            PyExc_TypeError,
            "bytearray indices must be integers or slices, not %.200s",
            object_type(index).view(1)[0].tp_name
        );
        return i32(-1);
    }
    data = ptr[u8]();
    needed: i64 = 0;
    if values {
        if values == op or not bytearray_check(values) {
            if PyNumber_Check(values) != i32(0) or unicode_check(values) {
                PyErr_SetString(
                    PyExc_TypeError,
                    "can assign only bytes, buffers, or iterables of ints in range(0, 256)"
                );
                return i32(-1);
            }
            # Make a copy and call this function recursively
            copy = PyByteArray_FromObject(values);
            if not copy {
                return i32(-1);
            }
            err = bytearray_ass_subscript(op, index, copy);
            object_decref(copy);
            return err;
        }
        data = ba_as_string(values);
        needed = object_size(values);
    }
    # Make sure b[5:2] = ... inserts before 5, not before 2.
    if (step < 0 and start < stop) or (step > 0 and start > stop) {
        stop = start;
    }
    if step == 1 {
        return bytearray_setslice_linear(op, start, stop, data, needed);
    }
    if needed == 0 {
        # Delete slice
        return bytearray_delete_extended(op, start, step, slicelen);
    }
    # Assign slice
    buf = ba_as_string(op);
    if needed != slicelen {
        PyErr_Format(
            PyExc_ValueError,
            "attempt to assign bytes of size %zd to extended slice of size %zd",
            needed,
            slicelen
        );
        return i32(-1);
    }
    cur = start;
    for k in range(slicelen) {
        poke(buf + cur, peek(data + k));
        cur = wrapping_add(cur, step);
    }
    return i32(0);
}

def bytearray_contains(op: ptr[PyObject], arg: ptr[PyObject]) -> i32 {
    # Increase exports to prevent bytearray storage from changing during
    # _Py_bytes_contains().
    add_exports(op, 1);
    ret = _Py_bytes_contains(ba_as_string(op), object_size(op), arg);
    add_exports(op, -1);
    return ret;
}

# --------------------------------------------------------- bytearray()
"""A str argument as clinic converts it to a C string: (True, its UTF-8),
or False with an error set. `which` names the argument in the TypeError."""
def text_arg(value: ptr[PyObject], which: i64) -> tuple[bool, ptr[u8]] {
    if not unicode_check(value) {
        if which == ARG_DECODE_ENCODING {
            _PyArg_BadArgument("decode", "argument 'encoding'", "str", value);
        } elif which == ARG_DECODE_ERRORS {
            _PyArg_BadArgument("decode", "argument 'errors'", "str", value);
        } elif which == ARG_INIT_ENCODING {
            _PyArg_BadArgument("bytearray", "argument 'encoding'", "str", value);
        } else {
            _PyArg_BadArgument("bytearray", "argument 'errors'", "str", value);
        }
        return (False, ptr[u8]());
    }
    length: i64 = 0;
    text = PyUnicode_AsUTF8AndSize(value, &mut length);
    if not text {
        return (False, text);
    }
    if i64(strlen(text)) != length {
        PyErr_SetString(PyExc_ValueError, "embedded null character");
        return (False, ptr[u8]());
    }
    return (True, text);
}

"""TypeError for an encoding or errors argument without a str source."""
def without_string_error(encoding: ptr[u8]) -> i32 {
    if encoding {
        PyErr_SetString(PyExc_TypeError, "encoding without a string argument");
    } else {
        PyErr_SetString(PyExc_TypeError, "errors without a string argument");
    }
    return i32(-1);
}

"""bytearray(list or tuple): the items when every one is an exact int; 1
(with the bytearray emptied again) when one is not, for the iterator path."""
def init_from_sequence(op: ptr[PyObject], arg: ptr[PyObject]) -> i32 {
    size = object_size(arg);
    if PyByteArray_Resize(op, size) < i32(0) {
        return i32(-1);
    }
    items = fast_items(arg);
    s = ba_as_string(op);
    for i in range(size) {
        item = (items + i).view(1)[0];
        if not long_check_exact(item) {
            # Resize to 0 and go through slowpath
            if object_size(op) != 0 and PyByteArray_Resize(op, 0) < i32(0) {
                return i32(-1);
            }
            return i32(1);
        }
        (ok, value) = getbytevalue(item);
        if not ok {
            return i32(-1);
        }
        poke(s + i, u8(value));
    }
    return i32(0);
}

"""bytearray(iterable): append the bytes the iterator yields."""
def init_from_iterable(op: ptr[PyObject], arg: ptr[PyObject]) -> i32 {
    # Get the iterator
    it = PyObject_GetIter(arg);
    if not it {
        if PyErr_ExceptionMatches(PyExc_TypeError) != i32(0) {
            PyErr_Format(
                PyExc_TypeError,
                "cannot convert '%.200s' object to bytearray",
                object_type(arg).view(1)[0].tp_name
            );
        }
        return i32(-1);
    }
    iter_type = object_type(it);
    # Run the iterator to exhaustion
    while True {
        # Get the next item
        item = iter_type.view(1)[0].tp_iternext(it);
        if not item {
            if PyErr_Occurred() {
                if PyErr_ExceptionMatches(PyExc_StopIteration) == i32(0) {
                    object_decref(it);
                    return i32(-1);
                }
                PyErr_Clear();
            }
            break;
        }
        # Interpret it as an int (__index__)
        (ok, value) = getbytevalue(item);
        object_decref(item);
        if not ok {
            object_decref(it);
            return i32(-1);
        }
        # Append the byte
        if object_size(op) + 1 < ba_alloc(op) {
            set_size(op, object_size(op) + 1);
            poke(ba_as_string(op) + object_size(op), u8(0));
        } elif PyByteArray_Resize(op, object_size(op) + 1) < i32(0) {
            object_decref(it);
            return i32(-1);
        }
        poke(ba_as_string(op) + (object_size(op) - 1), u8(value));
    }
    # Clean up and return success
    object_decref(it);
    return i32(0);
}

def bytearray_init_impl(
    op: ptr[PyObject], arg: ptr[PyObject], encoding: ptr[u8], errors: ptr[u8]
) -> i32 {
    if object_size(op) != 0 {
        # Empty previous contents (yes, do this first of all!)
        if PyByteArray_Resize(op, 0) < i32(0) {
            return i32(-1);
        }
    }
    # Make a quick exit if no first argument
    if not arg {
        if encoding or errors {
            return without_string_error(encoding);
        }
        return i32(0);
    }
    if unicode_check(arg) {
        # Encode via the codec registry
        if not encoding {
            PyErr_SetString(PyExc_TypeError, "string argument without an encoding");
            return i32(-1);
        }
        encoded = PyUnicode_AsEncodedString(arg, encoding, errors);
        if not encoded {
            return i32(-1);
        }
        appended = bytearray_iconcat(op, encoded);
        object_decref(encoded);
        if not appended {
            return i32(-1);
        }
        object_decref(appended);
        return i32(0);
    }
    # If it's not unicode, there can't be encoding or errors
    if encoding or errors {
        return without_string_error(encoding);
    }
    # Is it an int?
    if PyIndex_Check(arg) != i32(0) {
        count = PyNumber_AsSsize_t(arg, PyExc_OverflowError);
        if count == -1 and PyErr_Occurred() {
            if PyErr_ExceptionMatches(PyExc_TypeError) == i32(0) {
                return i32(-1);
            }
            # fall through
            PyErr_Clear();
        } else {
            if count < 0 {
                PyErr_SetString(PyExc_ValueError, "negative count");
                return i32(-1);
            }
            if count > 0 {
                if PyByteArray_Resize(op, count) != i32(0) {
                    return i32(-1);
                }
                memset(ptr(ba_as_string(op)), i32(0), u64(count));
            }
            return i32(0);
        }
    }
    # Use the buffer API
    if PyObject_CheckBuffer(arg) != i32(0) {
        view = buffer_slot();
        if not view {
            return i32(-1);
        }
        if PyObject_GetBuffer(arg, view, PyBUF_FULL_RO) < i32(0) {
            buffer_free(view);
            return i32(-1);
        }
        size = view.view(1)[0].length;
        failed = PyByteArray_Resize(op, size) < i32(0)
            or PyBuffer_ToContiguous(ptr(ba_as_string(op)), view, size, i8(ORDER_C))
                < i32(0);
        buffer_free(view);
        return i32(-1) if failed else i32(0);
    }
    if list_check_exact(arg) or tuple_check_exact(arg) {
        rc = init_from_sequence(op, arg);
        if rc != i32(1) {
            return rc;
        }
    }
    return init_from_iterable(op, arg);
}

"""bytearray.__init__ with encoding and errors still objects (NULL when
omitted)."""
def init_with(
    op: ptr[PyObject],
    source: ptr[PyObject],
    encoding_obj: ptr[PyObject],
    errors_obj: ptr[PyObject]
) -> i32 {
    encoding = ptr[u8]();
    errors = ptr[u8]();
    if encoding_obj {
        (ok, encoding) = text_arg(encoding_obj, ARG_INIT_ENCODING);
        if not ok {
            return i32(-1);
        }
    }
    if errors_obj {
        (ok2, errors) = text_arg(errors_obj, ARG_INIT_ERRORS);
        if not ok2 {
            return i32(-1);
        }
    }
    return bytearray_init_impl(op, source, encoding, errors);
}

def bytearray_init_bound(args: BoundArguments) -> ptr[PyObject] {
    if init_with(args.context, args.values[0], args.values[1], args.values[2])
        < i32(0) {
        return NULL;
    }
    return object_new_ref(Py_None);
}

"""tp_init: bytearray(source=NULL, encoding=NULL, errors=NULL); positional
calls skip the keyword parser."""
def bytearray___init__(
    op: ptr[PyObject], args: ptr[PyObject], kwds: ptr[PyObject]
) -> i32 {
    nargs = object_size(args);
    if not kwds and nargs <= 3 {
        return init_with(
            op,
            tuple_get_item(args, 0) if nargs >= 1 else NULL,
            tuple_get_item(args, 1) if nargs >= 2 else NULL,
            tuple_get_item(args, 2) if nargs >= 3 else NULL
        );
    }
    result = invoke(bytearray_init_signature, args, kwds, bytearray_init_bound, op);
    if not result {
        return i32(-1);
    }
    object_decref(result);
    return i32(0);
}

# ------------------------------------------------------------------ slots
"""Mostly copied from string_repr, but without the "smart quote"
functionality."""
def bytearray_repr(op: ptr[PyObject]) -> ptr[PyObject] {
    class_name = _PyType_Name(ptr[PyObject](object_type(op)));
    length = object_size(op);
    # 6 == strlen(quote_prefix) + 2 + strlen(quote_postfix) + 1
    name_len = i64(strlen(class_name));
    if length > (PY_SSIZE_T_MAX - 6 - name_len) // 4 {
        PyErr_SetString(
            PyExc_OverflowError, "bytearray object is too large to make repr"
        );
        return NULL;
    }
    newsize = name_len + 6 + length * 4;
    buffer = ptr[u8](PyMem_Malloc(u64(newsize)));
    if not buffer {
        PyErr_NoMemory();
        return NULL;
    }
    # Figure out which quote to use; single is preferred
    quote = CH_QUOTE;
    start = ba_as_string(op);
    for i in range(length) {
        c = i64(peek(start + i));
        if c == CH_DQUOTE {
            # back to single
            quote = CH_QUOTE;
            break;
        } elif c == CH_QUOTE {
            quote = CH_DQUOTE;
        }
    }
    p = buffer;
    memcpy(ptr(p), ptr(class_name), u64(name_len));
    p = p + name_len;
    poke(p, u8(CH_LPAREN));
    poke(p + 1, u8(CH_LOWER_B));
    poke(p + 2, u8(quote));
    p = p + 3;
    data = ba_as_string(op);
    for i in range(length) {
        # There's at least enough room for a hex escape and a closing quote.
        c = i64(peek(data + i));
        if c == CH_QUOTE or c == CH_BACKSLASH {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(c));
            p = p + 2;
        } elif c == CH_TAB {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(CH_LOWER_T));
            p = p + 2;
        } elif c == CH_NEWLINE {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(CH_LOWER_N));
            p = p + 2;
        } elif c == CH_RETURN {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(CH_LOWER_R));
            p = p + 2;
        } elif c == 0 {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(CH_LOWER_X));
            poke(p + 2, u8(CH_ZERO));
            poke(p + 3, u8(CH_ZERO));
            p = p + 4;
        } elif c < CH_SPACE or c >= CH_DEL {
            poke(p, u8(CH_BACKSLASH));
            poke(p + 1, u8(CH_LOWER_X));
            poke(p + 2, hex_char((c & 0xf0) >> 4));
            poke(p + 3, hex_char(c & 0xf));
            p = p + 4;
        } else {
            poke(p, u8(c));
            p = p + 1;
        }
    }
    poke(p, u8(quote));
    poke(p + 1, u8(CH_RPAREN));
    p = p + 2;
    v = PyUnicode_FromStringAndSize(buffer, span(buffer, p));
    PyMem_Free(ptr(buffer));
    return v;
}

def bytearray_str(op: ptr[PyObject]) -> ptr[PyObject] {
    if config_bytes_warning() != i32(0)
        and PyErr_WarnEx(PyExc_BytesWarning, "str() on a bytearray instance", 1)
            != i32(0) {
        return NULL;
    }
    return bytearray_repr(op);
}

def bytearray_richcompare(
    op: ptr[PyObject], other: ptr[PyObject], cmp_op: i32
) -> ptr[PyObject] {
    if PyObject_CheckBuffer(op) == i32(0) or PyObject_CheckBuffer(other) == i32(0) {
        if (unicode_check(op) or unicode_check(other))
            and config_bytes_warning() != i32(0)
            and (cmp_op == Py_EQ or cmp_op == Py_NE)
            and PyErr_WarnEx(
                PyExc_BytesWarning, "Comparison between bytearray and string", 1
            )
                != i32(0) {
            return NULL;
        }
        return object_new_ref(Py_NotImplemented);
    }
    self_bytes = buffer_slot();
    if not self_bytes {
        return NULL;
    }
    other_bytes = buffer_slot();
    if not other_bytes {
        PyMem_Free(ptr(self_bytes));
        return NULL;
    }
    # Bytearrays can be compared to anything that supports the buffer API.
    if PyObject_GetBuffer(op, self_bytes, PyBUF_SIMPLE) != i32(0) {
        PyErr_Clear();
        buffer_free(self_bytes);
        buffer_free(other_bytes);
        return object_new_ref(Py_NotImplemented);
    }
    self_size = self_bytes.view(1)[0].length;
    if PyObject_GetBuffer(other, other_bytes, PyBUF_SIMPLE) != i32(0) {
        PyErr_Clear();
        buffer_free(self_bytes);
        buffer_free(other_bytes);
        return object_new_ref(Py_NotImplemented);
    }
    other_size = other_bytes.view(1)[0].length;
    if self_size != other_size and (cmp_op == Py_EQ or cmp_op == Py_NE) {
        # Shortcut: if the lengths differ, the objects differ
        buffer_free(self_bytes);
        buffer_free(other_bytes);
        return PyBool_FromLong(1 if cmp_op == Py_NE else 0);
    }
    # In ISO C, memcmp() guarantees to use unsigned bytes!
    cmp = memcmp(
        self_bytes.view(1)[0].buf,
        other_bytes.view(1)[0].buf,
        u64(min(self_size, other_size))
    );
    buffer_free(self_bytes);
    buffer_free(other_bytes);
    if cmp != i32(0) {
        return rich_compare_values(i64(cmp), 0, cmp_op);
    }
    return rich_compare_values(self_size, other_size, cmp_op);
}

def bytearray_dealloc(op: ptr[PyObject]) {
    if ba_exports(op) > 0 {
        PyErr_SetString(
            PyExc_SystemError, "deallocated bytearray object has exported buffers"
        );
        PyErr_Print();
    }
    if ba_bytes(op) {
        PyMem_Free(ptr(ba_bytes(op)));
    }
    object_type(op).view(1)[0].tp_free(ptr(op));
}

def bytearray_mod(v: ptr[PyObject], w: ptr[PyObject]) -> ptr[PyObject] {
    if not bytearray_check(v) {
        return object_new_ref(Py_NotImplemented);
    }
    # Increase exports to prevent bytearray storage from changing during op.
    add_exports(v, 1);
    res = _PyBytes_FormatEx(ba_as_string(v), object_size(v), w, i32(1));
    add_exports(v, -1);
    return res;
}

# ----------------------------------------------------------------- methods
"""The optional [start[, end]] of find, index, rfind, rindex, count,
startswith and endswith (slice_index: an int or None): (True, start, end),
or False with an error set."""
def slice_bounds(args: ptr[ptr[PyObject]], nargs: i64) -> tuple[bool, i64, i64] {
    start: i64 = 0;
    end: i64 = PY_SSIZE_T_MAX;
    if nargs >= 2 and _PyEval_SliceIndex((args + 1).view(1)[0], &mut start) == i32(0) {
        return (False, start, end);
    }
    if nargs >= 3 and _PyEval_SliceIndex((args + 2).view(1)[0], &mut end) == i32(0) {
        return (False, start, end);
    }
    return (True, start, end);
}

def bytearray_find(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("find", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_FIND, args.view(1)[0], start, end);
}

def bytearray_count(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("count", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_COUNT, args.view(1)[0], start, end);
}

def bytearray_clear(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    if PyByteArray_Resize(op, 0) < i32(0) {
        return NULL;
    }
    return object_new_ref(Py_None);
}

def bytearray_copy(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    return PyByteArray_FromStringAndSize(ba_as_string(op), object_size(op));
}

def bytearray_index(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("index", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_INDEX, args.view(1)[0], start, end);
}

def bytearray_rfind(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("rfind", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_RFIND, args.view(1)[0], start, end);
}

def bytearray_rindex(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("rindex", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_RINDEX, args.view(1)[0], start, end);
}

def bytearray_startswith(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("startswith", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_STARTSWITH, args.view(1)[0], start, end);
}

def bytearray_endswith(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 1 or nargs > 3)
        and _PyArg_CheckPositional("endswith", nargs, 1, 3) == i32(0) {
        return NULL;
    }
    (ok, start, end) = slice_bounds(args, nargs);
    if not ok {
        return NULL;
    }
    return bytearray_with_buffer(op, OP_ENDSWITH, args.view(1)[0], start, end);
}

"""removeprefix or removesuffix (METH_O, prefix/suffix: Py_buffer)."""
def remove_affix(op: ptr[PyObject], arg: ptr[PyObject], suffix: bool) -> ptr[PyObject] {
    affix = buffer_slot();
    if not affix {
        return NULL;
    }
    if PyObject_GetBuffer(arg, affix, PyBUF_SIMPLE) != i32(0) {
        buffer_free(affix);
        return NULL;
    }
    self_start = ba_as_string(op);
    self_len = object_size(op);
    affix_start = affix.view(1)[0].buf;
    affix_len = affix.view(1)[0].length;
    result = NULL;
    if suffix {
        if self_len >= affix_len
            and memcmp(
                ptr(self_start + (self_len - affix_len)), affix_start, u64(affix_len)
            )
                == i32(0) {
            result = PyByteArray_FromStringAndSize(self_start, self_len - affix_len);
        } else {
            result = PyByteArray_FromStringAndSize(self_start, self_len);
        }
    } elif self_len >= affix_len
        and memcmp(ptr(self_start), affix_start, u64(affix_len)) == i32(0) {
        result = PyByteArray_FromStringAndSize(
            self_start + affix_len, self_len - affix_len
        );
    } else {
        result = PyByteArray_FromStringAndSize(self_start, self_len);
    }
    buffer_free(affix);
    return result;
}

def bytearray_removeprefix(op: ptr[PyObject], prefix: ptr[PyObject]) -> ptr[PyObject] {
    return remove_affix(op, prefix, False);
}

def bytearray_removesuffix(op: ptr[PyObject], suffix: ptr[PyObject]) -> ptr[PyObject] {
    return remove_affix(op, suffix, True);
}

"""bytearray.resize(size): resize to `size`, setting new bytes to null
bytes."""
def bytearray_resize_method(op: ptr[PyObject], arg: ptr[PyObject]) -> ptr[PyObject] {
    (ok, size) = ssize_arg(arg);
    if not ok {
        return NULL;
    }
    start_size = object_size(op);
    if bytearray_resize(op, size) < i32(0) {
        return NULL;
    }
    # Set new bytes to null bytes
    if size > start_size {
        memset(ptr(ba_as_string(op) + start_size), i32(0), u64(size - start_size));
    }
    return object_new_ref(Py_None);
}

"""bytearray.translate with the views of table and delete (zeroed heap
slots the caller frees; releasing an unfilled one does nothing)."""
def translate_with(
    op: ptr[PyObject],
    table: ptr[PyObject],
    deletechars: ptr[PyObject],
    vtable: ptr[Py_buffer],
    vdel: ptr[Py_buffer]
) -> ptr[PyObject] {
    table_chars = ptr[u8]();
    if table != Py_None {
        if PyObject_GetBuffer(table, vtable, PyBUF_SIMPLE) != i32(0) {
            return NULL;
        }
        if vtable.view(1)[0].length != 256 {
            PyErr_SetString(
                PyExc_ValueError, "translation table must be 256 characters long"
            );
            return NULL;
        }
        table_chars = ptr[u8](vtable.view(1)[0].buf);
    }
    del_chars = ptr[u8]();
    dellen: i64 = 0;
    if deletechars {
        if PyObject_GetBuffer(deletechars, vdel, PyBUF_SIMPLE) != i32(0) {
            return NULL;
        }
        del_chars = ptr[u8](vdel.view(1)[0].buf);
        dellen = vdel.view(1)[0].length;
    }
    inlen = object_size(op);
    result = PyByteArray_FromStringAndSize(ptr[u8](), inlen);
    if not result {
        return NULL;
    }
    output_start = ba_as_string(result);
    output = output_start;
    input = ba_as_string(op);
    if dellen == 0 and table_chars {
        # If no deletions are required, use faster code
        for i in range(inlen) {
            poke(output + i, peek(table_chars + i64(peek(input + i))));
        }
        return result;
    }
    # C's int trans_table[256], on the heap.
    trans_table = ptr[i64](PyMem_Malloc(u64(256 * 8)));
    if not trans_table {
        object_decref(result);
        return PyErr_NoMemory();
    }
    for i in range(256) {
        if table_chars {
            (trans_table + i).view(1)[0] = i64(peek(table_chars + i));
        } else {
            (trans_table + i).view(1)[0] = i;
        }
    }
    for i in range(dellen) {
        (trans_table + i64(peek(del_chars + i))).view(1)[0] = -1;
    }
    for i in range(inlen) {
        code = i64(peek(input + i));
        translated = (trans_table + code).view(1)[0];
        if translated != -1 {
            poke(output, u8(translated));
            output = output + 1;
        }
    }
    PyMem_Free(ptr(trans_table));
    # Fix the size of the resulting bytearray
    if inlen > 0 and PyByteArray_Resize(result, span(output_start, output)) < i32(0) {
        object_decref(result);
        return NULL;
    }
    return result;
}

def bytearray_translate_impl(
    op: ptr[PyObject], table: ptr[PyObject], deletechars: ptr[PyObject]
) -> ptr[PyObject] {
    vtable = buffer_slot();
    if not vtable {
        return NULL;
    }
    vdel = buffer_slot();
    if not vdel {
        PyMem_Free(ptr(vtable));
        return NULL;
    }
    result = translate_with(op, table, deletechars, vtable, vdel);
    buffer_free(vtable);
    buffer_free(vdel);
    return result;
}

def bytearray_translate_bound(args: BoundArguments) -> ptr[PyObject] {
    return bytearray_translate_impl(args.context, args.values[0], args.values[1]);
}

def bytearray_translate(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs >= 1 and nargs <= 2 {
        return bytearray_translate_impl(
            op, args.view(1)[0], (args + 1).view(1)[0] if nargs >= 2 else NULL
        );
    }
    return invoke_vector(
        translate_signature, args, nargs, kwnames, bytearray_translate_bound, op
    );
}

"""bytearray.maketrans(frm, to) (a static method)."""
def bytearray_maketrans(
    _null: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs != 2 and _PyArg_CheckPositional("maketrans", nargs, 2, 2) == i32(0) {
        return NULL;
    }
    frm = buffer_slot();
    if not frm {
        return NULL;
    }
    to = buffer_slot();
    if not to {
        PyMem_Free(ptr(frm));
        return NULL;
    }
    result = NULL;
    if PyObject_GetBuffer(args.view(1)[0], frm, PyBUF_SIMPLE) == i32(0)
        and PyObject_GetBuffer((args + 1).view(1)[0], to, PyBUF_SIMPLE) == i32(0) {
        result = _Py_bytes_maketrans(frm, to);
    }
    buffer_free(frm);
    buffer_free(to);
    return result;
}

def bytearray_replace(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if (nargs < 2 or nargs > 3)
        and _PyArg_CheckPositional("replace", nargs, 2, 3) == i32(0) {
        return NULL;
    }
    old = buffer_slot();
    if not old {
        return NULL;
    }
    repl = buffer_slot();
    if not repl {
        PyMem_Free(ptr(old));
        return NULL;
    }
    result = NULL;
    if PyObject_GetBuffer(args.view(1)[0], old, PyBUF_SIMPLE) == i32(0)
        and PyObject_GetBuffer((args + 1).view(1)[0], repl, PyBUF_SIMPLE) == i32(0) {
        ok = True;
        count: i64 = -1;
        if nargs >= 3 {
            (ok, count) = ssize_arg((args + 2).view(1)[0]);
        }
        if ok {
            result = bl_replace(
                op,
                ptr[u8](old.view(1)[0].buf),
                old.view(1)[0].length,
                ptr[u8](repl.view(1)[0].buf),
                repl.view(1)[0].length,
                count
            );
        }
    }
    buffer_free(old);
    buffer_free(repl);
    return result;
}

"""bytearray.split and bytearray.rsplit: the sections of the bytearray
around `sep` (a bytes-like object, or None for runs of ASCII whitespace), at
most `maxsplit` of them when it is not negative."""
def split_impl(
    op: ptr[PyObject], sep: ptr[PyObject], maxsplit_in: i64, reverse: bool
) -> ptr[PyObject] {
    # Increase exports to prevent bytearray storage from changing during
    # the split.
    add_exports(op, 1);
    sbuf = ba_as_string(op);
    slen = object_size(op);
    maxsplit = maxsplit_in;
    if maxsplit < 0 {
        maxsplit = PY_SSIZE_T_MAX;
    }
    result = NULL;
    if sep == Py_None {
        if reverse {
            result = bl_rsplit_whitespace(op, sbuf, slen, maxsplit);
        } else {
            result = bl_split_whitespace(op, sbuf, slen, maxsplit);
        }
    } else {
        vsub = buffer_slot();
        if vsub {
            if PyObject_GetBuffer(sep, vsub, PyBUF_SIMPLE) == i32(0) {
                sub = ptr[u8](vsub.view(1)[0].buf);
                n = vsub.view(1)[0].length;
                if reverse {
                    result = bl_rsplit(op, sbuf, slen, sub, n, maxsplit);
                } else {
                    result = bl_split(op, sbuf, slen, sub, n, maxsplit);
                }
            }
            buffer_free(vsub);
        }
    }
    add_exports(op, -1);
    return result;
}

"""split or rsplit with sep and maxsplit still objects (NULL when
omitted)."""
def split_with(
    op: ptr[PyObject], sep: ptr[PyObject], maxsplit_obj: ptr[PyObject], reverse: bool
) -> ptr[PyObject] {
    maxsplit: i64 = -1;
    if maxsplit_obj {
        (ok, maxsplit) = ssize_arg(maxsplit_obj);
        if not ok {
            return NULL;
        }
    }
    return split_impl(op, sep if sep else Py_None, maxsplit, reverse);
}

def bytearray_split_bound(args: BoundArguments) -> ptr[PyObject] {
    return split_with(args.context, args.values[0], args.values[1], False);
}

def bytearray_rsplit_bound(args: BoundArguments) -> ptr[PyObject] {
    return split_with(args.context, args.values[0], args.values[1], True);
}

def bytearray_split(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs <= 2 {
        return split_with(
            op,
            args.view(1)[0] if nargs >= 1 else NULL,
            (args + 1).view(1)[0] if nargs >= 2 else NULL,
            False
        );
    }
    return invoke_vector(
        split_signature, args, nargs, kwnames, bytearray_split_bound, op
    );
}

def bytearray_rsplit(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs <= 2 {
        return split_with(
            op,
            args.view(1)[0] if nargs >= 1 else NULL,
            (args + 1).view(1)[0] if nargs >= 2 else NULL,
            True
        );
    }
    return invoke_vector(
        rsplit_signature, args, nargs, kwnames, bytearray_rsplit_bound, op
    );
}

"""bytearray.partition and bytearray.rpartition (METH_O): the separator is
copied into a bytearray first."""
def partition_with(
    op: ptr[PyObject], sep: ptr[PyObject], reverse: bool
) -> ptr[PyObject] {
    bytesep = bytearray_from_buffer_object(sep);
    if not bytesep {
        return NULL;
    }
    result = NULL;
    if reverse {
        result = bl_rpartition(
            op,
            ba_as_string(op),
            object_size(op),
            bytesep,
            ba_as_string(bytesep),
            object_size(bytesep)
        );
    } else {
        result = bl_partition(
            op,
            ba_as_string(op),
            object_size(op),
            bytesep,
            ba_as_string(bytesep),
            object_size(bytesep)
        );
    }
    object_decref(bytesep);
    return result;
}

def bytearray_partition(op: ptr[PyObject], sep: ptr[PyObject]) -> ptr[PyObject] {
    return partition_with(op, sep, False);
}

def bytearray_rpartition(op: ptr[PyObject], sep: ptr[PyObject]) -> ptr[PyObject] {
    return partition_with(op, sep, True);
}

def bytearray_reverse(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    n = object_size(op);
    j = n // 2;
    head = ba_as_string(op);
    tail = head + (n - 1);
    for i in range(j) {
        swap = peek(head);
        poke(head, peek(tail));
        poke(tail, swap);
        head = head + 1;
        tail = tail + (-1);
    }
    return object_new_ref(Py_None);
}

def bytearray_insert(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs != 2 and _PyArg_CheckPositional("insert", nargs, 2, 2) == i32(0) {
        return NULL;
    }
    (ok, index) = ssize_arg(args.view(1)[0]);
    if not ok {
        return NULL;
    }
    (ok2, item) = getbytevalue((args + 1).view(1)[0]);
    if not ok2 {
        return NULL;
    }
    n = object_size(op);
    if n == PY_SSIZE_T_MAX {
        PyErr_SetString(PyExc_OverflowError, "cannot add more objects to bytearray");
        return NULL;
    }
    if bytearray_resize(op, n + 1) < i32(0) {
        return NULL;
    }
    buf = ba_as_string(op);
    if index < 0 {
        index += n;
        if index < 0 {
            index = 0;
        }
    }
    if index > n {
        index = n;
    }
    memmove(ptr(buf + index + 1), ptr(buf + index), u64(n - index));
    poke(buf + index, u8(item));
    return object_new_ref(Py_None);
}

# The stringlib methods bytearray shares with bytes (bytes_methods.jac).
# C wraps each in a critical section, which the GIL build compiles out.
def bytearray_isalnum(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isalnum(op, ignored);
}

def bytearray_isalpha(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isalpha(op, ignored);
}

def bytearray_isascii(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isascii(op, ignored);
}

def bytearray_isdigit(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isdigit(op, ignored);
}

def bytearray_islower(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_islower(op, ignored);
}

def bytearray_isspace(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isspace(op, ignored);
}

def bytearray_istitle(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_istitle(op, ignored);
}

def bytearray_isupper(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_isupper(op, ignored);
}

def bytearray_capitalize(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_capitalize(op, ignored);
}

def bytearray_swapcase(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_swapcase(op, ignored);
}

def bytearray_title(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_title(op, ignored);
}

def bytearray_upper(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_upper(op, ignored);
}

def bytearray_lower(op: ptr[PyObject], ignored: ptr[PyObject]) -> ptr[PyObject] {
    return bl_lower(op, ignored);
}

def bytearray_center(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    return bl_center(op, args, nargs);
}

def bytearray_expandtabs(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    return bl_expandtabs(op, args, nargs, kwnames);
}

def bytearray_ljust(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    return bl_ljust(op, args, nargs);
}

def bytearray_rjust(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    return bl_rjust(op, args, nargs);
}

def bytearray_zfill(op: ptr[PyObject], arg: ptr[PyObject]) -> ptr[PyObject] {
    return bl_zfill(op, arg);
}

def bytearray_append(op: ptr[PyObject], arg: ptr[PyObject]) -> ptr[PyObject] {
    (ok, item) = getbytevalue(arg);
    if not ok {
        return NULL;
    }
    n = object_size(op);
    if n == PY_SSIZE_T_MAX {
        PyErr_SetString(PyExc_OverflowError, "cannot add more objects to bytearray");
        return NULL;
    }
    if bytearray_resize(op, n + 1) < i32(0) {
        return NULL;
    }
    poke(ba_as_string(op) + n, u8(item));
    return object_new_ref(Py_None);
}

def bytearray_extend(
    op: ptr[PyObject], iterable_of_ints: ptr[PyObject]
) -> ptr[PyObject] {
    # bytearray_setslice code only accepts something supporting PEP 3118.
    if PyObject_CheckBuffer(iterable_of_ints) != i32(0) {
        if bytearray_setslice(op, object_size(op), object_size(op), iterable_of_ints)
            == i32(-1) {
            return NULL;
        }
        return object_new_ref(Py_None);
    }
    it = PyObject_GetIter(iterable_of_ints);
    if not it {
        if PyErr_ExceptionMatches(PyExc_TypeError) != i32(0) {
            PyErr_Format(
                PyExc_TypeError,
                "can't extend bytearray with %.100s",
                object_type(iterable_of_ints).view(1)[0].tp_name
            );
        }
        return NULL;
    }
    # Try to determine the length of the argument. 32 is arbitrary.
    buf_size = PyObject_LengthHint(iterable_of_ints, 32);
    if buf_size == -1 {
        object_decref(it);
        return NULL;
    }
    bytearray_obj = PyByteArray_FromStringAndSize(ptr[u8](), buf_size);
    if not bytearray_obj {
        object_decref(it);
        return NULL;
    }
    buf = ba_as_string(bytearray_obj);
    length: i64 = 0;
    while True {
        item = PyIter_Next(it);
        if not item {
            break;
        }
        (ok, value) = getbytevalue(item);
        if not ok {
            if PyErr_ExceptionMatches(PyExc_TypeError) != i32(0)
                and unicode_check(iterable_of_ints) {
                PyErr_Format(
                    PyExc_TypeError, "expected iterable of integers; got: 'str'"
                );
            }
            object_decref(item);
            object_decref(it);
            object_decref(bytearray_obj);
            return NULL;
        }
        object_decref(item);
        if length >= buf_size {
            if length == PY_SSIZE_T_MAX {
                object_decref(it);
                object_decref(bytearray_obj);
                return PyErr_NoMemory();
            }
            addition = length >> 1 if length != 0 else 1;
            if addition > PY_SSIZE_T_MAX - length - 1 {
                buf_size = PY_SSIZE_T_MAX;
            } else {
                buf_size = length + addition + 1;
            }
            if bytearray_resize(bytearray_obj, buf_size) < i32(0) {
                object_decref(it);
                object_decref(bytearray_obj);
                return NULL;
            }
            # Recompute the `buf' pointer, since the resizing operation may
            # have invalidated it.
            buf = ba_as_string(bytearray_obj);
        }
        poke(buf + length, u8(value));
        length += 1;
    }
    object_decref(it);
    if PyErr_Occurred() {
        object_decref(bytearray_obj);
        return NULL;
    }
    # Resize down to exact size.
    if bytearray_resize(bytearray_obj, length) < i32(0) {
        object_decref(bytearray_obj);
        return NULL;
    }
    if bytearray_setslice(op, object_size(op), object_size(op), bytearray_obj)
        == i32(-1) {
        object_decref(bytearray_obj);
        return NULL;
    }
    object_decref(bytearray_obj);
    return object_new_ref(Py_None);
}

def bytearray_pop(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs > 1 and _PyArg_CheckPositional("pop", nargs, 0, 1) == i32(0) {
        return NULL;
    }
    index: i64 = -1;
    if nargs >= 1 {
        (ok, index) = ssize_arg(args.view(1)[0]);
        if not ok {
            return NULL;
        }
    }
    n = object_size(op);
    if n == 0 {
        PyErr_SetString(PyExc_IndexError, "pop from empty bytearray");
        return NULL;
    }
    if index < 0 {
        index += object_size(op);
    }
    if index < 0 or index >= object_size(op) {
        PyErr_SetString(PyExc_IndexError, "pop index out of range");
        return NULL;
    }
    if not can_resize(op) {
        return NULL;
    }
    buf = ba_as_string(op);
    value = peek(buf + index);
    memmove(ptr(buf + index), ptr(buf + index + 1), u64(n - index));
    if bytearray_resize(op, n - 1) < i32(0) {
        return NULL;
    }
    return get_small_int(i64(value));
}

def bytearray_remove(op: ptr[PyObject], arg: ptr[PyObject]) -> ptr[PyObject] {
    (ok, value) = getbytevalue(arg);
    if not ok {
        return NULL;
    }
    n = object_size(op);
    buf = ba_as_string(op);
    where = bl_find_char(buf, n, u8(value));
    if where < 0 {
        PyErr_SetString(PyExc_ValueError, "value not found in bytearray");
        return NULL;
    }
    if not can_resize(op) {
        return NULL;
    }
    memmove(ptr(buf + where), ptr(buf + where + 1), u64(n - where));
    if bytearray_resize(op, n - 1) < i32(0) {
        return NULL;
    }
    return object_new_ref(Py_None);
}

"""Whether strip removes byte `c`: one of the `byteslen` bytes at
`bytesptr`, or, when `whitespace`, one of the six ASCII whitespace bytes C
lists (Py_ISSPACE tests the same set)."""
def strip_member(c: u8, whitespace: bool, bytesptr: ptr, byteslen: i64) -> bool {
    if whitespace {
        return py_isspace(c);
    }
    return not memchr(bytesptr, i32(c), u64(byteslen)).is_null();
}

"""bytearray_strip_impl_helper: strip the bytes of `chars` (None for ASCII
whitespace) from the left, the right or both ends."""
def strip_helper(
    op: ptr[PyObject], chars: ptr[PyObject], striptype: i64
) -> ptr[PyObject] {
    whitespace = chars == Py_None;
    vbytes = ptr[Py_buffer]();
    bytesptr = ptr();
    byteslen: i64 = 0;
    if not whitespace {
        vbytes = buffer_slot();
        if not vbytes {
            return NULL;
        }
        if PyObject_GetBuffer(chars, vbytes, PyBUF_SIMPLE) != i32(0) {
            buffer_free(vbytes);
            return NULL;
        }
        bytesptr = vbytes.view(1)[0].buf;
        byteslen = vbytes.view(1)[0].length;
    }
    myptr = ba_as_string(op);
    mysize = object_size(op);
    left: i64 = 0;
    if striptype != RIGHTSTRIP {
        while left < mysize
            and strip_member(peek(myptr + left), whitespace, bytesptr, byteslen) {
            left += 1;
        }
    }
    right = mysize;
    if striptype != LEFTSTRIP {
        right -= 1;
        while right >= left
            and strip_member(peek(myptr + right), whitespace, bytesptr, byteslen) {
            right -= 1;
        }
        right += 1;
    }
    if vbytes {
        buffer_free(vbytes);
    }
    return PyByteArray_FromStringAndSize(myptr + left, right - left);
}

def bytearray_strip(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs > 1 and _PyArg_CheckPositional("strip", nargs, 0, 1) == i32(0) {
        return NULL;
    }
    return strip_helper(op, args.view(1)[0] if nargs >= 1 else Py_None, BOTHSTRIP);
}

def bytearray_lstrip(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs > 1 and _PyArg_CheckPositional("lstrip", nargs, 0, 1) == i32(0) {
        return NULL;
    }
    return strip_helper(op, args.view(1)[0] if nargs >= 1 else Py_None, LEFTSTRIP);
}

def bytearray_rstrip(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs > 1 and _PyArg_CheckPositional("rstrip", nargs, 0, 1) == i32(0) {
        return NULL;
    }
    return strip_helper(op, args.view(1)[0] if nargs >= 1 else Py_None, RIGHTSTRIP);
}

"""bytearray.decode with encoding and errors still objects (NULL when
omitted, for the codec defaults)."""
def decode_with(
    op: ptr[PyObject], encoding_obj: ptr[PyObject], errors_obj: ptr[PyObject]
) -> ptr[PyObject] {
    encoding = ptr[u8]();
    errors = ptr[u8]();
    if encoding_obj {
        (ok, encoding) = text_arg(encoding_obj, ARG_DECODE_ENCODING);
        if not ok {
            return NULL;
        }
    }
    if errors_obj {
        (ok2, errors) = text_arg(errors_obj, ARG_DECODE_ERRORS);
        if not ok2 {
            return NULL;
        }
    }
    if not encoding {
        encoding = PyUnicode_GetDefaultEncoding();
    }
    return PyUnicode_FromEncodedObject(op, encoding, errors);
}

def bytearray_decode_bound(args: BoundArguments) -> ptr[PyObject] {
    return decode_with(args.context, args.values[0], args.values[1]);
}

def bytearray_decode(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs <= 2 {
        return decode_with(
            op,
            args.view(1)[0] if nargs >= 1 else NULL,
            (args + 1).view(1)[0] if nargs >= 2 else NULL
        );
    }
    return invoke_vector(
        decode_signature, args, nargs, kwnames, bytearray_decode_bound, op
    );
}

"""B.__alloc__() -> int: the number of bytes actually allocated."""
def bytearray_alloc(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    return PyLong_FromSsize_t(ba_alloc(op));
}

def bytearray_join(
    op: ptr[PyObject], iterable_of_bytes: ptr[PyObject]
) -> ptr[PyObject] {
    # this protects `self` from being cleared/resized if `iterable_of_bytes`
    # is a custom iterator
    add_exports(op, 1);
    ret = bl_bytes_join(op, iterable_of_bytes);
    # unexport `self`
    add_exports(op, -1);
    return ret;
}

def splitlines_with(op: ptr[PyObject], keepends_obj: ptr[PyObject]) -> ptr[PyObject] {
    keepends = i32(0);
    if keepends_obj {
        keepends = PyObject_IsTrue(keepends_obj);
        if keepends < i32(0) {
            return NULL;
        }
    }
    return bl_splitlines(op, ba_as_string(op), object_size(op), keepends);
}

def bytearray_splitlines_bound(args: BoundArguments) -> ptr[PyObject] {
    return splitlines_with(args.context, args.values[0]);
}

def bytearray_splitlines(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs <= 1 {
        return splitlines_with(op, args.view(1)[0] if nargs >= 1 else NULL);
    }
    return invoke_vector(
        splitlines_signature, args, nargs, kwnames, bytearray_splitlines_bound, op
    );
}

"""bytearray.fromhex (a class method): a bytearray from hexadecimal digit
pairs, a subclass instance built from it for a subclass."""
def bytearray_fromhex(type: ptr[PyObject], string: ptr[PyObject]) -> ptr[PyObject] {
    exact = type == ptr[PyObject](bytearray_type());
    result = _PyBytes_FromHex(string, i32(1) if exact else i32(0));
    if not exact and result {
        converted = PyObject_CallOneArg(type, result);
        object_decref(result);
        result = converted;
    }
    return result;
}

def hex_with(
    op: ptr[PyObject], sep: ptr[PyObject], per_sep_obj: ptr[PyObject]
) -> ptr[PyObject] {
    bytes_per_sep = i32(1);
    if per_sep_obj {
        bytes_per_sep = PyLong_AsInt(per_sep_obj);
        if bytes_per_sep == i32(-1) and PyErr_Occurred() {
            return NULL;
        }
    }
    argbuf = ba_as_string(op);
    arglen = object_size(op);
    # Prevent 'self' from being freed if computing len(sep) mutates 'self'
    # in _Py_strhex_with_sep().
    # See: https://github.com/python/cpython/issues/143195.
    add_exports(op, 1);
    res = _Py_strhex_with_sep(ptr(argbuf), arglen, sep, bytes_per_sep);
    add_exports(op, -1);
    return res;
}

def bytearray_hex_bound(args: BoundArguments) -> ptr[PyObject] {
    return hex_with(args.context, args.values[0], args.values[1]);
}

def bytearray_hex(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64, kwnames: ptr[PyObject]
) -> ptr[PyObject] {
    if not kwnames and nargs <= 2 {
        return hex_with(
            op,
            args.view(1)[0] if nargs >= 1 else NULL,
            (args + 1).view(1)[0] if nargs >= 2 else NULL
        );
    }
    return invoke_vector(hex_signature, args, nargs, kwnames, bytearray_hex_bound, op);
}

"""_common_reduce: (type, (contents...), state) for pickling; protocols
below 3 get a latin-1 str for Python 2."""
def common_reduce(op: ptr[PyObject], proto: i32) -> ptr[PyObject] {
    state = _PyObject_GetState(op);
    if not state {
        return NULL;
    }
    tp = ptr[PyObject](object_type(op));
    if object_size(op) == 0 {
        return Py_BuildValue("(O()N)", tp, state);
    }
    buf = ba_as_string(op);
    if proto < i32(3) {
        # use str based reduction for backwards compatibility with Python 2.x
        latin1 = PyUnicode_DecodeLatin1(ptr(buf), object_size(op), ptr[u8]());
        return Py_BuildValue("(O(Ns)N)", tp, latin1, ptr[u8]("latin-1"), state);
    }
    # use more efficient byte based reduction
    return Py_BuildValue("(O(y#)N)", tp, buf, object_size(op), state);
}

def bytearray_reduce(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    return common_reduce(op, i32(2));
}

def bytearray_reduce_ex(
    op: ptr[PyObject], args: ptr[ptr[PyObject]], nargs: i64
) -> ptr[PyObject] {
    if nargs > 1 and _PyArg_CheckPositional("__reduce_ex__", nargs, 0, 1) == i32(0) {
        return NULL;
    }
    proto = i32(0);
    if nargs >= 1 {
        proto = PyLong_AsInt(args.view(1)[0]);
        if proto == i32(-1) and PyErr_Occurred() {
            return NULL;
        }
    }
    return common_reduce(op, proto);
}

"""Returns the size of the bytearray object in memory, in bytes."""
def bytearray_sizeof(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    res = u64(object_type(op).view(1)[0].tp_basicsize);
    res += u64(ba_alloc(op));
    return PyLong_FromSize_t(res);
}

# ---------------------------------------------------------------- iterator
def baiter_of(op: ptr[PyObject]) -> ptr[bytesiterobject] {
    return ptr[bytesiterobject](op);
}

"""The iterated bytearray, or NULL once the iterator is exhausted."""
def baiter_seq(op: ptr[PyObject]) -> ptr[PyObject] {
    return ptr[PyObject](baiter_of(op).view(1)[0].it_seq);
}

def bytearrayiter_dealloc(op: ptr[PyObject]) {
    object_gc_untrack(op);
    object_xdecref(baiter_seq(op));
    PyObject_GC_Del(ptr(op));
}

def bytearrayiter_traverse(op: ptr[PyObject], visit_proc: ptr, arg: ptr) -> i32 {
    return visit_reference(baiter_seq(op), visit_proc, arg);
}

def bytearrayiter_next(op: ptr[PyObject]) -> ptr[PyObject] {
    it = baiter_of(op);
    index = it.view(1)[0].it_index;
    if index < 0 {
        return NULL;
    }
    seq = baiter_seq(op);
    val: i64 = -1;
    if index < object_size(seq) {
        val = i64(peek(ba_as_string(seq) + index));
    }
    if val == -1 {
        it.view(1)[0].it_index = -1;
        it.view(1)[0].it_seq = ptr[PyByteArrayObject]();
        object_decref(seq);
        return NULL;
    }
    it.view(1)[0].it_index = index + 1;
    return get_small_int(val);
}

def bytearrayiter_length_hint(
    op: ptr[PyObject], _unused: ptr[PyObject]
) -> ptr[PyObject] {
    length: i64 = 0;
    index = baiter_of(op).view(1)[0].it_index;
    if index >= 0 {
        length = object_size(baiter_seq(op)) - index;
        if length < 0 {
            length = 0;
        }
    }
    return PyLong_FromSsize_t(length);
}

def bytearrayiter_reduce(op: ptr[PyObject], _unused: ptr[PyObject]) -> ptr[PyObject] {
    # _PyEval_GetBuiltin can invoke arbitrary code, call must be before
    # access of iterator pointers. see issue #101765
    iter_builtin = eval_builtin("iter");
    index = baiter_of(op).view(1)[0].it_index;
    if index >= 0 {
        return Py_BuildValue("N(O)n", iter_builtin, baiter_seq(op), index);
    }
    return Py_BuildValue("N(())", iter_builtin);
}

def bytearrayiter_setstate(op: ptr[PyObject], state: ptr[PyObject]) -> ptr[PyObject] {
    index = PyLong_AsSsize_t(state);
    if index == -1 and PyErr_Occurred() {
        return NULL;
    }
    it = baiter_of(op);
    if it.view(1)[0].it_index >= 0 {
        if index < -1 {
            index = -1;
        } else {
            size = object_size(baiter_seq(op));
            if index > size {
                # iterator at end
                index = size;
            }
        }
        it.view(1)[0].it_index = index;
    }
    return object_new_ref(Py_None);
}

def bytearray_iter(seq: ptr[PyObject]) -> ptr[PyObject] {
    if not bytearray_check(seq) {
        PyErr_BadInternalCall();
        return NULL;
    }
    op = _PyObject_GC_New(ptr[PyObject](addressof(PyByteArrayIter_Type)));
    if not op {
        return NULL;
    }
    it = baiter_of(op);
    # -1 indicates exhausted
    it.view(1)[0].it_index = 0;
    it.view(1)[0].it_seq = ptr[PyByteArrayObject](object_new_ref(seq));
    object_gc_track(op);
    return op;
}
