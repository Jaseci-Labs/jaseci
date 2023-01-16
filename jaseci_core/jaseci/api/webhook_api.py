"""
Webhook API
"""
from jaseci.api.interface import Interface
from fastapi import HTTPException
from json import loads


class WebhookApi:
    """
    Webhook API
    """

    @Interface.public_api(url_args=["type"], allowed_methods=["post"])
    def webhook(self, type: str, _req_ctx: dict = {}):
        """Handle webhook logic"""
        req_body = _req_ctx["body"]

        if type == "stripe":

            metadata = req_body["data"]["object"]["metadata"]

            if not metadata:
                return req_body

            walker_name = metadata.get("walker_name")

            if walker_name:
                master_id = metadata["master_id"]
                sentinel_id = metadata["sentinel_id"]

                if not master_id:
                    raise HTTPException(
                        status_code=400,
                        detail=str("Cannot call walker without master id supplied"),
                    )

                if not sentinel_id:
                    raise HTTPException(
                        status_code=400,
                        detail=str("Cannot call walker without sentinel id supplied"),
                    )

                snt = self._h.get_obj(master_id, sentinel_id)
                master = self._h.get_obj(master_id, master_id)

                gph = self._h.get_obj(master_id, master.active_gph_id)

                if metadata.get("walker_nd"):
                    gph = self._h.get_obj(master_id, metadata.get("walker_nd"))

                ctx = {"stripe_data": req_body}
                ctx.update(loads(metadata.get("walker_ctx")))

                return master.walker_run(
                    name=walker_name,
                    nd=gph,
                    snt=snt,
                    ctx=ctx,
                )

        else:
            raise HTTPException(
                status_code=400, detail=str(type + " webhook is not yet supported")
            )
