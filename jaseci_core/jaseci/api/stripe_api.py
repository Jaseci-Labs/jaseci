import stripe

stripe.api_key = "sk_test_51JZeGHDiHeCtNB1DdakkFaCUm89tDWmE6zA0qjZAoxZ1GqGHIyvur4t4yjlGITUfUHQgmurQKvzRyFCbWa3eRviU003YmENmVD"


class stripe_api():

    def admin_api_stripe_create_product(self, name: str = "VIP Plan",
                                        description: str = "Plan description"):
        """ create product """
        try:
            product = stripe.Product.create(
                namex=name,
                descriptionx=description
            )

            return {"data": product}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_modify_price(self, productId: str, amount: float = 50,
                                      interval: str = "month"):
        """ modify product price """
        try:
            price = stripe.Price.create(
                unit_amount=amount,
                currency="usd",
                recurring={"interval": interval},
                product=productId,
            )

            return {"data": price}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_create_customer(self, methodId: str,
                                         name: str = "cristopher evangelista",
                                         email: str = "imurbatman12@gmail.com",
                                         description: str = "Myca subscriber"):
        """ create customer """
        try:
            customer = stripe.Customer.create(
                name=name,
                email=email,
                description=description,
                payment_method=methodId,
                invoice_settings={"default_payment_method": methodId}
            )

            return {"data": customer}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_customer_info(self, customerId: str):
        """ retrieve customer information """
        try:
            customer = stripe.Customer.retrieve("cus_KH2zTwcvguOfGd")
            return {"data": customer}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_add_customer_payment_methods(self, paymentMethodId: str, customerId: str):
        """ add customer payment method """
        try:
            paymentMethods = self.admin_api_stripe_retrieve_customer_payment_methods(customerId)

            paymentMethod = stripe.PaymentMethod.attach(paymentMethodId, customer=customerId)

            if(len(paymentMethods["data"].data) == 0):
                self.admin_api_stripe_update_default_payment_method(customerId, paymentMethodId)
            
            return {"data": paymentMethod, "is_default": len(paymentMethods["data"].data) == 0}

        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_remove_customer_payment_methods(self, paymentMethodId: str):
        """ add customer payment method """
        try:
            paymentMethod = stripe.PaymentMethod.detach(paymentMethodId)
            
            return {"data": paymentMethod}

        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_retrieve_customer_payment_methods(self, customerId: str):
        """ get customer list of payment methods """
        try:
            paymentMethods = stripe.PaymentMethod.list(
                customer=customerId,
                type="card",
            )

            return {"data": paymentMethods}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_update_default_payment_method(self, customerId: str, paymentMethodId: str):
        """ update default payment method of customer """
        try:
            customer = stripe.Customer.modify(customerId, invoice_settings={"default_payment_method": paymentMethodId})
            
            return {"data": customer}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_customer_subscription(self, customerId: str, priceId: str):
        """ create customer subscription """
        try:
            subscription = stripe.Subscription.create(
                customer=customerId,
                items=[
                    {"price": priceId},
                ],
            )

            return {"data": subscription}
        except Exception as e:
            return {"message": str(e)}

    def admin_api_stripe_cancel_subscription(self, subscriptionId: str):
        """ cancel customer subscription """
        try:
            subscription = stripe.Subscription.delete(subscriptionId)

            return {"data": subscription}
        except Exception as e:
            return {"message": str(e)}
