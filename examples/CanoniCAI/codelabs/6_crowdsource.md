# Collect Training Data via Crowdsource

### Introduction
The performance of an AI model depends heavily on the training data.
Collecting and curating training data is a crucial step in improving the performance of your AI models.
In this section, we will walk through how to crowdsource training data via Amazon Mechanical Turk (mturk for short).

#### Step 1: Register as a Amazon Mechnical Turk requester
You will need to apply to be a requester to crowdsource data via mturk.
You can use existing AWS account or create a new account for mturk at [here](https://requester.mturk.com/signin_options).
The requester application process can take a couple of days to be approved so plan ahead.

#### Step 2: Sign In
When you sign into the requester account for amazon. Click on `New Project`.

![Alt text](../images/mturk/new_project.png?raw=true)

#### Step 3: Selecting Templates
You will need to select a customizable template to start a new project. In our case scenerio, we will choose the option to `collect utterance`. It will be highlighted in yellow in the image below, after you click on `collect utterance`, then proceed to click `Create Project`.

![Alt text](../images/mturk/collect_utterance.png?raw=true)

#### Step 4: Enter Properties
You will be redirected to the project page where you will specify the following.

> **_NOTE:_**  Make sure you follow instructions in this section properly because what you enter here will affect the quality of data you get from the crowd.

* **Project Name**: The name of the project 
* **Title**: A short to the point title of the task, be very specific as possible
* **Description**: Give more information about the task here
* **Keywords**: Keywords that will enable the general public or workers to find your task

 Try to be brief and concise with the description because most workers will skim through the task given. 

Here is how the form will look like.

![Alt text](../images/mturk/edit_project.png?raw=true)

#### Step 5: Setting up your task
> **_NOTE:_** The settings here decide the compensation for the crowd worker.

* **Reward per assignment**: This is how much a Worker will be paid for completing an assignment. Consider how long it will take a Worker to complete each assignment. As a default we usually assign this to `$0.05`

* **Number of assignments per task**: How much utterances you would like at the end to get out of this task. We usually set the default to 100 utterances because we would like to assess whether or not the utterances that came out is great to see if we can make changes in the future.

* **Time allotted per assignment**: Maximum time a Worker has to work on a single task. Be generous so that Workers are not rushed. The defaul 1 hour generally works well here. 

* **Task expires in**: Maximum time your task will be available to Workers on Mechanical Turk. The default 7 days usually works well here.

* **Auto-approve and pay Workers in**: This is the amount of time you have to reject a Worker's assignment after they submit the assignment.

Putting it together.
![Alt text](../images/mturk/setting_task.png?raw=true)

#### Step 6: Worker requirements
You can customize who can work on your mturk job by specifying additional requirements.
Usually, the default settings here work well for most data collection need.

![Alt text](../images/mturk/worker_requirements.png?raw=true)

After filling in all the information, Click `Save`

#### Step 7: Design Layouts

![Alt text](../images/mturk/design_layout.png?raw=true)

This is what you will see when you click on `Design Layout`. This html template when rendered will be viewable to all workers that accepted your task. Here is where they will add their utterances.

Below is a template you can use for collecting utterances for classification.
You can build off this to tweak it for other NLP tasks.

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
![Alt text](../images/mturk/finish_preview.png?raw=true)

Click `finish` you will be redirected to the projects page.

#### Step 9: Publish Batch
![Alt text](../images/mturk/publish_batch.png?raw=true)

Click on `Publish Batch`, A model will pop up.

![Alt text](../images/mturk/modal.png?raw=true)

You will need to create a CSV file that have `context` and `intent` in it.
These two fields will be used to replace the placeholder in the template html above and generate the actual view for the workers. 

```
context,intent
Imagine you are asking about today's weather what would you say, ask_weather
```

> **_NOTE:_** You can use spreadsheet to create the csv with two columns one called context and the other is intent and save it as a CSV. Make sure you have the correct spelling and it matches these two required column or you can use any code editor. **DO NOT ADD ANY COMMAS TO THE CONTEXT IT WILL THROW AN ERROR**.

Now save the file and go back to webpage and click choose file and select the file you just created. Then proceed to click `Upload`. Your modal should look like the one below.

![Alt text](../images/mturk/valid_file.png?raw=true)


#### Step 10: Preview Tasks
Here is where you will preview and confirm that everything looks fine.

![Alt text](../images/mturk/preview_task.png?raw=true)

Once everything looks fine, click `Next`

#### Step 11: Confirm and Publish Batch 
Here you will confirm all billing information. Then click `Publish`

![Alt text](../images/mturk/confirm_and_publish.png?raw=true)

#### Step 12: Batch Progress
Here you will see the the progress of your task.
> **_NOTE:_** Sometimes the last few percentage takes much longer to finish than the rest therefore it can take very long to reach 100%. You can download the result without it hitting 100%

![Alt text](../images/mturk/progress.png?raw=true)

#### Step 13: Download Results
![Alt text](../images/mturk/result.png?raw=true)

Click on the result button that is highlighted above. You will be redirected to the page below and then proceed to click download.

![Alt text](../images/mturk/download_csv.png?raw=true)

You will be redirected to another page where you will click `here` which is highlighted blue, check the image below for reference.

![Alt text](../images/mturk/here.png?raw=true)

It will proceed to download all the results in a CSV file.
