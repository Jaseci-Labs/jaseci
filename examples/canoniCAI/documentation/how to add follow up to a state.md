# How to add follow up to a state

##### Table of Contents  
- [ Introduction ](#introduction)
- [Create follow up states](#step-1-create-follow-up-states)
- [Connect follow up state to a state](#step-2-connect-follow-up-state-to-a-state)
- [Add business logic to follow up state](#step-3-add-business-logicc-to-follow-up-state)
- [Add response to follow up state](#step-4-add-response-to-follow-up-state)

# Introduction
In the example KFC bot we have a follow up state. In this tutorial we will explain how we build the follow up. In the order state there is a follow state attached to it, where the customer could either confirm the order or decline the order. So let's dive into it. Let pretend that there was no follow up state, let's build it from scratch.

# Step 1: Create follow up states
Navigate to the ``` fixture.jac ``` file

We will be adding an order confirmation state and an order denial state which are follow ups attached to the order state.

ADD: ``` state_order_confirmation = spawn node::state(name="order_confirmation"); ```
ADD: ``` state_order_denial = spawn node::state(name="order_denial"); ```

``` 
spawn { 
    state_order = spawn node::state(name="order");
    state_order_confirmation = spawn node::state(name="order_confirmation");
    state_order_denial = spawn node::state(name="order_denial");
}
```
# Step 2: Connect follow up state to a state
Next step we will attach the follow up state to the origin state, in this case it's the order state.

ADD: ``` state_order -[transition(intent_label = global.yes_label)]-> state_order_confirmation; ```

If yes_label for intent_label is true it will go to the order confirmation state

ADD: ``` state_order -[transition(intent_label = global.no_label)]-> state_order_denial; ```

If no_label for intent_label is true it will go to the order denial state

``` 
spawn { 
    conv_root -[transition(intent_label = global.order_label)]-> state_order;
    state_order -[transition(intent_label = global.yes_label)]-> state_order_confirmation;
    state_order -[transition(intent_label = global.no_label)]-> state_order_denial;
}
```

# Step 3: Add business logic to follow up state
Since there is no business logic required, we will create a slot ``` user ``` and attach their name to it so we could then use this slot for later use.

Navigate to ``` nodes.jac ```, then search for ``` state node ``` and look for the node ability called ``` business_logic```

ADD: ``` visitor.dialogue_context["user"] = "Jemmott"; ```

``` 
can business_logic {
    if (!visitor.hoping) { 
        if (here.name == "order_confirmation" or here.name == "order_denial") {
            // HERE YOU COULD DO ALL YOUR LOGICS FOR THESE SPECIFIC FOLLOW UP STATES
            visitor.dialogue_context["user"] = "Jemmott";
        }
    }
}
```
# Step 4: Add response to follow up state
Here we will add a response to the follow up state.

Navigate to ``` nodes.jac ```, then search for ``` state node ``` and look for the node ability called ``` gen_response ```

IF ``` here.name == "order_confirmation" ``` then ADD: ```  visitor.answer = "Thank you for ordering with us"; ```

IF ``` here.name == "order_denial" ``` then ADD: ```  visitor.answer = "TNo problem, If there anything I can help with feel free to ask"; ```

``` 
can gen_response {
        if (!visitor.hoping) {
            if (here.name == "soc") {
                visitor.answer = "Hello there, Welcome to KFC!";
            } elif (here.name == "order_confirmation") {
                visitor.answer = "Thank you for ordering with us";
            } elif (here.name == "order_denial") {
                visitor.answer = "No problem, If there anything I can help with feel free to ask";
            }
        }
}
```
