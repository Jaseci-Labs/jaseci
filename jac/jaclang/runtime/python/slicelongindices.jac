# _PySlice_GetLongIndices from Objects/sliceobject.c, in its own module so
# that sliceobject.jac (slice.indices) and rangeobject.jac (range[slice]) can
# both call it through its C symbol: `&mut` out-params lower to addresses for
# C externs, not for Jac `ptr` params, and a module cannot declare its own
# function as an extern.

import from jaclang.runtime.python.boolobject { PyLongObject_Layout, PyNumberMethods }

import from jaclang.runtime.python.refcount { py_xincref, py_xdecref }

import from c {
    obj PyObject;  obj PyObject_Layout {
        has ob_refcnt: i64 = 0,
            ob_type: ptr[PyObject] = ptr[PyObject]();
    }
    # PyTypeObject up to tp_as_number.
    obj PyTypeHead_Layout {
        has ob_refcnt: i64 = 0,
            ob_type: ptr = ptr(),
            ob_size: i64 = 0,
            tp_name: ptr = ptr(),
            tp_basicsize: i64 = 0,
            tp_itemsize: i64 = 0,
            tp_dealloc: ptr = ptr(),
            tp_vectorcall_offset: i64 = 0,
            tp_getattr: ptr = ptr(),
            tp_setattr: ptr = ptr(),
            tp_as_async: ptr = ptr(),
            tp_repr: ptr = ptr(),
            tp_as_number: ptr = ptr();
    }  obj PySliceObject_Layout {
        has ob_refcnt: i64 = 0,
            ob_type: ptr[PyObject] = ptr[PyObject](),
            start: ptr[PyObject] = ptr[PyObject](),
            stop: ptr[PyObject] = ptr[PyObject](),
            step: ptr[PyObject] = ptr[PyObject]();
    }
    # A `PyObject **` out-param.
    obj PyObjectSlot {
        has v: ptr[PyObject] = ptr[PyObject]();
    }  glob _Py_NoneStruct: PyObject_Layout; glob PyExc_TypeError: ptr[PyObject]; glob PyExc_ValueError:
             ptr[PyObject]; def PyErr_SetString(
        exc: ptr[PyObject], msg: ptr[u8]
    ) -> None;  def PyObject_RichCompareBool(
        a: ptr[PyObject], b: ptr[PyObject], op: i32
    ) -> i32;  def PyLong_FromSsize_t(v: i64) -> ptr[PyObject];  def PyNumber_Index(
        o: ptr[PyObject]
    ) -> ptr[PyObject];  def PyNumber_Add(
        a: ptr[PyObject], b: ptr[PyObject]
    ) -> ptr[PyObject];
    # The cached small ints 0 and 1 (borrowed, immortal).
    glob jacpy_small_zero: ptr[PyObject]; glob jacpy_small_one: ptr[PyObject];
}

# lv_tag sign encoding: (1 - sign) in the low two bits.
def gli_long_sign(o: ptr[PyObject]) -> i64 {
    return 1 - (ptr[PyLongObject_Layout](o).lv_tag & 3);
}

def gli_evaluate_index(v: ptr[PyObject]) -> ptr[PyObject] {
    ty = ptr[PyTypeHead_Layout](ptr[PyObject_Layout](v).ob_type);
    if ty.tp_as_number != ptr()
        and ptr[PyNumberMethods](ty.tp_as_number).nb_index != 0 {
        return PyNumber_Index(v);
    }
    PyErr_SetString(
        PyExc_TypeError,
        "slice indices must be integers or None or have an __index__ method"
    );
    return ptr[PyObject]();
}

# Clip an owned index: negative ones get `length` added and are raised to
# `lower`; others are lowered to `upper`. Consumes `v`; NULL on error.
def gli_clip(
    v: ptr[PyObject], length: ptr[PyObject], lower: ptr[PyObject], upper: ptr[PyObject]
) -> ptr[PyObject] {
    if gli_long_sign(v) < 0 {
        tmp = PyNumber_Add(v, length);
        py_xdecref(v);
        if tmp == ptr[PyObject]() {
            return ptr[PyObject]();
        }
        cmp_result = PyObject_RichCompareBool(tmp, lower, 0);
        if cmp_result < 0 {
            py_xdecref(tmp);
            return ptr[PyObject]();
        }
        if cmp_result != 0 {
            py_xdecref(tmp);
            py_xincref(lower);
            return lower;
        }
        return tmp;
    }
    cmp_result = PyObject_RichCompareBool(v, upper, 4);
    if cmp_result < 0 {
        py_xdecref(v);
        return ptr[PyObject]();
    }
    if cmp_result != 0 {
        py_xdecref(v);
        py_xincref(upper);
        return upper;
    }
    return v;
}

def gli_fail(
    start_ptr: ptr,
    stop_ptr: ptr,
    step_ptr: ptr,
    start: ptr[PyObject],
    step: ptr[PyObject],
    lower: ptr[PyObject],
    upper: ptr[PyObject]
) -> i32 {
    ptr[PyObjectSlot](start_ptr).v = ptr[PyObject]();
    ptr[PyObjectSlot](stop_ptr).v = ptr[PyObject]();
    ptr[PyObjectSlot](step_ptr).v = ptr[PyObject]();
    py_xdecref(start);
    py_xdecref(step);
    py_xdecref(lower);
    py_xdecref(upper);
    return -1;
}

# Compute slice indices given a slice and a nonnegative PyLong length.
# Returns -1 on failure (all three out-params set to NULL).
def:pub _PySlice_GetLongIndices(
    self_op: ptr, length_op: ptr, start_ptr: ptr, stop_ptr: ptr, step_ptr: ptr
) -> i32 {
    self = ptr[PySliceObject_Layout](self_op);
    length = ptr[PyObject](length_op);
    none_obj: ptr[PyObject] = _Py_NoneStruct;
    nul = ptr[PyObject]();

    step_is_negative = False;
    if self.step == none_obj {
        step = jacpy_small_one;
        py_xincref(step);
    } else {
        step = gli_evaluate_index(self.step);
        if step == nul {
            return gli_fail(start_ptr, stop_ptr, step_ptr, nul, nul, nul, nul);
        }
        sign = gli_long_sign(step);
        if sign == 0 {
            PyErr_SetString(PyExc_ValueError, "slice step cannot be zero");
            return gli_fail(start_ptr, stop_ptr, step_ptr, nul, step, nul, nul);
        }
        step_is_negative = sign < 0;
    }

    # Find lower and upper bounds for start and stop.
    if step_is_negative {
        lower = PyLong_FromSsize_t(-1);
        if lower == nul {
            return gli_fail(start_ptr, stop_ptr, step_ptr, nul, step, nul, nul);
        }
        upper = PyNumber_Add(length, lower);
        if upper == nul {
            return gli_fail(start_ptr, stop_ptr, step_ptr, nul, step, lower, nul);
        }
    } else {
        lower = jacpy_small_zero;
        py_xincref(lower);
        upper = length;
        py_xincref(upper);
    }

    # Compute start.
    if self.start == none_obj {
        start = upper if step_is_negative else lower;
        py_xincref(start);
    } else {
        start = gli_evaluate_index(self.start);
        if start != nul {
            start = gli_clip(start, length, lower, upper);
        }
        if start == nul {
            return gli_fail(start_ptr, stop_ptr, step_ptr, nul, step, lower, upper);
        }
    }

    # Compute stop.
    if self.stop == none_obj {
        stop = lower if step_is_negative else upper;
        py_xincref(stop);
    } else {
        stop = gli_evaluate_index(self.stop);
        if stop != nul {
            stop = gli_clip(stop, length, lower, upper);
        }
        if stop == nul {
            return gli_fail(start_ptr, stop_ptr, step_ptr, start, step, lower, upper);
        }
    }

    ptr[PyObjectSlot](start_ptr).v = start;
    ptr[PyObjectSlot](stop_ptr).v = stop;
    ptr[PyObjectSlot](step_ptr).v = step;
    py_xdecref(upper);
    py_xdecref(lower);
    return 0;
}
