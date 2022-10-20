# Build a conversational AI system in Jaseci

# Chapter 1: Introduction

### What is a Conversational AI agent?
Conversational AI is a type of artificial intelligence that enables consumers to interact with computer applications the way they would with other humans.

### Real world examples of conversational AI
* Amazon Alexa (Voice)

![Amazon Alexa (Voice) ](https://imageio.forbes.com/specials-images/imageserve/6022e0a7644b9ab003f0dcb7/iPhone-screenshots-of-the-Alexa-app-s-new-Light-and-Dark-modes/960x0.jpg?format=jpg&width=700)

* Example of a text-based chatbot ( Website )

![Example of a text-based chatbot](https://cdn2.hubspot.net/hubfs/4056626/BotHomePage.png)

## What AI will be used
### We will use the following AI capabilities:

### Intent Classification
#### What is Intent Classification?
Intent classification (Text classification) is the process of assigning tags or categories to text according to its content. It's one of the fundamental tasks in Natural Language Processing (NLP) with broad applications such as sentiment analysis, topic labeling, spam detection, and intent detection.

#### A (simple) diagram illustrating the input and output of Intent Classification

![Alt text](./images/intent_classification.png?raw=true)

Explanation Of The Current Nodes:
* **Input** Text: This is the text from the user.
* **Classes**: A groups of intent labels that helps an AI Model to make conversations.
* **Output Class**: A single intent label that makes the meaning of a user

When a user inputs a query either via speech or text it goes to the intent classification AI model alongside with the classes of intent. These together when gets processed by the AI model it will generate an output class of one single intent. I promise you in the real example you will understand this flow and you will walk out knowing what this intent classification state actually do.


#### A new version of the diagram with the real example
![Alt text](./images/intent_classification_example.png?raw=true "Title")


In this section, We will explain in real life how the flow works. Let's start with the current user. The user asked "Is it cold outside?" and keep in mind that a there will also be predefined classes that will also be fed to the Conversation AI and these classes of user intent are weather, fruits, music and greeting. What these classes are, its like, one word that would translate the meaning of an entire query a user may ask. So for example if the user asked "These bananas look very green", this statement belongs to the intent class **fruits**, and the word fruit translated the entire meaning of that statement the user asked. So the goal of the intent classification model is to look at classes of predefined words and based on the user input, try to figure out which class belongs to, or would suit the meaning of the user input. So, when the user input and the classes of intent get passed to the intent classification model it will figure out based on probability which intent belongs to that user query in this real example case that would be **weather**.

### Entity extraction
#### What is Entity extraction?
Entity extraction is a text analysis technique that uses Natural Language Processing (NLP) to automatically pull out specific data from unstructured text, and classifies it according to predefined categories. Entity extraction, also known as named entity extraction (NER), enables machines to automatically identify or extract entities, like product name, event, and location. It’s used by search engines to understand queries, chatbots to interact with humans, and teams to automate tedious tasks like data entry.

#### A (simple) diagram illustrating the input and output of Entity extraction
![Alt text](./images/entity_extraction.png?raw=true "Title")

Explanation Of The Current Nodes:
* **Input Text**: This is the text from the user.
* **Feature Dataset**: A lot of training data on where certain keywords would usually be located in a sentence.
* **Extract Features**: A process of picking out keywords and mapping a meaning to that keyword
* **Output Feature Set**: The result of defining the keyword and what class it belongs to.

Let's disect this diagram. Let's start from the input text (user input), that's being passed directly to the entity extraction model to extract the features. There is also a feature dataset that hosts all the training data where keywords are usually located in a sentence alongside with the class attached to the keyword. These two nodes combined will allow the AI model to use certain algorithms to extract all the necessary information from the user input and as a result it will output the feature set. This might be a bit confusing but I promise you after the example below you will come out with extensive knowledge of what this entity extraction model is all about.

#### A new version of the diagram with the real example
![Alt text](./images/entity_extraction_example.png?raw=true "Title")

Great, let's explain this. Let's say we are talking to a bot that interviews people and the bot asks "tell me about your best friend next to you, what's his name, the company he worked at, and where does he reside" and you proceed to answer like "Jemmott from Guyana is a developer that works at V75 Inc". How can the bot use this information and find exactly where the name, company, location at and makes sense of it and how the hell would the bot know what are important in that statement you provided. That is where entity extraction comes into place. The bot beforehand would be taught where certain words would be located in a large dataset prior and what class it belongs to. So that's where the feature dataset comes in. This is a large training data of similar sentences that is trained to know what are the important keywords in a sentence and map a class to it. So when the user ask that question it will go the the extract feature node and based on the feature dataset extract relavant keywords from the user input. It would then output, Jemmott is a name, Guyana is a location, V75 is a company based on what it been taught. That's entity extraction. We as human go through the exact process in many conversation overtime when we request certain things from one another. Hopefully, you understand now what is entity extraction and how it works.

#### Real example
![Real Example For Entity extraction](./images/real_example_er.png "Title")

This is another example of the AI figuring out based on the training data where certain keywords are located and mapping it to a class.


### Sentence Encoding
#### What is Sentence Encoding?
The Sentence Encoder encodes text into high dimensional vectors that can be used for text classification, semantic similarity, clustering, and other natural language tasks. The sentence embeddings can then be trivially used to compute sentence-level meaning similarity as well as to enable better performance on downstream classification tasks using less supervised training data.

#### A (simple) diagram illustrating the input and output of Sentence Encoding
![Sentence Encoding Example](./images/sentence_encoding.png?raw=true "Title")

Explanation Of The Current Nodes:
* **input**: A string or body of text
* **sentence encoding**: An encoding of the body of text provided from the input.
* **cosine similarity**: From 0-1, based on the two body of text how similar it is in meaning.The number closer to 1 is very similar in meaning.

Let's explain the flow, So in this model it requires two input. Each input is passed into a sentence encoding AI model which will use certain algorithm to encode a large body of text into vector which will then feed into the cosine similarity function which will compare the two vectors and find how similar the two input is from a score of 0-1. Take into consideration this score could be 0.002, 0.12, 0.08 and etc. The one closer to 1 is the highest in similarity. In the real example below you will understand it in more detail but keep this flow in mind.

#### A new version of the diagram with the real example
![Sentence Encoding Example](./images/sentence_encoding_example.png?raw=true "Title")

From this example, we are using the sentence encoder to look at the user input "Good morning"
and see how similar it is to a class "greeting" so when we pass the both to seperate sentence encoder which it will then vectorize it and pass it to the cosine similarity function which is will look deeper into to the vectors and find a score from 0-1, to see how similar it is in meaning, 0 from lowest and 1 as the highest. So why would we use this, let's say we are building a classifier what if we had like greeting, bye, fruits, and we want to know what "Good morning" is closest to in meaning. We can use this sentence encoder to find the similarity in each of the words greetings bye and fruits and the one that have the highest score, is similar in meaning. Let's say the results in greeting is 0.9, fruits is 0.0023, and bye is 0.02. Therefore greetings is similar to the user input "Good morning" because it ranks high from the scale 0-1 and the bye class would rank second. We can use the sentence encoder in many other application but in this example we used the sentence encoder to build a intent classification model, we can build a whole lot of other applications using sentence encoder. With that said, enjoying showing off your knowledge to others who don't know about sentence encoder.

### The AI models we will use in this tutorial

| Name                  | AI Model                                        | Links                                                                                            |
| --------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Intent classification | biencoder                                       | [link](https://arxiv.org/abs/2103.06523)                                                         |
| Entity extraction     | Transformer-based token classification          | [link](https://huggingface.co/docs/transformers/tasks/token_classification#token-classification) |
| Sentence encoding     | Universal Sentence Encoder (USE_ENC and USE_QA) | [link](https://arxiv.org/abs/1803.11175)                                                         |

# Chapter 2: Architecture Overview

## i. Architecture overview
![Architecture](./images/architecture.png?raw=true "Title")

### Three Architecture constituent components and their purpose

#### AI Model Management
It’s a centralized area for all types of AI models that does specific functions such as NER, Classification, etc. Which can be accessed by the conversational states to perform certain actions.

The purpose are as follows:
* **Intent Classification**: This will allow us to find the meaning of a particular user input. for e.g. "How cold is it?", The AI Model once trained it will understand that the intent of that input is "**weather**". The **USE Encoder (use_enc)** and **Bi-encoder (bi_enc)** are the two AI Model used in this architecture.

* **Named Entity Recognition (NER)**: This allows us to pick out specific objects from a user input, for e.g. I am 29 years old, this AI model will extract **29** and map it as an entity called "**age**". The AI Model used in this architecture is called **Transformer NER (tfm_ner)**.

* **Summarization**: This allows us to shorten a large body of text while retaining the meaning of the entire document. This is used in the FAQ architecture. We will get into more detail into this later in this chapter. The AI Model used in this architecture is called **Summarizer (cl_summer)**.


#### FAQ Management Architecture

This state intakes a link from the user which is then read to scrape data from the website into a summarized fashion in order to be stored as a faq. Which can be later accessed through conversation from a user.

The purpose are as follows:
* store a large body of data which accurate summarized segments can be accessed through text-based conversational AI.
* reduces the need of rebuilding the wheel or do addition work. What we mean by this, the FAQ state intake a link/pdf that navigate through a document or site that's already built, then proceed to process the information for later use.
* any data from multiple sites and pdf can be stored and referenced for later use.

#### Conversational AI Model Architecture

This is where the user query goes to get processed and a response is returned back to the user.

The purpose are as follows:
* task oriented: Conversation AI are single-purpose programs that focus on performing one function. Using rules, NLP, and very little ML, they generate automated but conversational responses to user inquiries.
* speed: It performs task relatively quicker than humans and more efficiently.
* reliability: it work's 24/7 unlike like humans that works 9-5.

### ii. Conversation AI component
![Conversation AI](./images/convai.png?raw=true "Title")

As we acknowledge, this is where the user query an utterance and gets a response from the application. In this section we will explain in more details how the diagram above works. Each nodes represents a conversational state and each of the edges represents the transition path between states. However, they are different type of edges, some are triggered by a certain intent which is tied to a conversational state as show above where state 1 and state 2 lies and some are triggered when they are fulfilled by the entities picked up from the user query. In this component, we leveraged the power of the intent classification using the bi-encoder AI model (bi_enc) and for entity extraction we utilized the Transformer NER Model (tsfm_ner). Each state nodes also have functions which can be shared between states for e.g. each state can have a function where it generates a response for the user and there can be another state function which deals with the business logics (extra processing of user input). So, what's the flow, The user query an utterance and is navigated to the conversational ai state which it goes through the intent classification model to grab the meaning of the query and based on the intent which are tied to a state it navigates the state through an edge and based on the states that's how it will traverse through the graph shown above.

### iii. Zero-shot FAQ
![Zero-shot FAQ](./images/faq.png?raw=true "Title")

In this section, we will explain how this works. Every node represents a faq state and the edges represent transition paths between states. In this component we are utilizing summarization AI model (cl_summer) and a sentence encoder (use_qa). Before anyone can query the FAQ state we have to first explain how data is stored in the FAQ states and how the FAQ answer states are generated. In the FAQ state, a link to a website or PDF have to be fed into the summarization model (cl_summer) and what this does it compute and scrape all the information from the website, summarize it and each summarized section is segmented and stored as new states in the faq section which will be later accessed through the AI. When a user queries and the input is sent to the FAQ state it will be intercepted by the sentence encoder (use_qa) which will look for the best possible faq answer state available, then returns it to the user as a response.

### iv. Model trainer

![Model trainer](./images/trainer.png?raw=true "Title")

We utilize 4 AI models in which each have a different method of training. The four models includes the bi-encoder (bi_enc), sentence encoder (use_enc), entity extraction (tsfm_ner) and summarization model (cl_summer). From the root node each AI model states are created which they all can be trained through the walkers. Each nodes have specific function for specific task and it can all be classified in this order load, train, save, set pretrained and infer model function.

* **Load_model**: load an ai model that was already trained
* **Train_model**: teaches an ai model
* **Save_model**: save the existing model
* **Set_pretrained_model**: switch between models that was already created and saved
* **Infer**: test out the model

### v. Tieing all components together

The first architecture we have to take into consideration is the AI model management state. This is where we map out the types of questions a user may ask alongside with the user intent. We also have to ask ourselves if there are entities that we have to capture in a conversation, like for example where is the location, name, amount of apples in the user question and from there we begin to build out and train the model before we could build any logic on top of that to connect the application. After the AI model management then we have to move on to the conversational state where we will focus on what we will do with the user intent and the entities extracted from it and from there generate a specific response where applicable. The faq architecture is like a cherry on top of the conversation AI state, how this feature works we first have to feed a website link to the conversational AI and it will take out the appropriate information from the site and maps a summarization form of it which will be fed into the faq state for later processing. We can then ask questions based on the link provided and the model will give you the best answer from what it has learned from the site. Now you should be able to understand how they are all tied together in a generalized fashion.

### vi. Tesla use case example
![Tesla Use Case](./images/tesla.png?raw=true "Title")
In this section, we will guide you how the entire architecture work with a real example. First, we will walk you through its design for the conversation AI component and then walk you through the FAQ component.

* **Conversation AI Component**: Imagine we are interacting with a tesla sales person but it's not human its a chatbot. As a user, we will ask a question and as we ask the question it will first go to the Top Level Classification State where it will decide whether to go to the FAQ state or the Conversation AI state using the sentence encoder (use_enc) AI Model, In this case we ask a question about wanting to test drive a tesla. The AI model will analyse then know we are asking a question that is not related to anything in the FAQ section so it will navigate us to the Conversation AI State where it will use the bi-encoder AI model to find the intent of the initial question and extract the entity if any from the user query. In this case we ask the tesla sales person if we can test drive the tesla. The tesla bot will navigate to the collect information state where it will ask for your name and address and when those slots are fulfilled, the edge will trigger to move to the next state (confirmation state) to confirm that the information is correct and based on your next response you can either cancel the entire process which will trigger the edge ,which will navigate you to the cancel state or you can confirm that all the information is accurate and get navigated to the confirmed state or you can update the information which will carry you back to the collect information state. The navigation from state to state is triggered either from intent classification or through entity extraction. That's how that process works.

* **FAQ Component**: Imagine you are asking a question "when do you guys open". In the Top Level Classification state, where it uses the sentence encoder to decide whether to navigate to the conversation AI state or the FAQ state. In this case the AI when processing this utterance it will navigate it to the FAQ state. Where it use a difference sentence encoder (use_qa) which is specialist for FAQ models. The edge will get triggered to the best appropriate faq answer state that is related to the query the user asked and display it to the user.

# Chapter 3: Dialogue System

### <span style="color:red">TODO</span>:
- [ ] Introduce conversational state here

### Two main stages in handling a conversational AI request
![Two Stages](./images/nlu_nlg.png?raw=true "Title")

There are two stages which handles the conversational aspect of the AI and they are NLU (Natural Language Understand) and NLG (Natural Language Generation).

* **NLU (Natural Language Understand)**: Natural language understanding is a branch of artificial intelligence that uses computer software to understand input in the form of sentences using text or speech. **What does NLU do?** If you look at the diagram above it intakes the user query and the NLU uses two component: intent classification (understanding the meaning of the utterance) and entity extraction (collects important words from the utterance) and this process gives the conversational AI the understanding of what the user is actually trying to say.

* **NLG (Natural Language Generation)**: Natural language generation (NLG) is the use of artificial intelligence (AI) programming to produce written or spoken narratives from a data set. **What does NLG do?** If you look above at the diagram, you would see after the AI understand what the user is trying to say using NLU it will then take those results and auto generate a suitable response to forward to the user and that is the purpose of the NLG.

### <span style="color:red">TODO</span>:
- [ ] Create first cai_state node with just NLU and NLG node abilities
- [ ] Create graph spawn block that just spawn a single cai_state node
- [ ] Teach how to run the graph spawn in jsctl and get the graph in dot format and use dot visualizer to check your graph

### **What do each node abilities do?**

* **nlu**: Process incoming request through NLU engines using intent classification or entity extraction AI models.
* **nlg**: Construct natural language response
* **classifiy_intent**: Figures out the user intention in any given question.
* **extract_entities**: Extract words of interests from the question
* **gen_response**: Generate a suitable response for the user.

### <span style="color:red">TODO</span>:
- [ ] Expand the cai_state node with additional node abilities beyond just nlu and nlg. Text to explain the below code snippet.

```
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

### **Inheritance**
**What is inheritance?**
 It is a mechanism where you can to derive a class from another class for a hierarchy of classes that share a set of attributes and methods.

 **Node Inheritance**
```
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
In the above code snippet. This is a very basic example of inheritance. We created a node named car and bus but since they are related and simply share the same property and node ability we created a node named vehicle and inherit its attributes. Without inheritance, the code will look like this.
```
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
We use inheritance here, because we will have multiple conversational state nodes like a confirm state, cancel state, collect information state and etc, that have the same functionality but does have different node abilities.
```
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

```
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

```
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

```
node confirmed:cai_state {
    has name = "confirmed";
    can gen_response {
        visitor.response = "You are all set for a Tesla test drive!";
    }
}
```

### canceled state
This state is triggered when the user wants to hop out of the entire conversation and it's done through intent classification.

```
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

```
edge intent_transition {
    has intent;
}
```

### entity_transition edge
This edge allows you to transition from state to state (node to node) when provided all the entities needed which is passed as a parameter. For e.g. when the user have to provide information in the collect_info state "My name is Jemmott I live in lot 1 pineapple street" it will go through the entity extraction AI model, extract "Jemmott" as the name and "lot 1 pineapple street" as the address and it will passed these information into the entity_transition edge and move you on to the next state, in this case it will be the confirmed state. If all the information is not provided it will not transition to the next state until all the entities are fulfilled.

```
edge entity_transition {
    has entities;
}
```

### **Graph Definition**
### spawning nodes
Nodes are the states we used to build out the conversation AI experiences. Below, shows how to create states (nodes) using jac.
```
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
```
    state_cai_root -[intent_transition(
            intent = "I would like to test drive"
        )]-> state_collect_info;
```
Here we have a intent transition going from the cai_root state to the collect_info state. This intent transition has its intent variable set to ""I would like to test drive"", which will be checked later in the walker "talk" to evaluate whether or not this transition should be triggered or not.

Entity Transition Example:
```
        state_collect_info -[entity_transition(
            entities = ["name", "address"]
        )]-> state_confirmation;
```
Here we have an entity transiton going from the collect_info state to the confirm state. This entity transition has its entities variable set as "name" and "address", which will be checked later in the talk walker to evaluate if this transition should be triggered or not.


### the anchor node
The anchor node is the main node or the starting node for the conversational AI state. This node is mandatory for the application.
```
graph tesla_sales_rep {
    has anchor state_cai_root;
}
```

### <span style="color:red">TODO</span>:
- [ ] Run the updated graph spawn block to get an updated graph. Visualize in DOT

### <span style="color:red">TODO</span>:
- [ ] Introduce the concept of walker
- [ ] Start with init walker, the init walker just spawn the graph
- [ ] Teach how to run the init walker and check the spawned graph.

### **Describe the talk walker**
### The parameters it takes
* **question**: This intakes the user utterance.
* **intent_override**: Allows you to override the intent produced by the intent classification model from the NLU.
* **entity_override**: Allows you to override the entities extracted from the entity extraction model from the NLU.
* **predicted_intent**: This is the variable that holds the intent predicted from the intent classification model.
* **extracted_entities**: This is the variable that holds the extracted entities that produced from the entity extraction model from the NLU.
* **traveled**: This variable tells you whether or not we moved on to the next state.
* **response**: This holds the response generated from the NLG.

### <span style="color:red">TODO</span>:
- [ ] Some of the code and description below needs to be updated to the latest code, e.g. the `traveled` flag is no longer needed.

### The "traveled" boolean flag
This boolean flag variable tells you whether or not we moved on to the next state. If its flagged as "false" it will execute all the logic from the NLU until it have the information to move on to the next state if not it will execute the NLG which will generate a reponse and go to the next state.

### The traversal logic
In this section I will explain how this code snippet works for the traversal logic.
From entity transition >> intent transition
```
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

```
take -[intent_transition(intent=predicted_intent)]-> node::cai_state;
```
\
**How does take, else work?**
The take, else works just like the if, else statement in any other programming language. If the node from the take statement does not exist it will activate the else statement and execute what is in the else block.

```
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
```
walker init {
    root {
        spawn here --> graph::tesla_sales_rep;
    }
}
```
The above code snippet shows how we utilize generating the graph using the init walker using jac. Note: the graph spawn statement returns the anchor node defined in the graph block. Therefore, the anchor node is a return statement. The init walker is also the first block of code that will be runned in the entire application and that will look for the graph we created for the tesla sales rep and generate all the nodes and edges of the application.

### <span style="color:red">TODO</span>:
- [ ] Run the talk walker, with the input question passed in as the context.
- [ ] Explain the response format of the walker, e.g. success, report.

# Chapter 4

### Explaining std.input and std.out

Let's start with std.input, std meaning "standard" and input meaning "what is put in". std.input is a function that intakes, what a user put in only from the terminal and can be stored in a variable. It pauses the program to intake data from the user. The function accepts an optional string to display to the terminal. It acts like a prompt so user know what to input to the terminal.  This function cannot be used to intake any data from api or anything external. That is what std.input is all about.

```
name = std.input('what is your name');
```

Let's now talk about std.out. std in jac means "standard" and out meaning "output". std.out is a function in jac when called it display data to a terminal or server and it intake a string parameter which is used to display.

```
std.out('Display TEXT here');
```

### <span style="color:red">TODO</span>:
- [ ] This jsctl introduction and installation step need to be brought up earlier, at the end of Chapter 2/begining of chapter 3.
- [ ] And this part will just become running the walker interactively with std.input/std.output to show the dialogue system working

### How to run the program interactively via jsctl

In this section we will be running you through how to run a program interactively via jsctl. Let's start from the first step. You need to install jaseci if you have not. Run the command below in the terminal.

```
pip install jaseci
```

After, installing jaseci we have to run the command jsctl meaning "jaseci control". Run the command below in the terminal.

```
jsctl
```

After running jaseci control (jsctl) you should see an active cursor. Now you can run any jac program by using the jac command. For e.g. We have a file named hello.py that runs "hello world!".
Run the command below in the terminal.

```
jac run hello.py
```

That's how to run the program interactively via jsctl.

### The journey of a dialogue session

First before we get started, let's run the code below in jsctl. What this does it will allow us to go through the dialogue in jsctl.
```
jac run main.jac -walk interactive
```

In this section, I will walk you through the journey of a dialogue session. We will go through several queries and explain what happens with each query, including what intent and entities came from that query and  which node it starts at and how it transitions from that node to another node. Let's get started.


```
> I want to test drive
To set you up with a test drive, we will need your name and address.
```
**I want to test drive**: When the user respond with that query it first go through the conversational AI root state (node) for intent classification. Based on the intent extracted it will do an intent transition (edge) to the next state (node) in this case it will transition to collect information state (node).


```
> My  name is Tony Stark
What is your address?
```

**My  name is Tony Stark**: After coming from the conversation AI root state from the first query above and it get's transitioned to the collect information state, it will prompt the user for their name and address information, Then the user respond with this query and it will go to the entity extraction model and pulls out the features from the user utterance in this case it will pull out the name because only the name was provided. Since the entity transition required two keys, one is the name and one is the address, since only one of the data was provided it will re-transition to the current state (node) "collect information" while keeping the context of the last query provided alongside with the features.


```
> My address is at 10880 Malibu Point
Can you confirm your name to be Tony Stark and your address as 10880 Malibu Point?
```

**My address is at 10880 Malibu Point**: Coming from the last query, when get re-transitioned to the collect information state and the bot prompt the user for data and the user responds with the current query. The entity extraction model will extract the feature address and map  **10880 Malibu Point** to address, alongside with the last features extracted from the last query and with both information provided it will do an entity transition and move to the next state (node) called confirmation state.

```
> Yes that looks correct
You are all set for a Tesla test drive!
```

**Yes that looks correct**: When transitioned to confirmation state, it will be prompted by the bot for confirmation and when the user responds with the current query, it will go through the intent classification model to know whether or not they confirmed or not, based on the current query the user agreed and it will do an intent transition to move to confirmed state (node) which the bot will prompt the user with the information required based on the user data.

# Chapter 5: FAQ

In this chapter, we are introducing the capability of handling FAQ to our chatbot.

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

### <span style="color:red">TODO</span>:
- [ ] Create graph spawn block and init walker for the FAQ
- [ ] Run the init walker for the FAQ and visualizes the graph in DOT

If you were to interact with the faq state it would use the zero-shot technique to find the appropriate response and if you were to test it based on the information provided in the application it would have respond as follows:
```
> How do I order a Tesla?
Visit our Design Studio to explore our latest options and place your order. The purchase price and estimated delivery date will change based on your configuration.
```

### <span style="color:red">TODO</span>:
- [ ] Introduce the concept of jaseci action, for leveraing AI models.

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

### <span style="color:red">TODO</span>:
- [ ] Small example walker that uses the use_qa action to check it is correctly loaded and working.

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

### <span style="color:red">TODO</span>:
- [ ] Run the ingest_faq walker to read in a FAQ file
- [ ] Observe the graph is now updated with more answer nodes, according to the FAQ file.

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

# Chapter 6: Training the AI models

## Bringing in the AI models for the dialogue system
In this section, we will explain how we added the AI model into this application. We have added two AI models the bi-encoder and tfm ner model. Before we explain the code implementation for both models, we will explain the top inheritance AI model they inherit.

### <span style="color:red">TODO</span>:
- [ ] Introduce biencoder and ner model used here

**Explanation of the ai_model node**
```
    can train with train entry {}
```
This allows you to train the ai model and it also inherits the train walker which accepts certain parameters.

```
    can test_model with test_model entry {}
```
This allow you to test the ai model, it inherits the test_model walker.
```
    can eval with eval entry {
        ::train;
        ::test_model;
    }
```
this node ability enables you to evaluate the ai model by training it and testing it when the eval walker is called.

```
    can infer with infer entry {}
```
This node ability allows you to pass query and get a response.

```
walker train {
    has train_file, num_train_epochs, from_scratch;
    has batch_size, learning_rate;
}
```
This walker takes in a few parameters: **train_file** (where the training file is located in the repository). **num_train_epochs** (amount of time you want the ai model to learn from the dataset), **from_scratch** (if you want to train the model from scratch or not), **batch_size** (the number of training examples utilized in one iteration) and **learning_rate** (The amount that the weights are updated during training).

```
walker test_model {
    has eval_file;
}
```
This walker allows you to test the model using the file location you provided in it's parameter.

```
walker eval {
    has train_file, eval_file, num_train_epochs, from_scratch;
}
```
Allows you to evaluate the model.

```
walker infer {
    has input;
}
```
This walker allows you to pass an input (user query) to the parameter and receive the necessary information for that ai model based on the input.

**Explanation of the bi_enc node**
In the last section we explained the ai_model node and in this section we integrated the ai_model node into the bi-encoder ai model which is called bi_enc. The explanation of each code input is as follows:

```
can bi_enc.train, bi_enc.infer, bi_enc.save_model;
```
This logic enables you to import functions from the jaseci kit modules imported from actions.

```
can train {
        train_data = file.load_json(visitor.train_file);
        bi_enc.train(
            dataset=train_data,
            from_scratch=visitor.train_from_scratch,
            training_parameters={
                "num_train_epochs": visitor.num_train_epochs
            }
        );
        if (visitor.model_name):
            bi_enc.save_model(model_path=visitor.model_name);
    }
```
This node ability allows you to train the bi_encoder (bi_enc) model, as you can see it overrides the train function from ai_mode node and it also requires some parameter and these parameter are presented from the walker.

```
can infer {
        res = bi_enc.infer(
            contexts=[visitor.query],
            candidates=here.candidates,
            context_type="text",
            candidate_type="text"
        )[0];

        max_score = 0;
        max_intent = "";
        for i=0 to i<res["candidate"].length by i+=1 {
            if (res["score"][i] > max_score){
                max_intent = res["candidate"][i];
                max_score = res["score"][i];
            }
        }
        report [max_intent, max_score];
    }
```
The infer function in the bi_enc module allows you to query the model and receive the intent of the user utterance.

```
can test_model {
        eval_set = file.load_json(visitor.eval_file);
        candidates = eval_set.dict::keys;

        correct = [];
        failure = [];
        for intent in candidates {
            preds = bi_enc.infer(
                contexts=eval_set[intent],
                candidates=candidates,
                context_type="text",
                candidate_type="text"
            );
            for i=0 to i<preds.length by i+=1 {
                pred = preds[i];
                max_score = 0;
                max_intent = "";
                for j=0 to j<pred["candidate"].length by j+=1 {
                    if (pred["score"][j] > max_score){
                        max_intent = pred["candidate"][j];
                        max_score = pred["score"][j];
                    }
                }
                if (intent == max_intent): correct.l::append(eval_set[intent][i]);
                else {
                    failure.l::append({
                        "sent": eval_set[intent][i],
                        "ground truth": intent,
                        "prediction": max_intent
                    });
                }
            }
        }
        report {
            "accuracy": correct.length/(correct.length+failure.length),
            "correct": correct.length,
            "failure": failure.length,
            "failed_sents": failure
        };
    }
```
This node ability allows you to test the model for the bi-encoder.

### <span style="color:red">TODO</span>:
- [ ] Update the graph spawn block to include the biencoder node
- [ ] Run the train/eval/infer walker to train a biencoder model

**Explanation of the ent_ext node**
In this section we will explain each functions for the entity extraction model for ent_ext node. The explanation goes as follows:

```
can ent_ext.entity_detection, ent_ext.train, ent_ext.save_model, ent_ext.load_model;
```
This is how we import all the functionalities for the jaseci kit module called ent_ext.


```
can train {
        train_data = file.load_json(visitor.train_file);

        if(visitor.from_scratch) {
            ent_ext.load_model({"default": true});
            here.labels = [];
        }
        for item in train_data {
            for ent in item["entities"] {
                ent_label = ent["entity_type"];
                if (ent_label not in here.labels): here.labels.l::append(ent_label);
            }
        }
        ent_ext.train(
            train_data=train_data,
            val_data=val_data,
            test_data=test_data,
            train_params={
                "num_epoch": (visitor.num_train_epochs).int,
                "batch_size": (visitor.batch_size).int,
                "LR": (visitor.learning_rate).float
            }
        );
        if (visitor.model_name):
            ent_ext.save_model(model_path=visitor.model_name);
    }
```
This is how we train the model, it requires training data, test data, val data, the number of train epochs, batch size and learning rate which was briefly explained in a earlier section.

```
can infer {
        report ent_ext.entity_detection(
            text=input["text"],
            ner_labels=input["labels"]
        );
    }
```
This is the node ability which allows you to query (user input) and get back the entity extracted from the user.

### <span style="color:red">TODO</span>:
- [ ] Update the graph spawn block to include the entity node
- [ ] Run the train/eval/infer walker to train an entity extraction model


**Integrate AI models into node abilities**
In this section we will explain the changes made to the va state to utilize the trained models.

```
can classify_intent {

        train_data = file.load_json("data/clf_train.json");
        candidates = train_data.d::keys;

        res = bi_enc.infer(
            contexts=[visitor.question],
            candidates= candidates,
            context_type="text",
            candidate_type="text"
        );

        for pred in res.list{
            # Sort result
            max_score = 0;
            max_intent = "";

            for i=0 to i < pred["candidate"].length by i+=1 {
                if (pred["score"][i] > max_score){
                    max_intent = pred["candidate"][i];
                    max_score = pred["score"][i];
                }
            }
        }

        visitor.predicted_intent = max_intent;
    }
```
At first we had hardcoded data here but it was changed after we brought in the ai models. For the classify intent node we use the bi encoder to do our intent classification. Based on the training data it will generate candidates (intent in this case) and the user query will be passed to the bi encoder model which will return the predicted intent.

```
can extract_entities {
        labels = [];

        train_data = file.load_json("data/flair_ner.json");

        for item in train_data {
            for ent in item["entities"] {
                ent_label = ent["entity_type"];
                if (ent_label not in labels): labels.l::append(ent_label);
            }
        }

        entity_result = ent_ext.entity_detection(
            text=visitor.question.str,
            ner_labels=labels.list
        );

        for ent in entity_result['entities'] {
            if (ent["conf_score"] > 0.4){
                entity_label = ent["entity_value"];
                entity_text = ent["entity_text"];
                if (entity_text not in visitor.extracted_entities ) {
                    visitor.extracted_entities[entity_label] = [];
                }
                    visitor.extracted_entities[entity_label] += [entity_text];
            }
            std.out(visitor.extracted_entities);
        }
    }
```
This also had hardcoded data however we drafted the ent_ext model into the extract_entities node ability. Which will extract all the required slot data based on the training data provided. When users query it will extract all the features and will be presented for the rest of application to work on.

### <span style="color:red">TODO</span>:
- [ ] Run the walker with the AI actions integrated

## Global root_node
In this section, we will explain the architecture of the global root node and how it works in this application. The global root node in this case is the cai_root, it utilizes the use_enc (Universal Sentence Encoder) AI module.

#### How does it work?
```
node cai_root {
    has name = "cai_root";
    can use.text_classify;
    can categorize {
        res = use.text_classify(
            text=visitor.question,
            classes=[
                "i want to test drive",
                "I have a Model 3 reservation, how do I configure my order",
                "How do I order a tesla",
                "Can I request a Test Drive"
            ]
        );
        if (res["match_idx"] == 0):
            visitor.question_type = "va";

        else:
            visitor.question_type = "faq";
    }
}
```
As you can see here it uses the sentence encoding model (use.text_classify) function which intakes a query from the user and classes (in this case the questions from the FAQ), this enables it to check match ID and if match ID is equal to zero it will then set the question type to va (virtual assistance) and if it's not equal to zero it will set the question type to faq (frequent asked question) and this will be used for further used for processing, which will be explained next. Simple right, this is how it the categorizing of user query is done.

```
cai_root {
    if (question_type == "va"):
        take --> node::va_state;
    elif (question_type == "faq"):
        take --> node::faq_state;
}
```
In the ``main.jac`` file. It will utilize the question type variable to transition to the next node. As you can see if the question type is ``va`` it will transition to the va_state and if the question type is ``faq`` it will transition the to the faq state.

### <span style="color:red">TODO</span>:
- [ ] Update the graph spawn block with the new global root
- [ ] Spawn the graph and visualizes it in dot

## Using Yield
In this section, we will show you how we utilize yield in this program.

#### What is Yield?
Yield is a way to temporarily suspend the walker and return/report to the user. When the same user calls the same walker, the walker context from previous call is retained and the walker will resume on the node it was going to go to next.

#### How is it being utilized in this application
```
if (interactive): std.out(response);
else: yield report response;
```
In the ``main.jac`` file you see that yield is being implemented. Let's explain this bit of code. If interactive is true everytime you send a query it will print the response to terminal and if it's false it would temporarily suspend the walker and report to the user the response for the query. Below you will see an example.

```
> I would like to test drive?
To set you up with a test drive, we will need your name and address.
```
When interactive is true (this is in the terminal). If you exited out and return to the program it will lose context and will restart from the beginning.

```
I would like to test drive?

{
  "success": true,
  "report": [
    "To set you up with a test drive, we will need your name and address."
  ],
  "final_node": "urn:uuid:50baeba7-b14a-4033-8c08-c0389f27bd53",
  "yielded": true
}
```
When interactive is false, yield comes into place. So if we had to pass another query it will remember the last state it was at and will act accordingly.

### <span style="color:red">TODO</span>:
- [ ] Run the walker with yield/non-interactive


## Bringing your application to production

### Register and update your jac code on a remote instance
In this section, we will walk you through on how to register and update your jac code on a remote instance. The steps are as follows:

#### Register jac code on a remote instance

First you have to login to jaseci control from the terminal.
```
jsctl -m
```

Then you will login into your remote instance by using the following. It will require you to pass in the username and password.
```
login [link here]
```

Terminal View
```
> Username:
test
> Password:
password
```

Next step is to load all jaseci actions that the application requires. One of the earlier chapter we explained the ways of loading the actions and how to.
```
actions load remote [link to jaseci actions on remote]
```

We move on to registering the sentinel.
```
sentinel register -set_active true -mode ir [jir main file of the jaseci application]
```

After registering the sentinel we will have to create the graph for application and this goes as follows.
```
graph create -set_active true
```

If you have to delete the graph however, incase of a mistake you can do that using the following command and then you can recreate.
```
graph delete active:graph
```
Next step, you will have to run the init walker
```
walker run init
```

Great, and that's how you register jac code on a remote instance.

#### Updating jac code on a remote instance
Let us walk you through on how to update jac code on the remote instance. After you make your edits to the main jac file and build it. Run the following command each time you make an update to the jac code.

```
sentinel set -snt active:sentinel -mode ir [main jir file of the application]
```

### Interact with your jac application through restful API endpoints
In this section, we will be walking you through on how to interact with your jac application through restful API endpoints, if you notice we have been running all the walker commands on the terminal, let's run it through the API. The steps to interact through the API is as follows:

```
pip install jaseci-serv
```
We will be using jaseci serve to run the application on the webserver

```
jsserv makemigrations base
```
Here we will be making the migrations for the default base module in our jaseci program. This will create a database that will be used to run a jaseci instance of our application. It creates a mydatabase file in your working directory.

```
jsserv migrate
```
This will install the schema and database.

```
jsserv createsuperuser
```
This will allow you to create the account for the server and you will be prompted to enter an email and password.

```
jsserv runserver 0.0.0.0:8000
```
This will start your Jaseci Server to run your application. Visit localhost:8000/docs to check if the webserver is up and running.

```
REQUEST [POST]: http://localhost:8000/user/token/

PAYLOAD: {
"email" : "email@gmail",
"password" : "passsword"
}

RESPONSE: {
"expiry": null,
"token": "2b4824cd3136616aa5380580578b2f5d1fccd3cad669f78029911e239300d3c0"
}
```
We will send a POST request to /user/token and get a token response now you can now make API calls to your JAC program once you copy token returned. Add it to the authorization header with the word "token" before sending any request.
```
REQUEST [POST]: http://localhost:8000/js/sentinel_register

PAYLOAD: {
    "name": "some string",
    "code": "some string",
    "code_dir": "some string",
    "mode": "some string",
    "encoded": false,
    "auto_run": "some string",
    "auto_run_ctx": {},
    "auto_create_graph": false,
    "set_active": false
}
```
This will allow you to register the sentinel for the application.

```
REQUEST [POST]: http://localhost:8000/js/graph_create

PAYLOAD: {
    "set_active": false
}
```
This will allow you to create a graph instance and return root node graph object

```
REQUEST [POST]: http://localhost:8000/js/walker_run

PAYLOAD: {
    "name": "init",
    "ctx": {},
    "snt": "urn:uuid:d32de620-27cd-4920-a31e-2e2f41bc2a9d",
    "detailed": false
}
```
This request will run the init walker which will spawn the graph and the AI models in the application.

```
REQUEST [POST]: http://localhost:8000/js/walker_run

PAYLOAD: {
    "name": "talk",
    "ctx": {
        "question": "i would like to test drive."
    },
    "snt": "urn:uuid:d32de620-27cd-4920-a31e-2e2f41bc2a9d",
    "detailed": false
}
```
For the payload sent to the /js/walker_run, the name (name of walker to be called), ctx (information sent to the walker), snt (sentinel ID  of the program ), detailed (returns additional information for the walker), nd (node walker will be set to, if not included will go to the root node). This is how we interact with jac application through restful API endpoints. In this example we ran the talk walker.

# Chapter 7

### Creating Test Cases
In this section we will explain to you the steps required to create test cases in the jac application for this application.

There are multiple ways in creating test in jac and we will explore two ways and each is as follows:

#### Test 1
In the ``test.jac file`` we will test the VA and FAQ flow from the file ``tests.json`` in the data folder.

```
walker empty {}
```
An empty walker was created to host the loading of the test suite json file. So we can run multiple walker based on the file on top of this walker.

```
test "testing faq and va flows"
```
This is how we label a test. This must go on top on of an unit test.

```
with graph::tesla_sales_rep by walker::empty {}
```
Here we referenced the graph we will be running the test on and which walker will run on top of this graph. This is how we start to create the test.

```
std.get_report();
```
This line of code returns the data returned from a report statement in a walker. This will be very important statement to use in testing.

```
assert(value_1, value_2);
```
In test in jac we mainly use the key ``assert`` which checks two values and see whether it's true or false, if it's false the test will fail and if true the test will pass. In this case we us it to match against the response of the current query from the flow file to the response that comes back when data is being reported.

```
test "testing faq and va flows"
with graph::tesla_sales_rep by walker::empty {
    flows = file.load_json("data/tests.json");

    for flow in flows {

        for step in flow["flow"] {

            spawn here walker::talk(
                question=step["query"]
            );

            res = std.get_report();

            assert(res[-1] == step["response"]);
        }
    }
}
```
Here is the entire test. Essentially, the purpose of this test is to load the test suite with all the flow in a json file and pass each query from the test suite to the walker `talk` and from the response check if it matched the data from the test suite. If it matches the test will pass if not it will fail.

#### Test 2
```
test "testing a single query"
with graph::tesla_sales_rep by walker::talk(question="Hey I would like to go on a test drive")
{
    res = std.get_report();
    assert(res[-1] == "To set you up with a test drive, we will need your name and address.");
}
```
In this test the only difference from the test above is that we are utilizing a walker that have parameters. This test allow us to test for a single query.

#### How to run test
This section will teach you how to run test. To run test use the following command below.

```
jac test test.jac
```
