
walker test_train_ner{
    can tfm_ner.train;
    train_data=["my name is [Shawn](name)","[Jemmott](name) is my name","I'm [Juan](name)","Everyone call me by the name [Katryn](name)","You can call me [Spence](name)","My mother give me the name [marks](name)"];
    report tfm_ner.train("default",5, train_data);
}

walker test_extract_entity{
    can tfm_ner.extract_entity;
     report tfm_ner.extract_entity("you can call me joe");
}

walker test_tfm_ner_get_train_config{
    can tfm_ner.get_train_config;
    report tfm_ner.get_train_config();
}

walker test_tfm_ner_set_train_config{
    can tfm_ner.set_train_config;
    report tfm_ner.set_train_config({"EPOCHS": 50});
}

walker test_tfm_ner_get_model_config{
    can tfm_ner.get_model_config;
    report tfm_ner.get_model_config();
}

walker test_tfm_ner_set_model_config{
    can tfm_ner.set_model_config;
    report tfm_ner.set_model_config({"model_save_path": 'test'});
}

walker test_tfm_ner_load_model{
    can tfm_ner.load_model;
    report tfm_ner.load_model("modeloutput");
}

walker test_tfm_ner_save_model{
    can tfm_ner.save_model;
    report tfm_ner.save_model("modeloutput");
}