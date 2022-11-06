node Action {
    has fn;   
    has json = {};
}

node call_endpoint:Action {
    has fn = "callEndpoint";
    has headers;
    has method;
    has endpoint;

    can set_action_json {
        json["fn"] = fn;
        json["args"] = [method, {}, headers];
    }
}



node store_value:Action {
    has fn = "storeValue";
    has target;
    has key;
    has value;
    
    can set_action_json {
        json["fn"] = fn;
        json["target"] = target;
        json["args"] = [key, value];
    }   
    
}

node show_toast:Action {
    has fn = "showToast";
    has message;
    has timeout;
    
    can set_action_json {
        json["fn"] = fn;
        json["args"] = [{"message": message, "timeout": timeout}];
    }

}

node text_to_speech:Action {
    has fn = "textToSpeech";
    has message;
    
    can set_action_json {
        json["fn"] = fn;
        json["args"] = [message];
    }
}

node run_operation:Action {
    has fn = "runOperation";
    has operation;
    has args;
    
    
    can set_action_json {
        json["fn"] = fn;
        json["operation"] = operation;
        json["args"] = [args];
    }
}

