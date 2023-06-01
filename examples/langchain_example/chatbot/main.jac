walker query {
    has question;
    has chat_history;
    can langchain.generate;

    report langchain.generate(input={"query": question, "chat_history": chat_history});
}

walker update_chain {
    has text;
    has openai_api_key;
    can langchain.setup;

    langchain.setup(flow_type="document-chat-flow", text=text, openai_api_key=openai_api_key);
}