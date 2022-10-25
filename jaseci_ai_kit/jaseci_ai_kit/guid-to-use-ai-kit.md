
# Jaseci Onboarding Guidance

In this page, you will find all the basic commands needed to work with Jaseci. 

##
 ### Starting a Jaseci Shell session;
```
jsctl
```
At this point a `js.session` file will be generated at the current directory which we are working on. This session file will stores status of memory, graphs, walkers, configurations, etc. Every time when the state changes via the `jsctl` tool the session file will update. We also can have multiple session files as of our need with `-f` or `--filename` flag.

To start a in memory session `-m` or `--mem-only` flag can be used. This won't create a session file but will create a temporary session in memory;

### Running a Jaseci Program

We can run Jaseci program within jaseci shell or directly from the command line. 
```
jsctl> jac dot [file_name].jac
```
or 
```
jsctl> jac run [file_name].jac
```
The difference between `jac dot` and `jac run` is only that `jac dot` will produce the graph in `DOT` format. 

We can launch any `jsctl` commands such as `jac run`,`jac dot` directly from the terminal without first entering to the jaseci shell. To run Jaseci program directly from the command line;
```
jsctl jac run [file_name].jac
```
or 
```
jsctl jac dot [file_name].jac
```
To ensure the program runs fast, we can first compile the program using `build` command in prior to run the program.
```
jsctl jac build [file_name].jac
``` 
This will create a `[file_name].jir` file in the working directory. To run the compiled program run this `jir` file.

```
jsctl jac run [file_name].jir
```
### Using Jaseci AI kit
 
 We can load modules from Jaseci AI kit from locally or remotely.
 #### To load a module from Jaseci AI kit;
 ``` 
 actions load module jaseci_ai_kit.[module_name]
 ```
#### Load from remote
```
actions load remote [url_to_model]
```
#### Load from local
```
actions load local [path_to_model]
```
The complete list of available module names and their details can be viewed [here](https://github.com/Jaseci-Labs/jaseci/tree/main/jaseci_ai_kit#readme).

### Retraining a Jaseci model with customized data.

Jaseci AI kit provides pretrained model with large scale of data. We can retrain these models with our own data. Before training any model the model should be load from one of the method which is mentioned above.  The training data should be in JSON format. An example of training jac code is in below;

````
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
		spawn here --> node::bi_enc;
		take --> node::bi_enc;
		}
	bi_enc: here::train;
}

walker infer {
	has query, interactive = true;
	has labels, prediction;
	root {
		spawn here --> node::bi_enc;
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
As we can see there are three walkers in the jac code above, `train`, `infer`, `save_model` and `load_model`. 

    jac run [file_name].jac -walk train -ctx "{\"train_file\": \[file_nam_of_training_data].json\"}"

 -   `-walk`  specifies the name of the walker to run. By default, it runs the  `init`  walker.
 - `-ctx`  stands for  `context`. This lets us provide input parameters to the walker. This accept parameters in `JSON` format. 

### Make inferencing with the retrained model

    jac run [file_name].jac -walk infer -ctx "{\"labels\": [\"[label_1]\", \"[label_2"]}"

We set walker as 'infer' here. The labels are the list of classes which we trained. Inside the model file we should create a node with the name `infer`


### Saving the retrained model in Jaseci.

    jac run [file_name].jac -walk save_model -ctx "{\"model_path\": \"[model_name]\"}"

We set walker as `save_model` here. Inside the model file we should create a node with the name `save_model`