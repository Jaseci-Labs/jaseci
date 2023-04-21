walker identify_number {
  has input_image;
  can ph.create_head_list, ph.create_head, ph.predict, ph.train_head;
  can file.load_str;

  root {
    #loading the python script
    python_file = file.load_str("custom.py");

    #creating a head_list
    ph.create_head_list({
        "Model":{
            "args": {
                "num_classes": 10
            },
            "type": "CustomModel"
        },
        "Inference":{
            "postprocess": {
                "type": "CustomProcessor",
                "args": {}
            },
            "preprocess": {
                "type": "CustomProcessor",
                "args": {}
            }
        }
    }, python_file);

    #creating the head
    uid = ph.create_head(uuid='mnist');
    #making the prediction using default weights
    pred = ph.predict(uuid=uid, data=input_image);
    report pred;

      # training the head
    ph.train_head('mnist', {
        "Trainer":{
            "name": "MnistTrainer",
            "trainer":{
                "epochs": 3
            },
            "dataloader": {
                "args":{
                    "data_dir": "data/"
                },
                "type": "CustomDataLoader"
            }
        }
    });

    #predicting again
    pred = ph.predict(uuid=uid, data=input_image);
    report pred;
  }
}

walker init {
  has input_image;
  has output;

  root {
      spawn here walker::identify_number(input_image=input_image);
  }
}