# **Text Segmenter (text_seg)**

Module `text_seg` implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.

1. Import [`text_seg`](#1-import-text_segementer-text_seg-module-in-jac) module in jac
2. Get [segments](#2-get-segments)

# **Walk through**

## **1. Import text_segementer (`text_seg`) module in jac**
1. For executing jaseci Open terminal and run follow command.
    ```
    jsctl -m
    ```
2.  Load `text_seg` module in jac by command
    ```
    actions load module jaseci_ai_kit.text_seg
    ```


## **2. Get segments**
For this tutorial, we are going to leverage the **text segmenter** (`text_seg`) for the purpose of text segmentation, 

* Creating Jac Program **text segmenter** (`text_seg`)

    1. Create a file by name **`segment.jac`**
    2. Create node model_dir and `text_seg` in `segment.jac` file.

        ```
        node model_dir;
        node text_seg{};
        ```
    3. Initializing node text_seg and import `text_seg.load_model` and `text_seg.get_segments` ability inside node `text_seg`.

        ```
        # import ability
        can text_seg.load_model, text_seg.get_segments;
        ```

    4. Initialize module `load_model` and `get_segments` inside `get_seg` node.

        ```python
        # loading model 
        can load_model with text_segment entry{
            text_seg.load_model(
                model_name = visitor.model_name
            );
        }

        # text segmentation
        can get_segments with text_segment entry{
            data = file.load_json(visitor.data);
            
            report text_seg.get_segments(
                text = data["text"],
                threshold = data["threshold"]
            );      
        }
        ```
        `load_model` to load the available model for text segmentation.
        `get_segements`: gets different topics in the context provided, given a threshold

        **Parameter details**
        * Input
            * `model_name(String)`: name of the transformer model to load, options are:
                * `wiki` : trained on wikipedia data
                * `legal`: trained on legal documents

            * **Input Data**

                ```
                {
                    "text": "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains. One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. 'Poor thing,' said Bruce: 'you, too, know what it is to fail. But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time. Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there.",
                    "threshold": 0.65
                }
                ```
                * `text(String)`: text the contain the entire context 
                * `threshold(Float)`: range is between 0-1, make each sentence as segment if, threshold is 1.

            * **Output**
            List of Sentences that best summarizes the context

    5. Adding edge name of `seg_model` in `segment.jac` file for connecting nodes inside graph.
        ```
        # adding edge
        edge seg_model {
            has model_type;
        }
        ```
    6. Adding graph name of `text_seg_graph` for initializing node.
        ```
        graph text_seg_graph {
            has anchor seg_model_dir;
            spawn {
                seg_model_dir = spawn node::model_dir;
                text_seg_node = spawn node::text_seg;
                seg_model_dir -[seg_model(model_type="text_seg")]-> text_seg_node;
            }
        }
        ```
    7. Initializing walker init for calling graph.
        ```
        walker init {
            root {
            spawn here --> graph::text_seg_graph; 
            }
        }
        ```
    8. Creating walker name of `text_segment` for getting parameter from context or default and calling ability `load_model` and `get_segments`.
        ```python
        # declaring walker for summerize text
        walker text_segment{
            has model_name="wiki";
            has data="text.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
        **Final `segment.jac` program**
        ```python
        node model_dir;
        node text_seg{
            # import all module ability
            can text_seg.load_model, text_seg.get_segments;

            # loading model 
            can load_model with text_segment entry{
                text_seg.load_model(
                    model_name = visitor.model_name
                );
            }

            # text segmentation
            can segment with text_segment entry{
                data = file.load_json(visitor.data);
                
                report text_seg.get_segments(
                    text = data["text"],
                    threshold = data["threshold"]
                );      
            }
        }



        # adding edge
        edge seg_model {
            has model_type;
        }

        # adding graph
        graph text_seg_graph {
            has anchor seg_model_dir;
            spawn {
                seg_model_dir = spawn node::model_dir;
                text_seg_node = spawn node::text_seg;
                seg_model_dir -[seg_model(model_type="text_seg")]-> text_seg_node;
            }
        }

        # declare init graph
        walker init {
            root {
            spawn here --> graph::text_seg_graph; 
            }
        }


        # declaring walker for summerize text
        walker text_segment{
            has model_name="wiki";
            has data="text.json";    

            root {
                take --> node::model_dir;
            }
            model_dir {
                take -->;
            }
        }
        ```
    * **Steps for running `segment.jac` program**

        * Execute the follow command for Build `segment.jac`

            ```
            jac build segment.jac
            ```
        * Execute the follow command to Activate sentinal

            ```
            sentinel set -snt active:sentinel -mode ir segment.jir
            ```
            **Note**: If getting error **`ValueError: badly formed hexadecimal UUID string`** execute only once
            > sentinel register -set_active true -mode ir segment.jir

        * Execute the walker `text_segment` with default parameter for `text segmentation (text_seg)` module by following command
            ```
            walker run text_segment
            ```
            After executing walker `text_segment` result data will show on console.

            **Result**
            ```
            "report": [
                        [
                            "There was once a king of Scotland whose name was Robert Bruce. He needed to be both brave and wise because the times in which he lived were wild and rude. The King of England was at war with him and had led a great army into Scotland to drive him out of the land. Battle after battle had been fought. Six times Bruce had led his brave little army against his foes and six times his men had been beaten and driven into flight. At last his army was scattered, and he was forced to hide in the woods and in lonely places among the mountains.",
                            "One rainy day, Bruce lay on the ground under a crude shed listening to the patter of the drops on the roof above him. He was tired and unhappy. He was ready to give up all hope. It seemed to him that there was no use for him to try to do anything more. As he lay thinking, he saw a spider over his head making ready to weave her web. He watched her as she toiled slowly and with great care. Six times she tried to throw her frail thread from one beam to another, and six times it fell short. ' Poor thing,' said Bruce: 'you, too, know what it is to fail. But the spider did not lose hope with the sixth failure. With still more care, she made ready to try for the seventh time.",
                            "Bruce almost forgot his own troubles as he watched her swing herself out upon the slender line. Would she fail again? No! The thread was carried safely to the beam and fastened there."
                    ]
            ```