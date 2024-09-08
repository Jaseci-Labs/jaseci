graph acme_graph_dot {
    has anchor state_conv_root;
    graph G {
        state_conv_root [node=conv_state, name=conv_root]

        state_office_hour [node=conv_state, name=office_hour]
        state_payment_method [node=conv_state, name=payment_method]
        state_phone_number [node=conv_state, name=phone_number]
        state_email_address [node=conv_state, name=email_address]
        state_promotions [node=conv_state, name=promotions]

        state_cancel_appointment [node=conv_state, name=cancel_appointment]
        state_reschedule_appointment [node=conv_state, name=reschedule_appointment]
        state_refunds [node=conv_state, name=refunds]
        state_feedback [node=conv_state, name=feedback]

        state_service_inquiry [node=conv_state, name=service_inquiry]

        state_conv_root -> state_office_hour [edge=transition, intent="office hour"]
        state_conv_root -> state_payment_method [edge=transition, intent="payment method"]
        state_conv_root -> state_phone_number [edge=transition, intent="phone number"]
        state_conv_root -> state_email_address [edge=transition, intent="email address"]
        state_conv_root -> state_promotions [edge=transition, intent="promotions"]
        state_conv_root -> state_cancel_appointment [edge=transition, intent="cancel appointment"]
        state_conv_root -> state_reschedule_appointment [edge=transition, intent="reschedule appointment"]
        state_conv_root -> state_refunds [edge=transition, intent="refunds"]
        state_conv_root -> state_feedback [edge=transition, intent="feedback"]
        state_conv_root -> state_service_inquiry [edge=transition, intent="service inquiry"]
    }
}