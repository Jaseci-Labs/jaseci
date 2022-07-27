---
sidebar_position: 2
---

# Jaseci Kit

Jaseci Kit is a collection of powerful modules which used together create amazing Conversational Agents.Jaseci Kit uses  pytorch and Tensorflow 

Before we can continure let's ensure we install Jaseci-kit.

```
pip install jaseci-kit --upgrade

```
Activate the Jaseci terminal by running:
```
jsctl
```
Jaseci default libraries can be seen by running :

```
actions list 
```
We can load additional modules by running <strong>actions load module</strong> in the terminal followed by the specific module.
A module that reduce the time to train modules and generate the apporaite response is the questions and answer module.

To load the Question and Answer Module run :
```
actions load module jaseci_kit.use_qa
```
Running ``` actions list ```  will show the new modules loaded.

Lets test the Module out by copying and pasting the following code .

```jac
walker init {
        # when using external libraries we use the (can) keyword to load them in to the program.
        can use.enc_question , use.enc_answer;


        answers = ['I am 20 years old' , 'My dog is hungry','My TV is broken'];
        question = "If i wanted to fix something what should i fix ?";


        q_enc = use.enc_question(question);
        a_enc  = use.enc_answer(answers); # can take list or single strings

        a_scores = [];

        for i in a_enc:

            a_scores.l::append(vector.cosine_sim(q_enc,i));

            report a_scores;


}

```

The above code takes in a list of answers and a question and then returns a report with the probability of each answer. The probability represents how likely each answer is to answer the question. The higher the probability the more likely it is to answer the question.

To run the code  :


```jac

jac run main.jac

```




