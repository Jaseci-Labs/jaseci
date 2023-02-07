#  Vector Actions

### Cosine Similarity


```jac
#Calculate the Cosine similarity score between 2 vectors.
# return list[float] floats betweeen  0 and 1
# vectora :list[list[float]]] | list[float]
# vectorb : list[list[float]]] | list[float]
similarity = vector.cosine_sim(vectora, vectorb);

```

### Dot Product

```jac
# Calculate the dot product between 2 vectors.
# return float betweeen  0 and 1
# vectora :list
# vectorb : list

dot_product = vector.dot_product(vectora,vectorb);
```

### Centroid
```jac
# Calculate the centroid of the given list of vectors.
# list of vectors
# returns [centroid vectors , cluster tightness]

centroid  = vector.get_centroid(vectors);
```

### Softmax
```jac
# calculate the softmax value
# returns list
# vectors : dictionary
values = vectors.softmax(vectors);

```

### Dimensionality Reduction
```jac
// fit the model with the given vector. save this model(str) to a file for the future usage

data = [[1,2,3],[4,5,6],[7,8,9]];
model = vector.dim_reduce_fit(data, 2);

// transform the given vectors with the given model

new_data = [[3,2,3],[4,9,6]];
reduced_data = vector.dim_reduce_apply(new_data, model);
```


