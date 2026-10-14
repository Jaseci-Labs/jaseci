"""Actual manually constructed FX forward; weights are explicit arguments."""
import torch
from math import inf

def forward(self, source, target, weight_0, weight_1, weight_2, weight_3, weight_4, weight_5, weight_6, weight_7, weight_8, weight_9, weight_10, weight_11, weight_12, weight_13, weight_14, weight_15, weight_16, weight_17, weight_18, weight_19, weight_20, weight_21, weight_22, weight_23, weight_24, weight_25, weight_26, weight_27, weight_28, weight_29, weight_30, weight_31, weight_32, weight_33, weight_34, weight_35, weight_36, weight_37, weight_38, weight_39, weight_40, weight_41, weight_42, weight_43, weight_44, weight_45, weight_46):
    index_select_default = torch.ops.aten.index_select.default(weight_35, 0, source);  weight_35 = source = None
    mul_scalar = torch.ops.aten.mul.Scalar(index_select_default, 2.8284271247461903);  index_select_default = None
    slice_tensor = torch.ops.aten.slice.Tensor(weight_44, 0, 0, 4)
    add_tensor = torch.ops.aten.add.Tensor(mul_scalar, slice_tensor);  slice_tensor = None
    index_select_default_1 = torch.ops.aten.index_select.default(weight_16, 0, target);  weight_16 = target = None
    mul_scalar_1 = torch.ops.aten.mul.Scalar(index_select_default_1, 2.8284271247461903);  index_select_default_1 = None
    slice_tensor_1 = torch.ops.aten.slice.Tensor(weight_44, 0, 0, 3);  weight_44 = None
    add_tensor_1 = torch.ops.aten.add.Tensor(mul_scalar_1, slice_tensor_1);  slice_tensor_1 = None
    t_default = torch.ops.aten.t.default(weight_32);  weight_32 = None
    mm_default = torch.ops.aten.mm.default(add_tensor, t_default);  t_default = None
    add_tensor_2 = torch.ops.aten.add.Tensor(mm_default, weight_31);  mm_default = weight_31 = None
    reshape_default = torch.ops.aten.reshape.default(add_tensor_2, [4, 2, 4])
    transpose_int = torch.ops.aten.transpose.int(reshape_default, 0, 1);  reshape_default = None
    t_default_1 = torch.ops.aten.t.default(weight_28);  weight_28 = None
    mm_default_1 = torch.ops.aten.mm.default(add_tensor, t_default_1);  t_default_1 = None
    add_tensor_3 = torch.ops.aten.add.Tensor(mm_default_1, weight_27);  mm_default_1 = weight_27 = None
    reshape_default_1 = torch.ops.aten.reshape.default(add_tensor_3, [4, 2, 4])
    transpose_int_1 = torch.ops.aten.transpose.int(reshape_default_1, 0, 1);  reshape_default_1 = None
    t_default_2 = torch.ops.aten.t.default(weight_34);  weight_34 = None
    mm_default_2 = torch.ops.aten.mm.default(add_tensor, t_default_2);  t_default_2 = None
    add_tensor_4 = torch.ops.aten.add.Tensor(mm_default_2, weight_33);  mm_default_2 = weight_33 = None
    reshape_default_2 = torch.ops.aten.reshape.default(add_tensor_4, [4, 2, 4])
    transpose_int_2 = torch.ops.aten.transpose.int(reshape_default_2, 0, 1);  reshape_default_2 = None
    transpose_int_3 = torch.ops.aten.transpose.int(transpose_int_1, -2, -1);  transpose_int_1 = None
    bmm_default = torch.ops.aten.bmm.default(transpose_int, transpose_int_3);  transpose_int = transpose_int_3 = None
    div_scalar = torch.ops.aten.div.Scalar(bmm_default, 2.0);  bmm_default = None
    _softmax_default = torch.ops.aten._softmax.default(div_scalar, -1, False)
    bmm_default_1 = torch.ops.aten.bmm.default(_softmax_default, transpose_int_2);  transpose_int_2 = None
    transpose_int_4 = torch.ops.aten.transpose.int(bmm_default_1, 0, 1)
    contiguous_default = torch.ops.aten.contiguous.default(transpose_int_4);  transpose_int_4 = None
    reshape_default_3 = torch.ops.aten.reshape.default(contiguous_default, [4, 8]);  contiguous_default = None
    t_default_3 = torch.ops.aten.t.default(weight_30);  weight_30 = None
    mm_default_3 = torch.ops.aten.mm.default(reshape_default_3, t_default_3);  reshape_default_3 = t_default_3 = None
    add_tensor_5 = torch.ops.aten.add.Tensor(mm_default_3, weight_29);  mm_default_3 = weight_29 = None
    add_tensor_6 = torch.ops.aten.add.Tensor(add_tensor_5, add_tensor)
    mean_dim = torch.ops.aten.mean.dim(add_tensor_6, [-1], True)
    sub_tensor = torch.ops.aten.sub.Tensor(add_tensor_6, mean_dim);  mean_dim = None
    square_default = torch.ops.aten.square.default(sub_tensor)
    mean_dim_1 = torch.ops.aten.mean.dim(square_default, [-1], True);  square_default = None
    add_scalar = torch.ops.aten.add.Scalar(mean_dim_1, 1e-05);  mean_dim_1 = None
    rsqrt_default = torch.ops.aten.rsqrt.default(add_scalar);  add_scalar = None
    mul_tensor = torch.ops.aten.mul.Tensor(sub_tensor, rsqrt_default);  sub_tensor = rsqrt_default = None
    mul_tensor_1 = torch.ops.aten.mul.Tensor(mul_tensor, weight_41);  mul_tensor = weight_41 = None
    add_tensor_7 = torch.ops.aten.add.Tensor(mul_tensor_1, weight_40);  mul_tensor_1 = weight_40 = None
    t_default_4 = torch.ops.aten.t.default(weight_39);  weight_39 = None
    mm_default_4 = torch.ops.aten.mm.default(add_tensor_7, t_default_4);  t_default_4 = None
    add_tensor_8 = torch.ops.aten.add.Tensor(mm_default_4, weight_38);  mm_default_4 = weight_38 = None
    relu_default = torch.ops.aten.relu.default(add_tensor_8)
    t_default_5 = torch.ops.aten.t.default(weight_37);  weight_37 = None
    mm_default_5 = torch.ops.aten.mm.default(relu_default, t_default_5);  t_default_5 = None
    add_tensor_9 = torch.ops.aten.add.Tensor(mm_default_5, weight_36);  mm_default_5 = weight_36 = None
    add_tensor_10 = torch.ops.aten.add.Tensor(add_tensor_9, add_tensor_7)
    mean_dim_2 = torch.ops.aten.mean.dim(add_tensor_10, [-1], True)
    sub_tensor_1 = torch.ops.aten.sub.Tensor(add_tensor_10, mean_dim_2);  mean_dim_2 = None
    square_default_1 = torch.ops.aten.square.default(sub_tensor_1)
    mean_dim_3 = torch.ops.aten.mean.dim(square_default_1, [-1], True);  square_default_1 = None
    add_scalar_1 = torch.ops.aten.add.Scalar(mean_dim_3, 1e-05);  mean_dim_3 = None
    rsqrt_default_1 = torch.ops.aten.rsqrt.default(add_scalar_1);  add_scalar_1 = None
    mul_tensor_2 = torch.ops.aten.mul.Tensor(sub_tensor_1, rsqrt_default_1);  sub_tensor_1 = rsqrt_default_1 = None
    mul_tensor_3 = torch.ops.aten.mul.Tensor(mul_tensor_2, weight_43);  mul_tensor_2 = weight_43 = None
    add_tensor_11 = torch.ops.aten.add.Tensor(mul_tensor_3, weight_42);  mul_tensor_3 = weight_42 = None
    t_default_6 = torch.ops.aten.t.default(weight_13);  weight_13 = None
    mm_default_6 = torch.ops.aten.mm.default(add_tensor_1, t_default_6);  t_default_6 = None
    add_tensor_12 = torch.ops.aten.add.Tensor(mm_default_6, weight_12);  mm_default_6 = weight_12 = None
    reshape_default_4 = torch.ops.aten.reshape.default(add_tensor_12, [3, 2, 4])
    transpose_int_5 = torch.ops.aten.transpose.int(reshape_default_4, 0, 1);  reshape_default_4 = None
    t_default_7 = torch.ops.aten.t.default(weight_9);  weight_9 = None
    mm_default_7 = torch.ops.aten.mm.default(add_tensor_1, t_default_7);  t_default_7 = None
    add_tensor_13 = torch.ops.aten.add.Tensor(mm_default_7, weight_8);  mm_default_7 = weight_8 = None
    reshape_default_5 = torch.ops.aten.reshape.default(add_tensor_13, [3, 2, 4])
    transpose_int_6 = torch.ops.aten.transpose.int(reshape_default_5, 0, 1);  reshape_default_5 = None
    t_default_8 = torch.ops.aten.t.default(weight_15);  weight_15 = None
    mm_default_8 = torch.ops.aten.mm.default(add_tensor_1, t_default_8);  t_default_8 = None
    add_tensor_14 = torch.ops.aten.add.Tensor(mm_default_8, weight_14);  mm_default_8 = weight_14 = None
    reshape_default_6 = torch.ops.aten.reshape.default(add_tensor_14, [3, 2, 4])
    transpose_int_7 = torch.ops.aten.transpose.int(reshape_default_6, 0, 1);  reshape_default_6 = None
    transpose_int_8 = torch.ops.aten.transpose.int(transpose_int_6, -2, -1);  transpose_int_6 = None
    bmm_default_2 = torch.ops.aten.bmm.default(transpose_int_5, transpose_int_8);  transpose_int_5 = transpose_int_8 = None
    div_scalar_1 = torch.ops.aten.div.Scalar(bmm_default_2, 2.0);  bmm_default_2 = None
    ones_default = torch.ops.aten.ones.default([3, 3], dtype = torch.bool, device = device(type='cpu'))
    triu_default = torch.ops.aten.triu.default(ones_default, 1);  ones_default = None
    masked_fill_scalar = torch.ops.aten.masked_fill.Scalar(div_scalar_1, triu_default, -inf)
    _softmax_default_1 = torch.ops.aten._softmax.default(masked_fill_scalar, -1, False)
    bmm_default_3 = torch.ops.aten.bmm.default(_softmax_default_1, transpose_int_7);  transpose_int_7 = None
    transpose_int_9 = torch.ops.aten.transpose.int(bmm_default_3, 0, 1)
    contiguous_default_1 = torch.ops.aten.contiguous.default(transpose_int_9);  transpose_int_9 = None
    reshape_default_7 = torch.ops.aten.reshape.default(contiguous_default_1, [3, 8]);  contiguous_default_1 = None
    t_default_9 = torch.ops.aten.t.default(weight_11);  weight_11 = None
    mm_default_9 = torch.ops.aten.mm.default(reshape_default_7, t_default_9);  reshape_default_7 = t_default_9 = None
    add_tensor_15 = torch.ops.aten.add.Tensor(mm_default_9, weight_10);  mm_default_9 = weight_10 = None
    add_tensor_16 = torch.ops.aten.add.Tensor(add_tensor_15, add_tensor_1)
    mean_dim_4 = torch.ops.aten.mean.dim(add_tensor_16, [-1], True)
    sub_tensor_2 = torch.ops.aten.sub.Tensor(add_tensor_16, mean_dim_4);  mean_dim_4 = None
    square_default_2 = torch.ops.aten.square.default(sub_tensor_2)
    mean_dim_5 = torch.ops.aten.mean.dim(square_default_2, [-1], True);  square_default_2 = None
    add_scalar_2 = torch.ops.aten.add.Scalar(mean_dim_5, 1e-05);  mean_dim_5 = None
    rsqrt_default_2 = torch.ops.aten.rsqrt.default(add_scalar_2);  add_scalar_2 = None
    mul_tensor_4 = torch.ops.aten.mul.Tensor(sub_tensor_2, rsqrt_default_2);  sub_tensor_2 = rsqrt_default_2 = None
    mul_tensor_5 = torch.ops.aten.mul.Tensor(mul_tensor_4, weight_22);  mul_tensor_4 = weight_22 = None
    add_tensor_17 = torch.ops.aten.add.Tensor(mul_tensor_5, weight_21);  mul_tensor_5 = weight_21 = None
    t_default_10 = torch.ops.aten.t.default(weight_5);  weight_5 = None
    mm_default_10 = torch.ops.aten.mm.default(add_tensor_17, t_default_10);  t_default_10 = None
    add_tensor_18 = torch.ops.aten.add.Tensor(mm_default_10, weight_4);  mm_default_10 = weight_4 = None
    reshape_default_8 = torch.ops.aten.reshape.default(add_tensor_18, [3, 2, 4])
    transpose_int_10 = torch.ops.aten.transpose.int(reshape_default_8, 0, 1);  reshape_default_8 = None
    t_default_11 = torch.ops.aten.t.default(weight_1);  weight_1 = None
    mm_default_11 = torch.ops.aten.mm.default(add_tensor_11, t_default_11);  t_default_11 = None
    add_tensor_19 = torch.ops.aten.add.Tensor(mm_default_11, weight_0);  mm_default_11 = weight_0 = None
    reshape_default_9 = torch.ops.aten.reshape.default(add_tensor_19, [4, 2, 4])
    transpose_int_11 = torch.ops.aten.transpose.int(reshape_default_9, 0, 1);  reshape_default_9 = None
    t_default_12 = torch.ops.aten.t.default(weight_7);  weight_7 = None
    mm_default_12 = torch.ops.aten.mm.default(add_tensor_11, t_default_12);  t_default_12 = None
    add_tensor_20 = torch.ops.aten.add.Tensor(mm_default_12, weight_6);  mm_default_12 = weight_6 = None
    reshape_default_10 = torch.ops.aten.reshape.default(add_tensor_20, [4, 2, 4])
    transpose_int_12 = torch.ops.aten.transpose.int(reshape_default_10, 0, 1);  reshape_default_10 = None
    transpose_int_13 = torch.ops.aten.transpose.int(transpose_int_11, -2, -1);  transpose_int_11 = None
    bmm_default_4 = torch.ops.aten.bmm.default(transpose_int_10, transpose_int_13);  transpose_int_10 = transpose_int_13 = None
    div_scalar_2 = torch.ops.aten.div.Scalar(bmm_default_4, 2.0);  bmm_default_4 = None
    _softmax_default_2 = torch.ops.aten._softmax.default(div_scalar_2, -1, False)
    bmm_default_5 = torch.ops.aten.bmm.default(_softmax_default_2, transpose_int_12);  transpose_int_12 = None
    transpose_int_14 = torch.ops.aten.transpose.int(bmm_default_5, 0, 1)
    contiguous_default_2 = torch.ops.aten.contiguous.default(transpose_int_14);  transpose_int_14 = None
    reshape_default_11 = torch.ops.aten.reshape.default(contiguous_default_2, [3, 8]);  contiguous_default_2 = None
    t_default_13 = torch.ops.aten.t.default(weight_3);  weight_3 = None
    mm_default_13 = torch.ops.aten.mm.default(reshape_default_11, t_default_13);  reshape_default_11 = t_default_13 = None
    add_tensor_21 = torch.ops.aten.add.Tensor(mm_default_13, weight_2);  mm_default_13 = weight_2 = None
    add_tensor_22 = torch.ops.aten.add.Tensor(add_tensor_21, add_tensor_17)
    mean_dim_6 = torch.ops.aten.mean.dim(add_tensor_22, [-1], True)
    sub_tensor_3 = torch.ops.aten.sub.Tensor(add_tensor_22, mean_dim_6);  mean_dim_6 = None
    square_default_3 = torch.ops.aten.square.default(sub_tensor_3)
    mean_dim_7 = torch.ops.aten.mean.dim(square_default_3, [-1], True);  square_default_3 = None
    add_scalar_3 = torch.ops.aten.add.Scalar(mean_dim_7, 1e-05);  mean_dim_7 = None
    rsqrt_default_3 = torch.ops.aten.rsqrt.default(add_scalar_3);  add_scalar_3 = None
    mul_tensor_6 = torch.ops.aten.mul.Tensor(sub_tensor_3, rsqrt_default_3);  sub_tensor_3 = rsqrt_default_3 = None
    mul_tensor_7 = torch.ops.aten.mul.Tensor(mul_tensor_6, weight_24);  mul_tensor_6 = weight_24 = None
    add_tensor_23 = torch.ops.aten.add.Tensor(mul_tensor_7, weight_23);  mul_tensor_7 = weight_23 = None
    t_default_14 = torch.ops.aten.t.default(weight_20);  weight_20 = None
    mm_default_14 = torch.ops.aten.mm.default(add_tensor_23, t_default_14);  t_default_14 = None
    add_tensor_24 = torch.ops.aten.add.Tensor(mm_default_14, weight_19);  mm_default_14 = weight_19 = None
    relu_default_1 = torch.ops.aten.relu.default(add_tensor_24)
    t_default_15 = torch.ops.aten.t.default(weight_18);  weight_18 = None
    mm_default_15 = torch.ops.aten.mm.default(relu_default_1, t_default_15);  t_default_15 = None
    add_tensor_25 = torch.ops.aten.add.Tensor(mm_default_15, weight_17);  mm_default_15 = weight_17 = None
    add_tensor_26 = torch.ops.aten.add.Tensor(add_tensor_25, add_tensor_23)
    mean_dim_8 = torch.ops.aten.mean.dim(add_tensor_26, [-1], True)
    sub_tensor_4 = torch.ops.aten.sub.Tensor(add_tensor_26, mean_dim_8);  mean_dim_8 = None
    square_default_4 = torch.ops.aten.square.default(sub_tensor_4)
    mean_dim_9 = torch.ops.aten.mean.dim(square_default_4, [-1], True);  square_default_4 = None
    add_scalar_4 = torch.ops.aten.add.Scalar(mean_dim_9, 1e-05);  mean_dim_9 = None
    rsqrt_default_4 = torch.ops.aten.rsqrt.default(add_scalar_4);  add_scalar_4 = None
    mul_tensor_8 = torch.ops.aten.mul.Tensor(sub_tensor_4, rsqrt_default_4);  sub_tensor_4 = rsqrt_default_4 = None
    mul_tensor_9 = torch.ops.aten.mul.Tensor(mul_tensor_8, weight_26);  mul_tensor_8 = weight_26 = None
    add_tensor_27 = torch.ops.aten.add.Tensor(mul_tensor_9, weight_25);  mul_tensor_9 = weight_25 = None
    t_default_16 = torch.ops.aten.t.default(weight_46);  weight_46 = None
    mm_default_16 = torch.ops.aten.mm.default(add_tensor_27, t_default_16);  t_default_16 = None
    add_tensor_28 = torch.ops.aten.add.Tensor(mm_default_16, weight_45);  mm_default_16 = weight_45 = None
    _softmax_default_3 = torch.ops.aten._softmax.default(add_tensor_28, -1, False)
    return (_softmax_default_3, mul_scalar, add_tensor, mul_scalar_1, add_tensor_1, add_tensor_2, add_tensor_3, add_tensor_4, div_scalar, _softmax_default, bmm_default_1, add_tensor_5, add_tensor_6, add_tensor_7, add_tensor_8, relu_default, add_tensor_9, add_tensor_10, add_tensor_11, add_tensor_12, add_tensor_13, add_tensor_14, div_scalar_1, triu_default, masked_fill_scalar, _softmax_default_1, bmm_default_3, add_tensor_15, add_tensor_16, add_tensor_17, add_tensor_18, add_tensor_19, add_tensor_20, div_scalar_2, _softmax_default_2, bmm_default_5, add_tensor_21, add_tensor_22, add_tensor_23, add_tensor_24, relu_default_1, add_tensor_25, add_tensor_26, add_tensor_27, add_tensor_28, _softmax_default_3)
