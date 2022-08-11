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
    def stripe_product_create(
        self, name: str = "VIP Plan", description: str = "Plan description"
    ):
        """create product"""
        try:
            return stripe.Product.create(namex=name, descriptionx=description)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_product_price_set(
        self, productId: str, amount: float = 50, interval: str = "month"
    ):
        """modify product price"""
        try:
            return stripe.Price.create(
                unit_amount=amount,
                currency="usd",
                recurring={"interval": interval},
                product=productId,
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_product_list(self, detalied: bool = True):
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
    def stripe_customer_create(email: str, name: str, metadata: dict = {}, address: dict or None = {}, payment_method_id: str or None = None):
        """create customer"""
        try:
            return stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata,
                address=address,
                payment_method=payment_method_id,
                invoice_settings={ "default_payment_method": payment_method_id },
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
    def stripe_create_payment_method(card_type: str, card: dict):
        """create payment method"""
        try:
            paymentMethod = stripe.PaymentMethod.create(type=card_type, card=card)

            return paymentMethod

        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_add(self, payment_method_id: str, customer_id: str):
        """attach customer payment method"""
        try:
            paymentMethods = self.stripe_customer_payment_list_get(self, customer_id)

            paymentMethod = stripe.PaymentMethod.attach(
                payment_method_id, customer=customer_id
            )

            if len(paymentMethods.data) == 0:
                self.stripe_customer_default_payment_update(self, customer_id, payment_method_id)

            paymentMethod.is_default = len(paymentMethods.data) == 0

            return paymentMethod

        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_delete(self, payment_method_id: str):
        """remove customer payment method"""
        try:
            return stripe.PaymentMethod.detach(payment_method_id)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_list_get(self, customer_id: str):
        """get customer list of payment methods"""
        try:
            return stripe.PaymentMethod.list(
                customer=customer_id,
                type="card",
            )
        except Exception as e:
            return {"message": str(e)}
    

    @interface.admin_api()
    def stripe_customer_default_payment_update(self, customer_id: str, payment_method_id: str):
        """update default payment method of customer"""
        try:
            setting = {"default_payment_method": payment_method_id}
            return stripe.Customer.modify(customer_id, invoice_settings=setting)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_trial_subscription_create(self, payment_method_id: str, price_id: str, customer_id: str, trial_period_days: int = 30):
        """create customer trial subscription"""
        try:
            # attach payment method to customer
            self.stripe_customer_payment_add(self, payment_method_id, customer_id)

            # set card to default payment method
            self.stripe_customer_default_payment_update(self, customer_id, payment_method_id)

            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    { "price": price_id },
                ],
                trial_period_days=trial_period_days,
            )

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_create(self, payment_method_id: str, price_id: str, customer_id: str):
        """create customer subscription"""
        try:
            # attach payment method to customer
            self.stripe_customer_payment_add(self, payment_method_id, customer_id)

            # set card to default payment method
            self.stripe_customer_default_payment_update(self, customer_id, payment_method_id)

            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    { "price": price_id },
                ],
            )

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_delete(subscriptionId: str):
        """cancel customer subscription"""
        try:
            return stripe.Subscription.delete(subscriptionId)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_list_get(self, customer_id: str):
        """retrieve customer subcription list"""
        try:
            subscription = stripe.Subscription.list(customer=customer_id)

            if len(subscription.data) == 0:
                return {"status": "inactive", "message": "Customer has no subscription"}

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_get(subscription_id: str):
        """retrieve customer subcription details"""
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_invoices_list(
        self, customer_id: str, subscriptionId: str, limit: int = 10, lastItem: str = ""
    ):
        """retrieve customer list of invoices"""
        try:
            if lastItem != "":
                invoices = stripe.Invoice.list(
                    customer=customer_id,
                    limit=limit,
                    starting_after=lastItem,
                    subscription=subscriptionId,
                )
            else:
                invoices = stripe.Invoice.list(
                    customer=customer_id, limit=limit, subscription=subscriptionId
                )
            return invoices
        except Exception as e:
            return {"message": str(e)}
