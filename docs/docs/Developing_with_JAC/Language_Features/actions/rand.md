---
title :  Rand Actions
---

```jac
# seeds random num generator
rand.seed(4);

```
```jac
# Generates random integer between range (0-10)
num = rand.integer(0, 10);
```
```jac
a_list = ['apple','mango','orange']
# Randomly selects and return item from list
num = rand.choice(a_list);
```

```jac 
# generate a random word
 wrd = rand.word();
 ```


```jac
# generates a random sentence
# min_lenght - optional , minimum amount of words defaut is 4
# max_lenght - optional ,  maximum amount of words default is 10
# sen - optional
senetence  = rand.sentence();
```

```jac
# generates a random paragraph
# min_lenght - optional , minimum amount of setences defaut is 4
# max_lenght - optional ,  maximum amount of sentences default is 8
# sen - optional
paragraph = rand.paragraph();
```

```jac
# generates a random text
# min_lenght - optional , minimum amount of paragraph ,defaut is 3
# max_lenght - optional ,  maximum amount of paragraph default is 6
# sen - optional
 test  = rand.text();
 ```

```jac 
# Generate a random datetime between range.

returned time = rand.time("2020-10-25", "2020-11-26);

```