import:py from mtllm.llms {OpenAI}
import:py from mtllm.tools.wikipedia_utils {wikipedia_summary}

glob llm = OpenAI(model_name="gpt-4o-mini");

can 'Ask Opponent for Input'
ask_opponent(statement: 'Your Statement': str) -> str {
    user_input = input(f"AI -> {statement} ");
    return f"Opponents Answer -> {user_input}";
}

can 'States the Facts to the Opponent'
state_facts(information: str) -> None {
    print(f"AI -> {information}");
}

can 'Perform a debate session with a opponent on the given topic, for information use given tools'
debate_agent(topic: 'Debate Topic': str) -> 'Summary of the Conversation': str
by llm(
    method='ReAct',
    tools=[wikipedia_summary, ask_opponent, state_facts],
    context=[
        "You have to defend the given topic while the opponent is defending the counter topic",
        "If you dont know about the topic or you want to verify the opponents claims use the given tools",
        "You can ask opponent counter questions",
        "You are a humorous, cunning, very arrogant debater."
    ]
);

with entry {
    debate_agent('Merlin the Wizard is still alive.');
}