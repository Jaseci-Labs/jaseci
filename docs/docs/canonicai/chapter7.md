# Build a conversational AI system in Jaseci

# Chapter 7

### Creating Test Cases
In this section we will explain to you the steps required to create test cases in the jac application for this application.

There are multiple ways in creating test in jac and we will explore two ways and each is as follows:

#### Test 1
In the ``test.jac file`` we will test the VA and FAQ flow from the file ``tests.json`` in the data folder.

```
walker empty {}
```
An empty walker was created to host the loading of the test suite json file. So we can run multiple walker based on the file on top of this walker.

```
test "testing faq and va flows"
```
This is how we label a test. This must go on top on of an unit test.

```
with graph::tesla_sales_rep by walker::empty {}
```
Here we referenced the graph we will be running the test on and which walker will run on top of this graph. This is how we start to create the test.

```
std.get_report();
```
This line of code returns the data returned from a report statement in a walker. This will be very important statement to use in testing.

```
assert(value_1, value_2);
```
In test in jac we mainly use the key ``assert`` which checks two values and see whether it's true or false, if it's false the test will fail and if true the test will pass. In this case we us it to match against the response of the current query from the flow file to the response that comes back when data is being reported.


In the next section which is very important, we will be modifying the `talk` walker so it can allow us to test multiple flows in one test without sharing contexts to other new conversations.

More specifically why we need to modify the `talk` walker because, it houses `yield` (will be explained in the next section) which in this case it retains the context of the walker and we are building a dynamic test file that houses many conversation flow.

We added a key to the walker called `retain_context`, when set to `false` it will walk through the graph and automatically unset the yield.
```
walker talk {
    has question, interactive = false; has retain_context = true;
    has wlk_ctx = {
        "intent": null,
        "entities": {},
        "prev_state": null,
        "next_state": null,
        "respond": false
    };
    has response;
    root {
        take --> node::dialogue_root;
    }
    cai_state {
        if(retain_context){
            if (!question and interactive) {
                question = std.input("Question (Ctrl-C to exit)> ");
                here::init_wlk_ctx;
            } elif (!question and !interactive){
                std.err("ERROR: question is required for non-interactive mode");
                disengage;
            }
            here::nlu;
            here::process;
            if (visitor.wlk_ctx["respond"]) {
                here::nlg;
                if (interactive): std.out(response);
                else {
                    yield report response;
                    here::init_wlk_ctx;
                }
                question = null;
                take here;
            } else {
                take visitor.wlk_ctx["next_state"] else: take here;
            }
        }else{
            take -->;
        }
    }
}
```
So let's get to the test file. This test will
```
test "testing va flows"
with graph::tesla_sales_rep by walker::empty {
    flows = file.load_json("[LOCATION OF TEST FILE].json");

    for flow in flows {

        for s, step in flow["flow"] {
           spawn here walker::talk(question = step["query"], retain_context=true);
                res = std.get_report();

                std.log("HERE >>> ", step["query"] , " ==== ", res[-1]);

                assert(res[-1] == step['response']);

                if((s+1) == flow['flow'].length){
                    spawn here walker::talk(retain_context=false);
                }
        }
    }
}
```
Here is the entire test. Essentially, the purpose of this test is to load the test suite with all the flow in a json file and pass each query from the test suite to the walker `talk` and from the response check if it matched the data from the test suite. If it matches the test will pass if not it will fail.

#### Test 2
```
test "testing a single query"
with graph::tesla_sales_rep by walker::talk(question="Hey I would like to go on a test drive")
{
    res = std.get_report();
    assert(res[-1] == "To set you up with a test drive, we will need your name and address.");
}
```
In this test the only difference from the test above is that we are utilizing a walker that have parameters. This test allow us to test for a single query.

#### How to run test
This section will teach you how to run test. To run test use the following command below.

```
jac test test.jac
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
In the ``main.jac`` file you see that yield is being implemented. Let's explain this bit of code. If interactive is true everytime you send a query it will print the response to terminal and if it's false it would temporarily suspend the walker and report to the user the response for the query. Below you will see an example.

```
> I would like to test drive?
To set you up with a test drive, we will need your name and address.
```
When interactive is true (this is in the terminal). If you exited out and return to the program it will lose context and will restart from the beginning.

```
I would like to test drive?

{
  "success": true,
  "report": [
    "To set you up with a test drive, we will need your name and address."
  ],
  "final_node": "urn:uuid:50baeba7-b14a-4033-8c08-c0389f27bd53",
  "yielded": true
}
```
When interactive is false, yield comes into place. So if we had to pass another query it will remember the last state it was at and will act accordingly.

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
