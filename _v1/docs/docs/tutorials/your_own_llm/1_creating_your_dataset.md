---
sidebar_position: 1
title: Creating your dataset
description: How to create your own Instruction dataset
---
## How to Create a Dataset for your LLM

Creating a high-quality dataset is a crucial step in training your own LLM using the Jaseci platform. A well-curated dataset ensures that your model captures the desired language patterns and context relevant to your specific application. In this section, we will explore different ways to create datasets and provide an example using the Alpaca Cleaned format, which is supported by Jac NLP's LLM.

1. Pre-existing Datasets: One way to create a dataset is by utilizing pre-existing datasets available in the desired domain. These datasets can be obtained from various sources such as academic research, open data repositories, or domain-specific collections. Some popular pre-existing datasets for language modeling include the OpenAI GPT dataset, the Common Crawl dataset, or domain-specific corpora like medical or legal texts.

2. Web Scraping: Web scraping involves extracting text data from websites. It allows you to create a dataset specific to your application or domain. You can write scripts or use tools like Beautiful Soup or Scrapy to scrape text from web pages, blogs, forums, or social media platforms. However, when web scraping, it is essential to respect the website's terms of service and follow ethical guidelines.

3. User-Generated Content: User-generated content from platforms such as online forums, social media, or customer reviews can be a valuable source for creating datasets. You can collect and filter relevant text data from these sources to train your LLM. Keep in mind that user-generated content may contain noise or biases, so careful preprocessing and filtering are necessary.

4. Crowdsourcing: Crowdsourcing platforms like Amazon Mechanical Turk or Figure Eight allow you to create datasets by outsourcing the annotation or collection of text data. You can design tasks to gather specific types of text or annotate existing text with labels or sentiment. Crowdsourcing provides a scalable and cost-effective way to create datasets, but quality control and guidelines are crucial to ensure accurate annotations.

5. Domain-Specific Apps or Games: Developing small applications or games that capture specific language patterns or behaviors can be an interactive and engaging way to collect data. These apps can prompt users to generate text, provide feedback, or engage in dialogue, resulting in a dataset that aligns with your application's requirements.


**Example: Alpaca Cleaned Format**

The [Alpaca Cleaned](https://github.com/gururise/AlpacaDataCleaned) format is a dataset used in the Jac NLP's LLM module. It contains instructions from various domains, cleaned and organized for training LLMs. The format typically includes text examples with corresponding labels or metadata if applicable. For instance:

```json
[
    {
        "instruction": "Give three tips for staying healthy.",
        "input": "",
        "output": "1.Eat a balanced diet and make sure to include plenty of fruits and vegetables. \n2. Exercise regularly to keep your body active and strong. \n3. Get enough sleep and maintain a consistent sleep schedule."
    },
    {
        "instruction": "Convert the following sentence into the present continuous tense",
        "input": "He reads books",
        "output": "He is reading books."
    }
]
```

The Alpaca Cleaned format provides a structured representation of instructions with associated domains and labels. This format facilitates the training process and ensures that the LLM can learn and generate text within specific domains or tasks.

When creating your dataset, consider the specific requirements of your application and the type of language patterns you want your LLM to capture. Design your data collection or annotation process accordingly to ensure that the dataset is diverse, representative, and aligns with the task your LLM will perform.

Remember to properly clean and preprocess the dataset by removing irrelevant or noisy text, standardizing formats, and ensuring data consistency. This prepares the dataset for effective training and improves the overall performance of your LLM.

## Creating a Dataset for your LLM

The Jaseci platform provides a convenient way to create and manage datasets for your LLM. Run the following command in JSCTL to run the GUI. Make sure to have jaseci, jac_nlp[llm], streamlit are installed. if not, run `pip install jaseci jac_nlp[llm] streamlit` to install them.

```bash
jaseci> actions load module jac_nlp.llm
jaseci> actions call llm.run_dataset_builder

  You can now view your Streamlit app in your browser.

  Network URL: http://172.31.46.187:8501
  External URL: http://34.211.22.126:8501

# You can use the Network or External URL to access the GUI from your browser. Press Ctrl+C to stop the GUI. and exit the JSCTL shell when you are done.
```

## References
- [HuggingFace Datasets for Text Generation](https://huggingface.co/datasets?task_categories=task_categories:text-generation&sort=downloads)
- [Alpaca Cleaned Dataset](https://github.com/gururise/AlpacaDataCleaned)