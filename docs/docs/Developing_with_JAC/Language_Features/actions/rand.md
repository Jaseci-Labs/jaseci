---
title :  Rand Actions
---
### Seeds random number generator
```jac
# seeds random num generator
rand.seed(4);

```
### Generate random generator
```jac
# Generates random integer between range (0-10)
num = rand.integer(0, 10);
```
### Random Selection
```jac
a_list = ['apple','mango','orange']
# Randomly selects and return item from list
num = rand.choice(a_list);
```
### Generate Random Word
```jac
# generate a random word
 wrd = rand.word();
 ```

### Generate Random Sentence
```jac
# generates a random sentence
# min_lenght - optional , minimum amount of words defaut is 4
# max_lenght - optional ,  maximum amount of words default is 10
# sen - optional
senetence  = rand.sentence();
```
### Generate Random Paragraph

```jac
# generates a random paragraph
# min_lenght - optional , minimum amount of setences defaut is 4
# max_lenght - optional ,  maximum amount of sentences default is 8
# sen - optional
paragraph = rand.paragraph();
```
### Generate Random Text
```jac
# generates a random text
# min_lenght - optional , minimum amount of paragraph ,defaut is 3
# max_lenght - optional ,  maximum amount of paragraph default is 6
# sen - optional
 test  = rand.text();
 ```
### Generate time
```jac
# Generate a random datetime between range.

returned time = rand.time("2020-10-25", "2020-11-26);

```