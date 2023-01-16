"""Built in actions for Jaseci"""
import stripe
from datetime import datetime
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def create_product(api_key: str, name: str, description: str, metadata: dict = {}):
    """create product"""
    return stripe.Product.create(
        api_key=api_key, name=name, description=description, metadata=metadata
    )


@jaseci_action()
def create_product_price(
    api_key: str,
    productId: str,
    amount: int,
    currency: str,
    interval: str,
    metadata: dict = {},
):
    """modify product price"""

    return stripe.Price.create(
        api_key=api_key,
        product=productId,
        unit_amount=amount,
        currency=currency,
        recurring={"interval": interval},
        metadata=metadata,
    )


@jaseci_action()
def product_list(api_key: str, detailed: bool):
    """retrieve all producs"""

    return stripe.Product.list(api_key=api_key, **{"active": True} if detailed else {})


@jaseci_action()
def create_customer(
    api_key: str,
    email: str,
    name: str,
    address: dict = {},
    metadata: dict = {},
):
    """create customer"""

    return (
        MetaService()
        .get_service("stripe")
        .poke(STRIPE_ERR_MSG)
        .Customer.create(
            email=email,
            name=name,
            address=address,
            metadata=metadata,
        )
    )


@jaseci_action()
def get_customer(api_key: str, customer_id: str):
    """retrieve customer information"""

    return stripe.Customer.retrieve(api_key=api_key, id=customer_id)


@jaseci_action()
def attach_payment_method(api_key: str, payment_method_id: str, customer_id: str):
    """attach payment method to customer"""

    paymentMethods = get_payment_methods(api_key, customer_id)

    paymentMethod = stripe.PaymentMethod.attach(
        api_key=api_key, payment_method=payment_method_id, customer=customer_id
    )

    is_default = True
    if paymentMethods.get("data"):
        update_default_payment_method(api_key, customer_id, payment_method_id)
        is_default = False

    paymentMethod.is_default = is_default

    return paymentMethod


@jaseci_action()
def delete_payment_method(api_key: str, payment_method_id: str):
    """detach payment method from customer"""

    return stripe.PaymentMethod.detach(
        api_key=api_key, payment_method=payment_method_id
    )


@jaseci_action()
def get_payment_methods(api_key: str, customer_id: str):
    """get customer list of payment methods"""

    return stripe.PaymentMethod.list(
        api_key=api_key,
        customer=customer_id,
        type="card",
    )


@jaseci_action()
def update_default_payment_method(
    api_key: str, customer_id: str, payment_method_id: str
):
    """update default payment method of customer"""

    return (
        MetaService()
        .get_service("stripe")
        .poke(STRIPE_ERR_MSG)
        .Customer.modify(
            sid=customer_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    )


@jaseci_action()
def create_invoice(api_key: str, customer_id: str, metadata: dict = {}):
    """create customer invoice"""

    return stripe.Invoice.create(
        api_key=api_key, customer=customer_id, metadata=metadata
    )


@jaseci_action()
def get_invoice_list(
    api_key: str,
    customer_id: str,
    subscription_id: str,
    starting_after: str = "",
    limit: int = 10,
):
    """retrieve customer list of invoices"""

    return stripe.Invoice.list(
        api_key=api_key,
        customer=customer_id,
        limit=limit,
        subscription=subscription_id,
        **{"starting_after": starting_after} if starting_after else {}
    )


@jaseci_action()
def get_payment_intents(
    api_key: str, customer_id: str, starting_after: str = "", limit: int = 10
):
    """get customer payment intents"""

    return stripe.PaymentIntent.list(
        api_key=api_key,
        customer=customer_id,
        limit=limit,
        **{"starting_after": starting_after} if starting_after else {}
    )


@jaseci_action()
def create_payment_intents(
    api_key: str,
    customer_id: str,
    amount: int,
    currency: str,
    payment_method_types: str = "card",
    metadata: dict = {},
):
    """Create customer payment"""

    return stripe.PaymentIntent.create(
        api_key=api_key,
        customer=customer_id,
        amount=amount,
        currency=currency,
        payment_method_types=[payment_method_types],
        metadata=metadata,
    )


@jaseci_action()
def get_customer_subscription(api_key: str, customer_id: str):
    """retrieve customer subcription list"""

    subscription = stripe.Subscription.list(api_key=api_key, customer=customer_id)

    if not subscription.data:
        return {"status": "inactive", "message": "Customer has no subscription"}

    return subscription


@jaseci_action()
def create_payment_method(
    api_key: str, card_type: str, card: dict, metadata: dict = {}
):
    """create payment method"""

    return stripe.PaymentMethod.create(
        api_key=api_key, type=card_type, card=card, metadata=metadata
    )


@jaseci_action()
def create_trial_subscription(
    api_key: str,
    payment_method_id: str,
    customer_id: str,
    items: list,
    trial_period_days: int = 14,
    expand: list = [],
    metadata: dict = {},
):
    """create customer trial subscription"""

    # attach payment method to customer
    attach_payment_method(api_key, payment_method_id, customer_id)

    # set card to default payment method
    update_default_payment_method(api_key, customer_id, payment_method_id)

    return stripe.Subscription.create(
        api_key=api_key,
        customer=customer_id,
        items=items,
        trial_period_days=trial_period_days,
        expand=expand,
        metadata=metadata,
    )


@jaseci_action()
def create_subscription(
    api_key: str,
    payment_method_id: str,
    items: list,
    customer_id: str,
    metadata: dict = {},
):
    """create customer subscription"""

    # attach payment method to customer
    attach_payment_method(api_key, payment_method_id, customer_id)

    # set card to default payment method
    update_default_payment_method(api_key, customer_id, payment_method_id)

    return stripe.Subscription.create(
        api_key=api_key, customer=customer_id, items=items, metadata=metadata
    )


@jaseci_action()
def cancel_subscription(subscription_id: str):
    """cancel customer subscription"""

    return stripe.Subscription.delete(api_key=api_key, sid=subscription_id)


@jaseci_action()
def get_subscription(api_key: str, subscription_id: str):
    """retrieve customer subcription details"""

    return stripe.Subscription.retrieve(api_key=api_key, id=subscription_id)


@jaseci_action()
def update_subscription(
    api_key: str,
    subscription_id: str,
    subscription_item_id: str,
    price_id: str,
    metadata: dict = {},
):
    """update subcription details"""

    return stripe.Subscription.modify(
        api_key=api_key,
        sid=subscription_id,
        cancel_at_period_end=False,
        items=[
            {
                "id": subscription_item_id,
                "price": price_id,
            },
        ],
        metadata=metadata,
    )


@jaseci_action()
def get_invoice(api_key: str, invoice_id: str):
    """get invoice information"""

    return stripe.Invoice.retrieve(api_key=api_key, id=invoice_id)


@jaseci_action()
def create_usage_report(api_key: str, subscription_item_id: str, quantity: int):
    """Create usage record"""

    return stripe.SubscriptionItem.create_usage_record(
        api_key=api_key,
        id=subscription_item_id,
        quantity=quantity,
        timestamp=datetime.now(),
    )
