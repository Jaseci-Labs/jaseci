# Jaseci Misc Package `(jac_misc)`
The `jac_misc` package contains a collection of miscellaneous models that can be used to perform various tasks such as translation, pdf extraction, personalized head etc. following is a list of all the models available in the `jac_misc` package.

## Installation
Each module can be installed individually or all at once. To install all modules at once.
```bash
pip install jac_misc[all] # Installs all the modules present in the jac_misc package
pip install jac_misc[translator] # Installs the translator module present in the jac_misc package
pip install jac_misc[cluster,pdf_ext] # Installs the cluster and pdf_ext module present in the jac_misc package
```

## List of Models


| Module      | Model Name       | Example                             | Type                    | Status       | Description                                                 | Resources                                 |
| ----------- | ---------------- | ----------------------------------- | ----------------------- | ------------ | ----------------------------------------------------------- | ----------------------------------------- |
| `translator` | Text Translation | [Link](jac_misc/translator/README.md) | No Training req. | Ready       | Text Translation for 50 languages to 50 languages | [Multilingual Denoising Pre-training for Neural Machine Translation](https://arxiv.org/abs/2001.08210), [Huggingface MBart Docs](https://huggingface.co/transformers/model_doc/mbart.html) |
| `cluster` | Text Cluster | [Link](jac_misc/cluster/README.md) | No Training req. | Experimetal | Indentifying Posible Similar Clusters in Set of Documents | [UMAP](https://umap-learn.readthedocs.io/en/latest/) , [HBDSCAN](https://hdbscan.readthedocs.io/en/latest/how_hdbscan_works.html) |
| `pdf_ext` | PDF Extractor | [Link](jac_misc/pdf_ext/README.md) | No Training req.| Ready  | Extract content from a PDF file via PyPDF2 | [Doc.](https://pypdf2.readthedocs.io/en/latest/) |
| `ph` | Personalized Head | [Link](jac_misc/ph/README.md) | Training Req. | Experimental  | Extract content from a PDF file via PyPDF2 | |


## Usage

To load the `jac_misc.translator` package into jaseci in local environment, run the following command in the jsctl console.
```bash
jsctl > actions load module jac_misc.translator
```
