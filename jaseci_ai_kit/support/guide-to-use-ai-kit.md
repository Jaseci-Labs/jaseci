
# Guidance to work with Jaseci AI kit

In this page, you will find all the basic commands needed to work with Jaseci AI kit and it's sub packages.

### Starting a Jaseci Shell session;
```
jsctl
```
At this point a `js.session` file will be generated at the current directory which we are working on. This session file will stores status of memory, graphs, walkers, configurations, etc. Every time when the state changes via the `jsctl` tool the session file will update. We also can have multiple session files as of our need with `-f` or `--filename` flag.

To start a in memory session `-m` or `--mem-only` flag can be used. This won't create a session file but will create a temporary session in memory;

### **Running a Jaseci Program**

```
jsctl> jac run [file_name].jac
```
We can launch any `jsctl` commands directly from the terminal without first entering to the jaseci shell. To run Jaseci program directly from the below command line;
```
jsctl jac run [file_name].jac
```
To ensure the program runs fast, we can first compile the program using `build` command in prior to run the program.
```
jsctl jac build [file_name].jac
```
This will create a `[file_name].jir` file in the working directory. To run the compiled program run this `jir` file.

```
jsctl jac run [file_name].jir
```
### **Using Jaseci AI kit**

 Jaseci Kit is a collection of state-of-the-art machine learning models that are already trained on large amount of data and available to load into jaseci can retrained with our owndata.

 The AI models in Jaseci AI kit falls under four categories, Jac NLP, Jac Speech, Jac Vision and Jac Miscellaneous. For instance, if you only intend to use the "bi enc" model from the JAC NLP, you can simply install only the necessary packages for `bi_enc` with only a single command. For examples that will make this more clear, see below.

 #### **Installing and loading models from Jaseci AI kit**


If you wanna install only a specific model you can simply do `pip install model_group[model_name]` in the python environment which you currently working. Use "pip install model group[model name1,model name2]" to install several models from the same group, or "pip install model group[all]" to install all of the models. Details of model groups and available models in each group can be viewed [here](../README.md).


**Examples**

To install `bi_enc` model.

```
pip install jac_nlp[bi_enc]
```

To install `bi_enc` and `use_enc` models at once.

```
pip install jac_nlp[bi_enc,use_enc]
```

### **Load installed models in Jaseci Shell**

To use the models features in jac code you have to load the installed model as a jaseci action. There are three ways to load models.


	- Module load
	- Remote load
	- Local load
 Example model load in jaseci shell:

#### Load module

After successfull `pip` installation you can load the module from jaseci shell with `actions load module [model_group].model_name`

Example:

 ```
 $ jsctl
jaseci > actions load module jac_nlp.bi_enc
{
  "success": true
}
```

#### **Load from remote**

Also we can load jaseci ai models from a remote server using  `actions load remote [url_to_model]` command. For this each AI model should deployed as a separate service. This URL should obtained from the remote server which AI model was deployed.

Example remote load:
```
jaseci > actions load remote  http://192.168.49.2:32267
{
  "success": true
}
```

#### **Load from local**S

Once we cloned the jaseci main repository to local machine we can load AI models from jaseci_ai_kit using `actions load local [path_to_model]`.
Example local load:

```
jaseci > actions load local jaseci_ai_kit\jaseci_nlp\use_enc\use_enc.py

{
  "success": true
}
```
The complete list of available module names and their details can be viewed [here](https://github.com/Jaseci-Labs/jaseci/tree/main/jaseci_ai_kit#readme). once loaded any model use `actions list` command to view available actions' as below.

```
jaseci > actions list
[
  "net.max",
  "net.min",
  "net.pack",
  "net.unpack",
  "net.root",
  "rand.seed",
  "rand.integer",
  "rand.choice",
  "rand.sentence",
  "rand.paragraph",
  .
  .
  .
  .
]
```

### Retraining a Jaseci model with customized data.

Jaseci AI kit provides pretrained model with large scale of data. We can retrain these models with custom data. Before training any model the model should be load from one of the method which is mentioned above.  The training data should be in JSON format. An example of training jac code is in below;

```jac
node bi_enc {
	can bi_enc.train, bi_enc.infer;
	can train {
		train_data = file.load_json(visitor.train_file);
		bi_enc.train(
			dataset=train_data,
			from_scratch=visitor.train_from_scratch,
			training_parameters={
			"num_train_epochs": visitor.num_train_epochs
			});
			if (visitor.model_name):
			bi_enc.save_model(model_path=visitor.model_name);
			}
	can infer {
		res = bi_enc.infer(
		contexts=[visitor.query],
		candidates=visitor.labels,
		context_type="text",
		candidate_type="text")[0];
		std.out(res);
		visitor.prediction = res["predicted"];
		}
	}

walker train {
	has train_file;
	has  num_train_epochs = 50, from_scratch = true;
	root {
		spawn here ++> node::bi_enc;
		take --> node::bi_enc;
		}
	bi_enc: here::train;
}

walker infer {
	has query, interactive = true;
	has labels, prediction;
	root {
		spawn here ++> node::bi_enc;
		take --> node::bi_enc;
		}
	bi_enc {
		if (interactive) {
			while  true {
				query = std.input("Enter input text (Ctrl-C to exit)>");
				here::infer;
				std.out(prediction);}}
		else {
	here::infer;
	report prediction;}}
}

walker save_model {
	has model_path;
	can bi_enc.save_model;
	bi_enc.save_model(model_path);
}

walker load_model {
	has model_path;
	can bi_enc.load_model;
	bi_enc.load_model(model_path);
}
````
As we can see there are four walkers in the jac code above, `train`, `infer`, `save_model` and `load_model`.

`jac run [file_name].jac -walk train -ctx "{\"train_file\": \[file_nam_of_training_data].json\"}"`

 -   `-walk`  specifies the name of the walker to run. By default, it runs the  `init`  walker. but in this case we have set the walker as train.
 - `-ctx`  stands for  `context`. This lets us provide input parameters to the walker. This accept parameters in `JSON` format.

 Example:

 ```
 jaseci > jac run bi_enc.jac -walk train -ctx "{\"train_file\": \"clf_train_1.json\"}"
 .
 .
 .

            Epoch : 50
            loss : 0.0435857983926932
            LR : 0.0

Epoch: 100%|████████████████████████████████████████████████████████████████| 50/50 [00:59<00:00,  1.19s/batch]{
  "success": true,
  "report": [],
  "final_node": "urn:uuid:529fae48-ea21-4f4c-9cac-02d2750b4ceb",
  "yielded": false
}
 ```
Each training epoch, the above output will print with the training loss and learning rate at that epoch. By default, the model is trained for 50 epochs.If the training successfully finishes, you should see "success": true at the end.

### Make inferencing with the retrained model

After finishes the training the `infer` walker can be used to make inferencing,

`jac run [file_name].jac -walk infer -ctx "{\"labels\": [\"[label_1]\", \"[label_2"]}"`

An example of inferensing is shown below;

```
jaseci > jac run bi_enc.jac -walk infer -ctx "{\"labels\": [\"test drive\", \"order a tesla\"]}"
Enter input text (Ctrl-C to exit)> how can I order a tesla?
{"context": "how can I order a tesla?", "candidate": ["test drive", "order a tesla"], "score": [3.8914384187135695, 9.004763714012604], "predicted": {"label": "order a tesla", "score": 9.004763714012604}}
{"label": "order a tesla", "score": 9.004763714012604}
```

### Saving the retrained model in Jaseci.

The retrained model is kept in memory it can be save into the local machine in a preffered location.

`jac run [file_name].jac -walk save_model -ctx "{\"model_path\": \"[model_path]\"}"`

We set walker as `save_model` here. Inside the model file we should create a node with the name `save_model`

Example:
```
jaseci > jac run bi_enc.jac -walk save_model -ctx "{\"model_path\": \"retrained_model\"}"
Saving non-shared model to : retrained_model
{
  "success": true,
  "report": [],
  "final_node": "urn:uuid:f43dc5e0-bd77-4c6b-b5eb-0e117dfc36d8",
  "yielded": false
}
```
If the model is saved successfully the `success` status will be shown as `true`.

### Loading a saved model

Similarly, you can load a saved model with load_model,

`jac run [file_name].jac -walk load_model -ctx "{\"model_path\": \"model_path\"}"`

Example:
```
jaseci > jac run bi_enc.jac -walk load_model -ctx "{\"model_path\": \"retrained_model\"}"
Loading non-shared model from : retrained_model
{
  "success": true,
  "report": [],
  "final_node": "urn:uuid:b1dd56b0-865a-4150-9df0-50e97ffb8388",
  "yielded": false
}
```
If the model is saved successfully the `success` status will be shown as `true`.
