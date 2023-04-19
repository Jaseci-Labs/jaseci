# Vectors Actions Library

## Cosine Similarity

Calculate the Cosine similarity score between 2 vectors.
return list[float] floats betweeen  0 and 1
vectora :list[list[float] | list[float]
vectorb : list[list[float] | list[float]

```jac
similarity = vector.cosine_sim(vectora, vectorb);
```

## Dot Product

Calculate the dot product between 2 vectors.
return float betweeen  0 and 1
`vectora` :list
`vectorb` : list

```jac
dot_product = vector.dot_product(vectora,vectorb);
```

## Centroid

Calculate the centroid of the given list of vectors.
list of vectors
returns [centroid vectors , cluster tightness]

```jac
centroid  = vector.get_centroid(vectors);
```

## Softmax

Calculate the softmax value
returns list
`vectors` : dictionary

```jac
values = vectors.softmax(vectors);
```

## Dimensionality Reduction

Fit the model with the given vector. save this model(str) to a file for the future usage.
Transform the given vectors with the given model.

```jac
data = [[1,2,3],[4,5,6],[7,8,9]];
model = vector.dim_reduce_fit(data, 2);

new_data = [[3,2,3],[4,9,6]];
reduced_data = vector.dim_reduce_apply(new_data, model);
```

## Vector Sort by Key

Param 1 - List of items
Param 2 - if Reverse
Param 3 (Optional) - Index of the key to be used for sorting if param 1 is a list of tuples. Deprecated.

```jac
args: data: dict (*req), reverse: _empty (False), key_pos: _empty (None)
```