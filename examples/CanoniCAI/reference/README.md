### Running example canoniCAI chatbot

<br>
<br>

**Step 1: Load required jac modules**
```
actions load module jac_nlp.bi_enc

actions load module jac_nlp.tfm_ner

actions load module jac_nlp.use_qa
```

**Step 2: Train ner**

Get the `tfm_ner.jac` and `ner_train.json` files from the `./code` directory and train `tfm_ner` with the training data.

```
jac tfm_ner.jac -walk train -ctx "{\"train_file\": \"ner_train.json\"}"
```
**Step 3: Train encoder**

Get the `bi_enc.jac` and `clf_train.json` files from the `./code` directory and train `bi_enc` with the training data.

```
jac run bi_enc.jac -walk train -ctx "{\"train_file\": \"clf_train.json\"}"
```

**Step 4: Build the tesla conversational ai system**

```
jac build tesla_ai.jac
```

**Step 5: Run the conversational ai program**
```
jac run tesla_ai.jir
```