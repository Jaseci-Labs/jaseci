from jaseci.api.interface import interface
import stripe

stripe_test_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"


class stripe_api():
    """
    Stripe APIs
    Set of APIs to expose jaseci stripe management
    """

    def __init__(self):
        stripe.api_key = self._h.resolve_glob('STRIPE_KEY', stripe_test_key)

    @interface.admin_api()
    def stripe_product_create(self, name: str = "VIP Plan",
                              description: str = "Plan description"):
        """ create product """
        try:
            return stripe.Product.create(
                namex=name,
                descriptionx=description
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_product_price_set(self, productId: str,
                                 amount: float = 50,
                                 interval: str = "month"):
        """ modify product price """
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
        """ retrieve all producs """
        if(not detalied):
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
    def stripe_customer_create(self, paymentId: str,
                               name: str = "cristopher evangelista",
                               email: str = "imurbatman12@gmail.com",
                               description: str = "Myca subscriber"):
        """ create customer """
        try:
            return stripe.Customer.create(
                name=name,
                email=email,
                description=description,
                payment_method=paymentId,
                invoice_settings={"default_payment_method": paymentId}
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_get(self, customerId: str):
        """ retrieve customer information """
        try:
            return stripe.Customer.retrieve(customerId)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_add(self, paymentMethodId: str,
                                    customerId: str):
        """ add customer payment method """
        try:
            paymentMethods = \
                self.stripe_retrieve_customer_payment_methods(
                    customerId)

            paymentMethod = stripe.PaymentMethod.attach(
                paymentMethodId, customer=customerId)

            if(len(paymentMethods.data) == 0):
                self.stripe_update_default_payment_method(
                    customerId, paymentMethodId)

            paymentMethod.is_default = len(paymentMethods.data) == 0

            return paymentMethod

        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_delete(self, paymentMethodId: str):
        """ remove customer payment method """
        try:
            return stripe.PaymentMethod.detach(paymentMethodId)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_get(self, customerId: str):
        """ get customer list of payment methods """
        try:
            return stripe.PaymentMethod.list(
                customer=customerId,
                type="card",
            )
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_customer_payment_default(self, customerId: str,
                                        paymentMethodId: str):
        """ update default payment method of customer """
        try:
            setting = {"default_payment_method": paymentMethodId}
            return stripe.Customer.modify(customerId,
                                          invoice_settings=setting)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_create(self, paymentId: str,
                                   name: str, email: str,
                                   priceId: str, customerId: str):
        """
        create customer subscription
        TODO: name and email parameters not used!
        """
        try:
            # attach payment method to customer
            self.stripe_add_customer_payment_methods(
                paymentId, customerId)

            # set card to default payment method
            self.stripe_update_default_payment_method(
                customerId, paymentId)

            subscription = stripe.Subscription.create(
                customer=customerId,
                items=[
                    {"price": priceId},
                ],
                trial_period_days=30
            )

            subscription.payment_method = paymentId

            return subscription
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_delete(self, subscriptionId: str):
        """ cancel customer subscription """
        try:
            return stripe.Subscription.delete(subscriptionId)
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_subscription_get(self, customerId: str):
        """ retrieve customer subcription """
        try:
            subscription = stripe.Subscription.list(customer=customerId)

            if (len(subscription.data) == 0):
                return {"status": "inactive", "message":
                        "Customer has no subscription"}

            subscription.pop("items", None)

            return subscription.data[0]
        except Exception as e:
            return {"message": str(e)}

    @interface.admin_api()
    def stripe_invoices_list(self, customerId: str,
                             subscriptionId: str,
                             limit: int = 10,
                             lastItem: str = ""):
        """ retrieve customer list of invoices """
        try:
            if(lastItem != ''):
                invoices = stripe.Invoice.list(
                    customer=customerId, limit=limit, starting_after=lastItem,
                    subscription=subscriptionId)
            else:
                invoices = stripe.Invoice.list(
                    customer=customerId, limit=limit,
                    subscription=subscriptionId)
            return invoices
        except Exception as e:
            return {"message": str(e)}
