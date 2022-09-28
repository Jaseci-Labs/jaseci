# Build a conversational AI system in Jaseci

# Chapter 3

### **cai_state node**
### Two main stages in handling a conversational AI request
![Two Stages](./images/nlu_nlg.png?raw=true "Title")

There are two stages which handles the conversational aspect of the AI and they are NLU (Natural Language Understand) and NLG (Natural Language Generation).

* **NLU (Natural Language Understand)**: Natural language understanding is a branch of artificial intelligence that uses computer software to understand input in the form of sentences using text or speech. **What does NLU do?** If you look at the diagram above it intakes the user query and the NLU uses two component: intent classification (understanding the meaning of the utterance) and entity extraction (collects important words from the utterance) and this process gives the conversational AI the understanding of what the user is actually trying to say.

* **NLG (Natural Language Generation)**: Natural language generation (NLG) is the use of artificial intelligence (AI) programming to produce written or spoken narratives from a data set. **What does NLG do?** If you look above at the diagram, you would see after the AI understand what the user is trying to say using NLU it will then take those results and auto generate a suitable response to forward to the user and that is the purpose of the NLG.

### **What do each node abilities do?**

* **classifiy_intent**: Figures out the user intention in any given question.
* **extract_entities**: Extract words of interests from the question
* **gen_response**: Generate a suitable response for the user.
* **nlu**: Process incoming request through NLU engines using intent classification or entity extraction AI models.
* **nlg**: Construct natural language response


### **Inheritance**
**What is inheritance?**
 It is a mechanism where you can to derive a class from another class for a hierarchy of classes that share a set of attributes and methods.
 
 **Node Inheritance**
```jac
node vehicle {
    has plate_number;
    
    can drive {
        report 'yes';
    }
}

node car:vehicle {
    has plate_number = "RAC001";
}

node bus:vehicle {
    has plate_number = "SUB002";
}
```
In the above code snippet. This is a very basic example of inheritance. We created a node named car and bus but since they are related and simply share the same property and node ability we created a node named vehicle and inherit its attributes. Imagine life without inheritance, the code will look like this.
```jac
node car {
    has plate_number = "RAC001";
    
    can drive {
        report 'yes';
    }
}

node bus {
    has plate_number = "SUB002";
    
    can drive {
        report 'yes';
    }
}
```
In this case it will seem that writing it this way will be more effient, however what if each vehicles have more functions like blow_horn, accelerate, breaks, park and etc or they are more vehicles like truck, scooter, and etc you can imagine how big this code base will be and that's why it's important to have inheritance in our code base and in this program we use inheritance to increase the efficiency of the entire application.

So, lets use what's in the code base and see how we implemented it. ```Do not worry about what each nodes and state works, that will be explained in detailed in the next section, just look at how it is implemented.```
```jac
node cai_state {
    has name;
    has prepared_entities = {
            "name": "Tony Stark",
            "address": "10880 Malibu Point"
    };

    # Classify the intent of the question
    can classify_intent {
        # NOTE: Hardcode intent for now
        visitor.predicted_intent = visitor.intent_override;
    }

    # Extract words of interests from the question
    can extract_entities {
        # NOTE: Hardcode entities for now
        for ent in visitor.entity_override {
            visitor.extracted_entities[ent] = prepared_entities[ent];
        }
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
Above, this is a conversational state node. We use inheritance here, because we will have multiple conversational state nodes like a confirm state, cancel state, collect information state and etc, that have the same functionality but does have different node abilities.

```jac
node collect_info:cai_state {
    has name = "collect_info";
    can gen_response {
        if ("name" in visitor.extracted_entities and
                "address" not in visitor.extracted_entities):
            visitor.response = "What is your address?"
        elif ("address" in visitor.extracted_entities and
                "name" not in visitor.extracted_entities):
            visitor.response = "What is your name?"
        else:
            visitor.response =
                "To set you up with a test drive, we will need your name and address.";
    }
}

node confirmation:cai_state {
    has name = "confirmation";
    can gen_response {
        visitor.response =
            "Can you confirm your name to be " + visitor.extracted_entities["name"] + " and your address as " + visitor.extracted_entities["address"] + " ?";
    }
}

node confirmed:cai_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}

node canceled:cai_state {
    has name = "canceled";
    can gen_response {
        visitor.response = "No worries. We look forward to hear from you in the future!";
    }
}
```
As you can see here, all of the conversational state node have something in common, that's why it is very important to use inheritance, because this code instead of being 200 lines of code it can be over 1000+ lines of code and it could be very hard to manage and read.

You can go to [jaseci docs](https://docs.jaseci.org/docs/Developing_with_JAC/Language_Features/OOP) for more information on inheritance. If you are still confused about inheritance and how it works.

### **Nodes (States)**
### collect_info state
This state collects the address and name of the user from the user utterance. If the user only provides their address the AI will ask the user for their name and vice versa. It will ask the user for those information until it is fulfilled before moving on to the next state which is the **confirmation** state, this process is done using entity extraction. The user can also cancel the entire process and this will move them to the **cancel** state, this is triggered by intent classification. Below shows how the node is created. 

```jac
node collect_info:cai_state {
    has name = "collect_info";
    can gen_response {
        if ("name" in visitor.extracted_entities and
                "address" not in visitor.extracted_entities):
            visitor.response = "What is your address?"
        elif ("address" in visitor.extracted_entities and
                "name" not in visitor.extracted_entities):
            visitor.response = "What is your name?"
        else:
            visitor.response =
                "To set you up with a test drive, we will need your name and address.";
    }
}
```
#### confirmation state
This state confirms whether or not the information provided by the user is completely correct. If there is any mistake made, the AI will revert to the **collect_info** state where it will repeat the process, if all the data provided is confirmed by the user it will them move to the next state which is the **confirmed** state. Below shows how the node is created. 

```jac
node confirmation:cai_state {
    has name = "confirmation";
    can gen_response {
        visitor.response =
            "Can you confirm your name to be " + visitor.extracted_entities["name"] + " and your address as " + visitor.extracted_entities["address"] + " ?";
    }
}
```

### confirmed state
This state is triggered after the user have positively agreed that all the data provided is correct and based on the information provided the company will makes it decision afterwards. In this case the sales person will tell the user "You are all set for a tesla test drive". Below shows how the node is created. 

```jac
node confirmed:cai_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}
```

### canceled state
This state is triggered when the user wants to hop out of the entire conversation and it's done through intent classification. 

```jac
node canceled:cai_state {
    has name = "canceled";
    can gen_response {
        visitor.response = "No worries. We look forward to hear from you in the future!";
    }
}
```

### **Edges**
### intent_transition edge
This edge allows you to transition from state to state (node to node) when provided an intent which is passed as a parameter. For e.g. when the user ask "Can I test drive the tesla" it will go through the bi-encoder AI model which is used for intent classification and find the intent and through the edge it will pass the intent to the intent_transition edge which will search for which node to travel to, to move to the next state. In this case it will be the collect_info state.

```jac
edge intent_transition {
    has intent;
}
```

### entity_transition edge
This edge allows you to transition from state to state (node to node) when provided all the entities needed which is passed as a parameter. For e.g. when the user have to provide information in the collect_info state "My name is Jemmott I live in lot 1 pineapple street" it will go through the entity extraction AI model, extract "Jemmott" as the name and "lot 1 pineapple street" as the address and it will passed these information into the entity_transition edge and move you on to the next state, in this case it will be the confirmed state. If all the information is not provided it will not transition to the next state until all the entities are fulfilled. 

```jac
edge entity_transition {
    has entities;
} 
```

### **Graph Definition**
### spawning nodes
Nodes are the states we used to build out the conversation AI experiences. Below, shows how to create states (nodes) using jac.
```jac
spawn {
    state_cai_root = spawn node::cai_root;
    state_collect_info  = spawn node::collect_info;
    state_confirmation = spawn node::confirmation;
    state_confirmed = spawn node::confirmed;
    state_canceled = spawn node::canceled;
}
```

### connecting the nodes with the two types of edges
There are two types of edges: intent_transition edge and entity_transition edge and we will use these to connect states (nodes) to each other. 

Intent Transition Example:
```jac
    state_cai_root -[intent_transition(
            intent = "I would like to test drive"
        )]-> state_collect_info;
```
Here we have a intent transition going from the cai_root state to the collect_info state. This intent transition has its intent variable set to ""I would like to test drive"", which will be checked later in the walker "talk" to evaluate whether or not this transition should be triggered or not.

Entity Transition Example:
```jac
        state_collect_info -[entity_transition(
            entities = ["name", "address"]
        )]-> state_confirmation;
```
Here we have an entity transiton going from the collect_info state to the confirm state. This entity transition has its entities variable set as "name" and "address", which will be checked later in the talk walker to evaluate if this transition should be triggered or not.


### the anchor node
The anchor node is the main node or the starting node for the conversational AI state. This node is mandatory for the application. 
```jac
graph tesla_sales_rep {
    has anchor state_cai_root;
}
```

### **Describe the talk walker**
### The parameters it takes
* **question**: This intakes the user utterance.
* **intent_override**: Allows you to override the intent produced by the intent classification model from the NLU.
* **entity_override**: Allows you to override the entities extracted from the entity extraction model from the NLU.
* **predicted_intent**: This is the variable that holds the intent predicted from the intent classification model. 
* **extracted_entities**: This is the variable that holds the extracted entities that produced from the entity extraction model from the NLU.
* **traveled**: This variable tells you whether or not we moved on to the next state.
* **response**: This holds the response generated from the NLG.

### The "traveled" boolean flag
This boolean flag variable tells you whether or not we moved on to the next state. If its flagged as "false" it will execute all the logic from the NLU until it have the information to move on to the next state if not it will execute the NLG which will generate a reponse and go to the next state.

### The traversal logic
In this section I will explain how this code snippet works for the traversal logic.
From entity transition >> intent transition
```jac
take -[entity_transition(entities=extracted_entities.d::keys)]-> node::cai_state else {
    take -[intent_transition(intent=predicted_intent)]-> node::cai_state else {
        # Fall back to stay at current state if no valid transitions can be taken
        take here;
    }
```

If all the keys in the array of extracted_entities matches any edge in the entity_transition that is attached to a node it will transition you to the appropriate conversation AI state if not it will check if the predicted intent matches any record in the edge of the intent_transition and move you to that state. If both of the requirements was not met it will continue at the current state and ask you the same question until it gets the information it wants from you.

### The take statement
**How does it work?** \
The take statement allows you to transition from node to node (state to state). If the requirements are met it will transition you to the node you specified. If you see the code snippet below, once the parameters are met the take statement will transfer you to the appropriate node that matched the cai_state. But if the parameters are not met it will throw an error and that is where the else comes into place. That will be explained in the next section.

```jac
take -[intent_transition(intent=predicted_intent)]-> node::cai_state;
```
\
**How does take, else work?**
The take, else works just like the if, else statement in any other programming language. If the node from the take statement does not exist it will activate the else statement and execute what is in the else block. 

```jac
take -[intent_transition(intent=predicted_intent)]-> node::cai_state else {
        # execute code in here
    }
```

For more information about what the take statement and take, else statement works. Reference the [Jaseci Documentation](https://docs.jaseci.org/docs/getting-started/JAC-Language-Overview/take) 

### The Flow 
NLU ➝ traversal ➝ NLG ➝ return response
\
We know already that the NLU is responsible for understanding the context of the user query using the intent classification model and the entity extraction model. The traversal is essentially the state of the graph that collects information and if the information is not met it will ask the user until it understands and get all the user information required in order to move to the next state. The NLG is responsible for the natural generation of the response based on the current state, entities and intent and based on the response generated from the NLG it will return this information to the user. That's basically the rundown of how the flow works in this application.

### **init walker to initiate the graph**
```jac
walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
    }
} 
```
The above code snippet shows how we utilize generating the graph using the init walker using jac. Note: the graph spawn statement returns the anchor node defined in the graph block. Therefore, the anchor node is a return statement. The init walker is also the first block of code that will be runned in the entire application and that will look for the graph we created for the tesla sales rep and generate all the nodes and edges of the application.

