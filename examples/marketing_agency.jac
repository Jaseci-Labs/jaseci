import:py from mtllm.llms { OpenAI }
import:py from mtllm.tools.wikipedia_utils { wikipedia_summary }
import:py os;

glob llm = OpenAI(model_name="gpt-4o-mini");

can 'Save the output as a markdown file'
save_output_as_md(output:'Markdown formatted Text': str, filename: str) -> None {
    with open(filename, 'w') as f {f.write(output);}
}

can 'Expert Persona Generation Agent'
persona_expert(requirements: 'Managers Requirements': str) -> 'Markdown Styled Report': str
by llm(method="ReAct", tools=[wikipedia_summary]);

can 'Expert Demographic Analysis Agent'
demographic_expert(requirements: 'Managers Requirements': str) -> 'Markdown Styled Report': str
by llm(method="ReAct", tools=[wikipedia_summary]);

can 'Expert Market Analysis Agent'
market_expert(requirements: 'Managers Requirements': str) -> 'Markdown Styled Report': str
by llm(method="ReAct", tools=[wikipedia_summary]);

can 'Expert in demand analysis'
demand_expert(requirements: 'Managers Requirements': str) -> 'Markdown Styled Report': str
by llm(method="ReAct", tools=[wikipedia_summary]);

can 'Manager agent come up with a marketing strategy and delegate tasks with detailed requirements to the team'
manager(query: 'Customers Inquiry': str) -> "Summary": str
by llm(
    method="ReAct",
    tools=[save_output_as_md, persona_expert, demographic_expert, market_expert],
    max_react_iterations=100,
    max_prev_react_outputs=10,
    context=["MAKESURE TO SAVE THE COMPLETE REPORT IN THE END"]
);

with entry {
    query = "We are creating a product called 'HireHero' an intelligent talent acquition software."
            "Create a detailed market analysis with demand, personas, and demographics.";
    manager(query);
}