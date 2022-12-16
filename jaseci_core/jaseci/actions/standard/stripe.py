"""Built in actions for Jaseci"""
import stripe
from datetime import datetime
from jaseci.actions.live_actions import jaseci_action

DEFAULT_API_KEY = "sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"


def set_api_key(meta):
    api_key = meta["h"].get_glob("STRIPE_API_KEY")

    if not api_key:
        raise Exception(
            {
                "message": "Stripe is not yet configured. Please set a valid stripe key.",
                "success": False,
            }
        )

    stripe.api_key = api_key


@jaseci_action()
def create_product(
    name: str, description: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """create product"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Product.create(name=name, description=description)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_product_price(
    productId: str,
    amount: int,
    currency: str,
    interval: str,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """modify product price"""

    if mock_api:
        return {"success": True}

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
def product_list(
    detailed: bool, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """retrieve all producs"""

    if mock_api:
        return {"success": True}

    if not detailed:
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
    metadata: dict or None,
    address: dict or None,
    payment_method_id: str or None,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """create customer"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Customer.create(
            api_key=api_key,
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
def get_customer(
    customer_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """retrieve customer information"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Customer.retrieve(customer_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def attach_payment_method(
    payment_method_id: str,
    customer_id: str,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """attach payment method to customer"""

    if mock_api:
        return {"success": True}

    try:
        paymentMethods = get_payment_methods(customer_id)

        paymentMethod = stripe.PaymentMethod.attach(
            payment_method_id, customer=customer_id
        )

        if len(paymentMethods.data) == 0:
            update_default_payment_method(customer_id, payment_method_id)

        paymentMethod.is_default = len(paymentMethods.data) == 0

        return paymentMethod

    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def delete_payment_method(
    payment_method_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """detach payment method from customer"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.PaymentMethod.detach(payment_method_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_payment_methods(
    customer_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """get customer list of payment methods"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.PaymentMethod.list(
            customer=customer_id,
            type="card",
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def update_default_payment_method(
    customer_id: str,
    payment_method_id: str,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """update default payment method of customer"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_invoice(
    customer_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """create customer invoice"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Invoice.create(api_key=api_key, customer=customer_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_invoice_list(
    customer_id: str,
    subscription_id: str,
    api_key: str = DEFAULT_API_KEY,
    starting_after: str = "",
    limit: int = 10,
    mock_api: bool = False,
):
    """retrieve customer list of invoices"""

    if mock_api:
        return {"success": True}

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
    customer_id: str,
    api_key: str = DEFAULT_API_KEY,
    starting_after: str = "",
    limit: int = 10,
    mock_api: bool = False,
):
    """get customer payment intents"""

    if mock_api:
        return {"success": True}

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
    api_key: str = DEFAULT_API_KEY,
    payment_method_types: str = "card",
    mock_api: bool = False,
):
    """Create customer payment"""

    if mock_api:
        return {"success": True}

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
def get_customer_subscription(
    customer_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """retrieve customer subcription list"""

    if mock_api:
        return {"success": True}

    try:
        subscription = stripe.Subscription.list(customer=customer_id)

        if len(subscription.data) == 0:
            return {"status": "inactive", "message": "Customer has no subscription"}

        return subscription
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_payment_method(
    card_type: str,
    card: dict,
    api_key: str = DEFAULT_API_KEY,
    billing_details: dict = {},
    mock_api: bool = False,
):
    """create payment method"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.PaymentMethod.create(
            type=card_type, card=card, billing_details=billing_details
        )

    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_trial_subscription(
    payment_method_id: str,
    customer_id: str,
    api_key: str = DEFAULT_API_KEY,
    items: list = [],
    trial_period_days: int = 14,
    expand: list = [],
    mock_api: bool = False,
):
    """create customer trial subscription"""

    if mock_api:
        return {"success": True}

    try:
        if payment_method_id:
            # attach payment method to customer
            attach_payment_method(payment_method_id, customer_id)

            # set card to default payment method
            update_default_payment_method(customer_id, payment_method_id)

        return stripe.Subscription.create(
            customer=customer_id,
            items=items,
            trial_period_days=trial_period_days,
            expand=expand,
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_subscription(
    payment_method_id: str,
    price_id: str,
    customer_id: str,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """create customer subscription"""

    if mock_api:
        return {"success": True}

    try:
        # attach payment method to customer
        attach_payment_method(payment_method_id, customer_id)

        # set card to default payment method
        update_default_payment_method(customer_id, payment_method_id)

        return stripe.Subscription.create(
            customer=customer_id,
            items=[
                {"price": price_id},
            ],
        )
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def cancel_subscription(
    subscription_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """cancel customer subscription"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Subscription.delete(subscription_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def get_subscription(
    subscription_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """retrieve customer subcription details"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Subscription.retrieve(subscription_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def update_subscription(
    subscription_id: str,
    subscription_item_id: str,
    price_id: str,
    api_key: str = DEFAULT_API_KEY,
    mock_api: bool = False,
):
    """update subcription details"""

    if mock_api:
        return {"success": True}

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
def get_invoice(
    invoice_id: str, api_key: str = DEFAULT_API_KEY, mock_api: bool = False
):
    """get invoice information"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.Invoice.retrieve(invoice_id)
    except Exception as e:
        return {"message": str(e)}


@jaseci_action()
def create_usage_report(
    subscription_item_id: str,
    quantity: int,
    api_key: str = DEFAULT_API_KEY,
    action: str = "increment",
    mock_api: bool = False,
):
    """Create usage record"""

    if mock_api:
        return {"success": True}

    try:
        return stripe.SubscriptionItem.create_usage_record(
            subscription_item_id,
            quantity=quantity,
            timestamp=datetime.now(),
            action=action,
        )
    except Exception as e:
        return {"message": str(e)}
