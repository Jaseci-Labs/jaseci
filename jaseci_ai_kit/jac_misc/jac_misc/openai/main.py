'''
OpenAI Integration for Jaseci
Features:
    - GPT-3 (Completion and Chat)
    - Codex (Code Completion)
    - DALL-E (Image Generation)
    - Whispers (Audio Transcription)

Requires OpenAI API Key
'''

from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import logger
import os
import openai
from typing import Union

@jaseci_action(act_group=["openai"], allow_remote=True)
def setup(api_key=os.environ.get('OPENAI_API_KEY', None)):
    """
    Sets up OpenAI API Key
    """
    if not api_key:
        logger.error("No OpenAI API Key Provided. Please set OPENAI_API_KEY environment variable or pass in api_key parameter though actions call openai.setup")
        return False
    else:
        openai.api_key = api_key
        return True

@jaseci_action(act_group=["openai"], allow_remote=True)
def completion(prompt: Union[str, list] = "<|endoftext|>", model: str= "text-davinci-003", suffix: str = None, 
                max_tokens:int = 16, temperature: float = 1, top_p: float = 1, n: int = 1, logprobs: int = None, 
               echo: bool = False, stop: Union[str, list] = None, presence_penalty: float = 0, frequency_penalty: float = 0,
                best_of: int = 1):
    """
    Completion API
    """
    response = openai.Completion.create(model = model, prompt = prompt,suffix=suffix, max_tokens = max_tokens, temperature = temperature,
                                        top_p = top_p, n = n, logprobs = logprobs, echo = echo, stop = stop,
                                        presence_penalty = presence_penalty, frequency_penalty = frequency_penalty,
                                        best_of = best_of)
    response = [x.text for x in response.choices]
    return response

@jaseci_action(act_group=["openai"], allow_remote=True)
def chat(messages: list, model:str = 'gpt-3.5-turbo', temperature:float = 1, top_p:float = 1, n:int = 1, stop: Union[str, list] = None,
         presence_penalty: float = 0, frequency_penalty: float = 0):
    """
    Chat API
    """
    response = openai.ChatCompletion.create(model = model, prompt = messages, temperature = temperature, top_p = top_p, n = n,
                                        stop = stop, presence_penalty = presence_penalty, frequency_penalty = frequency_penalty)
    response = [x.message for x in response.choices]
    return response

@jaseci_action(act_group=["openai"], allow_remote=True)
def get_embeddings(input: Union[str, list], model: str = "text-embedding-ada-002"):
    """
    Embedding API
    """
    response = openai.Embedding.create(model = model, inputs = input)
    response = [x.embedding for x in response.data]
    return response

@jaseci_action(act_group=["openai"], allow_remote=True)
def transcribe(audio_file:str = None, audio_url:str = None, audio_array:list = None, model:str = "whisper-1", prompt:str = None, temperature: float = 0,
               language:str = None, translate=False):
    """
    Whispers API
    """
    if audio_array:
        import soundfile as sf
        import tempfile
        import numpy as np

        audio_array = np.array(audio_array)

        with tempfile.NamedTemporaryFile(suffix=".wav") as fp:
            sf.write(fp.name, audio_array, 16000)
            audio_file = fp.name
    if audio_url:
        import urllib.request
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".wav") as fp:
            urllib.request.urlretrieve(audio_url, fp.name)
            audio_file = fp.name

    audio_file = open(audio_file, "rb")
    if not translate:
        transcription = openai.Audio.transcribe(file=audio_file, model=model, prompt=prompt, temperature=temperature, language=language)
    else:
        transcription = openai.Audio.translate(file=audio_file, model=model, prompt=prompt, temperature=temperature, language=language, translate=translate)
    return transcription.text
        

@jaseci_action(act_group=["openai"], allow_remote=True)
def generate_image(prompt:str, n:int = 1, size:str = "512x512", response_format:str = "url"):
    """
    DALL-E 2 Image Generation API
    """
    response = openai.Image.create(prompt=prompt, n=n, size=size, response_format=response_format)
    response = [x.url if response_format == 'url'else x.b64_json for x in response.data]
    return response

@jaseci_action(act_group=["openai"], allow_remote=True)
def edit_image(prompt:str, image_file:str = None, mask_file:str = None, image_b64:str= None, mask_b64:str = None,  n:int = 1, size:str = "512x512",
                response_format:str = "url"):
    """
    DALL-E 2 Image Edit API
    """
    if image_b64:
        import base64
        import tempfile
        image = base64.b64decode(image_b64)
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            fp.write(image)
            image_file = fp.name
    if mask_b64:
        import base64
        import tempfile
        mask = base64.b64decode(mask_b64)
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            fp.write(mask)
            mask_file = fp.name

    image = open(image_file, "rb")
    mask = open(mask_file, "rb")

    response = openai.Image.create_edit(prompt=prompt, n=n, size=size, response_format=response_format, image=image, mask=mask)
    response = [x.url if response_format == 'url'else x.b64_json for x in response.data]
    return response

@jaseci_action(act_group=["openai"], allow_remote=True)
def variations_image(image_file:str = None, image_b64:str= None,  n:int = 1, size:str = "512x512", response_format:str = "url"):
    """
    DALL-E 2 Image Variation API
    """
    if image_b64:
        import base64
        import tempfile
        image = base64.b64decode(image_b64)
        with tempfile.NamedTemporaryFile(suffix=".png") as fp:
            fp.write(image)
            image_file = fp.name
    
    image = open(image_file, "rb")

    response = openai.Image.create_variation(n=n, size=size, response_format=response_format, image=image)
    response = [x.url if response_format == 'url'else x.b64_json for x in response.data]
    return response