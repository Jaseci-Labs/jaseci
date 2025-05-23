import from mtllm.llms {OpenAI}
import from rag {RagEngine}

glob llm = OpenAI(model_name='gpt-4o');
glob rag_engine:RagEngine = RagEngine();

walker interact {
    has message: str;
    has session_id: str;

    can init_session with `root entry {
         visit [-->](`?Session)(?id == self.session_id) else {
            session_node = here ++> Session(id=self.session_id, chat_history=[], status=1);
            print("Session Node Created");

            visit session_node;
        }
    }
}
node Session {
    has id: str;
    has chat_history: list[dict];
    has status: int = 1;

    can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
    llm_chat(
        message:'current message':str,
        chat_history: 'chat history':list[dict],
        agent_role:'role of the agent responding':str,
        context:'retrieved context from documents':list
    ) -> 'response':str by llm();

    can chat with interact entry {
        self.chat_history.append({"role": "user", "content": visitor.message});
        response = infer(message=visitor.message, chat_history=self.chat_history) spawn root;
        self.chat_history.append({"role": "assistant", "content": response.response});

        report {
            "response": response.response
        };
    }
}

enum ChatType {
    RAG : 'Need to use Retrievable information in specific documents to respond' = "RAG",
    QA : 'Given context is enough for an answer' = "user_qa"
}

node Router {
    can 'route the query to the appropriate task type'
    classify(message:'query from the user to be routed.':str) -> ChatType by llm(method="Reason", temperature=0.0);
}

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
    can route with Router entry {
        classification = here.classify(message = self.message);
        visit [-->](`?Chat)(?chat_type==classification);
    }
}

node Chat {
    has chat_type: ChatType;
}

node RagChat(Chat) {
    has chat_type: ChatType = ChatType.RAG;

    can respond with infer entry {
        print("Responding to the message");
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
                    chat_history: 'chat history':list[dict],
                    agent_role:'role of the agent responding':str,
                    context:'retirved context from documents':list
                        ) -> 'response':str by llm();
        data = rag_engine.get_from_chroma(query=visitor.message);
        print("Data:", data);
        visitor.response = respond_with_llm(visitor.message, visitor.chat_history, "You are a conversation agent designed to help users with their queries based on the documents provided", data);
        print("Visitor:", visitor);
    }
}

node QAChat(Chat) {
    has chat_type: ChatType = ChatType.QA;

    can respond with infer entry {
        print("Responding to the message");
        can 'Respond to message using chat_history as context and agent_role as the goal of the agent'
        respond_with_llm(   message:'current message':str,
            chat_history: 'chat history':list[dict],
            agent_role:'role of the agent responding':str
                ) -> 'response':str by llm();
        visitor.response = respond_with_llm(visitor.message, visitor.chat_history, agent_role="You are a conversation agent designed to help users with their queries");
        print("Visitor:", visitor);
    }
}
