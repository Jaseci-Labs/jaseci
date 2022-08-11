from datetime import datetime
from jaseci.api.interface import interface
import stripe

stripe_test_key = "sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"


class stripe_api:
    """
    Stripe APIs
    Set of APIs to expose jaseci stripe management
    """

    def __init__(self):
        stripe.api_key = self._h.resolve_glob("STRIPE_KEY", stripe_test_key)

    @interface.admin_api()
    def stripe_product_create(name: str, description: str):
        """create product"""
        try:
            return stripe.Product.create(name=name, descriptionx=description)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_product_price_set(
        productId: str, amount: int, currency: str, interval: str
    ):
        """modify product price"""
        try:
            return stripe.Price.create(
                product=productId,
                unit_amount=amount,
                currency=currency,
                recurring={"interval": interval},
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_product_list(detalied: bool = True):
        """retrieve all producs"""
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

    @interface.admin_api()
    def stripe_customer_create(
        email: str,
        name: str,
        metadata: dict or None = None,
        address: dict or None = None,
        payment_method_id: str or None = None,
    ):
        """create customer"""
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

    @interface.admin_api()
    def stripe_customer_get(customer_id: str):
        """retrieve customer information"""
        try:
            return stripe.Customer.retrieve(customer_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_add(self, payment_method_id: str, customer_id: str):
        """attach payment method to customer"""
        try:
            paymentMethods = self.stripe_customer_payment_list_get(self, customer_id)

            paymentMethod = stripe.PaymentMethod.attach(
                payment_method_id, customer=customer_id
            )

            if len(paymentMethods.data) == 0:
                self.stripe_customer_default_payment_update(
                    self, customer_id, payment_method_id
                )

            paymentMethod.is_default = len(paymentMethods.data) == 0

            return paymentMethod

        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_delete(payment_method_id: str):
        """detach payment method from customer"""
        try:
            return stripe.PaymentMethod.detach(payment_method_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_list(customer_id: str):
        """get customer list of payment methods"""
        try:
            return stripe.PaymentMethod.list(
                customer=customer_id,
                type="card",
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_default_payment_method_update(
        customer_id: str, payment_method_id: str
    ):
        """update default payment method of customer"""
        try:
            return stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": payment_method_id},
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_invoice_create(customer_id: str):
        """create customer invoice"""
        try:
            return stripe.Invoice.create(customer=customer_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_invoice_list(
        customer_id: str,
        subscription_id: str,
        starting_after: str = "",
        limit: int = 10,
    ):
        """retrieve customer list of invoices"""
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

    @interface.admin_api()
    def stripe_customer_payment_intents_get(
        customer_id: str, starting_after: str = "", limit: int = 10
    ):
        """get customer payment intents"""
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

    @interface.admin_api()
    def stripe_customer_payment_intents_create(
        customer_id: str,
        amount: int,
        currency: str,
        payment_method_types: str,
    ):
        """Create customer payment"""
        try:
            return stripe.PaymentIntent.create(
                customer=customer_id,
                amount=amount,
                currency=currency,
                payment_method_types=payment_method_types,
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_subscription_get(customer_id: str):
        """retrieve customer subcription list"""
        try:
            subscription = stripe.Subscription.list(customer=customer_id)

            if len(subscription.data) == 0:
                return {"status": "inactive", "message": "Customer has no subscription"}

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_payment_method_create(card_type: str, card: dict):
        """create payment method"""
        try:
            return stripe.PaymentMethod.create(type=card_type, card=card)

        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_trial_create(
        self,
        payment_method_id: str,
        price_id: str,
        customer_id: str,
        trial_period_days: int = 30,
    ):
        """create customer trial subscription"""
        try:
            # attach payment method to customer
            self.stripe_customer_payment_add(self, payment_method_id, customer_id)

            # set card to default payment method
            self.stripe_customer_default_payment_method_update(
                self, customer_id, payment_method_id
            )

            return stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {"price": price_id},
                ],
                trial_period_days=trial_period_days,
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_create(
        self, payment_method_id: str, price_id: str, customer_id: str
    ):
        """create customer subscription"""
        try:
            # attach payment method to customer
            self.stripe_customer_payment_add(self, payment_method_id, customer_id)

            # set card to default payment method
            self.stripe_customer_default_payment_update(
                self, customer_id, payment_method_id
            )

            return stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {"price": price_id},
                ],
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_delete(subscription_id: str):
        """cancel customer subscription"""
        try:
            return stripe.Subscription.delete(subscription_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_get(subscription_id: str):
        """retrieve customer subcription details"""
        try:
            return stripe.Subscription.retrieve(subscription_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_update(
        subscription_id: str, subscription_item_id: str, price_id: str
    ):
        """update subcription details"""
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

    @interface.admin_api()
    def stripe_invoice_get(invoice_id: str):
        """get invoice information"""
        try:
            return stripe.Invoice.retrieve(invoice_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_create_usage_record(subscription_item_id: str, quantity: int):
        """Create usage record"""
        try:
            return stripe.SubscriptionItem.create_usage_record(
                subscription_item_id, quantity=quantity, timestamp=datetime.now()
            )
        except Exception as e:
            return {"message": str(e)}
