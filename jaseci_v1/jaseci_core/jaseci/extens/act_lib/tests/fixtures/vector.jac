walker get_centroid_test {
    report vector.get_centroid([[1, 2, 3], [1, 2, 4]]); //[[1.0, 2.0, 3.5], 0.9978409159861319]
}

walker softmax_test {
    report vector.softmax([1, 2, 3]); // [0.09003057317038043, 0.24472847105479767, 0.6652409557748218]
}

walker dot_product_test {
    report vector.dot_product([1, 2, 3], [1, 2, 4]); // 17
}

walker cosine_similarity_test {
    report vector.cosine_sim([1, 2, 3], [1, 2, 4]); // 0.9914601339836675
}

walker cosine_similarity_batch_test{
    report vector.cosine_sim([[1,2,3], [1,2,4]], [1,2,4]); // [0.9914601339836675, 1.0]
}

walker dimensionality_reduction_test {
    has test_data = [[1, 2, 3], [1, 2, 4], [1, 2, 5]];
    model =  vector.dim_reduce_fit(test_data, 2);
    report vector.dim_reduce_apply([3, 4, 5], model);
}