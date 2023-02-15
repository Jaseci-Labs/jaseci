import stripe
from unittest.mock import Mock
from unittest import mock
from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.svc.stripe.config import STRIPE_CONFIG
from jaseci.svc.meta import MetaService


class StripeTests(CoreTest):
    """Unit tests for Stripe actions"""

    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        STRIPE_CONFIG["enabled"] = True
        STRIPE_CONFIG[
            "api_key"
        ] = "sk_test_51JWUIeCZO78n7fsZnPvualWhmJg1DcCI332kKnWF3q2sKGwnPADjEmNblfFWi4pWAWPuJwHxpeSoJGc0J5ButHN900Q2xBz1se"
        STRIPE_CONFIG["webhook_key"] = "test_webhook_key"

        meta = MetaService()
        hook = meta.build_hook()

        meta.get_service("stripe").reset(hook)

        super(StripeTests, cls).setUpClass()
        stripe.Product.create = Mock()
        stripe.Price.create = Mock()
        stripe.Product.list = Mock()
        stripe.Customer.create = Mock()
        stripe.Customer.retrieve = Mock()
        stripe.PaymentMethod.list = Mock()
        stripe.PaymentMethod.attach = Mock()
        stripe.PaymentMethod.detach = Mock()
        stripe.Customer.modify = Mock()
        stripe.Invoice.create = Mock()
        stripe.Invoice.list = Mock()
        stripe.PaymentIntent.list = Mock()
        stripe.PaymentIntent.create = Mock()
        stripe.Subscription.list = Mock()
        stripe.PaymentMethod.create = Mock()
        stripe.Subscription.create = Mock()
        stripe.Subscription.delete = Mock()
        stripe.Subscription.retrieve = Mock()
        stripe.Subscription.modify = Mock()
        stripe.Invoice.retrieve = Mock()
        stripe.SubscriptionItem.create_usage_record = Mock()
        stripe.checkout.Session.create = Mock()

    @classmethod
    def tearDownClass(cls):
        super(StripeTests, cls).tearDownClass()

    @jac_testcase("stripe.jac", "create_product")
    def test_stripe_create_product(self, ret):
        stripe.Product.create.assert_called_once_with(
            name="product1", description="new product"
        )

    @jac_testcase("stripe.jac", "create_product_price")
    def test_stripe_create_product_price(self, ret):
        stripe.Price.create.assert_called_once_with(
            product="product1", unit_amount=12, currency="usd"
        )

    @jac_testcase("stripe.jac", "product_list")
    def test_stripe_product_list(self, ret):
        stripe.Product.list.assert_called_once_with(active=True)

    @jac_testcase("stripe.jac", "create_customer")
    def test_stripe_create_customer(self, ret):
        stripe.Customer.create.assert_called_once_with(
            email="test12@gmail.com",
            name="stripe customer",
            address={"billing_address": "123 metro manila"},
        )

    @jac_testcase("stripe.jac", "get_customer")
    def test_stripe_get_customer(self, ret):
        stripe.Customer.retrieve.assert_called_once_with(id="cus_NBsqL1C1GrrHYM")

    @jac_testcase("stripe.jac", "attach_payment_method")
    def test_stripe_attach_payment_method(self, ret):
        stripe.PaymentMethod.list.assert_called_once_with(
            customer="cus_NBsqL1C1GrrHYM", type="card"
        )

        stripe.PaymentMethod.attach.assert_called_once_with(
            payment_method="pm_1MN1iN2xToAoV8chTjvX94hm", customer="cus_NBsqL1C1GrrHYM"
        )

    @jac_testcase("stripe.jac", "detach_payment_method")
    def test_stripe_detach_payment_method(self, ret):
        stripe.PaymentMethod.detach.assert_called_once_with(
            payment_method="pm_1MN1iN2xToAoV8chTjvX94hm"
        )

    @jac_testcase("stripe.jac", "get_payment_methods")
    def test_stripe_get_payment_methods(self, ret):
        stripe.PaymentMethod.list.assert_called_with(
            customer="cus_NBsqL1C1GrrHYM", type="card"
        )

    @jac_testcase("stripe.jac", "update_default_payment_method")
    def test_stripe_update_default_payment_method(self, ret):
        stripe.Customer.modify.assert_called_with(
            sid="cus_NBsqL1C1GrrHYM",
            invoice_settings={"default_payment_method": "pm_1MN1iN2xToAoV8chTjvX94hm"},
        )

    @jac_testcase("stripe.jac", "create_invoice")
    def test_stripe_create_invoice(self, ret):
        stripe.Customer.modify.assert_called_once_with(
            sid="cus_NBsqL1C1GrrHYM",
            invoice_settings={"default_payment_method": "pm_1MN1iN2xToAoV8chTjvX94hm"},
        )

    @jac_testcase("stripe.jac", "get_invoice_list")
    def test_stripe_get_invoice_list(self, ret):
        stripe.Invoice.list.assert_called_once_with(
            customer="cus_NBsqL1C1GrrHYM",
            limit=10,
            subscription="sub_1MTgMQCZO78n7fsZqu1dk6nD",
        )

    @jac_testcase("stripe.jac", "get_payment_intents")
    def test_stripe_get_payment_intents(self, ret):
        stripe.PaymentIntent.list.assert_called_once_with(
            customer="cus_NBsqL1C1GrrHYM", limit=10
        )

    @jac_testcase("stripe.jac", "create_payment_intents")
    def test_stripe_create_payment_intents(self, ret):
        stripe.PaymentIntent.create.assert_called_once_with(
            customer="cus_NBsqL1C1GrrHYM",
            amount=12,
            currency="usd",
            payment_method_types=["card"],
        )

    @jac_testcase("stripe.jac", "get_customer_subscription")
    def test_stripe_get_customer_subscription(self, ret):
        stripe.Subscription.list.assert_called_once_with(
            customer="sub_1MTgMQCZO78n7fsZqu1dk6nD"
        )

    @jac_testcase("stripe.jac", "create_payment_method")
    def test_stripe_create_payment_method(self, ret):
        stripe.PaymentMethod.create.assert_called_once_with(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 8,
                "exp_year": 2024,
                "cvc": "314",
            },
            billing_details={"city": "Caloocan", "country": "philippines"},
        )

    @jac_testcase("stripe.jac", "create_trial_subscription")
    def test_stripe_create_trial_subscription(self, ret):
        stripe.Subscription.create.assert_called_with(
            customer="cus_NBsqL1C1GrrHYM",
            items=[{"price": "price_1MR9T6CZO78n7fsZmNdIJplr"}],
            trial_period_days=14,
        )

    @jac_testcase("stripe.jac", "create_subscription")
    def test_stripe_create_subscription(self, ret):
        stripe.Subscription.create.assert_called_with(
            customer="cus_NBsqL1C1GrrHYM",
            items=[{"price": "price_1MR9T6CZO78n7fsZmNdIJplr"}],
        )

    @jac_testcase("stripe.jac", "cancel_subscription")
    def test_stripe_cancel_subscription(self, ret):
        stripe.Subscription.delete.assert_called_once_with(
            sid="sub_1MTgMQCZO78n7fsZqu1dk6nD"
        )

    @jac_testcase("stripe.jac", "get_subscription")
    def test_stripe_get_subscription(self, ret):
        stripe.Subscription.retrieve.assert_called_once_with(
            id="sub_1MTgMQCZO78n7fsZqu1dk6nD"
        )

    @jac_testcase("stripe.jac", "update_subscription_item")
    def test_stripe_update_subscription_item(self, ret):
        stripe.Subscription.modify.assert_called_once_with(
            sid="sub_1MTgMQCZO78n7fsZqu1dk6nD",
            cancel_at_period_end=False,
            items=[
                {
                    "id": "su_1MTgMQCZO78n7fsZqu1dk6nD",
                    "price": "price_1MTgMQCZO78n7fsZqu1dk6nD",
                }
            ],
        )

    @jac_testcase("stripe.jac", "get_invoice")
    def test_stripe_get_invoice(self, ret):
        stripe.Invoice.retrieve.assert_called_once_with(
            id="inv_1MTgMQCZO78n7fsZqu1dk6nD"
        )

    @jac_testcase("stripe.jac", "create_usage_report")
    def test_stripe_create_usage_report(self, ret):
        stripe.SubscriptionItem.create_usage_record.assert_called()

    @jac_testcase("stripe.jac", "create_checkout_session")
    def test_stripe_create_checkout_session(self, ret):
        stripe.checkout.Session.create.assert_called_once_with(
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            line_items=[{"price": "price_H5ggYwtDq4fbrJ", "quantity": 12}],
            mode="payment",
        )
