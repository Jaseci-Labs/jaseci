---
title: Generating Text Embeddings with Different Models
---

# **Generate Embeddings (`gen_emb`)**
**`gen_emb`** is a module that provides an interface to generate text embeddings using different pre-trained language models. It supports multiple models, including BERT-based models, GPT-2, Sentence-BERT (SBERT), Universal Sentence Encoder (USE), and Universal Sentence Encoder for Question Answering (USE-QA). The module allows users to choose from a variety of models to generate embeddings for given texts.

This guide will walk you through the usage of APIs available for generating embeddings with the `gen_emb` module through Jac codes.

1. Import [Generate Embeddings (`gen_emb`)](#1-import-generate-embeddings-genemb-module-in-jac) module in Jac
2. [Generate Embeddings](#2-generate-embeddings)

## **Walkthrough**

### **1. Import `Generate Embeddings (gen_emb)` module in Jac**
1. Open the terminal and run Jaseci by executing the following command:
   > jsctl -m

2. Load the `gen_emb` module in Jac by executing the following command:
   > actions load module jac_nlp.gen_emb

### **2. Generate Embeddings**
To generate embeddings for a list of texts, you can use the `generate_embedding` API provided by the `gen_emb` module. The API allows you to choose a specific language model from the available options to generate embeddings.

* **Creating Jac Program (gen_emb)**
  1. Create a file named `gen_emb.jac`.

  2. Initialize walker functions for different models (`bi_enc`, `gpt2`, `sbert_sim`, `use_enc`, `use_qa`) and call the `generate_embedding` function:
     ```jac
     walker generate_embedding_bi_enc {
         can gen_emb.generate_embedding;
         report gen_emb.generate_embedding(
             ["This is a test text.", "Another test text."],
             "bi_enc"
         );
     }
     ```
     **Parameter Details**
     * `generate_embedding`: Generates text embeddings for a list of texts using the selected language model.
         * Input:
           * `texts` (list of strings): List of texts to generate embeddings for.
           * `selected_module` (string): The name of the selected language model (e.g., "use_enc", "use_qa", "gpt2", "sbert_sim", "bi_enc").
         * Return: A list of lists containing embeddings for each text.

  **Steps for Running `gen_emb.jac` Program**
  1. Build `gen_emb.jac` by executing the following command:
     > jac build gen_emb.jac

  2. Activate the Sentinel by executing the following command:
     > sentinel set -snt active:sentinel -mode ir gen_emb.jir

  3. Calling walker `generate_embedding_bi_enc` to generate embeddings using the `bi_enc` model by executing the following command:
     > walker run generate_embedding_bi_enc
