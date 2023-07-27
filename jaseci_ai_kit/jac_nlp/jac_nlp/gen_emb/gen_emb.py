from typing import List, Union
from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException

# Mapping of user-friendly module names to the corresponding functions and setup functions # noqa
model_name_map = {
    "bi_enc": ("jac_nlp.bi_enc.bi_enc", "get_context_emb", "setup"),
    "gpt2": ("jac_nlp.gpt2.gpt2", "get_embeddings", "setup"),
    "sbert_sim": ("jac_nlp.sbert_sim.sbert_sim", "getembeddings", "setup"),
    "use_enc": ("jac_nlp.use_enc.use_enc", "encode", "setup"),
    "use_qa": ("jac_nlp.use_qa.use_qa", "question_encode", "setup"),
}


@jaseci_action(act_group=["gen_emb"], allow_remote=True)
def generate_embedding(texts: Union[List[str], str], selected_module: str):
    if selected_module not in model_name_map:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid module selected. Please choose from the available options: {', '.join(model_name_map.keys())}",  # noqa
        )

    module_path, embeddings_function, setup_function = model_name_map[selected_module]
    module = __import__(module_path, fromlist=[embeddings_function, setup_function])
    embeddings_function = getattr(module, embeddings_function)
    setup_function = getattr(module, setup_function)

    setup_function()  # Setup the selected module
    embeddings = embeddings_function(texts)
    return embeddings


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
