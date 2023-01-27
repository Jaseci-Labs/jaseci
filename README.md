# Jaseci Docs and Guides

[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml/badge.svg)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Getting Started

- [Installing Jaseci](support/guide/getting_started/installation.md)
  - [Installing on Windows](support/guide/getting_started/installation.md#installing-on-windows)
  - [Installing on Mac](support/guide/getting_started/installation.md#installing-on-mac)
  - [Installing on Linux](support/guide/getting_started/installation.md#installing-on-linux)
  - [Installation for Contributors](support/guide/getting_started/installation.md#installation-for-contributors-of-jaseci)
- [Jaseci Quickstart](support/guide/getting_started/quickstart.md)
- [Setting Up Your Editor](support/guide/getting_started/setting_up_your_editor.md)
- [Writing Your First App](support/guide/getting_started/writing_your_first_app.md)
- [Understanding JAC Programs](support/guide/getting_started/understanding_jac_programs.md)

## Codelabs and Guides

- [Building a Conversational AI System](examples/CanoniCAI/CCAI_codelab.md)
  1. [Preparation and Background](examples/CanoniCAI/codelabs/1_preparation.md)
  2. [Automated FAQ Answering Chatbot](examples/CanoniCAI/codelabs/2_faq.md)
  3. [Multi-turn Dialogue System](examples/CanoniCAI/codelabs/3_dialogue_system.md)
  4. [Unify the Dialogue and FAQ Systems](examples/CanoniCAI/codelabs/4_unify_system.md)
  5. [Bring Your Application to Production](examples/CanoniCAI/codelabs/5_production.md)
  6. [Use speech to text and speech to text modules](examples/CanoniCAI/codelabs/6_speech2text_and_text2speech.md)
  7. [Collect Training Data via Crowdsource](examples/CanoniCAI/codelabs/7_crowdsource.md)
  8. [Contritbute to Jaseci Open Source](examples/CanoniCAI/codelabs/8.contributing_to_jaseci.md)
- [Build a Custom Jaseci Module](support/codelabs/custom_jaseci_module_codelab.md)
- [Stand Up an Jaseci Action Library Server](docs/docs/canonicai/chapter9.md)
- [Requests to APIs in Jac](docs/docs/canonicai/chapter8.md)
- [Testing CCAI Dialogues in Jac](docs/docs/canonicai/chapter7.md)
- [Package up Your Jac Program and Jaseci Server for Deployment](support/docker/how_to_package.md)
## The JAC Language Guide

- [Key Abstractions and Concepts](examples/CanoniCAI/codelabs/lang_docs/key_concepts.md)
  - [Graphs](examples/CanoniCAI/codelabs/lang_docs/graphs.md)
  - [Walkers](examples/CanoniCAI/codelabs/lang_docs/walkers.md)
    - [Walkers By Example](examples/CanoniCAI/codelabs/lang_docs/walkers_by_example.md)
  - [Abilities](examples/CanoniCAI/codelabs/lang_docs/abilities.md)
    - [`here` and `visitor`](examples/CanoniCAI/codelabs/lang_docs/here_visitor.md)
    - [Abilities By Example](examples/CanoniCAI/codelabs/lang_docs/abilities_by_example.md)
  - [Actions](examples/CanoniCAI/codelabs/lang_docs/actions.md)
    - [Actions By Example](examples/CanoniCAI/codelabs/lang_docs/actions_by_example.md)

## Jac Language Features

- [Main](docs/docs/Developing_with_JAC/Language_Feature.md)
  - [ControlFlow](docs/docs/Developing_with_JAC/Language_Features/ControlFlow.md)
  - [FileHnadling](docs/docs/Developing_with_JAC/Language_Features/FileHnadling.md)
  - [OOP](docs/docs/Developing_with_JAC/Language_Features/OOP.md)
  - [Operator](docs/docs/Developing_with_JAC/Language_Features/Operator.md)
  - [Data Types](docs/docs/Developing_with_JAC/Language_Features/dataTypes.md)
  - [Function](docs/docs/Developing_with_JAC/Language_Features/function.md)
  - [Globals](docs/docs/Developing_with_JAC/Language_Features/globals.md)
  - [Input/Output](docs/docs/Developing_with_JAC/Language_Features/input_output.md)
  - [Multipart](docs/docs/Developing_with_JAC/Language_Features/multipart.md)
  - [Report Custom](docs/docs/Developing_with_JAC/Language_Features/report_custom.md)
  - [Walker Callback](docs/docs/Developing_with_JAC/Language_Features/walker_callback.md)

## Standard Actions

  - [Alias](docs/docs/Developing_with_JAC/Language_Features/actions/alias.md)
  - [Date](docs/docs/Developing_with_JAC/Language_Features/actions/date.md)
  - [File](docs/docs/Developing_with_JAC/Language_Features/actions/file.md)
  - [Global](docs/docs/Developing_with_JAC/Language_Features/actions/global.md)
  - [Jaseci](docs/docs/Developing_with_JAC/Language_Features/actions/jaseci.md)
  - [Net](docs/docs/Developing_with_JAC/Language_Features/actions/net.md)
  - [Rand](docs/docs/Developing_with_JAC/Language_Features/actions/rand.md)
  - [Request](docs/docs/Developing_with_JAC/Language_Features/actions/request.md)
  - [Std](docs/docs/Developing_with_JAC/Language_Features/actions/std.md)
  - [Vectors](docs/docs/Developing_with_JAC/Language_Features/actions/vectors.md)
  - [Walker](docs/docs/Developing_with_JAC/Language_Features/actions/walker.md)
  - [Elastic](docs/docs/Developing_with_JAC/Language_Features/actions/elastic.md)

## Jaseci AI Library Reference

- [Jaseci AI Kit Overview](jaseci_ai_kit/README.md)
  - [Jaseci NLP features](jaseci_ai_kit/jac_nlp/README.md)
    - [CL Summarization](jaseci_ai_kit/jac_nlp/jac_nlp/cl_summer/README.md)
    - [Bart Summarization](jaseci_ai_kit/jac_nlp/jac_nlp/bart_sum/README.md)
    - [T5 Summarization](jaseci_ai_kit/jac_nlp/jac_nlp/t5_sum/README.md)
    - [Bi-Encoder](jaseci_ai_kit/jac_nlp/jac_nlp/bi_enc/README.md)
    - [FLair NER](jaseci_ai_kit/jac_nlp/jac_nlp/ent_ext/README.md)
    - [Fasttext Classifier](jaseci_ai_kit/jac_nlp/jac_nlp/fast_enc/README.md)
    - [Text Segmenter](jaseci_ai_kit/jac_nlp/jac_nlp/text_seg/README.md)
    - [Transformer NER](jaseci_ai_kit/jac_nlp/jac_nlp/tfm_ner/README.md)
    - [USE Encoder](jaseci_ai_kit/jac_nlp/jac_nlp/use_enc/README.md)
    - [USE QA](jaseci_ai_kit/jac_nlp/jac_nlp/use_qa/README.md)
    - [ZS Classifier](jaseci_ai_kit/jac_nlp/jac_nlp/zs_classifier/README.md)
    - [Topic Extraction](jaseci_ai_kit/jac_nlp/jac_nlp/topic_ext/README.md)
    - [BI Encoder for NER](jaseci_ai_kit/jac_nlp/jac_nlp/bi_ner/README.md)
    - [SBERT Similarity](jaseci_ai_kit/jac_nlp/jac_nlp/sbert_sim/README.md)

  - [Jaseci Speech Features](jaseci_ai_kit/jac_speech/README.md)

    - [Speech2Text](jaseci_ai_kit/jac_speech/jac_speech/stt/README.md)
    - [Text2Speech](jaseci_ai_kit/jac_speech/jac_speech/tts/README.md)

  - [Jaseci miscellaneous AI features](jaseci_ai_kit/jac_misc/README.md)
    - [Clustering](jaseci_ai_kit/jac_misc/jac_misc/cluster/README.md)
    - [Personalized Head](jaseci_ai_kit/jac_misc/jac_misc/ph/README.md)
    - [Translator](jaseci_ai_kit/jac_misc/jac_misc/translator/README.md)

- [Guide to use Jaseci AI Kit](jaseci_ai_kit/support/guide-to-use-ai-kit.md)
- [Guide to create Jaseci AI Kit Test Cases](jaseci_ai_kit/README.md)

## Jaseci Studio and UI Widget Library

- [Jaseci Studio Features](jaseci_studio/features.md)
- [Jaseci UI Kit](ui_components/readme.md)
  - [Introduction](ui_components/docs/what-is-jaseci-ui-kit.md)
  - [Basic Concepts](ui_components/docs/basic-concepts.md)
  - [Built-in Actions](ui_components/docs/built-in-actions.md)
  - [Connecting an API](ui_components/docs/connecting-an-api.md)

## Jaseci X Features
- [Stripe Integration](jaseci_serv/jaseci_serv/jsx_stripe/README.md)
- [Single Sign-on Socail](jaseci_serv/jaseci_serv/jsx_oauth/README.md)

## Jaseci Core Internals

- [Services/JsOrc](jaseci_core/jaseci/svc/README.md)
  - [Task](jaseci_core/jaseci/svc/task/README.md)
  - [Mail](jaseci_core/jaseci/svc/mail/README.md)
- [JSORC Action Management Engine](jaseci_core/jaseci/svc/JSORC.md)

## Contributing to Jaseci

- [Guide on Contributing](examples/CanoniCAI/codelabs/8.contributing_to_jaseci.md)
- [Being an Contributor](support/guide/other/contributor_policy.md)
- [General Guide](CONTRIBUTING.md)
- [Contributors](CONTRIBUTORS.md)

## Documenation TODOs

- [Stuff that needs docs](support/guide/other/DOCTODOS.md)

## Other Resources

- [About this Release](CHANGELOG.md)
- [Archived Notes](NOTES.md)
- [Join our Community](https://forum.jaseci.org/)
- [Online Documentation](https://docs.jaseci.org/)
- [The Jaseci Bible](https://github.com/Jaseci-Labs/jaseci_bible/blob/main/pdf/jaseci_bible.pdf)
- [Our Website](https://jaseci.org/)
  - [Learn more at the Dojo](https://jaseci.org/dojo)
  - [Products Built with Jaseci](https://jaseci.org/products/)
  - [Jaseci in the News](https://jaseci.org/blog/)
  - [Contact Us](https://jaseci.org/contact-us/)

## Misc DevOps Guides
- [Install Jaseci using Helm](support/helmcharts/jaseci/README.md)
- [Create AWS EKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/aws/README.md)
- [Create Azure AKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/azure/README.md)
- [Locust Load Test for JASECI](support/locust/README.md)
- [Setting up Monitoring for JASECI](support/monitoring/README.md)