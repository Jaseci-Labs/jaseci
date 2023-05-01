node dialogue_root;

node dialogue_state {
    has name;
    has response;
}

edge intent_transition {
    has intent;
}

#build the graph

graph dialogue_system {
    has anchor dialogue_root;
    spawn {
        dialogue_root = spawn node::dialogue_root;
        pricing_state = spawn node::dialogue_state(
            name = "ec2_price_method",
            response = "EC2 offers five pricing options: On-Demand, Savings Plans, Reserved Instances, Spot price, and Dedicated Hosts pricing. Other costs include egress data transfers, premium support, and block storage costs."
        );
        ebs_state = spawn node::dialogue_state(
            name = "ebs_storage",
            response = "An Amazon EBS volume is a durable, block-level storage device that you can attach to your instances."
        );

        dialogue_root +[intent_transition(intent="pricing categories")]+> pricing_state;
        dialogue_root +[intent_transition(intent="ebs storage")]+> ebs_state;
    }
}
