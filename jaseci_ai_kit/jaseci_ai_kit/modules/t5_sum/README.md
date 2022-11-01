# **Summarization(`t5_sum`)**

Module `t5_sum` uses the hugging face T5 transformer model to provide abstractive summary from text.

1. Import [`t5_sum`](#1-import-summarizer-t5_sum-module-in-jac) module in jac
2. [Summarization](#2-summarization)

# **Walk through**

## **1. Import Summarizer (`t5_sum`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load cl_summer module in jac by command
    ```
    actions load module jaseci_ai_kit.t5_sum
    ```


## **2. Summarization**
For this tutorial, we are going to leverage the **Summarizer**(`t5_sum`) which would generate the summary from text. 

* Creating Jac Program for **summarizer** (`t5_sum`)

    1. Create a file by name summarizer.jac
    2. Create node model_dir and `summarizer` in `summarizer.jac` file.

        ```
        node model_dir;
        node summarizer{};
        ```
    3. import `t5_sum.classify_text` ability inside node `summarizer`.

        ```
        # import ability
        can t5_sum.classify_text;
        ```

    4. Initialize module `summarize` inside `summarizer` node.

        ```python
        # summarizer
        can summarize with summarizer entry{
            data = file.load_json(visitor.dataset);
            report t5_sum.classify_text(
                text = data["text"],
                min_length = data["min_length"],
                max_length = data["max_length"]
                );
        }
        ```
        `classify_text`: use the T5 model to summarize a body of text

        **Parameter details**
        * **Input Data**  **`dataset.json`** file

            ```
            {
                "text": "The US has passed the peak on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month. The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world. At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors. We'll be the comeback kids, all of us, he said. We want to get our country back. The Trump administration has  previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.",
                "min_length": 30,
                "max_length": 100
            }
            ```
            * `text (string)`: text to summarize
            * `min_length (integer):` the least amount of words you want returned from the model
            * `max_length (integer):` the most amount of words you want returned from the model

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
            has dataset="dataset.json";

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
        **Final get_seg.jac program**
        ```python
        node model_dir;
        node summarizer{
            # import ability
            can t5_sum.classify_text;

            # summarizer
            can summarize with summarizer entry{
                data = file.load_json(visitor.dataset);
                
                report t5_sum.classify_text(
                    text = data["text"],
                    min_length = data["min_length"],
                    max_length = data["max_length"]
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

        walker init {
            root {
            spawn here --> graph::summ_graph; 
            }
        }

        # declaring walker for summerize text
        walker summarizer{
            has dataset="data.json";

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
                            "the president predicts some states will reopen this month. the country has over 637,000 confirmed cases and over 30,826 deaths, the highest for any country in the world. we'll be the comeback kids, all of us."
                        ]
            ```