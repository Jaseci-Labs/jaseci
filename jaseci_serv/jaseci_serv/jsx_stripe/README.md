## Setting up Stripe API key
---
For setting up Stripe API key, you need to follow few steps:

### Step 1 : Signup and Signin
1. Signup of Signin your stripe account here.  https://dashboard.stripe.com/login


### Step 2 : Get api keys
1. Go here https://dashboard.stripe.com/test/apikeys
2. Now click on **"Reveal test key"** button
3. Then copy the **"Secret key"**


### Step 3 : Add Stripe API key to your django server
1. Run command **`jsserv runserver`**.
2. go to your admin page and login. http://127.0.0.1:8000/admin/login/?next=/admin/
3. go to **`global vars`** and click **`ADD GLOBAL VARS`**. http://127.0.0.1:8000/admin/base/globalvars/

- see the following image for reference




---
### Getting the Stripe Webhooks URL
---

1. Call the login api to get the admin token.
```JSON
{
  url: '/user/token',
  method: 'POST',
  data: {
    email: [EMAIL],
    password: [PASSWORD]
  }
}
```
**Sample Response**
```JSON
{
  expiry: null,
  token: "70283dce1cc7ceb65ae88a884533da76d672414206c35980e062f9647df743a9"
}
```
2. Call the stripe init api.
```JSON
{
  url: '/js_admin/stripe/init',
  method: 'POST',
  data: {
    email: [EMAIL],
    password: [PASSWORD]
  },
  header: {
    Authorization: "bearer ADMIN_TOKEN"
  }
}
```
**Sample Response**
```JSON
{
  data: "/js_public/walker_callback/6d223ae3-8ea5-4a74-8a41-907bda321189/a150ed0a-a256-4b72-83cc-e4d85a6acd42?key=b3c421ff52874461eedc1e73645e8e29",
  success: true
}
```

---
### Setting up the Stripe Webhooks
---
1. Go to https://dashboard.stripe.com/test/webhooks.
2. Click "**Add an endpoint**" button.
3. Paste the stripe webhook url **[STRIPE_WEBHOOK_URL]**
4. Select all events you want to listen.


---
### Creating a Jaseci Action for Stripe APIs
---
1. Go to the folder **/jaseci_serv/jaseci_serv/jsx_stripe**.
2. Edit the [stripe.py](./actions/stripe.py) file and there you can add all the logic and use the APIs from stripe.

**Sample Action**
```python
import stripe

@jaseci_action()
def create_customer(
    email: str,
    name: str,
    metadata: dict or None = None,
    address: dict or None = None,
    payment_method_id: str or None = None,
):
    """create customer"""
    stripe.api_key = [STRIPE_API_KEY]

    try:
        return stripe.Customer.create(
            email=email,
            name=name,
            metadata=metadata,
            address=address,
            payment_method=payment_method_id,
            invoice_settings={"default_payment_method": payment_method_id},
        )
    except Exception as e:
        return {"message": str(e)}
```
**note:** `@jaseci_action()` decorator is required to make your method to be a jaseci action.

3. Now go to your [stripe.jac](stripe.jac).
4. You will see the `walker stripe_webhook: anyone`.
5. That is where you will put the logic for each of **STRIPE EVENTS** you selected in you stripe webhooks/

```jac
walker stripe_webhook: anyone {
    root {
        req_ctx = global.info['request_context'];
        req_data = req_ctx['body']['data']['object'];
        event_type = req_ctx['body']['type'];

        if( event_type == 'customer.created' ) {
          if( req_data["metadata"]["node_id"] ) {
            # DO LOGIC HERE
            # you can update the user node in here to add the customer_ID
          }
        } elif( event_type == 'customer.subscription.created' ) {
          if( req_data["metadata"]["node_id"] ) {
            # DO LOGIC HERE
          }
        }
    }
}
```
**note:** This public walker is the one that stripe will call if there is an event in your webhook.

**Sample Walker**
```jac
walker create_customer {
  has email, name, metadata, payment_method_id, address,;
  can stripe.create_customer; #this is the action

  try {
    report stripe.create_customer(email, name, metadata, address, payment_method_id);
  } else with error {
    report error;
    report:error = error;
  }
}
````