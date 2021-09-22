import json
import sys
import stripe
from django.http import JsonResponse

stripe.api_key = "sk_test_51JZeGHDiHeCtNB1DdakkFaCUm89tDWmE6zA0qjZAoxZ1GqGHIyvur4t4yjlGITUfUHQgmurQKvzRyFCbWa3eRviU003YmENmVD"


class stripe_api():

    """ create product """

    def admin_api_create_product(self, name="VIP Plan", description="Plan description"):
        try:
            product = stripe.Product.create(
                namex=name,
                descriptionx=description
            )

            return json.dumps({"data": product})
        except Exception as e:
            return json.dumps({"message": str(e)})

    """ modify product price """

    def admin_api_modify_price(self, productId, amount=50, interval="month"):
        try:
            price = stripe.Price.create(
                unit_amount=amount,
                currency="usd",
                recurring={"interval": interval},
                product=productId,
            )

            return json.dumps({"data": price})
        except Exception as e:
            return json.dumps({"message": str(e)})

    """ create customer """

    def admin_api_create_customer(self, methodId, name="cristopher evangelista", email="imurbatman12@gmail.com", description="Myca subscriber"):
        try:
            customer = stripe.Customer.create(
                name=name,
                email=email,
                description=description,
                payment_method=methodId,
                invoice_settings={"default_payment_method": methodId}
            )

            return json.dumps({"data": customer})
        except Exception as e:
            return json.dumps({"message": str(e)})

    """ create customer subscription """

    def admin_api_customer_subscription(self, customerId, priceId):
        try:
            subscription = stripe.Subscription.create(
                customer=customerId,
                items=[
                    {"price": priceId},
                ],
            )

            return json.dumps({"data": subscription})
        except Exception as e:
            return json.dumps({"message": str(e)})

    """ cancel customer subscription """

    def admin_api_cancel_subscription(self, subscriptionId):
        try:
            subscription = stripe.Subscription.delete(subscriptionId)

            return json.dumps({"data": subscription})
        except Exception as e:
            return json.dumps({"message": str(e)})


PAYMENT = stripe_api()

if __name__ == '__main__':
    # id = sys.argv[1]
    # amount = int(sys.argv[2])

    # PAYMENT.admin_api_create_payment(id, amount)
    PAYMENT.admin_api_create_customer(sys.argv[1])
    # PAYMENT.admin_api_create_product(sys.argv[1])
    # PAYMENT.admin_api_modify_price(sys.argv[1])
    # PAYMENT.admin_api_customer_subscription(sys.argv[1], sys.argv[2])
    # PAYMENT.admin_api_cancel_subscription(sys.argv[1])
