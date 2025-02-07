# RAG + Dialogue Routing Chatbot (Part 3/3)
Now that you have built a RAG chatbot, you can enhance it by adding dialogue routing capabilities. Dialogue routing is the process of directing the conversation to the appropriate dialogue model based on the user's input.

In some cases, the user query that comes in may not be suitable for the RAG model, and it may be better to route the conversation to a different model or a different dialogue system altogether. In this part of the tutorial, you will learn how to build a RAG chatbot with dialogue routing capabilities using Jac Cloud and Streamlit.

Let's modify the RAG chatbot we built in the previous part to include dialogue routing. We will add a simple dialogue router that will route the conversation to the appropriate dialogue model based on the user's input.

First, let's add a new enum `ChatType` to define the different dialogue states we will use. Add this to `server.jac`.

```jac
enum ChatType {
    RAG : 'Need to use Retrievable information in specific documents to respond' = "RAG",
    QA : 'Given context is enough for an answer' = "user_qa"
}
```

- `RAG` state is used when we need to use retrievable information in specific documents to respond to the user query.
- `QA` state is used when the given context is enough for an answer.

Next, we'll a new node to our graph called `router`. The `router` node is responsible for determining which type of model (RAG or QA) should be used to handle the query.

```jac
node Router {
    can 'route the query to the appropriate task type'
    classify(message:'query from the user to be routed.':str) -> ChatType by llm(method="Reason", temperature=0.0);
}
```

The `router` node has an ability called `classify` that takes the user query as input and classifies it into one of the `ChatType` states using the ` by llm` feature from MTLLM.

Let's now define two different modes of chatbots that the router can direct the request to accordingly.

```jac
node Chat {
    has chat_type: ChatType;
}

node RagChat :Chat: {
    has chat_type: ChatType = ChatType.RAG;

    can respond with infer entry {
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
                    chat_history: 'chat history':list[dict],
                    agent_role:'role of the agent responding':str,
                    context:'retirved context from documents':list
                        ) -> 'response':str by llm();
        data = rag_engine.get_from_chroma(query=here.message);
        here.response = respond_with_llm(here.message, here.chat_history, "You are a conversation agent designed to help users with their queries based on the documents provided", data);
    }
}

node QAChat :Chat: {
    has chat_type: ChatType = ChatType.QA;

    can respond with infer entry {
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
            chat_history: 'chat history':list[dict],
            agent_role:'role of the agent responding':str
                ) -> 'response':str by llm();
        here.response = respond_with_llm(here.message, here.chat_history, agent_role="You are a conversation agent designed to help users with their queries");
    }
}
```

We define two new nodes `RagChat` and `QAChat` that extend the `Chat` node. The `RagChat` node is used for the RAG model, and the `QAChat` node is used for a simple question-answering model. Both nodes have the ability `respond` that responds to the user query using the respective model.

In the `RagChat` node, we have a new ability `respond_with_llm` that responds to the user query using the RAG model. The ability retrieves the relevant information from the documents and responds to the user query. In the `QAChat` node, we have a new ability `respond_with_llm` that responds to the user query using a simple question-answering model.


Next, we'll add a new walker called `infer`. The `infer` walker contains the logic for routing the user query to the appropriate dialogue model based on the classification from the `Router` node.

```jac
walker infer {
    has message:str;
    has chat_history: list[dict];

    can init_router with `root entry {
        visit [-->](`?Router) else {
            router_node = here ++> Router();
            router_node ++> RagChat();
            router_node ++> QAChat();
            visit router_node;
        }
    }
}
```

Here we have a new ability `init_router` that initializes the `Router` node and creates and edge to two new nodes `RagChat` and `QAChat`. These nodes will be used to handle the RAG and QA models respectively. We'll define these nodes later. Let's finish the `infer` walker first.

The following `can` abilities should be added to the `infer` walker scope.

We add an ability `route` that classifies the user query using the `Router` node and routes it to the appropriate node based on the classification.


```jac
    can route with Router entry {
        classification = here.classify(message = self.message);
        visit [-->](`?Chat)(?chat_type==classification);
    }
```

Lastly, we'll update our `Session` node. We will maintain a record of previous conversation histories so the chatbot can have a continuous back-and-forth conversation with memories of previous interactions.

Add the following `chat` abilities to the `Session` node scope.

```jac
node Session {
    can chat with interact entry {
        self.chat_history.append({"role": "user", "content": here.message});
        response = infer(message=here.message, chat_history=self.chat_history) spawn root;
        self.chat_history.append({"role": "assistant", "content": response.response});

        report {
            "response": response.response
        };
    }
}
```

In our updated `Session` node, we have a new ability `chat` that is triggered by the `interact` walker. This means that when the interact walker traverses to the `Session` node, it will trigger the `chat` ability. The `chat` ability will then spawns the `infer` walker on `root`. The `infer` walker will execute its logic to route the user query to the appropriate dialogue model based on the classification. The response from the dialogue model is then appended to the `infer` walker's object and reported back to the frontend. This is the magic of Data Spacial programming!

**Note*+: the `can chat with Session entry` ability needs to be removed from the `interact` walker.


To summarize, here are the changes we made to our RAG chatbot to add dialogue routing capabilities:

- Our first addition is the enum `ChatType`, which defines the different types of chat models we will use. We have two types: `RAG` and `QA`. `RAG` is for the RAG model, and `QA` is for a simple question-answering model. This will be used to classify the user query and route it to the appropriate model.
- Next we have a new node `Router`, with the ability `classify`. The ability classifies the user query and route it to the appropriate model.
- We have a new walker `infer`, which has the ability `route`. The ability routes the user query to the appropriate model based on the classification.
- We have two new nodes `RagChat` and `QAChat`, which are the chat models for the RAG and QA models respectively. These nodes extend the `Chat` node and have the ability `respond`. The ability responds to the user query using the respective model.
- In the `RagChat` node, we have a new ability `respond_with_llm`, which responds to the user query using the RAG model. The ability retrieves the relevant information from the documents and responds to the user query.
- In the `QAChat` node, we have a new ability `respond_with_llm`, which responds to the user query using a simple question-answering model.
- We update our `interact` walker to include the new `init_router` ability, which initializes the router node and routes the user query to the appropriate model.
- Lastly, we update the `Session` node to have the ability `chat`, which is triggered by the when the `interact` walker is on the node. This ability spawns the `infer` walker and reports the response back to the frontend.

Now that we have added dialogue routing capabilities to our RAG chatbot, we can test it out by running the following command:

```bash
DATABASE_HOST=mongodb://localhost:27017/?replicaSet=my-rs jac serve server.jac
```

Viola! You have successfully built a RAG chatbot with dialogue routing capabilities using Jac Cloud and Streamlit. You can now test your chatbot by interacting with it in the Streamlit frontend. Have fun chatting!