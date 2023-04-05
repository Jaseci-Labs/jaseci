"""
Webhook API
"""
from jaseci.extens.api.interface import Interface
from fastapi import HTTPException
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.stripe_svc import StripeService

import stripe as _stripe


class WebhookApi:
    """
    Webhook API
    """

    @Interface.public_api(url_args=["provider"], allowed_methods=["post"])
    def webhook(self, provider: str, _req_ctx: dict = {}, _raw_req_ctx: str = None):
        """Handle webhook logic"""
        req_body = _req_ctx["body"]

        if provider == "stripe":
            stripe_service = JsOrc.svc("stripe", StripeService)
            stripe = stripe_service.poke(_stripe)

            # to be updated
            stripe_service.get_event(_raw_req_ctx, _req_ctx["headers"])

            payload_obj = req_body.get("data").get("object")
            customer_id = payload_obj.get("customer")

            if customer_id:
                customer = stripe.Customer.retrieve(id=customer_id)
                metadata = customer.get("metadata")
            else:
                metadata = payload_obj.get("metadata")

            master_id = metadata.get("master_id")
            master = self._h.get_obj(master_id, master_id)

            node_id = metadata.get("node")
            if not node_id:
                node_id = master.active_gph_id

            node = self._h.get_obj(master_id, node_id)

            global_snt_id = self._h.get_glob("GLOB_SENTINEL")
            global_snt = self._h.get_obj(master_id, global_snt_id)

            payload = {"event": req_body}
            self.seek_committer(master)

            wlk = stripe_service.get_walker(req_body["type"])

            return master.walker_run(
                name=wlk, nd=node, ctx=payload, _req_ctx=_req_ctx, snt=global_snt
            )
        else:
            raise HTTPException(
                status_code=400, detail=str(type + " webhook is not yet supported")
            )
