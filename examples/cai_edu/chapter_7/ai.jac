import {*} with "./bi_enc.jac";
import {*} with "./ner.jac";

node ai_model {
    can train with train entry {}
    can test_model with test_model entry {}
    can eval with eval entry {
        ::train;
        ::test_model;
    }
    can infer with infer entry {}
}

walker train {
    has train_file, num_train_epochs, from_scratch;
    has batch_size, learning_rate;
    has model_name;

    if(model_name == "bi_enc"){
        root: take --> node::cai_root;
        cai_root: take --> node::bi_enc;
        bi_enc: here::train;    
    }
    elif(model_name == "ent_ext"){
        root: take --> node::cai_root;
        cai_root: take --> node::ent_ext;
        ent_ext: here::train;  
    }
    else {}
}

walker test_model {
    has eval_file;

    has model_name;

    if(model_name == "bi_enc"){
        root: take --> node::cai_root;
        cai_root: take --> node::bi_enc;
        bi_enc: here::test_model;        
    }
    elif(model_name == "ent_ext"){
        root: take --> node::cai_root;
        cai_root: take --> node::ent_ext;
        ent_ext: here::test_model;  
    }
    else {}
}

walker eval {
    has train_file, eval_file, num_train_epochs, from_scratch;
    has model_name;

    if(model_name == "bi_enc"){
        root: take --> node::cai_root;
        cai_root: take --> node::bi_enc;
        bi_enc: here::eval;        
    }
    elif(model_name == "ent_ext"){
        root: take --> node::cai_root;
        cai_root: take --> node::ent_ext;
        ent_ext: here::eval;  
    }
    else {}
}

walker infer {
    has input;
    has model_name;

    if(model_name == "bi_enc"){
        root: take --> node::cai_root;
        cai_root: take --> node::bi_enc;
        bi_enc: here::infer;        
    }
    elif(model_name == "ent_ext"){
        root: take --> node::cai_root;
        cai_root: take --> node::ent_ext;
        ent_ext: here::infer;  
    }
    else {}

} 