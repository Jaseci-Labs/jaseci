---
title :  Vector Actions
---
### Cosine Similarity 

```jac
#Calculate the Cosine similarity score between 2 vectors.
# return float betweeen  0 and 1 
# vectora :list
# vectorb : list 
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



