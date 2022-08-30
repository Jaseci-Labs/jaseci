from base64 import encode
import json
from re import A
from jaseci.actor.walker import walker
from jaseci.api.graph_api import graph_api
from jaseci.jac.ir.jac_code import jac_code
from jaseci.jac.ir.ast import ast
from jaseci.utils.stripe_hook import stripe_hook
import stripe
import requests
import uuid
from jaseci.actor.sentinel import sentinel
from jaseci.api.interface import interface
from jaseci.api.sentinel_api import sentinel_api
from jaseci.api.walker_api import walker_api

stripe_test_key = "sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"


class stripe_api:
    """
    Stripe APIs
    Set of APIs to expose jaseci stripe management
    """

    def __init__(self):
        stripe.api_key = self._h.resolve_glob("STRIPE_KEY", stripe_test_key)

    @interface.admin_api()
    def get_config(self, name: str):
        """get stripe config by name"""
        return stripe_hook.get_obj(name)

    @interface.admin_api()
    def set_config(self, name: str, value: str):
        """set stripe config"""
        return stripe_hook.save_obj(name, value)

    @interface.admin_api()
    def stripe_init(self):
        """initialize stripe"""

        def resolve_semicolon(str: str):
            return str if str.endswith(";") else str + ";"

        stripe_walker = """walker stripe_webhook: anyone {
                root {
                    req_ctx = global.info['request_context'];
                    req_data = req_ctx['body']['data'];
                    event_type = req_ctx['body']['type'];

                    if( event_type == 'payment_intent.create') {
                        %s
                        disengage;
                    } elif ( event_type == 'payment_intent.succeeded') {
                        %s
                        disengage;
                    } elif ( event_type == 'payment_intent.canceled') {
                        %s
                        disengage;
                    } elif ( event_type == 'payment_intent.payment_failed') {
                        %s
                        disengage;
                    } elif ( event_type == 'payment_intent.requires_action') {
                        %s
                        disengage;
                    } elif ( event_type == 'subscription_schedule.canceled') {
                        %s
                        disengage;
                    } elif ( event_type == 'subscription_schedule.expiring') {
                        %s
                        disengage;
                    } elif ( event_type == 'subscription_schedule.updated') {
                        %s
                        disengage;
                    } elif ( event_type == 'invoice.created') {
                        %s
                        disengage;
                    } elif ( event_type == 'invoice.finalized') {
                        %s
                        disengage;
                    } elif ( event_type == 'invoice.paid') {
                        %s
                        disengage;
                    } elif ( event_type == 'invoice.payment_succeeded') {
                        %s
                        disengage;
                    } elif ( event_type == 'customer.subscription.created') {
                        %s
                        disengage;
                    } elif ( event_type == 'customer.subscription.deleted') {
                        %s
                        disengage;
                    } else {
                        report:status = 403;
                        report:custom = {'error': 'Forbidden Request!', 'event': event_type};
                        disengage;
                    }
                }
            }
        """ % (
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_CREATE")),
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_SUCCEEDED")),
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_CANCELED")),
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_PAYMENT_FAILED")),
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_REQUIRES_ACTION")),
            resolve_semicolon(stripe_hook.get_obj("SUBSCRIPTION_SCHEDULE_CANCELED")),
            resolve_semicolon(stripe_hook.get_obj("SUBSCRIPTION_SCHEDULE_EXPIRING")),
            resolve_semicolon(stripe_hook.get_obj("SUBSCRIPTION_SCHEDULE_UPDATED")),
            resolve_semicolon(stripe_hook.get_obj("INVOICE_CREATED")),
            resolve_semicolon(stripe_hook.get_obj("INVOICE_FINALIZED")),
            resolve_semicolon(stripe_hook.get_obj("INVOICE_PAID")),
            resolve_semicolon(stripe_hook.get_obj("INVOICE_PAYMENT_SUCCEEDED")),
            resolve_semicolon(stripe_hook.get_obj("CUSTOMER_SUBSCRIPTION_CREATED")),
            resolve_semicolon(stripe_hook.get_obj("PAYMENT_INTENT_SUCCEEDED")),
        )

        # return stripe_walker

        active_snt_id = sentinel_api.sentinel_active_get(self)["jid"]
        active_snt = self._h.get_obj(self._m_id, uuid.UUID(active_snt_id))

        wlk = active_snt.walker_ids.get_obj_by_name("stripe_webhook")
        keys = None

        # return wlk

        if wlk:
            # TODO - REFACTOR -> just update the code of the WALKER, but dont create new instance of walker
            # tree = active_snt.parse_jac(stripe_walker, "./", start_rule="walker")
            # # wlk.apply_ir(stripe_walker)
            # # active_snt.parse_jac(stripe_walker, start_rule="walker")
            # # wlk.apply_ir(stripe_walker)
            # wlk.save()
            # # wlk = walker_api.walker_get(self, wlk=wlk)

            walker_api.walker_set(self, wlk=wlk, code=stripe_walker)
            # wlk = wlk.serialize()
            wlk = self._h.get_obj(self._m_id, uuid.UUID(wlk.jid))
        else:
            wlk = walker_api.walker_register(self, active_snt, stripe_walker)
            wlk = self._h.get_obj(self._m_id, uuid.UUID(wlk["jid"]))

        # wlk = walker_api.walker_register(self, active_snt, stripe_walker)
        # return wlk

        keys = walker_api.walker_get(self, wlk=wlk, mode="keys")["anyone"]

        root_node = graph_api.graph_active_get(self)["jid"].split(":")[2]

        stripe_webhook_url = (
            f"/js_public/walker_callback/{root_node}/{str(wlk.id)}?key={keys}"
        )

        return {"stripe_webhook_url": stripe_webhook_url}
