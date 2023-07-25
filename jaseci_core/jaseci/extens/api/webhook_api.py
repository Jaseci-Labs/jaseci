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
    def webhook(self, provider: str, _req_ctx: dict = {}):
        """Handle webhook logic"""
        req_body = _req_ctx["body"]

        if provider == "stripe":
            stripe_service = JsOrc.svc("stripe", StripeService)
            stripe = stripe_service.poke(_stripe)

            # to be updated
            stripe_service.get_event(
                self._h.get_file_handler(_req_ctx["raw"]).to_bytes(),
                _req_ctx["headers"],
            )

            payload_obj = req_body.get("data").get("object")
            payload_meta = payload_obj.get("metadata")

            customer_id = payload_obj.get("customer")
            customer_meta = (
                stripe.Customer.retrieve(id=customer_id).get("metadata")
                if customer_id
                else {}
            )

            master_id = payload_meta.get("master") or customer_meta.get("master")
            master = self._h.get_obj(master_id, master_id)

            node_id = payload_meta.get("node") or customer_meta.get("node")
            if not node_id:
                node_id = master.active_gph_id
            node = self._h.get_obj(master_id, node_id)

            sentinel_id = (
                payload_meta.get("sentinel")
                or customer_meta.get("sentinel")
                or master.active_snt_id
                or self._h.get_glob("GLOB_SENTINEL")
            )
            sentinel = self._h.get_obj(
                master_id,
                self._h.get_glob("GLOB_SENTINEL")
                if sentinel_id == "global"
                else sentinel_id,
            )

            payload = {"event": req_body}
            self.seek_committer(master)

            wlk = stripe_service.get_walker(req_body["type"])

            return master.walker_run(
                name=wlk, nd=node, ctx=payload, _req_ctx=_req_ctx, snt=sentinel
            )
        else:
            raise HTTPException(
                status_code=400, detail=str(provider + " webhook is not yet supported")
            )
