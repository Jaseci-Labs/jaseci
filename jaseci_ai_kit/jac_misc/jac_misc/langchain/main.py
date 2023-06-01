from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import logger
import os

DEFAULT_PREFIX = "Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer."
chat_flows = {}


@jaseci_action(act_group=["langchain"], allow_remote=True)
def setup(flow_type: str = "json", **kwargs):
    """
    Setup a flow for use in the generate action.
    """
    uid = kwargs.pop("uid", "default")
    if flow_type == "json":
        from langflow import load_flow_from_json

        json_file = kwargs.pop("json_file", None)
        if not json_file:
            logger.error(
                "No json file was passed. Please pass a json file using the json_file argument."
            )
            return
        chat_flows[uid] = load_flow_from_json(json_file)
        return
    elif flow_type == "qa-flow":
        chat_flows[uid] = QuestionAnsweringFlow(**kwargs, uid=uid)
        return
    elif flow_type == "document-chat-flow":
        chat_flows[uid] = DocumentChatFlow(**kwargs, uid=uid)
        return
    logger.error("Flow type not found. Please use either 'json' or 'qa-flow'.")


@jaseci_action(act_group=["langchain"], allow_remote=True)
def generate(input: dict, flow: str = "default") -> str:
    """
    Generate text using a flow that was setup using the setup action.
    """
    if not flow in chat_flows:
        logger.error("Flow not found. Please setup a flow using the setup action.")
        return
    return chat_flows[flow](**input)


class QuestionAnsweringFlow:
    """
    A flow that can be used to answer questions based on a given text.
    """

    def __init__(
        self,
        text: str,
        uid: str,
        prefix: str = DEFAULT_PREFIX,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        **kwargs,
    ):
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.vectorstores import Chroma
        from langchain.prompts import PromptTemplate

        if os.path.isfile(text) and text.endswith(".txt"):
            with open(text) as f:
                data = f.read()
        else:
            data = text
        text_splitter = CharacterTextSplitter(
            chunk_size=kwargs.get("chunk_size", 1000),
            chunk_overlap=kwargs.get("chunk_overlap", 0),
        )
        texts = text_splitter.split_text(data)

        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key, **kwargs.get("embeddings_kwargs", {})
        )
        self.vectorstore = Chroma.from_texts(
            texts,
            embeddings,
            metadatas=[{"source": str(i)} for i in range(len(texts))],
            collection_name=f"{uid}_data",
            persist_directory=f".jaseci/{uid}",
        ).as_retriever()

        from langchain.chains.question_answering import load_qa_chain
        from langchain.llms import OpenAI

        llm = OpenAI(openai_api_key=openai_api_key, **kwargs.get("llm_kwargs", {}))

        prompt_template = prefix + "\n\n{context}\nQuestion: {question}\nAnswer:"
        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        self.chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)

    def __call__(self, query: str):
        docs = self.vectorstore.get_relevant_documents(query)
        output = self.chain(
            {"input_documents": docs, "question": query}, return_only_outputs=True
        )
        return {"output": output["output_text"].strip()}


class DocumentChatFlow:
    """
    A flow that can be used to chat with a chatbot based on a given text.
    """

    def __init__(
        self,
        text: str,
        uid: str,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        **kwargs,
    ):
        from langchain.embeddings.openai import OpenAIEmbeddings
        from langchain.vectorstores import Chroma
        from langchain.text_splitter import CharacterTextSplitter
        from langchain.llms import OpenAI
        from langchain.chains import ConversationalRetrievalChain
        from langchain.document_loaders import TextLoader

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        if not (os.path.isfile(text) and text.endswith(".txt")):
            import tempfile

            file = tempfile.NamedTemporaryFile(mode="w", delete=False)
            file.write(text)
            file.close()
            text = file.name
        loader = TextLoader(text)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(
            chunk_size=kwargs.get("chunk_size", 1000),
            chunk_overlap=kwargs.get("chunk_overlap", 0),
        )
        documents = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key, **kwargs.get("embeddings_kwargs", {})
        )
        vectorstore = Chroma.from_documents(documents, embeddings)

        from langchain.llms import OpenAI

        llm = OpenAI(openai_api_key=openai_api_key, **kwargs.get("llm_kwargs", {}))

        self.chain = ConversationalRetrievalChain.from_llm(
            llm, vectorstore.as_retriever()
        )

    def __call__(self, query: str, chat_history: list = []):
        chat_history = [tuple(i) for i in chat_history]
        result = self.chain({"question": query, "chat_history": chat_history})
        return {"answer": result["answer"].strip()}
