from typing import Union
from fastapi import FastAPI
from fastapi import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="Jaseci UIKit Renderer",version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

loaded_json = {};

class Route(BaseModel):
    route_name: str
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/load-json")
def load_json(request: Request, route: Route):
    global loaded_json
   
    loaded_json[route.route_name] = route.content
    return {}

@app.get("/site/{route}")
async def home(request: Request, route: str):
    return templates.TemplateResponse("site/index.html", {"request": request, "json": loaded_json[route]})

