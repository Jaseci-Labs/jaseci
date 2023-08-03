from typing import List, Union, Optional, Dict, Tuple
from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException

# Mapping of module names to the corresponding functions and setup functions
model_name_map: Dict[str, Tuple[str, str, str]] = {
    "gpt2": ("jac_nlp.gpt2.gpt2", "generate", "setup"),
    "llm": ("jac_nlp.llm.llm", "generate", "setup"),
    "dolly": ("jac_nlp.dolly.dolly", "generate", "setup"),
}

# Initialize variables for selected module and functions
selected_module: Optional[str] = None
generate_function: Optional[callable] = None
setup_function: Optional[callable] = None


@jaseci_action(act_group=["gen_text"], allow_remote=True)
def setup(module_name: str = "gpt2"):
    """
    Set up the module provided.

    Args:
        module_name (str): The name of the module to setup.

    Raises:
        HTTPException: If the selected module is not valid or an error occurs during setup. # noqa
    """
    global selected_module, generate_function, setup_function

    if module_name not in model_name_map:
        raise HTTPException(
            status_code=500,
            detail=f"Invalid module selected. Please choose from the available options: {', '.join(model_name_map.keys())}",  # noqa
        )

    try:
        module_path, generate_function_name, setup_function_name = model_name_map[
            module_name
        ]
        module = __import__(
            module_path, fromlist=[generate_function_name, setup_function_name]
        )
        generate_function = getattr(module, generate_function_name)
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


@jaseci_action(act_group=["gen_text"], allow_remote=True)
def generate_text(
    prompt: str, num_words: int = 30, kwargs: Optional[Dict] = None
) -> Union[List[str], str]:
    """
    Generate text based on the provided prompt using the selected module.

    Args:
        prompt (str): The input prompt for text generation.
        num_words (int): The number of words to generate.
        kwargs (Optional[Dict]): Additional keyword arguments for text generation.

    Returns:
        The generated text.

    Raises:
        HTTPException: If the module has not been set up yet or an error occurs during text generation. # noqa
    """
    global selected_module, generate_function

    if selected_module is None:  # Check if module is setup
        raise HTTPException(
            status_code=500,
            detail="Please run setup() to select the module",
        )

    try:
        if kwargs is None:
            kwargs = {}
        generated_text = generate_function(prompt, **kwargs)
        return generated_text
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during text generation: {str(e)}",
        )


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
