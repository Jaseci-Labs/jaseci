# **`STRIPE ACTION LIBRARY`**

Stripe is a hybrid action. Configuration of stripe can be set manually or by enabling stripe service. If webhook integration is not required, standalone stripe action should be enough.

## **Documentation Reference**
We have aligned jaseci stripe actions to [stripe api docs](https://stripe.com/docs/api). You may use that docs as reference. However, currently, not all api from stripe api docs are included in actions. You may follow this [docs](https://github.com/Jaseci-Labs/jaseci/blob/main/CONTRIBUTING.md) if you wish to include new stripe api on the stripe actions.

### **Action Naming Scheme**
Stripe uses underscore naming pattern. Any **`new`** stripe action should follow this rules
| Python Module | Jaseci Action |
| - | - |
| `stripe.Customer.create` | `stripe.customer_create` |
| `stripe.PaymentMethod.create` | `stripe.payment_method_create` |
| `stripe.SubscriptionItem.create_usage_record` | `stripe.subscription_item_create_usage_record` |


### **Generic Action**
Even tho we haven't included every api from stripe. You may still be able to request custom stripe action. You may need to check the python module on [stripe api docs](https://stripe.com/docs/api) for reference.
```js
walker custom_stripe_action {
    can stripe.exec;

    with entry {
        // stripe.SetupIntent.create(*args, **kwargs)
        report stripe.exec("SetupIntent.create", {{your_args}}, {{your_kwargs}});

        // stripe.Customer.create_source(*args, **kwargs)
        report stripe.exec("Customer.create_source", {{your_args}}, {{your_kwargs}});

        // stripe.TaxCode.list(*args, **kwargs)
        report stripe.exec("TaxCode.list", {{your_args}}, {{your_kwargs}});
    }
}
```
---
## via Manual Stripe Action
You may trigger stripe actions without a service. However, stripe webhook integration requires stripe service to able to work properly. Manual trigger will always need to include api_key.
```js
walker manual_stripe_action {
    can stripe.customer_create;
    with entry {
        report stripe.customer_create(name="test", email="test@test.com", api_key="{{your_api_key}}");
    }
}
```

## via Stripe Service in Jaseci

First, make sure Stripe is enabled by setting the `enabled` field in Stripe config to be True. We first get the current config via the `config_get` endpoint. (We are going to use jsctl for the following examples but you can also use API requests)

Run the following command in `jsctl` shell.

```bash
config get STRIPE_CONFIG
```

This will return a json of the current configuration for the Stripe Service. Check the field and make sure they are configured to your needs. (More details on the configuration attributes below.)

Update the `enabled` field to be True if it is not already.
Then save it with `config_set`.

```bash
config set STRIPE_CONFIG -value JSON_STRING_OF_THE_CONFIG
```

Final step to enable Stripe is to refresh the Stripe service for the updated configuration to take effect.

```bash
service refresh stripe
```

JSORC will then refresh the Elastic service and creates the necessary kuberentes resources.

### **CONFIGURATION**

#### **`ATTRIBUTES`**

| Attribute         | Description                                                                                                   |
| ----------------- | ------------------------------------------------------------------------------------------------------------- |
| enabled           | If service is enabled in config. The service can be available (upon building) but not enabled (from config)   |
| quiet             | if error logs should be suppressed                                                                            |
| api_key           | Api key for stripe api request                                                                                |
| fallback_walker   | default walker to be triggered if event is not present in event_walker                                        |
| event_walker      | event walker mapping for the callback                                                                         |

### **`DEFAULT CONFIG`**

```js
STRIPE_CONFIG = {
    "enabled": false,
    "quiet": false,
    "api_key": null,
    "webhook_key": null,
    "fallback_walker": "stripe",
    "event_walker": {},
}
```

### **`ENABLED CONFIG`**

```js
STRIPE_CONFIG = {
    "enabled": true,
    "quiet": false,
    "api_key": "sk_test_******vwzcEz",
    "webhook_key": "whsec_******pfxf2J",
    "fallback_walker": "stripe",
    "event_walker": {
        // your custom event mapping
        "customer.subscription.created": "walker_for_subs_created"
    },
}
```
---
# **`ACTION LIST`**
## stripe.**`product_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/products/create
##### **`HOW TO TRIGGER`**
```js
stripe.product_create(name = "Product1"):
```
---
## stripe.**`price_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/prices/create
##### **`HOW TO TRIGGER`**
```js
stripe.price_create(product = "product_id", unit_amount = 100, currency = "aud"):
```
---
## stripe.**`product_list`**
> **`Docs`:** \
> https://stripe.com/docs/api/products/list
##### **`HOW TO TRIGGER`**
```js
stripe.product_list():
```
---
## stripe.**`customer_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/customers/create
##### **`HOW TO TRIGGER`**
```js
stripe.customer_create():
```
---
## stripe.**`customer_modify`**
> **`Docs`:** \
> https://stripe.com/docs/api/customers/update
##### **`HOW TO TRIGGER`**
```js
stripe.customer_modify(customer_id = "customer_id"):
```
---
## stripe.**`customer_retrieve`**
> **`Docs`:** \
> https://stripe.com/docs/api/customers/retrieve
##### **`HOW TO TRIGGER`**
```js
stripe.customer_retrieve(customer_id = "customer_id"):
```
---
## stripe.**`payment_method_attach`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_methods/attach
##### **`HOW TO TRIGGER`**
```js
stripe.payment_method_attach(payment_method_id = "payment_method_id", customer_id = "customer_id"):
```
---
## stripe.**`payment_method_detach`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_methods/detach
##### **`HOW TO TRIGGER`**
```js
stripe.payment_method_detach(payment_method_id ="payment_method_id"):
```
---
## stripe.**`payment_method_list`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_methods/list
##### **`HOW TO TRIGGER`**
```js
stripe.payment_method_list():
```
---
## stripe.**`invoice_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/invoices/create
##### **`HOW TO TRIGGER`**
```js
stripe.invoice_create(customer="customer_id"):
```
---
## stripe.**`invoice_list`**
> **`Docs`:** \
> https://stripe.com/docs/api/invoices/list
##### **`HOW TO TRIGGER`**
```js
stripe.invoice_list():
```
---
## stripe.**`payment_intent_list`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_intents/list
##### **`HOW TO TRIGGER`**
```js
stripe.payment_intent_list():
```
---
## stripe.**`payment_intent_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_intents/create
##### **`HOW TO TRIGGER`**
```js
stripe.payment_intent_create(amount = 1000, currency = "aud"):
```
---
## stripe.**`subscription_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/subscriptions/create
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_create(customer = "customer_id", items: [{"price": "price_id"}]):
```
---
## stripe.**`subscription_modify`**
> **`Docs`:** \
> https://stripe.com/docs/api/subscriptions/update
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_modify(subscription_id: "subscription_id"):
```
---
## stripe.**`subscription_list`**
> **`Docs`:** \
> https://stripe.com/docs/api/subscriptions/list
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_list():
```
---
## stripe.**`subscription_retrieve`**
> **`Docs`:** \
> https://stripe.com/docs/api/subscriptions/retrieve
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_retrieve(subscription_id: "subs_id"):
```
---
## stripe.**`payment_method_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/payment_methods/create
##### **`HOW TO TRIGGER`**
```js
stripe.payment_method_create(type: "card", card = {
    "number": "4242424242424242",
    "exp_month": 8,
    "exp_year": 2020,
    "cvc": "314",
}):
```
---
## stripe.**`subscription_delete`**
> **`Docs`:** \
> https://stripe.com/docs/api/subscriptions/cancel
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_delete(subscription_id: "subs_id"):
```
---
## stripe.**`invoice_retrieve`**
> **`Docs`:** \
> https://stripe.com/docs/api/invoices/retrieve
##### **`HOW TO TRIGGER`**
```js
stripe.invoice_retrieve(invoice_id: "invoice_id"):
```
---
## stripe.**`subscription_item_list_usage_record_summaries`**
> **`Docs`:** \
> https://stripe.com/docs/api/usage_records/subscription_item_summary_list
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_item_list_usage_record_summaries(subscription_item_id: "subscription_item_id"):
```
---
## stripe.**`subscription_item_create_usage_record`**
> **`Docs`:** \
> https://stripe.com/docs/api/usage_records/create
##### **`HOW TO TRIGGER`**
```js
stripe.subscription_item_create_usage_record(subscription_item_id: "subscription_item_id", quantity: 1000):
```
---
## stripe.**`checkout_session_create`**
> **`Docs`:** \
> https://stripe.com/docs/api/checkout/sessions/create
##### **`HOW TO TRIGGER`**
```js
stripe.checkout_session_create(
    success_url: "https://yourdomain.com",
    line_items: [{
        "price": "price_H5ggYwtDq4fbrJ",
        "quantity": 1,
    }],
    mode: "payment"):
```
---
# **`ACTION LIST WITH PRE PROCESS` (DEPRECATED)**
## stripe.**`update_default_payment_method`**
> **`Usage`:** \
> if you already have customer and this customer have multiple payment method
> you may call this action to switch default payment method
##### **`HOW TO TRIGGER`**
```js
stripe.update_default_payment_method(customer_id = "customer_id", payment_method_id = "payment_method_id"):
```
---
## stripe.**`attach_payment_method`**
> **`Usage`:** \
> If there's payment method created that's not yet attached
> you may call this action to bind that payment method to specific customer
##### **`HOW TO TRIGGER`**
```js
stripe.attach_payment_method(payment_method_id = "payment_method_id", customer_id = "customer_id"):
```
---
## stripe.**`create_trial_subscription`**
> **`Usage`:** \
> this is similar to create subscription. However, trial period will always added to the subscription
> specifying payment_method_id will set it as default payment method
##### **`HOW TO TRIGGER`**
```js
stripe.create_trial_subscription(customer_id = "customer_id", items = [{"price": "price_id"}], payment_method_id = "payment_method_id", trial_period_days = 14):
```
---
## stripe.**`create_subscription`**
> **`Usage`:** \
> this is similar to subscription_create.
> with option to specify payment_method_id that will be set as default payment method
##### **`HOW TO TRIGGER`**
```js
stripe.create_subscription(customer_id = "customer_id", items = [{"price": "price_id"}], payment_method_id = "payment_method_id"):
```
---
## stripe.**`update_subscription_item`**
> **`Usage`:** \
> this is similar to subscription_modify but with fixed argument
##### **`HOW TO TRIGGER`**
```js
stripe.update_subscription_item(subscription_id = "subscription_id", subscription_item_id = "subscription_item_id", price_id = "price_id"):
```