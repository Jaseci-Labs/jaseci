import uuid
import os.path

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import JSX_STRIPE_DIR
from jaseci_serv.base.models import JaseciObject


class StripeView(APIView):

    http_method_names = ["post"]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        master = request.user.get_master()
        api_key = master._h.get_glob("STRIPE_API_KEY")

        if not api_key:
            return Response(
                {
                    "message": "Stripe is not yet configured. Please set a valid stripe key.",
                    "success": False,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:

            stripe_sentinel = master.sentinel_active_get()
            stripe_sentinel = master._h.get_obj(master._m_id, stripe_sentinel["jid"])

            stripe_webhook_arch = stripe_sentinel.arch_ids.get_obj_by_name(
                "stripe_webhook"
            )

            stripe_webhook_wlk = None
            wlk = JaseciObject.objects.filter(
                name="stripe_webhook", j_type="walker"
            ).exists()

            if stripe_webhook_arch and not wlk:
                # if theres stripe_webhook architype and not yet have stripe_webhook walker
                # run run_architype to create walker
                stripe_webhook_wlk = stripe_webhook_arch.run_architype(
                    jac_ast=stripe_webhook_arch.get_jac_ast()
                )
            else:
                stripe_webhook_wlk = JaseciObject.objects.get(
                    name="stripe_webhook", j_type="walker"
                )

                stripe_webhook_wlk = master._h.get_obj(
                    master._m_id, stripe_webhook_wlk.jid
                )

            # if theres NO stripe_webhook architype and no stripe_webhook walker, return an error response
            if not stripe_webhook_arch and not stripe_webhook_wlk:
                return Response(
                    {
                        "message": "Walker stripe_webhook not found!",
                        "success": False,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            keys = stripe_webhook_wlk.namespace_keys()["anyone"]

            master.save()
            master._h.commit()

            root_node = master.graph_active_get()["jid"].split(":")[2]

            stripe_webhook_url = f"/js_public/walker_callback/{root_node}/{str(stripe_webhook_wlk.id)}?key={keys}"

            return Response({"data": stripe_webhook_url, "success": True})
        except Exception as e:
            return Response({"message": str(e), "success": False})


class StripeWebhook:

    # @Interface.admin_api()
    # @Interface.private_api()
    def stripe_webhook(self, request):

        # this should handle the logic for the stripe webhooks
        # from STRIPE, it will have the stripe event object, and metada from user ( sentinel_id, walker_id, token, master_id )

        # TODO: use `event.metadata.sentinel_id` to select the sentinel ?????
        # TODO: use `event.metadata.walker_id` to run the walker

        # metadata = request.data.metadata
        # sentinel_id = metadata.sentinel_id
        # walker_id = metadata.walker_id

        # walker call_this_when_customer_is_created {
        #     can mail.send;
        #
        #     mail.send();
        # }

        # find and run the WALKER by `walker_id`

        # should the walker be PUBLIC WALKER?
        print("test")
