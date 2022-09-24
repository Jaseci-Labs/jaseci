from fastapi import FastAPI, Request
import json
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from jaseci.actions.live_actions import jaseci_action, jaseci_expose

loaded_json = {}


@jaseci_action(act_group=["ui"], aliases=[], allow_remote=True)
def load_json(route: dict):
    """Loads JSON data for a given route."""
    global loaded_json

    loaded_json[route["route_name"]] = json.dumps(route["content"])
    return {}


@jaseci_expose(
    "/site/{route}", mount=["/static", StaticFiles(directory="static"), "static"]
)
def site(request: Request, route: str):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse(
        "site/index.html", {"request": request, "json": loaded_json[route]}
    )
