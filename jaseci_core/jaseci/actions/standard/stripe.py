"""Built in actions for Jaseci"""
import json
import stripe
from datetime import datetime
from jaseci.actions.live_actions import jaseci_action

stripe_test_key = '"sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"'


def set_api_key(meta):
    """set stripe api_key"""
    stripe.api_key = json.loads(meta["h"].resolve_glob("STRIPE_KEY", stripe_test_key))


@jaseci_action()
def create_product(name: str, description: str, meta):
    """create product"""
    set_api_key(meta)

    try:
        return stripe.Product.create(name=name, description=description)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_product_price(
    productId: str, amount: int, currency: str, interval: str, meta
):
    """modify product price"""
    set_api_key(meta)

    try:
        return stripe.Price.create(
            product=productId,
            unit_amount=amount,
            currency=currency,
            recurring={"interval": interval},
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def product_list(detalied: bool, meta):
    """retrieve all producs"""
    set_api_key(meta)

    if not detalied:
        try:
            return stripe.Product.list(active=True)
        except Exception as e:
            return {"message": str(e)}
    else:  # retrieve product price
        try:
            return stripe.Product.list()
        except Exception as e:
            return {"message": str(e)}


@jaseci_action()
def create_customer(
    email: str,
    name: str,
    metadata: dict or None = None,
    address: dict or None = None,
    payment_method_id: str or None = None,
    meta: dict = {},
):
    """create customer"""
    set_api_key(meta)

    try:
        return stripe.Customer.create(
            email=email,
            name=name,
            metadata=metadata,
            address=address,
            payment_method=payment_method_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_customer(customer_id: str, meta):
    """retrieve customer information"""
    set_api_key(meta)

    try:
        return stripe.Customer.retrieve(customer_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def attach_payment_method(payment_method_id: str, customer_id: str, meta):
    """attach payment method to customer"""
    set_api_key(meta)

    try:
        paymentMethods = get_payment_methods(customer_id, meta)

        paymentMethod = stripe.PaymentMethod.attach(
            payment_method_id, customer=customer_id
        )

        if len(paymentMethods.data) == 0:
            update_default_payment_method(customer_id, payment_method_id, meta)

        paymentMethod.is_default = len(paymentMethods.data) == 0

        return paymentMethod

    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def delete_payment_method(payment_method_id: str, meta):
    """detach payment method from customer"""
    set_api_key(meta)

    try:
        return stripe.PaymentMethod.detach(payment_method_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_payment_methods(customer_id: str, meta):
    """get customer list of payment methods"""
    set_api_key(meta)

    try:
        return stripe.PaymentMethod.list(
            customer=customer_id,
            type="card",
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def update_default_payment_method(customer_id: str, payment_method_id: str, meta):
    """update default payment method of customer"""
    set_api_key(meta)

    try:
        return stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_invoice(customer_id: str, meta):
    """create customer invoice"""
    set_api_key(meta)

    try:
        return stripe.Invoice.create(customer=customer_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_invoice_list(
    customer_id: str,
    subscription_id: str,
    starting_after: str = "",
    limit: int = 10,
    meta: dict = {},
):
    """retrieve customer list of invoices"""
    set_api_key(meta)

    try:
        if starting_after != "":
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit,
                starting_after=starting_after,
                subscription=subscription_id,
            )
        else:
            invoices = stripe.Invoice.list(
                customer=customer_id, limit=limit, subscription=subscription_id
            )
        return invoices
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_payment_intents(
    customer_id: str, starting_after: str = "", limit: int = 10, meta: dict = {}
):
    """get customer payment intents"""
    set_api_key(meta)

    try:
        if starting_after != "":
            payment_intents = stripe.PaymentIntent.list(
                customer=customer_id,
                limit=limit,
                starting_after=starting_after,
            )
        else:
            payment_intents = stripe.PaymentIntent.list(
                customer=customer_id, limit=limit
            )
        return payment_intents
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_payment_intents(
    customer_id: str,
    amount: int,
    currency: str,
    payment_method_types: str = "card",
    meta=dict,
):
    """Create customer payment"""
    set_api_key(meta)

    try:
        return stripe.PaymentIntent.create(
            customer=customer_id,
            amount=amount,
            currency=currency,
            payment_method_types=[payment_method_types],
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_customer_subscription(customer_id: str, meta):
    """retrieve customer subcription list"""
    set_api_key(meta)

    try:
        subscription = stripe.Subscription.list(customer=customer_id)

        if len(subscription.data) == 0:
            return {"status": "inactive", "message": "Customer has no subscription"}

        return subscription
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_payment_method(card_type: str, card: dict, meta):
    """create payment method"""
    set_api_key(meta)

    try:
        return stripe.PaymentMethod.create(type=card_type, card=card)

    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_trial_subscription(
    payment_method_id: str,
    price_id: str,
    customer_id: str,
    trial_period_days: int = 14,
    meta: dict = {},
):
    """create customer trial subscription"""
    set_api_key(meta)

    try:
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id, meta)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id, meta)

        return stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": price_id},
            ],
            trial_period_days=trial_period_days,
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_subscription(payment_method_id: str, price_id: str, customer_id: str, meta):
    """create customer subscription"""
    set_api_key(meta)

    try:
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id, meta)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id, meta)

        return stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": price_id},
            ],
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def cancel_subscription(subscription_id: str, meta):
    """cancel customer subscription"""
    set_api_key(meta)

    try:
        return stripe.Subscription.delete(subscription_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_subscription(subscription_id: str, meta):
    """retrieve customer subcription details"""
    set_api_key(meta)

    try:
        return stripe.Subscription.retrieve(subscription_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def update_subscription(
    subscription_id: str, subscription_item_id: str, price_id: str, meta
):
    """update subcription details"""
    set_api_key(meta)

    try:
        return stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False,
            items=[
                {
                    "id": subscription_item_id,
                    "price": price_id,
                },
            ],
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_invoice(invoice_id: str, meta):
    """get invoice information"""
    set_api_key(meta)

    try:
        return stripe.Invoice.retrieve(invoice_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_usage_report(subscription_item_id: str, quantity: int, meta):
    """Create usage record"""
    set_api_key(meta)

    try:
        return stripe.SubscriptionItem.create_usage_record(
            subscription_item_id, quantity=quantity, timestamp=datetime.now()
        )
    except Exception as e:
        return {"message": str(e)}
