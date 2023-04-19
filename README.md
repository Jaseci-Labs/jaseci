<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://www.jaseci.org/wp-content/uploads/2022/02/jaseki-logo-inverted-rgb.svg" alt="Jaseci" width="50%" />
</div>


# Jaseci: Build the Next Generation of AI Products at Scale

[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-core-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml/badge.svg)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci-serv-test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
[![Jac NLP](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-nlp-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-nlp-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_nlp/)](https://pypi.org/project/jac-nlp)
[![Jac Vision](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-vision-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-vision-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_vision/)](https://pypi.org/project/jac-vision)
[![Jac Speech](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-speech-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-speech-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_speech/)](https://pypi.org/project/jac-speech)
[![Jac Misc](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-misc-test.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jac-misc-test.yml)  [![PyPi version](https://badgen.net/pypi/v/jac_misc/)](https://pypi.org/project/jac-misc)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Introduction

- [What and Why Jaseci?](docs/docs/introduction.md)

# Getting Started

  - [Installation](docs/docs/getting_started/1_installation.md)
    - [Setting Up Windows](docs/docs/getting_started/1_installation.md#windows-setup)
    - [Install Jaseci in Debian or WSL2](docs/docs/getting_started/1_installation.md#install-jaseci-in-debian-or-wsl2)
    - [Install Jaseci on MacOS](docs/docs/getting_started/1_installation.md#install-jaseci-on-macos)
  - [Setting Up Your Editor](docs/docs/getting_started/2_setting_up_code_editor.md)
  - [Setting Up Jaseci Server](docs/docs/getting_started/3_setup_jaseci_serv.md)
  - [Installing Jaseci Studio](jaseci_studio/README.md) <!-- Should update more information on this images,etc -->
  - [Write your first Jaseci Application](docs/docs/getting_started/5_write_your_first_app.md) <!-- Should update more explanation on this code -->
  - [Learn More](README.md#appendix)

# Examples and Tutorials

- [Quickstart](docs/examples_and_tutorials/quickstart/quickstart.md)
  - [Understanding Jac Application](docs/examples_and_tutorials/quickstart/understanding_jac_programs.md)
  - [Write your First Jac Application](docs/examples_and_tutorials/quickstart/writing_your_first_app.md)
- [Building a Conversational AI](docs/examples_and_tutorials/CanoniCAI/CCAI_codelab.md)
  - [Preparation and Background](docs/examples_and_tutorials/CanoniCAI/codelabs/1_preparation.md)
  - [Automated FAQ Answering Chatbot](docs/examples_and_tutorials/CanoniCAI/codelabs/2_faq.md)
  - [Multi-turn Dialogue System](docs/examples_and_tutorials/CanoniCAI/codelabs/3_dialogue_system.md)
  - [Unify the Dialogue and FAQ Systems](docs/examples_and_tutorials/CanoniCAI/codelabs/4_unify_system.md)
  - [Bring Your Application to Production](docs/examples_and_tutorials/CanoniCAI/codelabs/5_production.md)

- [Text Analytics Engine](docs/examples_and_tutorials/CanoniAnalytics/README.md)
  - [Preparation and Background](docs/examples_and_tutorials/CanoniAnalytics/codelabs/1_preparation.md)
  - [Map the script into a graph](docs/examples_and_tutorials/CanoniAnalytics/codelabs/2_map_the_data_to_graph.md)
  - [Get the summery of scene descriptions](docs/examples_and_tutorials/CanoniAnalytics/codelabs/3_getting_summery_and_keywords_of_pharagraphs.md)
  - [Find semantically similar sentences](docs/examples_and_tutorials/CanoniAnalytics/codelabs/4_find_semantically_similar_sentences.md)
  - [Clustering documents](docs/examples_and_tutorials/CanoniAnalytics/codelabs/5_clustering_documents.md)
  - [Sentiment analysis of dialogues](docs/examples_and_tutorials/CanoniAnalytics/codelabs/6_sentiment_analysis.md)
  - [Creating custom action to scrap movie data](docs/examples_and_tutorials/CanoniAnalytics/codelabs/7_creating_custom_action_to_scrap_movie_data.md)

- [Guide to Use speech to text and text to speech modules](docs/examples_and_tutorials/CanoniCAI/codelabs/6_speech2text_and_text2speech.md)
- [Collect Training Data via Crowdsource](docs/examples_and_tutorials/CanoniCAI/codelabs/7_crowdsource.md)
- [Named Entity Recognition Module Example](docs/examples_and_tutorials/ner_examples/README.md)
- [Personalized Head Example Use Case](docs/examples_and_tutorials/ph_example/ph.md)

# Architecture
  - [Interfacing A Jaseci Machine](docs/docs/architecture/interfacing.md)
    - [Local JSCTL Mode](docs/docs/architecture/interfacing_jaseci/jsctl.md)
      - [CLI vs Shell-mode, and Session Files](docs/docs/architecture/interfacing_jaseci/basics.md)
    - [Remote JSCTL Mode](docs/docs/comming_soon.md)
    - [Application Mode: Jac Api Collection](support/guide/other/classes.md)

# Development
- [Abstractions of Jaseci](docs/docs/development/1_abstractions.md)
  - [Graphs](docs/docs/development/1_abstractions.md#graphs)
    - [Nodes](docs/docs/development/1_abstractions.md#nodes)
    - [Edges](docs/docs/development/1_abstractions.md#edges)
    - [Operators for connecting nodes and edges](docs/docs/development/1_abstractions.md#operators-for-connecting-nodes-and-edges)
    - [Creating Graphs Examples](docs/docs/development/1_abstractions.md#creating-graphs-examples)
    - [Referencing and Dereferencing Nodes and Edges](docs/docs/development/1_abstractions.md#referencing-and-dereferencing-nodes-and-edges)
    - [Plucking values from nodes and edges](docs/docs/development/1_abstractions.md#plucking-values-from-nodes-and-edges)
  - [Walkers](docs/docs/development/1_abstractions.md#walkers)
    - [Init Walker with Examples](docs/docs/development/1_abstractions.md#init-walker-with-examples)
    - [Walkers Navigating Graphs Examples](docs/docs/development/1_abstractions.md#walkers-navigating-graphs-examples)
    - [Walker Spawning Examples](docs/docs/development/1_abstractions.md#walker-spawning-examples)
    - [Walker Callback](docs/docs/development/1_abstractions.md#walker-callback)
  - [Abilities](docs/docs/development/1_abstractions.md#abilities)
    - [Node Abilities Example](docs/docs/development/1_abstractions.md#node-abilities-example)
    - [Walker Abilities Example](docs/docs/development/1_abstractions.md#walker-abilities-example)
    - [Edge Abilities Example](docs/docs/development/1_abstractions.md#edge-abilities-example)
    - [A Complete Example](docs/docs/development/1_abstractions.md#a-complete-example)
    - [Here and Visitor](docs/docs/development/1_abstractions.md#here-and-visitor)
  - [Actions](docs/docs/development/1_abstractions.md#actions)
- [Jaseci Operations](docs/docs/development/2_operations.md)
  - [Spawn](docs/docs/development/2_operations.md#spawn)
  <!--Need to add more information on this topic-->
  - [Info and Context](docs/docs/development/2_operations.md#info-and-context)
  - [Take](docs/docs/development/2_operations.md#take)
  - [Skip](docs/docs/development/2_operations.md#skip)
  - [Disengage](docs/docs/development/2_operations.md#disengage)
  - [Ignore](docs/docs/development/2_operations.md#ignore)
  - [Destroy](docs/docs/development/2_operations.md#destroy)
  - [Report](docs/docs/development/2_operations.md#report)
  - [Yield](docs/docs/development/2_operations.md#yield)
- [Upload files using Multi-part](docs/docs/development/multipart.md)
- [Inheritance](docs/docs/development/inheritance.md)
- [Jaseci Standard Actions Libraries](docs/docs/development/1_abstractions.md#jaseci-standard-actions)
  <!--Should explain input parameters of these actions-->
  - [Date](docs/docs/development/std_actions/2_date.md)
  - [File](docs/docs/development/std_actions/3_file.md)
  - [Rand](docs/docs/development/std_actions/4_rand.md)
  - [Net](docs/docs/development/std_actions/5_net.md)
  - [Regex](docs/docs/development/std_actions/6_regex.md)
  - [Request](docs/docs/development/std_actions/7_request.md)
  - [Standard](docs/docs/development/std_actions/8_std.md)
  - [Stripe](docs/docs/development/std_actions/9_stripe.md)
  - [Vectors](docs/docs/development/std_actions/10_vectors.md)
  - [Elastic](docs/docs/development/std_actions/11_elastic.md)
  - [Jaseci Core](docs/docs/development/std_actions/1_jaseci.md)
    - [Alias](docs/docs/development/std_actions/1_jaseci.md#alias)
    - [Objects](docs/docs/development/std_actions/1_jaseci.md#objects)
    - [Graphs](docs/docs/development/std_actions/1_jaseci.md#graphs)
    - [Sentinels](docs/docs/development/std_actions/1_jaseci.md#sentinels)
    - [Walkers](docs/docs/development/std_actions/1_jaseci.md#walker)
    - [Architypes](docs/docs/development/std_actions/1_jaseci.md#architypes)
    - [Masters](docs/docs/development/std_actions/1_jaseci.md#masters)
    - [Logger](docs/docs/development/std_actions/1_jaseci.md#logger)
    - [Global API](docs/docs/development/std_actions/1_jaseci.md#global-api)
    - [Super Master](docs/docs/development/std_actions/1_jaseci.md#super-master)
    - [Stripe](docs/docs/development/std_actions/1_jaseci.md#stripe)
    - [Actions](docs/docs/development/std_actions/1_jaseci.md#actions)
    - [Configurations](docs/docs/development/std_actions/1_jaseci.md#configurations-apis)
- [Jaseci AI kit Features](jaseci_ai_kit/README.md)
  - [Jac NLP Modules](jaseci_ai_kit/jac_nlp/README.md)
    - [Text Encoders](jaseci_ai_kit/jac_nlp/README.md#text-encoders)
    - [Named Entity Recognition Models](jaseci_ai_kit/jac_nlp/README.md#named-entity-recognition-models)
    - [Text Segmentation Modules](jaseci_ai_kit/jac_nlp/README.md#text-segmentation-modules)
    - [Summarization Modules](jaseci_ai_kit/jac_nlp/README.md#summarization-modules)
    - [Topic Modeling Modules](jaseci_ai_kit/jac_nlp/README.md#topic-modeling-modules)
    - [Sentiment Analysis Modules](jaseci_ai_kit/jac_nlp/README.md#sentiment-analysis-modules)
    - [Paraphraser Modules](jaseci_ai_kit/jac_nlp/README.md#paraphraser-modules)
    - [Text Generation Modules](jaseci_ai_kit/jac_nlp/README.md#text-generation-modules)
  - [Jac Speech Modules](jaseci_ai_kit/jac_speech/README.md)
    - [Speech to Text Modules](jaseci_ai_kit/jac_speech/README.md#speech-to-text-modules)
    - [Text to Speech Modules](jaseci_ai_kit/jac_speech/README.md#text-to-speech-modules)
  - [Jac Vision Modules](jaseci_ai_kit/jac_vision/README.md)
  - [Jac Miscellaneous Modules](jaseci_ai_kit/jac_misc/README.md)
    - [Clustering Modules](jaseci_ai_kit/jac_misc/README.md#clustering-modules)
    - [Translator Modules](jaseci_ai_kit/jac_misc/README.md#translator-modules)
    - [PDF Extractor Modules](jaseci_ai_kit/jac_misc/README.md#pdf-extractor-modules)
  - [Guide to use Jaseci AI Kit](jaseci_ai_kit/support/guide-to-use-ai-kit.md)
- [Running Jaseci Action as a Service](docs/docs/development/action_microservice.md)
- [Custom Jaseci Actions](docs/docs/development/custom_actions/custom_jaseci_module_codelab.md)
  - [Example: Custom Action Using T5](docs/docs/development/custom_actions/t5_custom_module_codelab.md)
- [Jaseci UI Kit](ui_components/readme.md)
  - [Introduction](ui_components/docs/what-is-jaseci-ui-kit.md)
  - [Basic Concepts](ui_components/docs/basic-concepts.md)
  - [Built-in Actions](ui_components/docs/built-in-actions.md)
  - [Connecting an API](ui_components/docs/connecting-an-api.md)
<!--this goes under development, content structure has to review - Assigned to Tharuka-->


# JAC Language Syntax Reference

- [Jac Language Basics](docs/docs/jac_language_guide/1_jac_lang_basics.md)
  - [Data Types](docs/docs/jac_language_guide/1_jac_lang_basics.md#data-types)
    - [Special Types](docs/docs/jac_language_guide/1_jac_lang_basics.md#special-types)
    - [Typecasting](docs/docs/jac_language_guide/1_jac_lang_basics.md#typecasting)
  - [Operators](docs/docs/jac_language_guide/1_jac_lang_basics.md#operators)
    - [Arithmatic Operators](docs/docs/jac_language_guide/1_jac_lang_basics.md#arithmatic-operators)
    - [Equality Operations](docs/docs/jac_language_guide/1_jac_lang_basics.md#equality-operations)
    - [Logical Operators](docs/docs/jac_language_guide/1_jac_lang_basics.md#logical-operators)
    - [Assigments Operators](docs/docs/jac_language_guide/1_jac_lang_basics.md#assigments-operators)
  - [Precedence of Jaseci Operators](docs/docs/jac_language_guide/1_jac_lang_basics.md#assigments-operators)
  - [Input and Output](docs/docs/jac_language_guide/1_jac_lang_basics.md#input-and-output-in-jaseci)
  - [File Handling](docs/docs/jac_language_guide/1_jac_lang_basics.md#file-handling-in-jaseci)
  - [Global Variables](docs/docs/jac_language_guide/1_jac_lang_basics.md#global-variables-in-jaseci)
  - [Working with Imports](docs/docs/jac_language_guide/1_jac_lang_basics.md#working-with-imports)
  - [Error Handling in Jaseci](docs/docs/jac_language_guide/4_error_handling.md)
  - [Logs in Jaseci](docs/docs/comming_soon.md)
<!--Error Handling and Loggings Should come under this-->
- [Data Structures in Jaseci](docs/docs/jac_language_guide/2_jac_data_types_and_ops.md)
  - [Dictionary](docs/docs/jac_language_guide/2_jac_data_types_and_ops.md#dictionaries)
  - [List](docs/docs/jac_language_guide/2_jac_data_types_and_ops.md#list)
  - [String](docs/docs/jac_language_guide/2_jac_data_types_and_ops.md#strings)
- [Loops and Conditions](docs/docs/jac_language_guide/3_loops_and_conditions.md)
  - [Control Flow](docs/docs/jac_language_guide/3_loops_and_conditions.md#control-flow)
  - [Looping](docs/docs/jac_language_guide/3_loops_and_conditions.md#looping)


# Testing and Debugging

- [Testing](docs/docs/testing_and_debugging/1_testing.md)
- [Jaseci Studio](docs/docs/testing_and_debugging/2_jaseci_studio.md)
  - [Login](docs/docs/testing_and_debugging/2_jaseci_studio.md#login)
  - [Dashboard](docs/docs/testing_and_debugging/2_jaseci_studio.md#dashboard-summery-view)
  - [Graph Viewer](docs/docs/testing_and_debugging/2_jaseci_studio.md#graph-viewer)
  - [Logs Viewer](docs/docs/testing_and_debugging/2_jaseci_studio.md#logs-viewer)
  - [Managing Architypes](docs/docs/testing_and_debugging/2_jaseci_studio.md#managing-architypes)


# Deployment
  - [Package up Your Jac Program and Jaseci Server for Deployment](docs/docs/deployment/how_to_package.md)
  - [Single Sign-on Social](jaseci_serv/jaseci_serv/jsx_oauth/README.md)
  - [Extension Services](docs/docs/comming_soon.md)
      - [Task](jaseci_core/jaseci/extens/svc/docs/task_svc.md)
      - [Mail](jaseci_core/jaseci/extens/svc/docs/mail_svc.md)
  - [Automatic Deployment and Scaling via JsOrc](jaseci_core/jaseci/extens/svc/docs/JSORC.md))
      - [Development](jaseci_core/jaseci/extens/svc/docs/jsorc_development.md)
  - [Install Jaseci using Helm](support/helmcharts/jaseci/README.md)
  - [Create AWS EKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/aws/README.md)
  - [Create Azure AKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/azure/README.md)

<!-- More context about Jaseci Server-->
<!-- More context about JSCTL-->

# Contributing to Jaseci
- [Installation for Contributors](support/guide/getting_started/installation.md#installation-for-contributors-of-jaseci)
- [Contributing to the Jaseci](CONTRIBUTING.md)
  - [How to be a Jaseci Contributor](CONTRIBUTING.md#how-to-be-a-jaseci-contributor)
  - [How to contribute code](CONTRIBUTING.md#how-to-contribute-code)
  - [How to Update the Official Documentation](CONTRIBUTING.md#how-to-update-the-official-documentation)
- [Contributors](CONTRIBUTORS.md)

<!-- Add coming soon sections-->

# Resources

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

<!-- For this section to be complete we must first rewrite some of the content so it assumes that the user followed the installation guide -->
<!-- Second we must write the content for the coming soon sections -->
