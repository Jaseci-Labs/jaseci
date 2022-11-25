walker identify_intent{
  has input_text;
  can ph.create_head_list, ph.create_head, ph.predict, ph.train_head;

  root {
      # This creates a headlist. you can pass a deafault config override here.
      ph.create_head_list({
          "Model":{
              "args":{
                  "batch_first": true,
                  "embedding_length": 768
              }
          }
      });

      # creating a head named 'ph' with the head_list config.
      # but you can pass a custom config here for a specific head.
      uid = ph.create_head(uuid='ph');

      # predicting using the default weights of the head.
      pred = ph.predict(uuid=uid, data=input_text);
      report pred;

      # training the head for 3 epochs. default is 100. you can override other parameters too. 
      # refer the default config.
      ph.train_head('ph', {
          "Trainer":{
              "trainer":{
                  "epochs": 3
              },
              "dataloader":{
                  "args":{"train_json": "train.json"}
              }
          }
      });
      # if the model has improved, ph will load the best weights.

      # predicting using the trained weights of the head.
      pred = ph.predict(uuid=uid, data=input_text);
      report pred;
  }
}

walker init {
  has input_text;
  root {
      spawn here walker::identify_intent(input_text=input_text);
  }
}