walker stripe_webhook: anyone {
    root {
        req_ctx = global.info['request_context'];
        req_data = req_ctx['body']['data']['object'];
        event_type = req_ctx['body']['type'];

        if( event_type == 'customer.created' ) {
          if( req_data["metadata"]["node_id"] ) {
            # DO LOGIC HERE
          }
        } elif( event_type == 'customer.subscription.created' ) {
          if( req_data["metadata"]["node_id"] ) {
            # DO LOGIC HERE
          }
        }
    }
}

walker create_product {
  has name, description, mock_api;
  can stripe.create_product;

  try {
    report stripe.create_product(name, description, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_product_price {
  has productId, amount, currency, interval, mock_api;
  can stripe.create_product_price;

  try {
    report stripe.create_product_price(productId, amount, currency, interval, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker product_list {
  has detailed, mock_api;
  can stripe.product_list;

  try {
    report stripe.product_list(detailed, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_customer {
  has email, name, metadata, payment_method_id, address, mock_api;
  can stripe.create_customer;

  try {
    report stripe.create_customer(email, name, metadata, address, payment_method_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_customer {
  has customer_id, mock_api;
  can stripe.get_customer;

  try {
    report stripe.get_customer(customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker attach_payment_method {
  has payment_method_id, customer_id, mock_api;
  can stripe.attach_payment_method;

  try {
    report stripe.attach_payment_method(payment_method_id, customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker delete_payment_method {
  has payment_method_id, mock_api;
  can stripe.delete_payment_method;

  try {
    report stripe.delete_payment_method(payment_method_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_payment_methods {
  has customer_id, mock_api;
  can stripe.get_payment_methods;

  try {
    report stripe.get_payment_methods(customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker update_default_payment_method {
  has payment_method_id, customer_id, mock_api;
  can stripe.update_default_payment_method;

  try {
    report stripe.update_default_payment_method(customer_id, payment_method_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_invoice {
  has customer_id, mock_api;
  can stripe.create_invoice;

  try {
    report stripe.create_invoice(customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_invoice_list {
  has customer_id, subscription_id, starting_after, limit, mock_api;
  can stripe.get_invoice_list;

  try {
    report stripe.get_invoice_list(customer_id, subscription_id, starting_after, limit, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_payment_intents {
  has customer_id, starting_after, limit, mock_api;
  can stripe.get_payment_intents;

  try {
    report stripe.get_payment_intents(customer_id, starting_after, limit, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_payment_intents {
  has amount, currency, payment_method_types, customer_id, mock_api;
  can stripe.create_payment_intents;

  try {
    report stripe.create_payment_intents(customer_id, amount, currency, payment_method_types, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_customer_subscription {
  has customer_id, mock_api;
  can stripe.get_customer_subscription;

  try {
    report stripe.get_customer_subscription(customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_payment_method {
  has card_type, card, mock_api;
  can stripe.create_payment_method;

  try {
    report stripe.create_payment_method(card_type, card, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_trial_subscription {
  has payment_method_id, price_id, customer_id, trial_period_days, mock_api;
  can stripe.create_trial_subscription;

  try {
    report stripe.create_trial_subscription(payment_method_id, price_id, customer_id, trial_period_days, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_subscription {
  has payment_method_id, price_id, customer_id, mock_api;
  can stripe.create_subscription;
  
  try {
    report stripe.create_subscription(payment_method_id, price_id, customer_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker cancel_subscription {
  has subscription_id, mock_api;
  can stripe.cancel_subscription;
  
  try {
    report stripe.cancel_subscription(subscription_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_subscription {
  has subscription_id, mock_api;
  can stripe.get_subscription;
  
  try {
    report stripe.get_subscription(subscription_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker update_subscription {
  has subscription_id, subscription_item_id, price_id, mock_api;
  can stripe.update_subscription;

  try {
    report stripe.update_subscription(subscription_id, subscription_item_id, price_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_invoice {
  has invoice_id, mock_api;
  can stripe.get_invoice;

  try {
    report stripe.get_invoice(invoice_id, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}

walker create_usage_report {
  has subscription_item_id, quantity, mock_api;
  can stripe.create_usage_report;

  try {
    report stripe.create_usage_report(subscription_item_id, quantity, mock_api);
  } else with error {
    report error;
    report:error = error;
  }
}









