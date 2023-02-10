# JacTalk - Conversational Chatbot through jaseci commandline

**What is JacTalk:** 


This tutorial show you how to instantiate, train and run a sample chat bot 

## Steps included
1. [JacTalk Init](#1-jactalk-init---initializing-bot)
2. [Jactalk Train](#2-jactalk-train---training-the-bot)
3. [JacTalk Shell](#3-jactalk-shell---talking-to-the-bot)

## 1. JacTalk Init - Initializing Bot </br>

The first step includes the intialization step, this would download a template with sample files required by the JacTalk. These files a are downloaded inside the folder named sample_bot </br>

* Starting the jaseci commandline 
> jsctl -m </br>
* Executing JacTalk init
> jactalk init
* This should download a folder named sample_bot in your current location.</br>
![Alt text](../images/sample_bot.png?raw=true)

* Sample bot directory content
1. encoder directory </br>
    * enc.jac - This is a jac file that contains the encoder model APIs for intent classification
    * train_enc.json - The train file that is ingested by encoder 
2. ner directory
    * ner.jac - This is a jac file that contains the NER model APIs for Entity Extraction 
    * train_ner.json - The train file that is ingested by encoder 
3. faq directory
    * faq.jac - This file that contains data about faq
    * faq_data.json - Json file that is ingested by fac.jac 
4. dialogue.jac - contains conversational state, which represents a possible user state during a dialgoue
5. graph.jac - contains code for graph creation and chat flow
6. jac_talk.jac - this is main jac file that is used for system input output

## 2. JacTalk Train - Training the Bot 

* Executing JacTalk train </br>
> jactalk train </br>

This command would trains the ner and encoder model with the data in respective json file

## 3. JacTalk Shell - Talking with the Bot
* Executing JacTalk Shell
> jactalk shell </br>

This command would execute the JacTalk sheel to test the bot
 