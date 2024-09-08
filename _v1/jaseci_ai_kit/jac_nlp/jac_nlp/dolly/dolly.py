from jaseci.jsorc.live_actions import jaseci_action
import torch
from transformers import pipeline
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFacePipeline


@jaseci_action(act_group=["dolly"], allow_remote=True)
def setup(
    model: str = "dolly-v2-3b", input_variables: list = None, template: str = None
):
    global llm_chain, llm_context_chain, custom_llm_chain, custom_prompt
    dolly_pipeline = pipeline(
        model=f"databricks/{model}",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
        device_map="auto",
        return_full_text=True,
    )
    prompt = PromptTemplate(input_variables=["instruction"], template="{instruction}")
    prompt_with_context = PromptTemplate(
        input_variables=["instruction", "subject"],
        template="{instruction}\n\nInput:\n{subject}",
    )

    if input_variables and template:
        custom_prompt = PromptTemplate(
            input_variables=input_variables, template=template
        )
    else:
        custom_prompt = None

    hf_pipeline = HuggingFacePipeline(pipeline=dolly_pipeline)

    llm_chain = LLMChain(llm=hf_pipeline, prompt=prompt)
    llm_context_chain = LLMChain(llm=hf_pipeline, prompt=prompt_with_context)
    if custom_prompt:
        custom_llm_chain = LLMChain(llm=hf_pipeline, prompt=custom_prompt)


@jaseci_action(act_group=["dolly"], allow_remote=True)
def generate(prompt: str = None, subject: str = None, **kwargs):
    global llm_chain, llm_context_chain, custom_llm_chain, custom_prompt
    if custom_prompt:
        return custom_llm_chain.predict(**kwargs).lstrip()
    if subject is None and prompt:
        return llm_chain.predict(instruction=prompt).lstrip()
    elif subject and prompt:
        return llm_context_chain.predict(instruction=prompt, subject=subject).lstrip()
    else:
        raise Exception(
            "No custom prompt specified, and no subject context or prompt given."
        )
