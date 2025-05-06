


import from action {actions}


with entry{

        openai = actions.LLM();
        agent = actions.AgentNode();
        print("openai: response: ", openai.testing_infer());


}