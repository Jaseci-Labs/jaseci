from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jaseci.actions.live_actions import jaseci_action, jaseci_expose

templates = Jinja2Templates(directory="templates")
app = FastAPI(title="Jaseci UIKit Renderer", version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")

loaded_json = {}


@jaseci_action(act_group=["ui"], aliases=[], allow_remote=True)
def load_json(route: dict):
    """Loads JSON data for a given route."""
    global loaded_json

    loaded_json[route["route_name"]] = route["content"]
    return {}


@jaseci_expose("/site/{route}")
def site(request: Request, route: str):
    return templates.TemplateResponse(
        "site/index.html", {"request": request, "json": loaded_json[route]}
    )
