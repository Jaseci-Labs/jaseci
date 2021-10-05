import stripe
from datetime import datetime
from datetime import timedelta

from stripe.api_resources import subscription

stripe.api_key = "sk_test_51JZeGHDiHeCtNB1DdakkFaCUm89tDWmE6zA0qjZAoxZ1GqGHIyvur4t4yjlGITUfUHQgmurQKvzRyFCbWa3eRviU003YmENmVD"


class stripe_api():

    def admin_api_stripe_create_product(self, name: str = "VIP Plan",
                                        description: str = "Plan description"):
        """ create product """
        try:
            return stripe.Product.create(
                namex=name,
                descriptionx=description
            )
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_creat_price(self, productId: str, amount: float = 50,
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

    def admin_api_stripe_create_customer(self, paymentId: str,
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

    def admin_api_stripe_retrieve_customer_info(self, customerId: str):
        """ retrieve customer information """
        try:
            return stripe.Customer.retrieve(customerId)
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_add_customer_payment_methods(self, paymentMethodId: str, customerId: str):
        """ add customer payment method """
        try:
            paymentMethods = self.admin_api_stripe_retrieve_customer_payment_methods(
                customerId)

            paymentMethod = stripe.PaymentMethod.attach(
                paymentMethodId, customer=customerId)

            if(len(paymentMethods.data) == 0):
                self.admin_api_stripe_update_default_payment_method(
                    customerId, paymentMethodId)

            paymentMethod.is_default = len(paymentMethods.data) == 0

            return paymentMethod

        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_remove_customer_payment_methods(self, paymentMethodId: str):
        """ add customer payment method """
        try:
            return stripe.PaymentMethod.detach(paymentMethodId)
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_customer_payment_methods(self, customerId: str):
        """ get customer list of payment methods """
        try:
            return stripe.PaymentMethod.list(
                customer=customerId,
                type="card",
            )
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_update_default_payment_method(self, customerId: str, paymentMethodId: str):
        """ update default payment method of customer """
        try:
            return stripe.Customer.modify(customerId, invoice_settings={"default_payment_method": paymentMethodId})
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_customer_subscription(self, paymentId: str, name: str, email: str, priceId: str):
        """ create customer subscription """
        try:
            customer = self.admin_api_stripe_create_customer(
                paymentId, name, email)

            billing_cycle_anchor = round(datetime.timestamp(
                datetime.now() + timedelta(days=30)))
            trial_start = round(datetime.timestamp(datetime.now()))
            # print(billing_cycle_anchor)
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {"price": priceId},
                ],
                trial_period_days=30
            )

            return {"tuper": billing_cycle_anchor}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_cancel_subscription(self, subscriptionId: str):
        """ cancel customer subscription """
        try:
            return stripe.Subscription.delete(subscriptionId)
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_products(self):
        """ retrieve all producs """
        try:
            return stripe.Product.list()
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_price(self):
        """ retrieve product price """
        try:
            return stripe.Product.list()
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_customer_subscription(self, customerId: str):
        """ retrieve customer subcription """

        try:
            subscription = stripe.Subscription.list(customer=customerId)

            if (len(subscription.data) == 0):
                return {"active": "inactive", "message": "Customer has no subscription"}

            subscription.pop("items", None)

            return subscription.data[0]
        except Exception as e:
            return {"message": str(e)}
