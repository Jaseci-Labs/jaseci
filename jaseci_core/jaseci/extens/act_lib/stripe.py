"""Built in actions for Jaseci"""
import stripe as s

from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import logger
from jaseci.extens.svc.stripe_svc import StripeService
from jaseci.jsorc.live_actions import jaseci_action


def stripe() -> s:
    _stripe = JsOrc.svc("stripe", StripeService)
    if _stripe.is_running():
        return _stripe.app
    else:
        logger.info(
            "Stripe service is not running! Fallback to direct stripe call with required api key params."
        )
        return s


@jaseci_action()
def product_create(name: str, **kwargs):
    """create product"""

    return stripe().Product.create(name=name, **kwargs)


@jaseci_action()
def price_create(
    product: str,
    unit_amount: int,
    currency: str,
    **kwargs,
):
    """create product price"""

    return stripe().Price.create(
        product=product, unit_amount=unit_amount, currency=currency, **kwargs
    )


@jaseci_action()
def product_list(**kwargs):
    """retrieve all producs"""

    return stripe().Product.list(**kwargs)


@jaseci_action()
def customer_create(**kwargs):
    """create customer"""

    return stripe().Customer.create(**kwargs)


@jaseci_action()
def customer_modify(customer_id: str, **kwargs):
    """update customer"""

    return stripe().Customer.modify(customer_id, **kwargs)


@jaseci_action()
def customer_retrieve(customer_id: str, **kwargs):
    """retrieve customer information"""

    return stripe().Customer.retrieve(customer_id, **kwargs)


@jaseci_action()
def customer_delete(customer_id: str, **kwargs):
    """delete customer"""

    return stripe().Customer.delete(customer_id, **kwargs)


@jaseci_action()
def payment_method_attach(payment_method_id: str, customer_id: str, **kwargs):
    """retrieve customer list of invoices"""

    return stripe().PaymentMethod.attach(
        payment_method_id, customer=customer_id, **kwargs
    )


@jaseci_action()
def payment_method_detach(payment_method_id: str, **kwargs):
    """detach payment method from customer"""

    return stripe().PaymentMethod.detach(payment_method_id, **kwargs)


@jaseci_action()
def payment_method_list(**kwargs):
    """get customer list of payment methods"""

    return stripe().PaymentMethod.list(**kwargs)


@jaseci_action()
def invoice_create(**kwargs):
    """create customer invoice"""

    return stripe().Invoice.create(**kwargs)


@jaseci_action()
def invoice_list(**kwargs):
    """retrieve customer list of invoices"""

    return stripe().Invoice.list(**kwargs)


@jaseci_action()
def payment_intent_list(**kwargs):
    """get customer payment intents"""

    return stripe().PaymentIntent.list(**kwargs)


@jaseci_action()
def payment_intent_create(amount: int, currency: str, **kwargs):
    """Create customer payment"""

    return stripe().PaymentIntent.create(amount=amount, currency=currency, **kwargs)


@jaseci_action()
def subscription_create(customer: str, items: list, **kwargs):
    """create subcriptions"""

    return stripe().Subscription.create(customer=customer, items=items, **kwargs)


@jaseci_action()
def subscription_modify(subscription_id: str, **kwargs):
    """modify subcriptions"""

    return stripe().Subscription.modify(subscription_id, **kwargs)


@jaseci_action()
def subscription_list(**kwargs):
    """list all customer's subcriptions"""

    return stripe().Subscription.list(**kwargs)


@jaseci_action()
def subscription_retrieve(subscription_id: str, **kwargs):
    """retrieve customer subcription details"""

    return stripe().Subscription.retrieve(subscription_id, **kwargs)


@jaseci_action()
def payment_method_create(type: str, **kwargs):
    """create payment method"""

    return stripe().PaymentMethod.create(type=type, **kwargs)


@jaseci_action()
def subscription_delete(subscription_id: str, **kwargs):
    """cancel customer subscription"""

    return stripe().Subscription.delete(subscription_id, **kwargs)


@jaseci_action()
def invoice_retrieve(invoice_id: str, **kwargs):
    """get invoice information"""

    return stripe().Invoice.retrieve(invoice_id, **kwargs)


@jaseci_action()
def subscription_item_list_usage_record_summaries(subscription_item_id: str, **kwargs):
    """Create usage record"""

    return stripe().SubscriptionItem.list_usage_record_summaries(
        subscription_item_id, **kwargs
    )


@jaseci_action()
def subscription_item_create_usage_record(
    subscription_item_id: str, quantity: int, **kwargs
):
    """Create usage record"""

    return stripe().SubscriptionItem.create_usage_record(
        subscription_item_id, quantity=quantity, timestamp="now", **kwargs
    )


@jaseci_action()
def checkout_session_create(success_url: str, mode: str, **kwargs):
    return stripe().checkout.Session.create(
        success_url=success_url,
        mode=mode,
        **kwargs,
    )


@jaseci_action()
def billing_portal_session_create(customer: str, **kwargs):
    return stripe().billing_portal.Session.create(
        customer=customer,
        **kwargs,
    )


#################################################
#            WITH PRE CUSTOM PROCESS            #
#################################################


@jaseci_action()
def update_default_payment_method(customer_id: str, payment_method_id: str, **kwargs):
    """update default payment method of customer"""

    return customer_modify(
        customer_id,
        invoice_settings={"default_payment_method": payment_method_id},
        **kwargs,
    )


@jaseci_action()
def attach_payment_method(payment_method_id: str, customer_id: str, **kwargs):
    """attach payment method to customer"""

    paymentMethods = payment_method_list(customer=customer_id)

    paymentMethod = payment_method_attach(payment_method_id, customer_id, **kwargs)

    is_default = True
    if paymentMethods.get("data"):
        update_default_payment_method(customer_id, payment_method_id)
        is_default = False

    paymentMethod["is_default"] = is_default

    return paymentMethod


@jaseci_action()
def create_trial_subscription(
    customer_id: str,
    items: list,
    payment_method_id: str = "",
    trial_period_days: int = 14,
    **kwargs,
):
    """create customer trial subscription"""

    if payment_method_id != "":
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id)

    return subscription_create(
        customer_id,
        items,
        trial_period_days=trial_period_days,
        **kwargs,
    )


@jaseci_action()
def create_subscription(
    customer_id: str,
    items: list,
    payment_method_id: str = "",
    **kwargs,
):
    """create customer subscription"""

    if payment_method_id != "":
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id)

    return subscription_create(customer_id, items, **kwargs)


@jaseci_action()
def update_subscription_item(
    subscription_id: str, subscription_item_id: str, price_id: str, **kwargs
):
    """update subcription details"""

    return subscription_modify(
        subscription_id,
        cancel_at_period_end=False,
        items=[
            {
                "id": subscription_item_id,
                "price": price_id,
            },
        ],
        **kwargs,
    )


#################################################
#            EXECUTE CUSTOM PROCESS             #
#################################################


@jaseci_action()
def exec(api: str, *args, **kwargs):
    apis = api.split(".")

    if not apis:
        raise Exception("API is required!")

    mod = stripe()

    for api in apis:
        mod = getattr(mod, api, None)
        if not mod:
            raise Exception("Not a valid stripe API!")

    return mod(*args, **kwargs)
