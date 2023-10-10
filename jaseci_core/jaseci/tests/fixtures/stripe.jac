walker create_product {
    has name = "product1", description = "new product";
    can stripe.product_create;

    stripe.product_create(name = name, description = description);
}

walker create_product_price {
    has productId = "product1", amount = 12, currency = "usd", recurring = {};
    can stripe.price_create;

    stripe.price_create(productId, amount, currency, recurring = recurring);
}

walker product_list {
    can stripe.product_list;

    stripe.product_list(active = true);
}

walker create_customer {
    has email = "test12@gmail.com", name = "stripe customer", address = {"billing_address": "123 metro manila"};
    can stripe.customer_create;

    stripe.customer_create(email=email, name=name, address=address);
}

walker get_customer {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.customer_retrieve;

    stripe.customer_retrieve(customer_id);
}

walker delete_customer {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.customer_delete;

    stripe.customer_delete(customer_id);
}

walker attach_payment_method {
    has payment_method_id = "pm_1MN1iN2xToAoV8chTjvX94hm", customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.attach_payment_method;

    stripe.attach_payment_method(payment_method_id, customer_id);
}

walker detach_payment_method {
    has payment_method_id = "pm_1MN1iN2xToAoV8chTjvX94hm";
    can stripe.payment_method_detach;

    stripe.payment_method_detach(payment_method_id);
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
    can stripe.invoice_create;

    stripe.invoice_create(customer_id);
}

walker get_invoice_list {
    has customer_id = "cus_NBsqL1C1GrrHYM", subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.invoice_list;

    stripe.invoice_list(customer = customer_id, subscription = subscription_id);
}

walker get_payment_intents {
    has customer_id = "cus_NBsqL1C1GrrHYM";
    can stripe.payment_intent_list;

    stripe.payment_intent_list(customer = customer_id);
}

walker create_payment_intents {
    has customer_id = "cus_NBsqL1C1GrrHYM", amount = 12, currency = "usd", payment_method_types = ["card"];
    can stripe.payment_intent_create;

    report stripe.payment_intent_create(amount, currency, customer = customer_id, payment_method_types = payment_method_types);
}

walker get_customer_subscription {
    has customer_id = "customer_id";
    can stripe.subscription_list;

    stripe.subscription_list(customer = customer_id);
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
    can stripe.payment_method_create;

    stripe.payment_method_create(card_type, card = card, billing_details = billing_details);
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
    can stripe.subscription_delete;

    stripe.subscription_delete(subscription_id);
}

walker get_subscription {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.subscription_retrieve;

    stripe.subscription_retrieve(subscription_id);
}

walker update_subscription_item {
    has subscription_id = "sub_1MTgMQCZO78n7fsZqu1dk6nD", subscription_item_id = "su_1MTgMQCZO78n7fsZqu1dk6nD", price_id = "price_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.update_subscription_item;

    stripe.update_subscription_item(subscription_id, subscription_item_id, price_id);
}

walker get_invoice {
    has invoice_id = "inv_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.invoice_retrieve;

    stripe.invoice_retrieve(invoice_id);
}

walker create_usage_report {
    has subscription_item_id = "si_1MTgMQCZO78n7fsZqu1dk6nD", quantity = 12;
    can stripe.subscription_item_create_usage_record;

    stripe.subscription_item_create_usage_record(subscription_item_id, quantity);
}

walker list_usage_report {
    has subscription_item_id = "si_1MTgMQCZO78n7fsZqu1dk6nD", quantity = 12;
    can stripe.subscription_item_list_usage_record_summaries;

    stripe.subscription_item_list_usage_record_summaries(subscription_item_id, limit=1);
}

walker subscription_item_retrieve {
    has subscription_item_id = "si_1MTgMQCZO78n7fsZqu1dk6nD";
    can stripe.subscription_item_retrieve;

    stripe.subscription_item_retrieve(subscription_item_id);
}

walker create_checkout_session {
    has success_url = "https://example.com/success", cancel_url = "https://example.com/cancel", line_items = [{"price": "price_H5ggYwtDq4fbrJ","quantity": 12}], mode = "payment";
    can stripe.checkout_session_create;

    stripe.checkout_session_create(success_url, mode, line_items = line_items, cancel_url = cancel_url);
}

walker create_billing_portal_session {
    can stripe.billing_portal_session_create;

    stripe.billing_portal_session_create(
        customer="cus_O7ECcoZCZFwinb",
        return_url="https://example.com/account"
    );
}