"""Built in actions for Jaseci"""
from jaseci.api.stripe_api import stripe_api
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def create_customer(email: str, name: str, metadata: dict = {}, address: dict or None = {}, payment_method: str or None = None):
    """Create customer stripe account"""
    customer = stripe_api.stripe_customer_create(email=email,
                name=name,
                metadata=metadata,
                address=address,
                payment_method=payment_method)
    
    return customer

@jaseci_action()
def get_customer(customer_id):
    """Get customer stripe account"""
    if( customer_id == "" ):
        return { "message": "Customer Id is required." }

    customer = stripe_api.stripe_customer_get(customer_id=customer_id)
    return customer

@jaseci_action()
def create_payment_method(card_type: str, card: dict):
    """Create payment method"""

    payment_method = stripe_api.stripe_create_payment_method(card_type=card_type, card=card)
    
    return payment_method

@jaseci_action()
def attach_payment_method(payment_method_id: str, customer_id: str):
    """Create customer stripe account"""
    if( not payment_method_id ):
        return { "message": "Payment method is required" }
    
    if( not customer_id ):
        return { "message": "Customer id is required" }

    payment_method = stripe_api.stripe_customer_payment_add(stripe_api, payment_method_id=payment_method_id, customer_id=customer_id)
    
    return payment_method

@jaseci_action()
def get_payment_method_list(customer_id: str):
    """Get payment method"""

    if( not customer_id ):
        return { "message": "Customer id is required" }

    payment_method = stripe_api.stripe_customer_payment_list_get(stripe_api, customer_id)
    
    return payment_method

@jaseci_action()
def update_default_payment_method(customer_id: str, payment_method_id: str):
    """Update default payment method"""

    if( not payment_method_id ):
        return { "message": "Payment method is required" }
    
    if( not customer_id ):
        return { "message": "Customer id is required" }

    payment_method = stripe_api.stripe_customer_default_payment_update(stripe_api, customer_id=customer_id, payment_method_id=payment_method_id)
    
    return payment_method

@jaseci_action()
def create_trial_subscription(payment_method_id: str, price_id: str, customer_id: str, trial_period_days: int = 30):
    """Create customer subscription"""

    if( not payment_method_id ):
        return { "message": "Payment method is required" }
    
    if( not customer_id ):
        return { "message": "Customer id is required" }
    
    if( not price_id ):
        return { "message": "Price id is required" }

    subscription = stripe_api.stripe_trial_subscription_create(stripe_api, payment_method_id=payment_method_id, price_id=price_id, customer_id=customer_id, trial_period_days=trial_period_days)
    
    return subscription

@jaseci_action()
def create_subscription(payment_method_id: str, price_id: str, customer_id: str):
    """Create customer subscription"""

    if( not payment_method_id ):
        return { "message": "Payment method is required" }
    
    if( not customer_id ):
        return { "message": "Customer id is required" }
    
    if( not price_id ):
        return { "message": "Price id is required" }

    subscription = stripe_api.stripe_subscription_create(stripe_api, payment_method_id=payment_method_id, price_id=price_id, customer_id=customer_id)
    
    return subscription

@jaseci_action()
def get_subscription(subscription_id: str):
    """Get customer subscription details"""

    if( not subscription_id ):
        return { "message": "Subscription id is required" }

    subscription = stripe_api.stripe_subscription_get(subscription_id)
    
    return subscription

@jaseci_action()
def cancel_subscription(subscription_id: str):
    """Cancel customer subscription"""

    if( not subscription_id ):
        return { "message": "Subscription id is required" }

    subscription = stripe_api.stripe_subscription_delete(subscription_id)
    
    return subscription