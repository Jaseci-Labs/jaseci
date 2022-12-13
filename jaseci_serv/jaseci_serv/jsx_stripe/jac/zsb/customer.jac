// import {*} with "./nodes_edges.jac";

walker create_customer {
  has email,
      name,
      metadata,
      payment_method_id,
      address,

  can stripe.create_customer;


  root {
    try {
      report:status = 201;
      report stripe.create_customer(email=email, name=name, metadata=metadata, address=address, payment_method_id=payment_method_id);
    } else with error {
      report error;
      report:error = error;
    }
  }
}

walker get_customer {
  has customer_id;
  can stripe.get_customer;

  try {
    report stripe.get_customer(customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker get_customer_payment_methods {
  has customer_id;
  can stripe.get_payment_methods;

  try {
    report stripe.get_payment_methods(customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker add_payment_method {
  has payment_method_id, customer_id;
  can stripe.attach_payment_method;

  try {
    report stripe.attach_payment_method(payment_method_id=payment_method_id, customer_id=customer_id);
  } else with error {
    report error;
    report:error = error;
  }
}

walker update_payment_method {
  has payment_method_id, customer_id;
  can stripe.update_default_payment_method;

  try {
    report stripe.update_default_payment_method(customer_id=customer_id, payment_method_id=payment_method_id);
  } else with error {
    report error;
    report:error = error;
  }
}