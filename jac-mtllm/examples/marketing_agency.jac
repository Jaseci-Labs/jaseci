import from mtllm.llms { OpenAI }
import from mtllm.tools.wikipedia_utils { wikipedia_summary }
import from mtllm.tools.serper { search, scrape }

glob llm = OpenAI(verbose=True, model_name="gpt-4o-mini");

def save_output_as_md(output: str, filename: str) -> None {
    with open(filename, 'w') as f {
        f.write(output);
    }
}

can 'Expert Persona Generation Agent, Generate detailed personas for a product'
persona_expert(requirements: 'Managers Requirements': str) -> 'Markdown Formatted Detailed Report with citations': str
by llm(
    method="ReAct",
    tools=[wikipedia_summary, search, scrape],
    max_prev_react_outputs=10,
    max_react_iterations=10,
    context=["DONOT SUMMARIZE. MAKE IT DETAILED"]
);
can 'Expert Demographic Analysis Agent, Perform a detailed analysis of the demographics for a product'
demographic_expert(requirements: 'Managers Requirements': str) -> 'Markdown Formatted Detailed Report with citations': str
by llm(
    method="ReAct",
    tools=[wikipedia_summary, search, scrape],
    max_prev_react_outputs=10,
    max_react_iterations=10,
    context=["DONOT SUMMARIZE. MAKE IT DETAILED"]
);
can 'Expert Market Analysis Agent, Perform a detailed analysis of the market for a product'
market_expert(requirements: 'Managers Requirements': str) -> 'Markdown Formatted Detailed Report with citations': str
by llm(
    method="ReAct",
    tools=[wikipedia_summary, scrape, search],
    max_prev_react_outputs=10,
    max_react_iterations=10,
    context=["DONOT SUMMARIZE. MAKE IT DETAILED"]
);
can 'Expert in demand analysis, Perform a detailed analysis of the demand for a product'
demand_expert(requirements: 'Managers Requirements': str) -> 'Markdown Formatted Detailed Report with citations': str
by llm(
    method="ReAct",
    tools=[wikipedia_summary, search, scrape],
    max_prev_react_outputs=10,
    max_react_iterations=10,
    context=["DONOT SUMMARIZE. MAKE IT DETAILED"]
);
can 'Manager agent come up with a marketing strategy and delegate tasks with detailed requirements to the team'
manager(query: 'Customers Inquiry': str) -> "Markdown Formatted Highy Detailed Report with an Executive Summary": str
by llm(
    method="ReAct",
    tools=[persona_expert, demographic_expert, market_expert, search, scrape],
    max_react_iterations=10,
    max_prev_react_outputs=10,
    context=["DONOT SUMMARIZE. MAKE IT DETAILED"]
);

with entry {
    query = "Jaclang is a native superset of python with a focus on AI and ML. Jaclang allows developers to"
        "prototype AI Applications with ease by providing high level abstractions for AIML Usecases."
        "Perform a detailed analysis of the market for Jaclang and provide a detailed report on the market,"
        "demand, demographics and personas for the product.";
    save_output_as_md(manager(query), "marketing_report.md");
}
