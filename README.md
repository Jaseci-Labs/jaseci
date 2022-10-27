# Jaseci Docs and Guides

[![jaseci_core Unit Tests](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml/badge.svg?branch=main&event=push)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_core_test.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci/)](https://pypi.org/project/jaseci)
[![jaseci_serv](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml/badge.svg?branch=main)](https://github.com/Jaseci-Labs/jaseci/actions/workflows/jaseci_serv_build.yml) [![PyPi version](https://badgen.net/pypi/v/jaseci-serv/)](https://pypi.org/project/jaseci-serv)
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
- [Build a Custom Jaseci Module](support/codelabs/custom_jaseci_module_codelab.md)
- [Install Jaseci using Helm](support/helmcharts/jaseci/README.md)
- [Create AWS EKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/aws/README.md)
- [Create Azure AKS Infrastructure for Jaseci using Terraform](support/infrastructure/terraform/azure/README.md)
- [Locust Load Test for JASECI](support/locust/README.md)
- [Setting up Monitoring for JASECI](support/monitoring/README.md)

## The JAC Language Guide

- [Key Abstractions and Concepts](support/guide/lang_docs/key_concepts.md)
  - [Graphs](support/guide/lang_docs/graphs.md)
  - [Walkers](support/guide/lang_docs/walkers.md)
  - [Abilities](support/guide/lang_docs/abilities.md)
    - [`here` and `visitor`](support/guide/lang_docs/here_visitor.md)
  - [Actions](support/guide/lang_docs/actions.md)

## Jaseci AI Library Reference

- [Jaseci AI Kit Overview](jaseci_ai_kit/README.md)
  - [CL Summarization](jaseci_ai_kit/jaseci_ai_kit/modules/cl_summer/README.md)
  - [Bi-Encoder](jaseci_ai_kit/jaseci_ai_kit/modules/encoders/README.md)
  - [FLair NER](jaseci_ai_kit/jaseci_ai_kit/modules/ent_ext/README.md)
  - [Fasttext Classifier](jaseci_ai_kit/jaseci_ai_kit/modules/fast_enc/README.md)
  - [Object Detection](jaseci_ai_kit/jaseci_ai_kit/modules/object_detection/readme.md)
  - [T5 Summarization](jaseci_ai_kit/jaseci_ai_kit/modules/t5_sum/README.md)
  - [Text Segmenter](jaseci_ai_kit/jaseci_ai_kit/modules/text_seg/README.md)
  - [Transformer NER](jaseci_ai_kit/jaseci_ai_kit/modules/tfm_ner/README.md)
  - [USE Encoder](jaseci_ai_kit/jaseci_ai_kit/modules/use_enc/README.md)
  - [USE QA](jaseci_ai_kit/jaseci_ai_kit/modules/use_qa/README.md)
- [Guide to use Jaseci AI Kit](jaseci_ai_kit/jaseci_ai_kit/guid-to-use-ai-kit.md)

## Jaseci UI Widget Library

- [Jaseci UI Kit](jaseci_ui_kit/README.md)
- [Introduction](jaseci_ui_kit/components/docs/what-is-jaseci-ui-kit.md)
- [Basic Concepts](jaseci_ui_kit/components/docs/basic-concepts.md)
- [Built-in Actions](jaseci_ui_kit/components/docs/built-in-actions.md)
- [Connecting an API](jaseci_ui_kit/components/docs/connecting-an-api.md)
- [Components](jaseci_ui_kit/README.md)

## Jaseci Core Implementation Guide
- [Services](jaseci_core/jaseci/svc/README.md)
  - [JsOrc](jaseci_core/jaseci/svc/jsorc/README.md)
  - [Task](jaseci_core/jaseci/svc/task/README.md)

## Contributing to Jaseci

- [Being an Contributor](support/guide/other/contributor_policy.md)
- [General Guide](CONTRIBUTING.md)
- [Contributors](CONTRIBUTORS.md)

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
