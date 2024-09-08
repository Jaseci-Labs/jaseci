
walker test_train_sbert_sim{
    can sbert_sim.train;
    train_data= [
                    ["A person is on a baseball team.","A person is playing basketball on a team.",0.99],
                    ["Our current vehicles will be in museums when everyone has their own aircraft.","The car needs to some work",0.99],
                    ["A woman supervisor is instructing the male workers.","A woman is working as a nurse.",0.99]
                ];
    report sbert_sim.train(train_data,{'num_epochs':2});
}

walker test_get_text_sim{
    can sbert_sim.get_text_sim;
     report sbert_sim.get_text_sim("A girl dancing on a sandy beach.","A girl is on a sandy beach.",1);
}

walker test_sbert_sim_get_train_config{
    can sbert_sim.get_train_config;
    report sbert_sim.get_train_config();
}

walker test_sbert_sim_load_model{
    can sbert_sim.load_model;
    report sbert_sim.load_model("all-MiniLM-L12-v2","default");
}

walker test_sbert_sim_get_embeddings{
    can sbert_sim.getembeddings;
    report sbert_sim.getembeddings(["A girl is on a sandy beach."]);
}

walker test_sbert_sim_get_cos_score{
    can sbert_sim.get_cos_score;
    report sbert_sim.get_cos_score([0.4659, -0.3153, 0.6579, 0.2519],[0.3732, -0.4034, 0.8592, 0.3341]);
}
walker test_sbert_sim_get_dot_score{
    can sbert_sim.get_dot_score;
    report sbert_sim.get_dot_score([0.4659, -0.3153, 0.6579, 0.2519],[0.3732, -0.4034, 0.8592, 0.3341]);
}