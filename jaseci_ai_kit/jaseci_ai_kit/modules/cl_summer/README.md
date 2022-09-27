# **Summarizer (`cl_summer`)**

Module `cl_summer` uses the `sumy summarizer` to extract summary from text.

1. Import [`cl_summer`](#1-import-summarizer-cl_summer-module-in-jac) module in jac
2. [Summarizer](#2-summarizer)

# **Walk through**

## **1. Import Summarizer (`cl_summer`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load cl_summer module in jac by command
    ```
    actions load module jaseci_ai_kit.cl_summer
    ```


## **2. Summarizer**
For this tutorial, we are going to leverage the **Summarizer** (`cl_summer`) which would help us to generate summary of the provided text.

* Creating Jac Program for **summarizer** (`cl_summer`)

    1. Create a file by name summarizer.jac
    2. Create node model_dir and `summarizer` in `summarizer.jac` file.

        ```
        node model_dir;
        node summarizer{};
        ```
    3. Initializing node `summarizer` and import `cl_summer.summarize` ability inside node `summarizer`.

        ```
        # import ability
        can cl_summer.summarize;
        ```

    4. Initialize module `summarize` inside `summarizer` node.

        ```python
        # summarizer
        can summarize with summarizer entry{
            data = file.load_json(visitor.data);
            
            report cl_summer.summarize(
                text = data["text"],
                url = data["url"],
                sent_count = data["sent_count"],
                summarizer_type = data["summarizer_type"]
                );      
        }
        ```
        `summarize`: to get the extractive summary of the text in the given number of sentence counts .

        **Parameter details**

        * **Input Data**
        
            **data.json** file
            ```
            {
                "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and   rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail.', But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as, he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there.",
                "url": "none",
                "sent_count": 5,
                "summarizer_type": "LsaSummarizer"
            }
            ```
            * `text(String)`: text the contain the entire context
            * `url(String)`: the link to the webpage
            * `sent_count(int)`: number of sentence you want in the summary
            * `summarizer_type(String)`: name of the summarizer type, available options are:
                * LsaSummarizer
                * LexRankSummarizer
                * LuhnSummarizer

        * **Output**
        List of Sentences that best summarizes the context

    5. Adding edge name of `summ_model` in `summarizer.jac` file for connecting nodes inside graph.
        ```
        # adding edge
        edge summ_model {
            has model_type;
        }
        ```
    6. Adding graph name of `summ_graph` for initializing node.
        ```python
        # adding graph
        graph summ_graph {
            has anchor summ_model_dir;
            spawn {
                summ_model_dir = spawn node::model_dir;
                summarizer_node = spawn node::summarizer;
                summ_model_dir -[summ_model(model_type="summarizer")]-> summarizer_node;
            }
        }
        ```
    7. Initializing walker init for calling graph.
        ```
        walker init {
            root {
            spawn here --> graph::summ_graph; 
            }
        }
        ```
    8. Creating walker name of `summarizer` for getting parameter from context or default and calling ability `summarize`.
        ```python
        # declaring walker for summerize text
        walker summarizer{
            has data="data.json";

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
        **Final summarizer.jac program**
        ```python
        node model_dir;
        node summarizer{
            # import ability
            can cl_summer.summarize;

            # summarizer
            can summarize with summarizer entry{
                data = file.load_json(visitor.data);
                
                report cl_summer.summarize(
                    text = data["text"],
                    url = data["url"],
                    sent_count = data["sent_count"],
                    summarizer_type = data["summarizer_type"]
                    );      
            }
        }

        # adding edge
        edge summ_model {
            has model_type;
        }

        # adding graph
        graph summ_graph {
            has anchor summ_model_dir;
            spawn {
                summ_model_dir = spawn node::model_dir;
                summarizer_node = spawn node::summarizer;
                summ_model_dir -[summ_model(model_type="summarizer")]-> summarizer_node;
            }
        }

        # declaring init walker
        walker init {
            root {
            spawn here --> graph::summ_graph; 
            }
        }

        # declaring walker for summerize text
        walker summarizer{
            has data="data.json";

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }    
        ```
    * **Steps for running `summarizer.jac` program**

        * Execute the follow command for Build `summarizer.jac`

            ```
            jac build summarizer.jac
            ```
        * Execute the follow command to Activate sentinal

            ```
            sentinel set -snt active:sentinel -mode ir summarizer.jir
            ```
        * Execute the walker `summarizer` with default parameter for `summarizer(cl_summer)` module by following command
            ```
            walker run summarizer
            ```
        * After executing walker `summarizer` result data will show on console.

            **Result**
            ```
             "report": [
                        [
                        "The King of England was at war with him and had led a great army into Scotland to drive him out of the land.",
                        "At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains.",
                        "One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him.",
                        "As he lay thinking, he saw a spider over his head making ready to weave her web.",
                        "Bruce almost forgot his own troubles as, he watched her swing herself out upon the slender line."
                        ]
                    ]
            ```