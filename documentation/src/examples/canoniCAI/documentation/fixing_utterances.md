# The thought process of fixing utterances

##### Table of Contents  
- [ Introduction ](#introduction)
- [Fixing misclassifications from bi-encoder model](#fixing-misclassifications-from-bi-encoder-model)
- [Fixing misclassifications from use-qa model](#fixing-misclassifications-from-use-qa-model)

# Introduction
Sometimes we will run into cases where we trained the utterances with one of the model for example using the bi-encoder or use-qa and there is misclassification. We will go through how we can solve each of those in this section.

# Fixing misclassifications from bi-encoder model
There could be several cases why the data is being misclassified. 
* **overfitted**: Meaning that they are so much of the same utterances in the dataset and there is basically just a one word change or there is not any distinguishing difference between these utterances. Try removing those.

If you navigate to the ```/data/clf_train.json/```

Try your best to avoid training data like these add more diverse data to the dataset.
```
{
    "order": [
    "i want a cheeseburger",
    "i need a cheeseburger",
    "want a cheeseburger",
    "I want burger",
  ]
}
```
* **label is not specific enough**: Most time it's either the label is vague or label does not extend for a wider scope. I'll explain this a bit more through the example below

If you navigate to the ```/data/clf_train.json/```

The word ``` order ``` in this case is the label. Sometimes all you need is to add an extra word to the label or remove, be more specific and it will increase the chances for being classified to the correct label. In this case if you want it to classify better remove ``` cancel order ``` to ``` cancel ``` and maybe it will work better rather than making most of the utterances classify to ``` order ```. Simple changes like that could work miracles.
``` 
{
    "order": [
    "i want a cheeseburger",
    "i need a cheeseburger",
    "want a cheeseburger",
    "I want burger",
  ],
  "cancel order": [
  "cancel the order please"
  ]
}
```

* **missing diverse dataset**: In this case you will have to go to the dataset and just add more training data with have more different strutural utterances for the label. Sometimes you need to add longer utterances, shorter utterances and etc. Most times you might have to go to the other dataset and see if there is conflicting utterances and delete and replace. These minor things can drastically change the accuracy.

# Fixing misclassifications from use-qa model
This is relatively easy since there is minimal training data required.

Navigate to ```/data/clf_labels.json/```

If you look below sometimes the use qa would misclassify utterances that is meant to label ```no``` to ```greetings```. Try changing up the label ```no``` to ```agree``` and ```yes``` to ```disagree``` . Simple changes like these will increase your chances for utterances to be classified better than orders. Even adding more words can also increase the chance of it classifying a larger dataset accurately for example instead of removing label ``` no ``` to ``` no disagree ``` can largely increase accuracy. Just change around these and test it to a large dataset and you will see better results.

``` 
[
    "greetings",
    "bye",
    "order",
    "yes",
    "no"
]
```