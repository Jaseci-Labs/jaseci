# How to use Mechanical Turk

# Chapter 10

### Introduction
Mechanical Turk is to collect new training data that is used to improve the AI. In this section, we will be using amazon mechanical turk.

#### Step 1: Register
If you do not have a requester account, you will have to create one. You may not be able to create a requester account based on the region you live in. If that's the case reach out to your admin and use their account. 

#### Step 2: Sign In
When you sign into the requester account for amazon. Click on `New Project`. Look at the image below for further assistance it's highlighted in yellow.

![Alt text](./images/new_project.png?raw=true)

#### Step 3: Selecting Templates
You will have to Select a customizable template to start a new project. In our case scenerio, we will choose the option to `collect utterance`. It will be highlighted in yellow in the image below, after you click on `collect utterance`, then proceed to click `Create Project`.

![Alt text](./images/collect_utterance.png?raw=true)

#### Step 4: Enter Properties
You will be redirected to the project page where you will have to specify the following below.

> **_NOTE:_**  Make sure you follow instructions in this section properly because what you enter here will determine whether you get good information from the general public.

* **Project Name**: The name of the project 
* **Title**: A short to the point title of the task, be very specific as possible
* **Description**: Give more information about the task here
* **Keywords**: Keywords that will enable the general public or workers to find your task

 Money is involved in this section so pay keen attention to details here Be as brief as possible because most workers will skim through the task given, try to avoid using words that confuses workers they will NOT go on google to find the meaning of the word. 

Here is how the form looks. 

![Alt text](./images/edit_project.png?raw=true)

#### Step 5: Setting up your task
> **_NOTE:_** Money is involved in this section, so pay keen attention to details here.

* **Reward per assignment**: This is how much a Worker will be paid for completing an assignment. Consider how long it will take a Worker to complete each assignment. As a default we usually assign this to `$0.05`

* **Number of assignments per task**: How much utterances you would like at the end to get out of this task. We usually set the default to 100 utterances because we would like to assess whether or not the utterances that came out is great to see if we can make changes in the future, keep a note of this.

* **Time allotted per assignment**: Maximum time a Worker has to work on a single task. Be generous so that Workers are not rushed. Default usually is set to 1 hour. 

* **Task expires in**: Maximum time your task will be available to Workers on Mechanical Turk. Default here usually get set to 7 days.

* **Auto-approve and pay Workers in**: This is the amount of time you have to reject a Worker's assignment after they submit the assignment. We usually set this to 6 hours.

> **_NOTE:_** `For Auto-approve and pay Workers in` make sure you download all the results before 6 hours timeframe because when it's auto approved the generation script used to convert the end result data to json will be limited to a short amount of utterances intended. To make it more clear when the task is completed you have 6 hours to download the results. Do not try to increase the auto approval time because it will tarnish your reputation to repeating workers meaning less eyes balls will be on your task.

Here is how this sections looks. 
![Alt text](./images/setting_task.png?raw=true)

#### Step 6: Worker requirements
These are the fields you will have to fill out. However, we usually keep them to default.
* **Require that Workers be Masters to do your tasks**: Do they need a masters to do complete your task?
* **Specify any additional qualifications Workers must meet to work on your tasks?**: 
* **Project contains adult content**: Yes/No

![Alt text](./images/worker_requirements.png?raw=true)

After filling in all the information, Click `Save`

#### Step 7: Design Layouts

![Alt text](./images/design_layout.png?raw=true)

This is what you will see when you click on `Design Layout`. This html template when rendered will be viewable to all workers that accepted your task. Here is where they will add their utterances.

We will be using this template instead so don't get too caught up on the default template.

```
<!-- You must include this JavaScript file -->
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>

<!-- For the full list of available Crowd HTML Elements and their input/output documentation,
      please refer to https://docs.aws.amazon.com/sagemaker/latest/dg/sms-ui-template-reference.html -->

<!-- You must include crowd-form so that your task submits answers to MTurk -->
<crowd-form answer-format="flatten-objects">

    <crowd-instructions link-text="View instructions" link-type="button">
        <short-summary>
            <p>Imagine you are talking about your feelings. What would you say?</p>
        </short-summary>

        <detailed-instructions>
            <h3>Talk about your feelings.</h3>
            <p>Talk as much about your feelings.</p>
        </detailed-instructions>

    </crowd-instructions>

    <p>What would you say?: <b>Please be natural. </b></p>

    <!-- Your contexts and intents will be substituted for the "context" and "intent" variables when you 
           publish a batch with an input file containing multiple contexts and intents -->
    <p><strong>Context: </strong>${context}</p>
    <p><strong>Intent: </strong>${intent}</p>

    <crowd-input name="utterance" placeholder="Type what you would say here..." required></crowd-input>
</crowd-form>
```

So let's explain in details the important bits of this template.

* **short-summary**: A short to the point summary of the task, be very specific as possible.
```
<short-summary>
    <p>Imagine you are talking about your feelings. What would you say?</p>
 </short-summary>
```

* **detailed-instructions**: Give more information about the task here

```
<detailed-instructions>
    <h3>Talk about your feelings.</h3>
    <p>Talk as much about your feelings.</p>
</detailed-instructions>
```

* **additional information**: Do not modify this, In a later section context and intent will be automatically filled. This is the section where the user will be prompt to enter the utterance.
```
    <p>What would you say?: <b>Please be natural. </b></p>
    <!-- Your contexts and intents will be substituted for the "context" and "intent" variables when you publish a batch with an input file containing multiple contexts and intents -->
    <p><strong>Context: </strong>${context}</p>
    <p><strong>Intent: </strong>${intent}</p>

    <crowd-input name="utterance" placeholder="Type what you would say here..." required></crowd-input>
```

#### Step 8: Preview and Finish 
![Alt text](./images/finish_preview.png?raw=true)

Click `finish` you will be redirected to the projects page.

#### Step 9: Publish Batch
![Alt text](./images/publish_batch.png?raw=true)

Click on `Publish Batch`, A model will pop up.

![Alt text](./images/modal.png?raw=true)

You will have to create a CSV file that have `context` and `intent` in it. In the CSV file the contents of it should look like the following. context will be the short summary you added from the above and the intent will be an intent you where initially creating or a short title choose any it doesn't matter really.

```
context,intent
Imagine you are speaking to a personal assistant about your feelings, document memory
```

> **_NOTE:_** You can use spreadsheet to create the csv with two columns one called context and the other is intent and save it as a CSV. Make sure you have the correct spelling and it matches these two required column or you can use any code editor and add the following. **DO NOT ADD ANY COMMAS TO THE CONTEXT IT WILL THROW AN ERROR**.

Now save the file and go back to webpage and click choose file and select the file you just created. Then proceed to click `Upload`. Your modal should look like the one below.

![Alt text](./images/valid_file.png?raw=true)


#### Step 10: Preview Tasks
Here is where you will preview and confirm that everything looks fine.

![Alt text](./images/preview_task.png?raw=true)

Once everything looks fine, click `Next`

#### Step 11: Confirm and Publish Batch 
Here you will confirm all billing information. Then click `Publish`

![Alt text](./images/confirm_and_publish.png?raw=true)

#### Step 12: Batch Progress
Here you will see the the progress of your task.
> **_NOTE:_** Sometimes it takes very long to meet 100% if it's 95%+ you can proceed to download the results. It's fine.

![Alt text](./images/progress.png?raw=true)

#### Step 13: Download Results
![Alt text](./images/result.png?raw=true)

After you see the task is 100%. Click on the result button that is highlighted above. You will be redirected to the page below and then proceed to click download.

![Alt text](./images/download_csv.png?raw=true)

You will be redirected to another page where you will click `here` which is highlighted blue, check the image below for reference.

![Alt text](./images/here.png?raw=true)

It will proceed to download all the results in a CSV file. That's the end of the crowdsourcing process. 
