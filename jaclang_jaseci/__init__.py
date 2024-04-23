"""JacLang FastAPI."""

from dotenv import find_dotenv, load_dotenv

from .core import FastAPI


load_dotenv(find_dotenv(), override=True)

start = FastAPI.start

__all__ = ["FastAPI", "start"]
