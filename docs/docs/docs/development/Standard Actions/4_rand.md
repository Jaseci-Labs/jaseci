# Rand Actions Library

- [Rand Actions Library](#rand-actions-library)
    - [Seeds random number generator](#seeds-random-number-generator)
    - [Generate random generator](#generate-random-generator)
    - [Random Selection](#random-selection)
    - [Generate Random Word](#generate-random-word)
    - [Generate Random Sentence](#generate-random-sentence)
    - [Generate Random Paragraph](#generate-random-paragraph)
    - [Generate Random Text](#generate-random-text)
    - [Generate time](#generate-time)

### Seeds random number generator

Seeds random num generator.

```jac
rand.seed(4);

```
### Generate random generator

Generates random integer between range.

```jac
num = rand.integer(0, 10);
```
### Random Selection

Randomly selects and return item from list.

```jac
a_list = ['apple','mango','orange'];
num = rand.choice(a_list);
```
### Generate Random Word

Generate a random word.

```jac
 wrd = rand.word();
```

### Generate Random Sentence

Generates a random sentence.

`min_lenght` - (`int`) optional , minimum amount of words defaut is 4
`max_lenght` - (`int`) ptional ,  maximum amount of words default is 10
`sen` - optional

```jac
senetence  = rand.sentence();
```
### Generate Random Paragraph

Generates a random paragraph
`min_lenght` - (`int`) optional , minimum amount of setences defaut is 4
`max_lenght` - (`int`) optional ,  maximum amount of sentences default is 8
`sen` - optional

```jac
paragraph = rand.paragraph();
```
### Generate Random Text

Generates a random text
`min_lenght` - (`int`) optional , minimum amount of paragraph ,defaut is 3
`max_lenght` - (`int`) optional ,  maximum amount of paragraph default is 6
`sen` - optional

```jac
 test  = rand.text();
```
### Generate time
Generate a random datetime between range.

```jac
returned time = rand.time("2020-10-25", "2020-11-26);
```