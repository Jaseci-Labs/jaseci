---
sidebar_position: 5
---

# Write your first app

Let's create a simple converational Agent using Jaseci and Jaseci Kit. We're gonna creat a Chat bot for students to sign up for Jaseci Dojo !

Before we begin ensure your have jaseci and jaseci kit installed. If not see the Installation here. 

Create a file called graph.jac. Here we are going to create the conversational flow for the chatbot .

```jac

node state {
    has title;
    has message;
    has prompts;
}

```
#get good definition
node represets