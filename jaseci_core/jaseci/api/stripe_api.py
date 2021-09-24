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


if __name__ == '__main__':
    PAYMENT = stripe_api()
    # id = sys.argv[1]
    # amount = int(sys.argv[2])

    # PAYMENT.admin_api_stripe_create_payment(id, amount)
    PAYMENT.admin_api_stripe_create_customer(sys.argv[1])
    # PAYMENT.admin_api_stripe_create_product(sys.argv[1])
    # PAYMENT.admin_api_stripe_modify_price(sys.argv[1])
    # PAYMENT.admin_api_stripe_customer_subscription(sys.argv[1], sys.argv[2])
    # PAYMENT.admin_api_stripe_cancel_subscription(sys.argv[1])
