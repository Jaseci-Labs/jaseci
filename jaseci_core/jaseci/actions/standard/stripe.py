"""Built in actions for Jaseci"""
import stripe as s

from jaseci.svc import MetaService
from datetime import datetime
from jaseci.actions.live_actions import jaseci_action


def stripe() -> s:
    return MetaService().get_service("stripe").poke()


@jaseci_action()
def create_product(name: str, description: str, **kwargs):
    """create product"""

    return stripe().Product.create(name=name, description=description, **kwargs)


@jaseci_action()
def create_product_price(
    productId: str,
    amount: int,
    currency: str,
    recurring: dict = {},
    **kwargs,
):
    """modify product price"""

    return stripe().Price.create(
        product=productId,
        unit_amount=amount,
        currency=currency,
        **recurring if recurring else {} ** kwargs,
    )


@jaseci_action()
def product_list(detailed: bool, **kwargs):
    """retrieve all producs"""

    return stripe().Product.list(**{"active": True} if detailed else {}, **kwargs)


@jaseci_action()
def create_customer(
    email: str,
    name: str,
    address: dict = {},
    **kwargs,
):
    """create customer"""

    return stripe().Customer.create(email=email, name=name, address=address, **kwargs)


@jaseci_action()
def get_customer(customer_id: str, **kwargs):
    """retrieve customer information"""

    return stripe().Customer.retrieve(id=customer_id, **kwargs)


@jaseci_action()
def attach_payment_method(payment_method_id: str, customer_id: str, **kwargs):
    """attach payment method to customer"""

    paymentMethods = get_payment_methods(customer_id)

    paymentMethod = stripe().PaymentMethod.attach(
        payment_method=payment_method_id, customer=customer_id, **kwargs
    )

    is_default = True
    if paymentMethods.get("data"):
        update_default_payment_method(customer_id, payment_method_id)
        is_default = False

    paymentMethod.is_default = is_default

    return paymentMethod


@jaseci_action()
def detach_payment_method(payment_method_id: str, **kwargs):
    """detach payment method from customer"""

    return stripe().PaymentMethod.detach(payment_method=payment_method_id, **kwargs)


@jaseci_action()
def get_payment_methods(customer_id: str, **kwargs):
    """get customer list of payment methods"""

    return stripe().PaymentMethod.list(customer=customer_id, type="card", **kwargs)


@jaseci_action()
def update_default_payment_method(customer_id: str, payment_method_id: str, **kwargs):
    """update default payment method of customer"""

    return stripe().Customer.modify(
        sid=customer_id,
        invoice_settings={"default_payment_method": payment_method_id},
        **kwargs,
    )


@jaseci_action()
def create_invoice(customer_id: str, **kwargs):
    """create customer invoice"""

    return stripe().Invoice.create(customer=customer_id, **kwargs)


@jaseci_action()
def get_invoice_list(
    customer_id: str,
    subscription_id: str,
    starting_after: str = "",
    limit: int = 10,
    **kwargs,
):
    """retrieve customer list of invoices"""

    return stripe().Invoice.list(
        customer=customer_id,
        limit=limit,
        subscription=subscription_id,
        **{"starting_after": starting_after} if starting_after else {},
        **kwargs,
    )


@jaseci_action()
def get_payment_intents(
    customer_id: str, starting_after: str = "", limit: int = 10, **kwargs
):
    """get customer payment intents"""

    return stripe().PaymentIntent.list(
        customer=customer_id,
        limit=limit,
        **{"starting_after": starting_after} if starting_after else {},
        **kwargs,
    )


@jaseci_action()
def create_payment_intents(
    customer_id: str,
    amount: int,
    currency: str,
    payment_method_types: list = ["card"],
    **kwargs,
):
    """Create customer payment"""

    return stripe().PaymentIntent.create(
        customer=customer_id,
        amount=amount,
        currency=currency,
        payment_method_types=payment_method_types,
        **kwargs,
    )


@jaseci_action()
def get_customer_subscription(customer_id: str, **kwargs):
    """retrieve customer subcription list"""

    return stripe().Subscription.list(customer=customer_id, **kwargs)


@jaseci_action()
def create_payment_method(card_type: str, card: dict, billing_details: dict, **kwargs):
    """create payment method"""

    return stripe().PaymentMethod.create(
        type=card_type, card=card, billing_details=billing_details, **kwargs
    )


@jaseci_action()
def create_trial_subscription(
    customer_id: str,
    items: list,
    payment_method_id: str,
    trial_period_days: int = 14,
    **kwargs,
):
    """create customer trial subscription"""

    if payment_method_id:
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id)

    return stripe().Subscription.create(
        customer=customer_id,
        items=items,
        trial_period_days=trial_period_days,
        **kwargs,
    )


@jaseci_action()
def create_subscription(
    customer_id: str,
    items: list,
    payment_method_id: str,
    **kwargs,
):
    """create customer subscription"""

    if payment_method_id:
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id)

    return stripe().Subscription.create(customer=customer_id, items=items, **kwargs)


@jaseci_action()
def cancel_subscription(subscription_id: str, **kwargs):
    """cancel customer subscription"""

    return stripe().Subscription.delete(sid=subscription_id, **kwargs)


@jaseci_action()
def get_subscription(subscription_id: str, **kwargs):
    """retrieve customer subcription details"""

    return stripe().Subscription.retrieve(id=subscription_id, **kwargs)


@jaseci_action()
def update_subscription_item(
    subscription_id: str, subscription_item_id: str, price_id: str, **kwargs
):
    """update subcription details"""

    return stripe().Subscription.modify(
        sid=subscription_id,
        cancel_at_period_end=False,
        items=[
            {
                "id": subscription_item_id,
                "price": price_id,
            },
        ],
        **kwargs,
    )


@jaseci_action()
def get_invoice(invoice_id: str, **kwargs):
    """get invoice information"""

    return stripe().Invoice.retrieve(id=invoice_id, **kwargs)


@jaseci_action()
def create_usage_report(subscription_item_id: str, quantity: int, **kwargs):
    """Create usage record"""

    return stripe().SubscriptionItem.create_usage_record(
        id=subscription_item_id, quantity=quantity, timestamp=datetime.now(), **kwargs
    )


@jaseci_action()
def create_checkout_session(
    success_url: str, cancel_url: str, line_items: list, mode: str, **kwargs
):
    return stripe().checkout.Session.create(
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=line_items,
        mode=mode,
        **kwargs,
    )


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
