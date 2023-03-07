# How to use stripe actions

### Create stripe product
**name (str)**: The product’s name, meant to be displayable to the customer.
**description (str)**: The product’s description, meant to be displayable to the customer. Use this field to optionally store a long form explanation of the product being sold for your own rendering purposes.

```jac
product  = stripe.create_product(name, description);
```

Response: Stripe product object

### Create stripe product price

**productId (str)**: The ID of the product that this price will belong to.
**amount (int)**: A positive integer in cents (or 0 for a free price) representing how much to charge.
**currency (str)**: Three-letter [ISO currency code](https://www.iso.org/iso-4217-currency-codes.html), in lowercase. Must be a [supported currency](https://stripe.com/docs/currencies)
**recurring (dict) (Optional)**: The recurring components of a price such as `interval` and `usage_type`.
- **recurring.interval (REQUIRED)**: Specifies billing frequency. Either `day`, `week`, `month` or `year`.
- **recurring.interval_count (Optional)**: The number of intervals between subscription billings. For example, `interval=month` and `interval_count=3` bills every 3 months. Maximum of one year interval allowed (1 year, 12 months, or 52 weeks).

[See more details here](https://stripe.com/docs/api/prices/create?lang=python).

```jac
product  = stripe.create_product_price(productId, amount, currency, recurring,  **kwargs);
```

Response: Stripe price object

### Retrieve stripe product list

**detailed (bool) (Optional)**: Only return prices that are active or inactive (e.g., pass `false` to list all inactive prices).

```jac
products  = stripe.product_list(detailed);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/prices",
  "has_more": false,
  "data": [LIST OF PRICE OBJECT]
}
```

### Create stripe customer
**email (str) (Optional)**: Customer’s email address. It’s displayed alongside the customer in your dashboard and can be useful for searching and tracking. This may be up to 512 characters.
**name (str) (Optional)**: The customer’s full name or business name.

```jac
customer  = stripe.create_customer(email, name, address,  **kwargs);
```

Response: Stripe customer Object

### Retrieve stripe customer
customer_id (str): The ID of the customer you want to retrieve.

```jac
customer  = stripe.get_customer(customer_id,  **kwargs);
```

Response: Returns the Customer object for a valid identifier. If it’s for a deleted Customer, a subset of the customer’s information is returned, including a deleted property that’s set to true.

### Attach a payment method to a customer
**payment_method_id (str)**: The ID of the customer payment method that will be attach.
**customer_id (str)**: The ID of the customer to which to attach the PaymentMethod.

```jac
payment_method  = stripe.attach_payment_method(payment_method_id, customer_id,  **kwargs);
```

Response: Returns a PaymentMethod object.

### Detaches a PaymentMethod object from a Customer
After a PaymentMethod is detached, it can no longer be used for a payment or re-attached to a Customer.
**payment_method_id (str)**: The ID of the customer payment method that will be detach.

```jac
payment_method  = stripe.detach_payment_method(payment_method_id,  **kwargs);
```

Response: Returns a PaymentMethod object.

### Retrieve a list of PaymentMethods for a given Customer
**customer_id (str)**: The ID of the customer.

[See more details here](https://stripe.com/docs/api/payment_methods/customer_list?lang=python).

```jac
payment_methods  = stripe.get_payment_methods(customer_id,  **kwargs);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/customers/cus_NBsqL1C1GrrHYM/payment_methods",
  "has_more": false,
  "data": [LIST OF PAYMENT METHODS OBJECT]
}
```

### Update customer default payment method
**customer_id (str)**: The ID of the customer.
**payment_method_id (str)**: The ID of the payment method that will be use as customer default payment method.

```jac
customer  = stripe.update_default_payment_method(customer_id, payment_method_id,  **kwargs);
```

Response: Stripe customer object

### Create invoice
**customer_id (str)**: The ID of the customer.

```jac
invoice  = stripe.create_invoice(customer_id,  **kwargs);
```

Response: Stripe invoice object

### Retrieve customer list of invoice
**customer_id (str)**: The ID of the customer.
**subscription_id (str)**: Return invoices for the subscription
**starting_after (str) (Optional)**: A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.
**limit (int) (Optional)**: A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

```jac
invoices  = stripe.get_invoice_list(customer_id, subscription_id, starting_after, limit,  **kwargs);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/invoices",
  "has_more": false,
  "data": [LIST OF INVOICE OBJECT]
}
```

### Retrieve customer list of payment intents
**customer_id (str)**: The ID of the customer.
**starting_after (str) (Optional)**: A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.
**limit (int) (Optional)**: A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.

```jac
payment_intents  = stripe.get_payment_intents(customer_id, starting_after, limit,  **kwargs);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/payment_intents",
  "has_more": false,
  "data": [LIST OF PAYMENT INTENTS OBJECT]
}
```

### Create customer payment intents
**customer_id (str)**: The ID of the customer.
**amount (int)**: Amount intended to be collected by this PaymentIntent. A positive integer representing how much to charge in the smallest currency unit (e.g., 100 cents to charge $1.00 or 100 to charge ¥100, a zero-decimal currency). The minimum amount is $0.50 US or equivalent in charge currency. The amount value supports up to eight digits (e.g., a value of 99999999 for a USD charge of $999,999.99).
**currency (str)**: Three-letter [ISO currency code](https://www.iso.org/iso-4217-currency-codes.html), in lowercase. Must be a [supported currency](https://stripe.com/docs/currencies)
**recurring (dict) (Option
**payment_method_types (list)**: The list of payment method types that this PaymentIntent is allowed to use. If this is not provided, defaults to ["card"]. Valid payment method types include: `acss_debit`, `affirm`, `afterpay_clearpay`, `alipay`, `au_becs_debit`, `bacs_debit`, `bancontact`, `blik`, `boleto`, `card`, `card_present`, `customer_balance`, `eps`, `fpx`, `giropay`, `grabpay`, `ideal`, `interac_present`, `klarna`, `konbini`, `link`, `oxxo`, `p24`, `paynow`, `pix`, `promptpay`, `sepa_debit`, `sofort`, `us_bank_account`, and `wechat_pay`.

```jac
payment_intent = stripe.create_payment_intents(customer_id, amount, currency, payment_method_types);
```

Response: Returns a PaymentIntent object.

### Retrieve customer list of subscriptions
**customer_id (str)**: The ID of the customer whose subscriptions will be retrieved.

[See more details here](https://stripe.com/docs/api/subscriptions/list?lang=python).

```jac
subscriptions = stripe.get_customer_subscription(customer_id);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/subscriptions",
  "has_more": false,
  "data": [LIST OF SUBSCRIPTION OBJECT]
}
```

### Create payment method
**card_type (str)**: The type of the PaymentMethod. An additional hash is included on the PaymentMethod with a name matching this value. It contains additional information specific to the PaymentMethod type. Required unless `payment_method` is specified (see the [Cloning PaymentMethods](https://stripe.com/docs/payments/payment-methods/connect#cloning-payment-methods) guide).
- **Possible values** - `acss_debit`, `affirm`, `afterpay_clearpay`, `alipay`, `au_becs_debit`, `bacs_debit`, `bancontact`, `blik`, `boleto`, `card`, `card_present`, `customer_balance`, `eps`, `fpx`, `giropay`, `grabpay`, `ideal`, `interac_present`, `klarna`, `konbini`, `link`, `oxxo`, `p24`, `paynow`, `pix`, `promptpay`, `sepa_debit`, `sofort`, `us_bank_account`, and `wechat_pay`.
**card (dict)**: Details of the card.

Sample card details:
```js
{
  "number": "4242424242424242",
  "exp_month": 8,
  "exp_year": 2024,
  "cvc": "314",
},
```

```jac
payment_method = stripe.create_payment_method(card_type, card);
```

Response:
```js
{
  "object": "list",
  "url": "/v1/subscriptions",
  "has_more": false,
  "data": [LIST OF SUBSCRIPTION OBJECT]
}
```

### Create trial subscription
**customer_id (str)**: The ID of the customer.
**items (list)**: A list of up to 20 subscription items, each with an attached price.
  1. **items.price (str) (Optional)**: The ID of the price object.

[items child parameter](https://stripe.com/docs/api/subscriptions/create#create_subscription-items).

**payment_method_id (str) (Optional)**: If you want to attach new payment method in the subscription
**trial_period_days (int)**: Integer representing the number of trial period days before the customer is charged for the first time. This will always overwrite any trials that might apply via a subscribed plan

```jac
subscription = stripe.create_trial_subscription(customer_id, items, payment_method_id, trial_period_days);
```

Response: Stripe subscription object

### Create subscription
**customer_id (str)**: The ID of the customer.
**items (list)**: A list of up to 20 subscription items, each with an attached price.
  1. **items.price (str) (Optional)**: The ID of the price object.

[items child parameter](https://stripe.com/docs/api/subscriptions/create#create_subscription-items).

**payment_method_id (str) (Optional)**: If you want to attach new payment method in the subscription

```jac
subscription = stripe.create_subscription(customer_id, items, payment_method_id);
```

Response: Stripe subscription object

### Cancel customer subscription
**subscription_id (str)**: The ID of the subscription you want to cancel.

```jac
subscription = stripe.cancel_subscription(subscription_id);
```

Response: Stripe subscription object

### Retrive customer subscription
**subscription_id (str)**: The ID of the subscription you want to retrieve.

```jac
subscription = stripe.get_subscription(subscription_id);
```

Response: Stripe subscription object

### Update customer subscription
**subscription_id (str)**: The ID of the customer subscription.
**subscription_item_id (str)**: Subscription item to update.
**price_id (str)**: The ID of the price object.

[See more details here](https://stripe.com/docs/api/subscriptions/update).

```jac
subscription = stripe.update_subscription_item(subscription_id, subscription_item_id, price_id);
```

Response: The newly updated Subscription object

### Retrieve invoice details
**invoice_id (str)**: The ID of the customer subscription.

[See more details here](https://stripe.com/docs/api/subscriptions/update).

```jac
invoice = stripe.get_invoice(invoice_id);
```

Response: Returns an invoice object if a valid invoice ID was provided

### Create usage report
Creates a usage record for a specified subscription item and date, and fills it with a quantity.

**subscription_item_id (str)**: Subscription item
**quantity (int)**: The usage quantity for the specified timestamp.

[See more details here](https://stripe.com/docs/api/subscriptions/update).

```jac
record = stripe.create_usage_report(subscription_item_id, quantity);
```

Response: Returns usage record object

### Create checkout session
**success_url (str)**: The URL to which Stripe should send customers when payment or setup is complete. If you’d like to use information from the successful Checkout Session on your page, read the guide on [customizing your success page](https://stripe.com/docs/payments/checkout/custom-success-page).
**cancel_url (int) (Optional)**: If set, Checkout displays a back button and customers will be directed to this URL if they decide to cancel payment and return to your website.
**line_items (list) (Optional)**: A list of items the customer is purchasing. Use this parameter to pass one-time or recurring `Prices.

For `payment` mode, there is a maximum of 100 line items, however it is recommended to consolidate line items if there are more than a few dozen.

For `subscription` mode, there is a maximum of 20 line items with recurring Prices and 20 line items with one-time Prices. Line items with one-time Prices will be on the initial invoice only.

**mode (str)**: The mode of the Checkout Session. Pass `subscription` if the Checkout Session includes at least one recurring item.
1. Possible enum values
  - `payment`: Accept one-time payments for cards, iDEAL, and more.
  - `setup`: Save payment details to charge your customers later.
  - `subscription`: Use Stripe Billing to set up fixed-price subscriptions.


[See more details about line_items](https://stripe.com/docs/api/checkout/sessions/create#create_checkout_session-line_items).

```jac
checkout_session = stripe.create_checkout_session(success_url, cancel_url, line_items, mode);
```

Response: Returns session object