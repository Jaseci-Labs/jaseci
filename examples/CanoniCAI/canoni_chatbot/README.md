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

```
jac run ner/tfm_ner.jac -walk train -ctx "{\"train_file\": \"ner/ner_train.json\"}"
```
**Step 3: Train encoder**

```
jac run encoder/bi_enc.jac -walk train -ctx "{\"train_file\": \"encoder/clf_train.json\"}"
```

**Step 4: Build the tesla conversational ai system**

```
jac build tesla_ai.jac
```

**Step 5: Run the conversational ai program**
```
jac run tesla_ai.jir
```