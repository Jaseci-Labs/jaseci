"""Built in actions for Jaseci"""
from jaseci.api.stripe_api import stripe_api
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def create_customer(
    email: str,
    name: str,
    metadata: dict or None = None,
    address: dict or None = None,
    payment_method_id: str or None = None,
):
    """Create customer stripe account"""

    return stripe_api.stripe_customer_create(
        email,
        name,
        metadata,
        address,
        payment_method_id,
    )


@jaseci_action()
def get_customer(customer_id):
    """Get customer stripe account"""
    if customer_id == "":
        return {"message": "Customer Id is required."}

    return stripe_api.stripe_customer_get(customer_id)


@jaseci_action()
def create_payment_method(card_type: str, card: dict):
    """Create payment method"""

    return stripe_api.stripe_payment_method_create(card_type, card)


@jaseci_action()
def attach_payment_method(payment_method_id: str, customer_id: str):
    """Create customer stripe account"""
    if not payment_method_id:
        return {"message": "Payment method is required"}

    if not customer_id:
        return {"message": "Customer id is required"}

    return stripe_api.stripe_customer_payment_add(
        stripe_api, payment_method_id, customer_id
    )


@jaseci_action()
def get_payment_method_list(customer_id: str):
    """Get payment method"""

    if not customer_id:
        return {"message": "Customer id is required"}

    return stripe_api.stripe_customer_payment_list(customer_id)


@jaseci_action()
def update_default_payment_method(customer_id: str, payment_method_id: str):
    """Update default payment method"""

    if not payment_method_id:
        return {"message": "Payment method is required"}

    if not customer_id:
        return {"message": "Customer id is required"}

    return stripe_api.stripe_customer_default_payment_method_update(
        customer_id, payment_method_id
    )


@jaseci_action()
def create_trial_subscription(
    payment_method_id: str, price_id: str, customer_id: str, trial_period_days: int = 30
):
    """Create customer subscription"""

    if not payment_method_id:
        return {"message": "Payment method is required"}

    if not customer_id:
        return {"message": "Customer id is required"}

    if not price_id:
        return {"message": "Price id is required"}

    return stripe_api.stripe_subscription_trial_create(
        stripe_api,
        payment_method_id,
        price_id,
        customer_id,
        trial_period_days,
    )


@jaseci_action()
def create_subscription(payment_method_id: str, price_id: str, customer_id: str):
    """Create customer subscription"""

    if not payment_method_id:
        return {"message": "Payment method is required"}

    if not customer_id:
        return {"message": "Customer id is required"}

    if not price_id:
        return {"message": "Price id is required"}

    return stripe_api.stripe_subscription_create(
        stripe_api,
        payment_method_id,
        price_id,
        customer_id,
    )


@jaseci_action()
def get_subscription(subscription_id: str):
    """Get customer subscription details"""

    if not subscription_id:
        return {"message": "Subscription id is required"}

    return stripe_api.stripe_subscription_get(subscription_id)


@jaseci_action()
def cancel_subscription(subscription_id: str):
    """Cancel customer subscription"""

    if not subscription_id:
        return {"message": "Subscription id is required"}

    return stripe_api.stripe_subscription_delete(subscription_id)


@jaseci_action()
def update_subscription(subscription_id: str, subscription_item_id: str, price_id: str):
    """Update subscription item"""

    if not subscription_id:
        return {"message": "Subscription id is required"}

    if not subscription_item_id:
        return {"message": "Subscription item id is required"}

    if not price_id:
        return {"message": "Price id is required"}

    return stripe_api.stripe_subscription_update(
        subscription_id, subscription_item_id, price_id
    )


@jaseci_action()
def report_usage(subscription_item_id: str, quantity: int):
    """Create usage record"""

    if not subscription_item_id:
        return {"message": "Subscription item id is required"}

    return stripe_api.stripe_create_usage_record(subscription_item_id, quantity)


@jaseci_action()
def create_invoice(customer_id: str):
    """Create customer invoice"""

    if not customer_id:
        return {"message": "Customer id is required"}

    return stripe_api.stripe_customer_invoice_create(customer_id)


@jaseci_action()
def get_invoice(invoice_id: str):
    """Get invoice details"""

    if not invoice_id:
        return {"message": "Invoice id is required"}

    return stripe_api.stripe_invoice_get(invoice_id)


@jaseci_action(aliases=["customer_invoices"], allow_remote=True)
def get_customer_invoices(
    customer_id: str, subscription_id: str, starting_after: str = "", limit: int = 10
):
    """Get customer invoice"""

    if not customer_id:
        return {"message": "Customer id is required"}

    if not subscription_id:
        return {"message": "Subscription id is required"}

    return stripe_api.stripe_customer_invoice_list(
        customer_id, subscription_id, starting_after, limit
    )


@jaseci_action()
def get_customer_payment(customer_id: str, starting_after: str = "", limit: int = 10):
    """Get customer payment intents"""

    if not customer_id:
        return {"message": "Customer id is required"}

    return stripe_api.stripe_customer_payment_intents_get(
        customer_id, starting_after, limit
    )


@jaseci_action()
def create_customer_payment(
    amount: int, currency: str, payment_method_types: list, customer_id: str
):
    """Get customer payment intents"""

    if not customer_id:
        return {"message": "Customer id is required"}

    if not currency:
        return {"message": "Currency is required"}

    return stripe_api.stripe_customer_payment_intents_create(
        customer_id,
        amount=amount,
        currency=currency,
        payment_method_types=payment_method_types,
    )
