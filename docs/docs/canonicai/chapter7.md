# Build a conversational AI system in Jaseci

# Chapter 7

### Creating Test Cases
In this section we will explain to you the steps required to create test cases in the jac application for this application.

In the ``test.jac file`` we will test the VA and FAQ flow from the file ``tests.json`` in the data folder. First we will start off by creating an empty.

```
graph empty {
    has anchor root;
    spawn {
        root = spawn node::cai_root;
    }
}
```
This graph we will use for a base to do any query related tests.

```
test "testing faq and va flows"
with graph::empty by walker::init {
    flows = file.load_json("data/tests.json");
    // cai_root = *(global.cai_root);
    
    for flow in flows {

        for step in flow["flow"] {

            spawn here walker::talk(
                question=step["query"]
            );

            res = std.get_report();

            assert(res[-1] == step["response"]);
        }
    }
}
```
In test in jac we mainly use the key ``assert`` which checks two values and see whether it's true or false, if it's false the test will fail and if true the test will pass. In this case we us it to match against the response of the current query from the flow file to the response that comes back when data is being reported.

#### How to run test
This section will teach you how to run test. To run test use the following command below.

```
jac test [file_name in jac]
```

### Using Yield
In this section, we will show you how we utilize yield in this program.

#### What is Yield?
Yield is a way to temporarily suspend the walker and return/report to the user. When the same user calls the same walker, the walker context from previous call is retained and the walker will resume on the node it was going to go to next.

#### How is it being utilized in this application
```
if (interactive): std.out(response);
else: yield report response;
```
In the ``main.jac`` file you see that yield is being implemented. Let's explain this bit of code. If interactive is true everytime you send a query it will print the response to terminal and if it's false it would temporarily suspend the walker and report to the user the response for the query. A mini terminal below will show you an example of what you would see.


```
> I would like to test drive?
To set you up with a test drive, we will need your name and address.
```
When interactive is true

```
>  I would like to test drive?
{
  "success": true,
  "report": [
    "To set you up with a test drive, we will need your name and address."
  ],
  "final_node": "urn:uuid:50baeba7-b14a-4033-8c08-c0389f27bd53",
  "yielded": true
}
```
When interactive is false, yield comes into place.

### Global root_node
In this section, we will explain the architecture of the global root node and how it works in this application. The global root node in this case is the cai_root, it utilizes the use_enc (Universal Sentence Encoder) AI module.

#### How does it work?
```
node cai_root {
    has name = "cai_root";
    can use.text_classify;
    can categorize {
        res = use.text_classify(
            text=visitor.question,
            classes=[
                "i want to test drive",
                "I have a Model 3 reservation, how do I configure my order",
                "How do I order a tesla",
                "Can I request a Test Drive"
            ]
        );
        if (res["match_idx"] == 0):
            visitor.question_type = "va";

        else:
            visitor.question_type = "faq";
    }
}
```
As you can see here it uses the sentence encoding model (use.text_classify) function which intakes a query from the user and classes (in this case the questions from the FAQ), this enables it to check match ID and if match ID is equal to zero it will then set the question type to va (virtual assistance) and if it's not equal to zero it will set the question type to faq (frequent asked question) and this will be used for further used for processing, which will be explained next. Simple right, this is how it the categorizing of user query is done.

```
cai_root {
    if (question_type == "va"):
        take --> node::va_state;
    elif (question_type == "faq"):
        take --> node::faq_state;
}
```
In the ``main.jac`` file. It will utilize the question type variable to transition to the next node. As you can see if the question type is ``va`` it will transition to the va_state and if the question type is ``faq`` it will transition the to the faq state.
