walker create_product {
    has name = "product1", description = "new product";
    can stripe.create_product;

    stripe.create_product(name, description);
}

walker create_product_price {
    has productId = "product1", amount = 12, currency = "usd", recurring = {};
    can stripe.create_product_price;

    stripe.create_product_price(productId, amount, currency, recurring);
}

walker product_list {
    has detailed = true;
    can stripe.product_list;

    stripe.product_list(detailed);
}

walker create_customer {
    has email = "test12@gmail.com", name = "stripe customer", address = {"billing_address": "123 metro manila"};
    can stripe.create_customer;

    stripe.create_customer(email, name, address);
}

walker get_customer {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.get_customer;

    stripe.get_customer(customer_id);
}

walker attach_payment_method {
    has payment_method_id = "pm_1MN1iN2xToAoV8chTjvX94hm", customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.attach_payment_method;

    stripe.attach_payment_method(payment_method_id, customer_id);
}

walker detach_payment_method {
    has payment_method_id = "pm_1MN1iN2xToAoV8chTjvX94hm";
    can stripe.detach_payment_method;

    stripe.detach_payment_method(payment_method_id);
}

walker get_payment_methods {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.get_payment_methods;

    stripe.get_payment_methods(customer_id);
}

walker update_default_payment_method {
    has customer_id = "cus_NBsqL1C1GrrHYM", payment_method_id = "pm_1MN1iN2xToAoV8chTjvX94hm";
    can stripe.update_default_payment_method;

    stripe.update_default_payment_method(customer_id, payment_method_id);
}

walker create_invoice {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.create_invoice;

    stripe.create_invoice(customer_id);
}

walker get_invoice_list {
    has customer_id = "cus_NBsqL1C1GrrHYM", subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.get_invoice_list;

    stripe.get_invoice_list(customer_id, subscription_id);
}

walker get_payment_intents {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.get_payment_intents;

    stripe.get_payment_intents(customer_id);
}

walker create_payment_intents {
    has customer_id = "cus_NBsqL1C1GrrHYM", amount = 12, currency = "usd", payment_method_types = ["card"];
    can stripe.create_payment_intents;

    report stripe.create_payment_intents(customer_id, amount, currency, payment_method_types);
}

walker get_customer_subscription {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.get_customer_subscription;

    stripe.get_customer_subscription(subscription_id);
}

walker create_payment_method {
    has card_type = "card";
    has billing_details = {"city": "Caloocan", "country": "philippines"};
    has card = {
        "number": "4242424242424242",
        "exp_month": 8,
        "exp_year": 2024,
        "cvc": "314"
    };
    can stripe.create_payment_method;

    stripe.create_payment_method(card_type, card, billing_details);
}

walker create_trial_subscription {
    has customer_id = "cus_NBsqL1C1GrrHYM", items = [{"price": "price_1MR9T6CZO78n7fsZmNdIJplr"}];
    can stripe.create_trial_subscription;

    stripe.create_trial_subscription(customer_id, items);
}

walker create_subscription {
    has customer_id = "cus_NBsqL1C1GrrHYM", items = [{"price": "price_1MR9T6CZO78n7fsZmNdIJplr"}];
    can stripe.create_subscription;

    stripe.create_subscription(customer_id, items);
}

walker cancel_subscription {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.cancel_subscription;

    stripe.cancel_subscription(subscription_id);
}

walker get_subscription {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.get_subscription;

    stripe.get_subscription(subscription_id);
}

walker update_subscription_item {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD", subscription_item_id = "su_1MTgMQCZO78n7fsZqu1dk6nD", price_id = "price_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.update_subscription_item;

    stripe.update_subscription_item(subscription_id, subscription_item_id, price_id);
}

walker get_invoice {
    has invoice_id = "inv_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.get_invoice;

    stripe.get_invoice(invoice_id);
}

walker create_usage_report {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD", quantity = 12;
    can stripe.create_usage_report;

    stripe.create_usage_report(subscription_id, quantity);
}

walker create_checkout_session {
    has success_url = "https://example.com/success", cancel_url = "https://example.com/cancel", line_items = [{"price": "price_H5ggYwtDq4fbrJ","quantity": 12}], mode = "payment";
    can stripe.create_checkout_session;

    stripe.create_checkout_session(success_url, cancel_url, line_items, mode);
}