import asyncio
from sys import argv

from jaseci.jsorc.live_actions import jaseci_action
from jac_misc.scraper.sync_scraper import scrape as sync_scrape
from jac_misc.scraper.async_scraper import scrape as async_scrape


if any(["uvicorn" in arg for arg in argv]):
    from os import getenv
    from orjson import dumps
    from fastapi import FastAPI
    from pydantic import BaseModel
    from websocket import WebSocketApp as wsa

    from jaseci.jsorc.jsorc import JsOrc
    from jaseci.utils.utils import logger
    from jaseci.extens.svc import SocketService as Ss

    @JsOrc.service(
        name="socket",
        config="SOCKET_CONFIG",
        manifest="SOCKET_MANIFEST",
        priority=1,
        pre_loaded=True,
    )
    class SocketService(Ss):
        def on_open(self, ws: wsa):
            pass

        def send(self, ws: wsa, data: dict):
            try:
                ws.send(dumps(data))
            except Exception:
                ss = JsOrc.svc_reset("socket", SocketService)
                ss.send(ss.app, data)

        def on_close(self, ws: wsa, close_status_code, close_msg):
            JsOrc.svc_reset("socket")

        def on_error(self, ws: wsa, error):
            JsOrc.svc_reset("socket")

    JsOrc.settings("SOCKET_CONFIG").update(
        {
            "enabled": getenv("SCRAPER_SOCKET_ENABLED") == "true",
            "url": getenv("SCRAPER_SOCKET_URL", "ws://jaseci-socket/ws"),
            "ping_url": getenv(
                "SCRAPER_SOCKET_PING_URL", "http://jaseci-socket/healthz"
            ),
            "auth": getenv("SCRAPER_SOCKET_AUTH", "12345678"),
        }
    )
    JsOrc.svc("socket").poke()

    class ScraperRequest(BaseModel):
        pages: list
        pre_configs: list = []
        detailed: bool = False
        target: str = None
        is_async: bool = False

    app = FastAPI()

    @app.post("/setup/")
    def setup():
        pass

    @app.post("/scrape/")
    async def scrape(sr: ScraperRequest):
        if sr.is_async:
            task = asyncio.create_task(
                async_scrape(sr.pages, sr.pre_configs, sr.detailed, sr.target)
            )
            return {"task": task.get_name()}
        else:
            return await async_scrape(sr.pages, sr.pre_configs, sr.detailed, sr.target)

    @app.get("/jaseci_actions_spec/")
    def action_list():
        return {
            "wbs.setup": [],
            "wbs.scrape": ["pages", "pre_configs", "detailed", "target", "is_async"],
        }

else:

    @jaseci_action(act_group=["wbs"])
    def setup():
        pass

    @jaseci_action(act_group=["wbs"])
    def scrape(
        pages: list, pre_configs: list = [], detailed: bool = False, target: str = None
    ):
        return sync_scrape(pages, pre_configs, detailed, target)
