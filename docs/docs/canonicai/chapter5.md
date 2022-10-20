# Build a conversational AI system in Jaseci

# Chapter 5

## What are we building?
We are building a Conversational AI.

### The Updated Inheritance Structure

Before:
```
node cai_state {
    has name;
    has example_entities = {
            "name": "Tony Stark",
            "address": "10880 Malibu Point"
    };

    # Classify the intent of the question
    can classify_intent {
        # Note: a simple hardcoded "classifier"
        # To be replaced with an AI model in a later chapter
        if ("test drive" in visitor.question.str::lower):
            visitor.predicted_intent = "test drive";
        elif ("yes" in visitor.question.str::lower):
            visitor.predicted_intent = "yes";
        elif ("no" in visitor.question.str::lower):
            visitor.predicted_intent = "no";
        elif ("cancel" in visitor.question.str::lower):
            visitor.predicted_intent = "cancel";
        else:
            visitor.predicted_intent = "out of scope";
    }

    # Extract words of interests from the question
    can extract_entities {
        # Note: a simple hardcoded entity extraction model
        # To be replaced with an AI model in a later chapter
        if ("name" in visitor.question.str::lower):
            visitor.extracted_entities["name"] = example_entities["name"];

        if ("address" in visitor.question.str::lower):
            visitor.extracted_entities["address"] = example_entities["address"];
    }

    # Generate response
    can gen_response {
        # Default response
        visitor.response =
            "Sorry I can't handle that just yet! Anything else I can help you with";
    }

    # Process incoming request through NLU engines
    can nlu {
        ::classify_intent;
        ::extract_entities;
    }

    # Construct natural language response
    can nlg {
        ::gen_response;
    }
}
```
Before, we had classify_intent, extract_entities, gen_response functionality in the cai_state for specifically virtual assistance. However, since we have added the FAQ model (faq node) to the conversation AI state we needed to centralize the functionality, they have completely different functionality when it comes to the NLU (Natural Language Understanding) where we used it for intent classification and entity extraction. Likewise, the FAQ model uses the NLU to find the faq node which matches the appropriate user query, and for the NLG (Natural Language Generation) they generates different responses based on the NLU.

After: 
```
node cai_state {
    has name;
    can nlu {
        std.err("Node ability invoked for cai_state node: nlu");
        disengage;
    }
    can nlg {
        std.err("Node ability invoked for cai_state node: nlg");
        disengage;
    }
}
```

So, what is happening here, since the cai_states are centralize, we can now inherit this node for the faq node (frequently asked question) and va node (virtual assistance) and just override the NLU and NLG. So, let's elborate on the new changes and explain the logics for specific abilities and etc.

### The general pattern of NLU -> NLG

**NLU logic for va_state which inherits cai_state**

```
can nlu {
        ::classify_intent;
        ::extract_entities;
    }
```

For the NLU here, intent classification and extract entities function have been called and it override the nlu logic from the cai_state. 

**NLG logic for va_state which inherits cai_state**

```
# Construct natural language response
    can nlg {
        ::gen_response;
    }
```

For the NLG logic it calls the gen response function in order to give the response to the user. Each va_state have unique responses and they all are overwritten using nlg node ability.

**There are 4 va_state (va nodes):**

**cai_va_root**
As you can see since this is the root node for the conversation we do not need any unique responses.
```
node cai_va_root:va_state {
    has name = "cai_va_root";
}
```


**collect_info**
If you see below the the gen response is unique to the slots extracted from the user query. If a user was at this state based on the root query if no slots was provided it would respond with "To set you up with a test drive, we will need your name and address.", if you have provided only an address however, it would have responded with "What is your name?" and vice versa.
```
node collect_info:va_state {
    has name = "collect_info";
    can gen_response {
        if ("name" in visitor.extracted_entities and
                "address" not in visitor.extracted_entities):
            visitor.response = "What is your address?";
        elif ("address" in visitor.extracted_entities and
                "name" not in visitor.extracted_entities):
            visitor.response = "What is your name?";
        else:
            visitor.response =
                "To set you up with a test drive, we will need your name and address.";
    }
}
```

**confirmation_state**
If you were at this state after providing all the information it will respond unique based on your data you provided like "Can you confirm your name to be Yiping and your address as 913 Mandela Avenue?"
```
node confirmation:va_state {
    has name = "confirmation";
    can gen_response {
        visitor.response =
            "Can you confirm your name to be " + visitor.extracted_entities["name"] + " and your address as " + visitor.extracted_entities["address"] + " ?";
    }
}
```

**confirmed_state**
When you confirm it will respond "You are all set for a Tesla test drive!"
```
node confirmed:va_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}
```
**cancelled_state**
If you were at this state and you cancelled it will respond with "No worries. We look forward to hear from you in the future!".
```
node canceled:va_state {
    has name = "canceled";
    can gen_response {
        visitor.response = "No worries. We look forward to hear from you in the future!";
    }
}
```

So as you can see the NLG logic is unique to each conversational state.

**NLU logic for faq_state which inherits cai_state**

```
can nlu {
        answers = [];
        for a in -[faq_transition]->.edge: answers += [a.answer];
        if (answers) {
            res = use.qa_classify(
                text = visitor.question,
                classes = answers
            );
            visitor.matched_answer = res["match"];
        }
    }
```
For the NLU here it iterates the edges in faq_transition as answer and it use the user query (question) and using an AI model it uses the user query to find the most appropriate answer for the user.

**NLG logic for faq_state which inherits cai_state**

For the NLG logic here it takes the answer provided by the NLU to provide to the user.
```
can nlg {
        visitor.response = here.answer;
    }
```

If you were to interact with the faq state it would use the zero-shot technique to find the appropriate response and if you were to test it based on the information provided in the application it would have respond as follows:
```
> How do I order a Tesla?
Visit our Design Studio to explore our latest options and place your order. The purchase price and estimated delivery date will change based on your configuration.
```



### How to load actions

In this section, we will discuss how to load actions in jsctl. There are three ways to load actions in jsctl. They are remote (server), local (custom) , builtin (jaseci built in actions)  The commands to loading actions are as follows:

We first will run the jsctl command in the terminal for jaseci to run it's own shell.
```
jsctl
```

The command below is used for local modules built by the developer. For example if you want to build a custom AI module in python you can use jaseci actions to create the module and use the command below to load it.
```
jsctl load local PATH_TO_PYTHON_FILE
```

The command below is used to load module from a remote jaseci server. For example if there is a bi-enc jaseci module on a server that you want to load into jaseci you can run it using the command below.
```
jsctl load remote https://bi-enc.org
```

This is the command use to run builtin jaseci kit modules that can be accessed anytime as long as you have jaseci installed on your system.

```
jsctl load module JASECI_AI_KIT_MODULE
```

### Tutorial on USE_QA

**What is the USE_QA model?**
It's a sentence level embeddings which is used to calculate best match between question and available answers via cosine similarity and/or dist_score.

**What does it do?**
It is used for text classification. It requires no training data. However it requires you to have the labels (classes) as prerequisite in order for you to match between the user query. 

**How to load it as an action?**
Above, we showed you how to load actions and now in this section we will show you how to implememt it by loading the use_qa actions. Once you run the command sucessfully you should be able to use all of it's functionality. The command for loading the actions is as follows:
* ```jsctl```
* ```actions load module jaseci_ai_kit.use_qa```

**What does the qa_classify action do?**
qa_classify is a built in function or api used in use_qa module in jaseci kit. It takes in two parameters: text (user input) and classes (list of string) and in returns it gives you the best matching class from the list of classes and this is what we are using for intent classification.

If you look at the code below you will see where it's being implemented.
```
node faq_state:cai_state {
    has answer;
    can use.qa_classify;
    can nlu {
        answers = [];
        for a in -[faq_transition]->.edge: answers += [a.answer];
        if (answers) {
            res = use.qa_classify(
                text = visitor.question,
                classes = answers
            );
            visitor.matched_answer = res["match"];
        }
    }

    can nlg {
        visitor.response = here.answer;
    }
} 
```

**How is it useful in this FAQ chatbot?**
Let's explain why would this be useful in the FAQ chatbot. Let's say you have a website that have all the information answering questions people would usually asked. In the faq module, what it would do is take all the answers from the website and store it as faq nodes. When a user query it will use that query and based on a cosine similarity algorithm using the use_qa model it will match that query to all the answers in the db and find the most appropriate answer and that's what makes it useful to be used in the FAQ chatbot.

### The faq_state node code

In this section, we will be explaining the code below.
```
node faq_state:cai_state {
    has answer;
    can use.qa_classify;
    can nlu {
        answers = [];
        for a in -[faq_transition]->.edge: answers += [a.answer];
        if (answers) {
            res = use.qa_classify(
                text = visitor.question,
                classes = answers
            );
            visitor.matched_answer = res["match"];
        }
    }

    can nlg {
        visitor.response = here.answer;
    }
} 
```

Let's begin. The faq state inherits the cai_state node because it's a part of the conversational state. It accepts **answer** as a parameter and that's all the faq answer node generated from the FAQ. The faq state also inherits a function from the use_qa module called **use.qa_classify** this will be used to find the mathing answer to be returned to the user. use_qa_classify function as discussed in a recent section, intakes two paramters: text (which is the question the user provided) and classes (the answers extracted from the faq_transition edges which is used to store all the answers) and these functions will be called when faq_state calls the nlu node ability and the nlg node ability when executed will return the answer.

### The new type of edge (answer_transition)
**What is the answer transition?**
This is a edge transition created for user query to navigate to node with the answer from the FAQ section. It intakes answer as the parameter which is being generated from the nlu.
```
edge answer_transition {
    has answer;
} 
```

### The updated talk walker logic
Take a look carefully at the code below. We will explain step by step of the changes made and why we made it.
```
walker talk {
    has question="";
    has if_nlu=false;
    has predicted_intent = null, extracted_entities = {}, matched_answer = null;
    has response;

    root {
        take --> node::cai_state;
    }

    cai_state {
        if (question == "") {
            question = std.input("> ");
            if_nlu = false;
        }

        if (!if_nlu) {
            predicted_intent = null;
            here::nlu;
            if_nlu = true;
        } else {
            # Clear the predicted intent if a NLU based transition has happened
            # This is to prevent infinite loop in certain situation
            predicted_intent = null;
        }

        take -[entity_transition(entities==extracted_entities.d::keys)]-> node::cai_state else {
            take -[intent_transition(intent==predicted_intent)]-> node::cai_state else {
                take -[answer_transition(answer==matched_answer)]-> node::cai_state else {
                    here::nlg;
                    std.out(response);
                    question = "";
                    take --> node::cai_root else: take here;
                }
            }
        }
    }
}
```

Below is the first changes you saw.
```
matched_answer = null;
```
This was created for the FAQ node. This house the answer for the user query passed when it goes through the faq_state nlu node ability. Which will be later used for transition.

Last change you saw is as follows.
```
take -[answer_transition(answer==matched_answer)]-> node::cai_state else { ... }
```
This was created for the faq state node. If all of the rest of transition failed it will take the matched_answer generated from the nlu from the faq_state node match it against the answer_transition and if it gets a response it will trigger the nlg functionality which in return will give the user a response. Thanks to inheritance we were able to share majority of the logic of the talk walker between the VA side and FAQ side because we inherit everything from cai_state. If we didn't inherit the functionalities from cai_state we would have multiple talk walker to do all of the transitions.

### The ingest_faq walker
```
walker ingest_faq {
    has kb_file;
    root: take --> node::faq_state;
    faq_state {
        kb = file.load_json(kb_file);
        for faq in kb {
            answer = faq["answer"];
            spawn here -[answer_transition(answer=answer)]-> node::faq_state(answer=answer);
        }
    }
}
```

So, let's explain what this walker does. Essentially, it takes a kb_file (knowledge base file) in the form of json that have a key of question and a key of answer. Then loop is created in the faq state to spawn answers nodes with answer transition edge from the answers from the knowledge based. This walker just intakes a file and generate faq answer nodes with edges.

### Interacting with the FAQ side using the interactive_faq walker 
In this section, we will walk you through a session interacting with the faq side. So let's get started.

Let's run jaseci control in the terminal.
```
jsctl
```
Let's run the interactive_faq walker in jsctl.
```
jac run main.jac -walk interactive_faq
```

Let's run a query and see if we get a response.
```
> how do I configure my order?
To configure your order, log into your Tesla Account and select manage on your existing reservation to configure your Tesla. Your original USD deposit has now been converted to SGD.
```

