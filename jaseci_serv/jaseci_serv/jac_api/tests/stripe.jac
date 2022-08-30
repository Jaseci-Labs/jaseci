walker create_customer {
  has email, name, metadata, payment_method_id, address;
  can stripe.create_customer;

  report stripe.create_customer(email, name, metadata, address, payment_method_id);
}

walker get_customer {
  has customer_id;
  can stripe.get_customer;

  report stripe.get_customer(customer_id);
}

walker create_payment_method {
  has card_type, card;
  can stripe.create_payment_method;

  report stripe.create_payment_method(card_type, card);
}

walker attach_payment_method {
  has payment_method_id, customer_id;
  can stripe.attach_payment_method;

  report stripe.attach_payment_method(payment_method_id, customer_id);
}

walker get_payment_methods {
  has customer_id;
  can stripe.get_payment_methods;

  report stripe.get_payment_methods(customer_id);
}

walker update_default_payment_method {
  has payment_method_id, customer_id;
  can stripe.update_default_payment_method;

  report stripe.update_default_payment_method(customer_id, payment_method_id);
}

walker create_subscription {
  has payment_method_id, price_id, customer_id;
  can stripe.create_subscription;

  report stripe.create_subscription(payment_method_id, price_id, customer_id);
}

walker create_trial_subscription {
  has payment_method_id, price_id, customer_id, trial_period_days;
  can stripe.create_trial_subscription;

  report stripe.create_trial_subscription(payment_method_id, price_id, customer_id, trial_period_days);
}

walker get_subscription {
  has subscription_id;
  can stripe.get_subscription;

  report stripe.get_subscription(subscription_id);
}

walker cancel_subscription {
  has subscription_id;
  can stripe.cancel_subscription;

  report stripe.cancel_subscription(subscription_id);
}

walker update_subscription {
  has subscription_id, subscription_item_id, price_id;
  can stripe.update_subscription;

  report stripe.update_subscription(subscription_id, subscription_item_id, price_id);
}

walker report_usage {
  has subscription_item_id, quantity;
  can stripe.report_usage;

  report stripe.create_usage_report(subscription_item_id, quantity);
}

walker create_invoice {
  has customer_id;
  can stripe.create_invoice;

  report stripe.create_invoice(customer_id);
}

walker get_invoice {
  has invoice_id;
  can stripe.get_invoice;

  report stripe.get_invoice(invoice_id);
}

walker get_invoice_list {
  has customer_id, subscription_id, starting_after, limit;
  can stripe.get_invoice_list;

  report stripe.get_invoice_list(customer_id, subscription_id, starting_after, limit);
}

walker get_payment_intents {
  has customer_id, starting_after, limit;
  can stripe.get_payment_intents;

  report stripe.get_payment_intents(customer_id, starting_after, limit);
}

walker create_payment_intents {
  has amount, currency, payment_method_types, customer_id;
  can stripe.create_payment_intents;

  report stripe.create_payment_intents(customer_id, amount, currency, payment_method_types);
}

walker payment_create {
  has test_data;

  report test_data;
}

walker payment_create2 {
  has test_data;

  report test_data;
}