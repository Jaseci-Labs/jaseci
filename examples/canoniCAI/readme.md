## Getting Started CanoniCAI

##### Clone CanonCAI repo using: https://github.com/marsninja/jac_convAI

- Registering the sentinel by using this command: 
``` sentinel register -set_active true -mode ir main.jir ```

- Then create the graph by using this command:
``` graph create -set_active true ```

- Then initialize the entire application by using:
``` walker run init ``` 



## Explanation of Walkers in CanoniCAI

- **talker**: This is the main walker to interact with the conversational AI. It takes in a question from the user, which then hops from state to state and triggers various node abilities to apply NLU to the question, process some custom logic and then generates an appropriate response.

- **init**: This walker loads the AI models, generates the graph, loads modules and links certain nodes from state to state.

- **train**: These walkers teach the AI model from an existing dataset to learn to do a specific task.

- **set_pretrained_model**: Allows you to interchange what pretrained model you want to use. If you want to use distilbert, tinybert etc.

- **save_model**: Allows you to save the current state of the model you have trained for later use.

- **infer**:  This is where you validate the model by passing a query to see how it’s performing.

- **read**: This walker takes in a source url, scraps the website and then summarizes it to populate the faq state so it can teach anyone of what it has read from the website.

- **forget**: This walker unlearns everything that is in the faq state.

- **maintainer**: Keeps track of the user and its dialogue context alongside with the last conversational state. 

- **update_user**: updates the user. 


## Graph Architecture 

#### There are 4 architectures of the graph.

- User Management
- Conversational States
- Faq Architecture
- AI Model Management


#### The User Management
This is actually straightforward, this state allows us to create and manage users in the entire application alongside with storing the last conversational state of each user.

#### Conversational States
This is where the user query goes to get processed and returned back to the user.

#### Faq Architecture
This state intakes a link from the user which is then read to scrape data from the website into a summarized fashion inorder to be stored as a faq. Which can be later accessed through conversation from a user.

#### AI Model Management

It’s a centralized area for all types of AI models that does specific functions such as NER, Classification, etc. Which can be accessed by the conversational states to perform certain actions.

Here I will explain some models that we used in the CanoniCAI repo and they are as follows:

```use-qa```: This is used for text classification that requires no training data.

```bi-encoder```: We use this for text classification for our programs. However the difference between the use-qa and this jaseci-kit tool is that this one requires the user to train data for classification. Why use this over the use-qa, sometimes you may run into cases where you want to classify complex groups of text, the use-qa in this case may probably fail and this is when this will come into action.

```flair-ner```: this is used for text entity extraction. For example if I ask a bot to order me 3pc chicken combo. It should extract 3 as the quantity and chicken combo as the item and this is what it means by entity extraction.


## How are they connected?

 The first architecture we have to take into consideration is the AI model management state. This is where we map out the types of questions a user may ask alongside with the user intent. We also have to ask ourselves if there are entities that we have to capture in a conversation, like for example where is the location, name, amount of apples in the user question and from there we begin to build out the model before we could build any logic on top of that to connect the application. After the AI model management then we have to move on to the conversational state where we will focus on what we will do with the user intent and the entities extracted from it and from there generate a specific response where applicable. The faq architecture is like a cherry on top of the conversation AI state, how this feature works we first have to feed a website link to the conversational AI and it will take out the appropriate information from the site and maps a summarization form of it which will be fed into the faq state for later processing. We can then ask questions based on the link provided and the model will give you the best answer from what it has learned from the site. The user management state stores all of the user contextual information along with the last conversation dialogue. Now you should be able to understand how they are all connected in a generalized fashion.


## What node actions each state has and how are they triggered by the walkers?

#### State Node

- **Listen**: This node action is responsible for saving results to the walker context. It performs the NLU to analyze the question.
- **Plan**: Based on the NLU result, this decides which state the walker should go next.
- **Take**: Allows the walker to travel to the destination state
- **Think**: The walker is now at the state corresponding to the question asked by the user and this is where State-specific logic is done through ::business_logic
- **Speak**: Construct a response to return to the user
- **Cleanup**: Save any context you wish to retain for the future conversation turns for example it saves the last thing you spoke to the AI and it also is responsible for Post-response wrap-up.




#### FAQ State Node

- **Seek_answer**: based on all the faq nodes that is saved in the graph it will choose the best one that it closest to the original question
- **Init_answer_states**: Based on a file of faq answers it will create nodes in the graph with the answers and its embeddings.
- **Read_url**: read the website and then returns a summarized version of it in which each important sentence will be created as a node on the faq state.
- **Clean_answer_db**: Delete all faq answer state nodes

#### Faq Answer State

- **Speak**: Construct a response to return to the user


#### User State

- **Start_conv**: It collects the user context and starts to save the last conversation state
- **Update_with_conv**: Updates the user context everytime maintainer walker gets called.
init_user : it collects all the user data from the api

#### User Directory State

- **Init_users**: maps the correct user based on the user id and if it's a new user it creates that user.

#### AI Model State

- **Load_model**: load an ai model that was already trained
- **Train_model**: teaches an ai model
- **Save_model**: save the existing model
- **Set_pretrained_model**: switch between models that was already created and saved
- **Infer**: test out the model

## How to build upon canonCAI for your conversational AI use cases

I have build out a simple KFC application which I will be running you through. After running you through this application you should be able to understand how to build a simple conversation AI using canoniCAI.

#### Step 1
I've created 5 states for the KFC application. One for the start of conversation (soc), end of conversation (eoc), one that accepts order (order), order confirmation and order denial. You can reference it in the fixture.jac from line 35 to line 40.

#### Step 2
We then proceed to link each states to their corresponding states for example we linked the eoc, soc and order state to the conversation root state because a conversation can be initiated  by greeting the AI or directly by ordering a item from kfc or it can be ended just incase you had an emergency that pops up. The order confirmation and denial states are linked to the order state because when you order an item you will have to confirm or deny the item while the AI keep context of the item that asked for initially. You can reference this in the fixture.jac file from line 42 to line 58.

#### Step 3
This stage we are dealing with the business logic. In the nodes.jac file from line 291 - 306. This is how far you will put your business logics when it comes in terms of slot data extracted. You can pull data from the net and manipulate slots or just add functionality that is convienent to you. But in this KFC example we didn't need anything extra.

#### Step 4
In this stage we will be adding responses based on each state. In nodes.jac from line 308. This is how far we add the responses for this basic applcation we created.

#### Step 5
In this example we used the use qa model for classification so no need for us to add training data for this basic example for classification, we just have to go to the clf label json file in the data folder and add the labels, this should correspond to the global.jac file, however we had to train the AI for entity extraction meaning allowing the AI to extract items from the user input. how we did that is as follows, In the data folder flair_ner.json file we added user input that people would usually ask and how far the items are located using the start index and end index of the slot, the entity value is the actual value you want to be extracted and the entity type is the type of slot you want to create. In this example we created a slot named "item" but you can create multiple slot as you wish for one user input. Now you can go ahead and run the train flair ner walker and it will work.

##### Step 6
In this stage you have completed building your first conversational AI. Now you can go ahead and test how good it is and tweak what's necessary. 
