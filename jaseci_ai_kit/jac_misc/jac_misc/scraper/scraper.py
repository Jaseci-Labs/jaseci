import asyncio
from sys import argv
from fastapi import FastAPI
from pydantic import BaseModel

from jaseci.jsorc.live_actions import jaseci_action
from jac_misc.scraper.sync_scraper import (
    scrape as sync_scrape,
    scrape_preview as sync_scrape_preview,
)
from jac_misc.scraper.async_scraper import (
    scrape as async_scrape,
    scrape_preview as async_scrape_preview,
)
from jac_misc.scraper.utils import Process


if any(["uvicorn" in arg for arg in argv]):

    class ScraperRequest(BaseModel):
        pages: list
        pre_configs: list = []
        detailed: bool = False
        target: str = None
        trigger_id: str = None
        is_async: bool = False

    class ScraperPreviewRequest(BaseModel):
        page: dict
        target: str = None
        is_async: bool = False

    class ScraperStopper(BaseModel):
        trigger_id: str = None

    app = FastAPI()

    @app.post("/setup/")
    def setup():
        pass

    @app.post("/scrape/")
    async def scrape(sr: ScraperRequest):
        if sr.is_async:
            task = asyncio.create_task(
                async_scrape(
                    sr.pages, sr.pre_configs, sr.detailed, sr.target, sr.trigger_id
                )
            )
            return {"task": task.get_name()}
        return await async_scrape(
            sr.pages, sr.pre_configs, sr.detailed, sr.target, sr.trigger_id
        )

    @app.post("/scrape_preview/")
    async def scrape_preview(spr: ScraperPreviewRequest):
        if spr.is_async:
            task = asyncio.create_task(async_scrape_preview(spr.page, spr.target))
            return {"task": task.get_name()}
        return await async_scrape_preview(spr.page, spr.target)

    @app.post("/scrape_stop/")
    async def scrape_stop(ss: ScraperStopper):
        Process.add(ss.trigger_id)
        return {"message": f"Successfully added {ss.trigger_id}"}

    @app.get("/jaseci_actions_spec/")
    def action_list():
        return {
            "wbs.setup": [],
            "wbs.scrape": [
                "pages",
                "pre_configs",
                "detailed",
                "target",
                "trigger_id",
                "is_async",
            ],
            "wbs.scrape_preview": ["page", "target", "is_async"],
            "wbs.scrape_stop": ["trigger_id"],
        }

else:

    @jaseci_action(act_group=["wbs"])
    def setup():
        pass

    @jaseci_action(act_group=["wbs"])
    def scrape(
        pages: list,
        pre_configs: list = [],
        detailed: bool = False,
        target: str = None,
        trigger_id: str = None,
    ):
        return sync_scrape(pages, pre_configs, detailed, target, trigger_id)

    @jaseci_action(act_group=["wbs"])
    def scrape_preview(page: dict, target: str = None):
        return sync_scrape_preview(page, target)

    @jaseci_action(act_group=["wbs"])
    def scrape_stop(trigger_id):
        Process.add(trigger_id)
        return {"message": f"Successfully added {trigger_id}"}
