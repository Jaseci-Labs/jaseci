from typing import List, Union, Optional, Dict, Tuple
from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException

# Mapping of module names to the corresponding functions and setup functions
model_name_map: Dict[str, Tuple[str, str, str]] = {
    "bi_enc": ("jac_nlp.bi_enc.bi_enc", "get_context_emb", "setup"),
    "gpt2": ("jac_nlp.gpt2.gpt2", "get_embeddings", "setup"),
    "sbert_sim": ("jac_nlp.sbert_sim.sbert_sim", "getembeddings", "setup"),
    "use_enc": ("jac_nlp.use_enc.use_enc", "encode", "setup"),
    "use_qa": ("jac_nlp.use_qa.use_qa", "question_encode", "setup"),
}

# Initialize variables for selected module and functions
selected_module: Optional[str] = None
embedding_function: Optional[callable] = None
setup_function: Optional[callable] = None


@jaseci_action(act_group=["gen_emb"], allow_remote=True)
def setup(module_name: str = "sbert_sim"):
    """
    Set up the module provided.

    Args:
        module_name (str): The name of the module to setup.

    Raises:
        HTTPException: If the selected module is not valid or an error occurs during setup.  # noqa
    """
    global selected_module, embedding_function, setup_function

    if module_name not in model_name_map:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid module selected. Please choose from the available options: {', '.join(model_name_map.keys())}",  # noqa
        )

    try:
        module_path, embedding_function_name, setup_function_name = model_name_map[
            module_name
        ]
        module = __import__(
            module_path, fromlist=[embedding_function_name, setup_function_name]
        )
        embedding_function = getattr(module, embedding_function_name)
        setup_function = getattr(module, setup_function_name)
        setup_function()  # Setup the selected module
        selected_module = module_name
        return {"message": f"Selected module instantiated: {module_name}"}
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to import module: {module_name}. Please ensure that the module is installed.",  # noqa
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during setup: {str(e)}",
        )


@jaseci_action(act_group=["gen_emb"], allow_remote=True)
def generate_embedding(texts: Union[List[str], str]):
    """
    Generate embeddings for the given text(s) using the selected module.

    Args:
        texts (Union[List[str], str]): The text(s) to generate embeddings for.

    Returns:
        The generated embeddings.

    Raises:
        HTTPException: If the module has not been set up yet.
    """
    global selected_module, embedding_function

    if selected_module is None:  # Check if module is setup
        raise HTTPException(
            status_code=500,
            detail="Please run setup() to select the module",
        )

    embeddings = embedding_function(texts)
    return embeddings


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
