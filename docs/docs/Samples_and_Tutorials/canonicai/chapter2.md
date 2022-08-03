---
title: Chapter 2
---
## i. Architecture overview
![Architecture](/img/tutorial/images/architecture.png?raw=true "Title")

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
![Conversation AI](/img/tutorial/images/convai.png?raw=true "Title")

As we acknowledge, this is where the user query an utterance and gets a response from the application. In this section we will explain in more details how the diagram above works. Each nodes represents a conversational state and each of the edges represents the transition path between states. However, they are different type of edges, some are triggered by a certain intent which is tied to a conversational state as show above where state 1 and state 2 lies and some are triggered when they are fulfilled by the entities picked up from the user query. In this component, we leveraged the power of the intent classification using the bi-encoder AI model (bi_enc) and for entity extraction we utilized the Transformer NER Model (tsfm_ner). Each state nodes also have functions which can be shared between states for e.g. each state can have a function where it generates a response for the user and there can be another state function which deals with the business logics (extra processing of user input). So, what's the flow, The user query an utterance and is navigated to the conversational ai state which it goes through the intent classification model to grab the meaning of the query and based on the intent which are tied to a state it navigates the state through an edge and based on the states that's how it will traverse through the graph shown above.

### iii. Zero-shot FAQ
![Zero-shot FAQ](/img/tutorial/images/faq.png?raw=true "Title")

In this section, we will explain how this works. Every node represents a faq state and the edges represent transition paths between states. In this component we are utilizing summarization AI model (cl_summer) and a sentence encoder (use_qa). Before anyone can query the FAQ state we have to first explain how data is stored in the FAQ states and how the FAQ answer states are generated. In the FAQ state, a link to a website or PDF have to be fed into the summarization model (cl_summer) and what this does it compute and scrape all the information from the website, summarize it and each summarized section is segmented and stored as new states in the faq section which will be later accessed through the AI. When a user queries and the input is sent to the FAQ state it will be intercepted by the sentence encoder (use_qa) which will look for the best possible faq answer state available, then returns it to the user as a response.

### iv. Model trainer

![Model trainer](/img/tutorial/images/trainer.png?raw=true "Title")

We utilize 4 AI models in which each have a different method of training. The four models includes the bi-encoder (bi_enc), sentence encoder (use_enc), entity extraction (tsfm_ner) and summarization model (cl_summer). From the root node each AI model states are created which they all can be trained through the walkers. Each nodes have specific function for specific task and it can all be classified in this order load, train, save, set pretrained and infer model function.

* **Load_model**: load an ai model that was already trained
* **Train_model**: teaches an ai model
* **Save_model**: save the existing model
* **Set_pretrained_model**: switch between models that was already created and saved
* **Infer**: test out the model

### v. Tieing all components together

The first architecture we have to take into consideration is the AI model management state. This is where we map out the types of questions a user may ask alongside with the user intent. We also have to ask ourselves if there are entities that we have to capture in a conversation, like for example where is the location, name, amount of apples in the user question and from there we begin to build out and train the model before we could build any logic on top of that to connect the application. After the AI model management then we have to move on to the conversational state where we will focus on what we will do with the user intent and the entities extracted from it and from there generate a specific response where applicable. The faq architecture is like a cherry on top of the conversation AI state, how this feature works we first have to feed a website link to the conversational AI and it will take out the appropriate information from the site and maps a summarization form of it which will be fed into the faq state for later processing. We can then ask questions based on the link provided and the model will give you the best answer from what it has learned from the site. Now you should be able to understand how they are all tied together in a generalized fashion.

### vi. Tesla use case example
![Tesla Use Case](/img/tutorial/images/tesla.png?raw=true "Title")
In this section, we will guide you how the entire architecture work with a real example. First, we will walk you through its design for the conversation AI component and then walk you through the FAQ component.

* **Conversation AI Component**: Imagine we are interacting with a tesla sales person but it's not human its a chatbot. As a user, we will ask a question and as we ask the question it will first go to the Top Level Classification State where it will decide whether to go to the FAQ state or the Conversation AI state using the sentence encoder (use_enc) AI Model, In this case we ask a question about wanting to test drive a tesla. The AI model will analyse then know we are asking a question that is not related to anything in the FAQ section so it will navigate us to the Conversation AI State where it will use the bi-encoder AI model to find the intent of the initial question and extract the entity if any from the user query. In this case we ask the tesla sales person if we can test drive the tesla. The tesla bot will navigate to the collect information state where it will ask for your name and address and when those slots are fulfilled, the edge will trigger to move to the next state (confirmation state) to confirm that the information is correct and based on your next response you can either cancel the entire process which will trigger the edge ,which will navigate you to the cancel state or you can confirm that all the information is accurate and get navigated to the confirmed state or you can update the information which will carry you back to the collect information state. The navigation from state to state is triggered either from intent classification or through entity extraction. That's how that process works.

* **FAQ Component**: Imagine you are asking a question "when do you guys open". In the Top Level Classification state, where it uses the sentence encoder to decide whether to navigate to the conversation AI state or the FAQ state. In this case the AI when processing this utterance it will navigate it to the FAQ state. Where it use a difference sentence encoder (use_qa) which is specialist for FAQ models. The edge will get triggered to the best appropriate faq answer state that is related to the query the user asked and display it to the user.
