"""
Webhook API
"""
from jaseci.api.interface import Interface
from jaseci.svc.meta import MetaService
from jaseci.actor.walker import Walker
from jaseci.graph.node import Node
from jaseci.actor.sentinel import Sentinel
from jaseci.utils.id_list import IdList
from fastapi import HTTPException


class WebhookApi:
    """
    Webhook API
    """

    @Interface.public_api(url_args=["type"], allowed_methods=["post"])
    def webhook(self, type: str, _req_ctx: dict = {}):
        """Handle all different webhook logic"""
        print(_req_ctx)
        if type == "stripe":
            print("asd")

        else:
            raise HTTPException(
                status_code=404, detail=str(type + " webhook is not yet supported")
            )
