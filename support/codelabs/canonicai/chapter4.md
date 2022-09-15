# Build a conversational AI system in Jaseci

# Chapter 4

## What are we building?
We are building a Conversational AI.

### Explaining std.input and std.out

Let's start with std.input, std meaning "standard" and input meaning "what is put in". std.input is a function that intakes, what a user put in only from the terminal and can be stored in a variable. It pauses the program to intake data from the user. The function accepts an optional string to display to the terminal. It acts like a prompt so user know what to input to the terminal.  This function cannot be used to intake any data from api or anything external. That is what std.input is all about. 

```jac
name = std.input('what is your name');
```

Let's now talk about std.out. std in jac means "standard" and out meaning "output". std.out is a function in jac when called it display data to a terminal or server and it intake a string parameter which is used to display. 

```jac
std.out('Display TEXT here');
```

### How to run the program interactively via jsctl

In this section we will be running you through how to run a program interactively via jsctl. Let's start from the first step. You need to install jaseci if you have not. Run the command below in the terminal.

``` 
pip install jaseci 
```

After, installing jaseci we have to run the command jsctl meaning "jaseci control". Run the command below in the terminal.

```
jsctl
```

After running jaseci control (jsctl) you should see an active cursor. Now you can run any jac program by using the jac command. For e.g. We have a file named hello.py that runs "hello world!".
Run the command below in the terminal.

```
jac run hello.py
```

That's how to run the program interactively via jsctl.

### The journey of a dialogue session

First before we get started, let's run the code below in jsctl. What this does it will allow us to go through the dialogue in jsctl.
```
jac run main.jac -walk interactive
```

In this section, I will walk you through the journey of a dialogue session. We will go through several queries and explain what happens with each query, including what intent and entities came from that query and  which node it starts at and how it transitions from that node to another node. Let's get started.


```
> I want to test drive
To set you up with a test drive, we will need your name and address.
```
**I want to test drive**: When the user respond with that query it first go through the conversational AI root state (node) for intent classification. Based on the intent extracted it will do an intent transition (edge) to the next state (node) in this case it will transition to collect information state (node).


```
> My  name is Tony Stark
What is your address?
```

**My  name is Tony Stark**: After coming from the conversation AI root state from the first query above and it get's transitioned to the collect information state, it will prompt the user for their name and address information, Then the user respond with this query and it will go to the entity extraction model and pulls out the features from the user utterance in this case it will pull out the name because only the name was provided. Since the entity transition required two keys, one is the name and one is the address, since only one of the data was provided it will re-transition to the current state (node) "collect information" while keeping the context of the last query provided alongside with the features.


```
> My address is at 10880 Malibu Point
Can you confirm your name to be Tony Stark and your address as 10880 Malibu Point?
```

**My address is at 10880 Malibu Point**: Coming from the last query, when get re-transitioned to the collect information state and the bot prompt the user for data and the user responds with the current query. The entity extraction model will extract the feature address and map  **10880 Malibu Point** to address, alongside with the last features extracted from the last query and with both information provided it will do an entity transition and move to the next state (node) called confirmation state.
 
```
> Yes that looks correct
You are all set for a Tesla test drive!
```

**Yes that looks correct**: When transitioned to confirmation state, it will be prompted by the bot for confirmation and when the user responds with the current query, it will go through the intent classification model to know whether or not they confirmed or not, based on the current query the user agreed and it will do an intent transition to move to confirmed state (node) which the bot will prompt the user with the information required based on the user data.