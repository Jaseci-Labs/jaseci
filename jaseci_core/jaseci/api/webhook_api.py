"""
Webhook API
"""
from jaseci.api.interface import Interface
from fastapi import HTTPException
from json import loads
from jaseci.svc import MetaService
from jaseci.svc.stripe import STRIPE_ERR_MSG


class WebhookApi:
    """
    Webhook API
    """

    @Interface.public_api(url_args=["type"], allowed_methods=["post"])
    def webhook(self, type: str, _req_ctx: dict = {}):
        """Handle webhook logic"""
        req_body = _req_ctx["body"]

        if type == "stripe":
            stripe = MetaService().get_service("stripe")

            payload_obj = req_body.get("data").get("object")
            customer_id = payload_obj.get("customer")

            if customer_id:
                customer = stripe.poke(STRIPE_ERR_MSG).Customer.retrieve(id=customer_id)
                metadata = customer.get("metadata")
            else:
                metadata = payload_obj.get("metadata")

            master_id = metadata.get("master_id")
            master = self._h.get_obj(master_id, master_id)

            node_id = metadata.get("node")
            if not node_id:
                node_id = master.active_gph_id

            node = self._h.get_obj(master_id, node_id)

            # walker name that will be called
            # set in global vars
            wlk = stripe.walker

            global_snt_id = self._h.get_glob("GLOB_SENTINEL")
            global_snt = self._h.get_obj(master_id, global_snt_id)

            payload = {"event_type": req_body["type"], "stripe_payload": req_body}
            self.seek_committer(master)

            return master.walker_run(
                name=wlk, nd=node, ctx=payload, _req_ctx=_req_ctx, snt=global_snt
            )
        else:
            raise HTTPException(
                status_code=400, detail=str(type + " webhook is not yet supported")
            )
