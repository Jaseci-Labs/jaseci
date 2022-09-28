# Jaseci Official Documentation

[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml/badge.svg?branch=main&event=push)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Getting Started

- [Introducing Jaseci](support/guide/getting_started/introduction.md)
- [Installing Jaseci](support/guide/getting_started/installation.md)
    - [Installing on Windows](support/guide/getting_started/installation.md#installing-on-windows)
    - [Installing on Mac](support/guide/getting_started/installation.md#installing-on-mac)
    - [Installing on Linux](support/guide/getting_started/installation.md#installing-on-linux)
    - [Installation for Contributors](support/guide/getting_started/installation.md#installation-for-contributors-of-jaseci)
- [Jaseci Quickstart](support/guide/getting_started/quickstart.md)
- [Setting Up Your Editor](support/guide/getting_started/setting_up_your_editor.md)
- [Writing Your First App](support/guide/getting_started/writing_your_first_app.md)
- [Understanding JAC Programs](support/guide/getting_started/understanding_jac_programs.md)


## The JAC Programming Language Guide

- [Language Overview](support/guide/jac_language_guide/jac_language_overview.md)
- [Grammar](support/guide/jac_language_guide/jac_grammar.md)
- [Operators](support/guide/jac_language_guide/operators.md)
- [Control Flow](support/guide/jac_language_guide/control_flow.md)
- [Collections](support/guide/jac_language_guide/collections.md)
- [Nodes](support/guide/jac_language_guide/nodes.md)
- [Edges](support/guide/jac_language_guide/edges.md)
- [Graphs](support/guide/jac_language_guide/graphs.md)
- [Walkers](support/guide/jac_language_guide/walkers.md)
    - [Traversing a Graph](support/guide/jac_language_guide/traversing_a_graph.md)
    - [Referencing a Node in Context](support/guide/jac_language_guide/referencing_node_context.md)
- [Passing Arguments](support/guide/jac_language_guide/passing_arguments.md)
- [Specifying Operating Context](support/guide/jac_language_guide/specifying_operating_context.md)
- [Actions](support/guide/jac_language_guide/actions.md)
    - [Date Actions](support/guide/jac_language_guide/date_actions.md)
    - [File Actions](support/guide/jac_language_guide/file_actions.md)
    - [Net Actions](support/guide/jac_language_guide/net_actions.md)
    - [Rand Actions](support/guide/jac_language_guide/rand_actions.md)
    - [Request Actions](support/guide/jac_language_guide/request_actions.md)
    - [Standard Actions](support/guide/jac_language_guide/standard_actions.md)
    - [Vector Actions](support/guide/jac_language_guide/vector_actions.md)
    - [Jaseci Actions](support/guide/jac_language_guide/jaseci_actions.md) 


## Codelabs and Guides

- [Build a Custom Jaseci Module](support/codelabs/custom_jaseci_module_codelab.md)
- [CanoniCAI Example](examples/CanoniCAI/CCAI_codelab.md)
- [Building a Conversational AI System](support/codelabs/canonicai/chapter1.md)
    - [Chapter 2](support/codelabs/canonicai/chapter2.md)
    - [Chapter 3](support/codelabs/canonicai/chapter3.md)
    - [Chapter 4](support/codelabs/canonicai/chapter4.md)
    - [Chapter 5](support/codelabs/canonicai/chapter5.md)
    - [Chapter 6](support/codelabs/canonicai/chapter6.md)
    - [Chapter 7](support/codelabs/canonicai/chapter7.md)
- [Install Jaseci using Helm](support/helmcharts/jaseci/README.md)
- [Create AWS EKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/aws/README.md)
- [Create Azure AKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/azure/README.md)
- [Locust Load Test for JASECI](support/locust/README.md)
- [Setting up Monitoring for JASECI](support/monitoring/README.md)
- [NER Examples](examples/ner_examples/README.md)


## Jaseci Library Reference

- [Jaseci AI Kit](jaseci_ai_kit/README.md)
    - [CL Summarization](jaseci_ai_kit/jaseci_ai_kit/modules/cl_summer/README.md)
    - [Bi-Encoder](jaseci_ai_kit/jaseci_ai_kit/modules/encoders/README.md)
    - [FLair NER](jaseci_ai_kit/jaseci_ai_kit/modules/ent_ext/README.md)
    - [Fasttext Classifier](jaseci_ai_kit/jaseci_ai_kit/modules/fast_enc/README.md)
    - [Object Detection](jaseci_ai_kit/jaseci_ai_kit/modules/object_detection/readme.md)
    - [PDF Extractor](support/guide/jaseci_ai_kit/modules/non_ai/pdf_ext/README.md)
    - [T5 Summarization](jaseci_ai_kit/jaseci_ai_kit/modules/t5_sum/README.md)
    - [Text Segmenter](jaseci_ai_kit/jaseci_ai_kit/modules/text_seg/README.md)
    - [Transformer NER](jaseci_ai_kit/jaseci_ai_kit/modules/tfm_ner/README.md)
    - [USE Encoder](jaseci_ai_kit/jaseci_ai_kit/modules/use_enc/README.md)
    - [USE QA](jaseci_ai_kit/jaseci_ai_kit/modules/use_qa/README.md)


## Jaseci Studio

- [Jaseci UI Kit](jaseci_ui_kit/README.md)
    - [Introduction](jaseci_ui_kit/components/docs/what-is-jaseci-ui-kit.md)
    - [Basic Concepts](jaseci_ui_kit/components/docs/basic-concepts.md)
    - [Built-in Actions](jaseci_ui_kit/components/docs/built-in-actions.md)
    - [Connecting an API](jaseci_ui_kit/components/docs/connecting-an-api.md)
    - [AuthForm](jaseci_ui_kit/components/docs/components/AuthForm.md)
    - [Badge](jaseci_ui_kit/components/docs/components/Badge.md)
    - [Breadcrumbs](jaseci_ui_kit/components/docs/components/Breadcrumbs.md)
    - [Button](jaseci_ui_kit/components/docs/components/Button.md)
    - [ButtonGroup](jaseci_ui_kit/components/docs/components/ButtonGroup.md)
    - [Card](jaseci_ui_kit/components/docs/components/Card.md)
    - [Carousel](jaseci_ui_kit/components/docs/components/Carousel.md)
    - [Checkbox](jaseci_ui_kit/components/docs/components/Checkbox.md)
    - [Collapse](jaseci_ui_kit/components/docs/components/Collapse.md)
    - [Column](jaseci_ui_kit/components/docs/components/Column.md)
    - [Container](jaseci_ui_kit/components/docs/components/Container.md)
    - [Datagrid](jaseci_ui_kit/components/docs/components/DataGrid.md)
    - [DataList](jaseci_ui_kit/components/docs/components/DataList.md)
    - [DatePicker](jaseci_ui_kit/components/docs/components/DatePicker.md)
    - [Dialog](jaseci_ui_kit/components/docs/components/Dialog.md)
    - [Divider](jaseci_ui_kit/components/docs/components/Divider.md)
    - [Dropdown](jaseci_ui_kit/components/docs/components/Dropdown.md)
    - [Hero](jaseci_ui_kit/components/docs/components/Hero.md)
    - [Inputbox](jaseci_ui_kit/components/docs/components/Inputbox.md)
    - [Navbar](jaseci_ui_kit/components/docs/components/Navbar.md)
    - [Popover](jaseci_ui_kit/components/docs/components/Popover.md)
    - [Progress](jaseci_ui_kit/components/docs/components/Progress.md)
    - [Radio](jaseci_ui_kit/components/docs/components/Radio.md)
    - [RadioGroup](jaseci_ui_kit/components/docs/components/RadioGroup.md)
    - [Range](jaseci_ui_kit/components/docs/components/Range.md)
    - [Rating](jaseci_ui_kit/components/docs/components/Rating.md)
    - [Row](jaseci_ui_kit/components/docs/components/Row.md)
    - [Select](jaseci_ui_kit/components/docs/components/Select.md)
    - [SpeechInput](jaseci_ui_kit/components/docs/components/SpeechInput.md)
    - [Stat](jaseci_ui_kit/components/docs/components/Stat.md)
    - [Tabs](jaseci_ui_kit/components/docs/components/Tabs.md)
    - [Text](jaseci_ui_kit/components/docs/components/Text.md)
    - [Textbox](jaseci_ui_kit/components/docs/components/Textbox.md)
    

## Other Resources  

- [About this Release](CHANGELOG.md)
- [How to Contribute](CONTRIBUTING.md)
- [Contributors](CONTRIBUTORS.md)
- [Notes](NOTES.md)
- [Join our Community](https://forum.jaseci.org/)

- [Online Documentation](https://docs.jaseci.org/)
- [The Jaseci Bible](https://github.com/Jaseci-Labs/jaseci_bible/blob/main/pdf/jaseci_bible.pdf)
- [Our Website](https://jaseci.org/)
    - [Learn more at the Dojo](https://jaseci.org/dojo)
    - [Products Built with Jaseci](https://jaseci.org/products/)
    - [Jaseci in the News](https://jaseci.org/blog/)
    - [Contact Us](https://jaseci.org/contact-us/)
