# Jaseci Misc Package `(jac_misc)`
The `jac_misc` package contains a collection of miscellaneous models that can be used to perform various tasks such as translation, pdf extraction, personalized head etc. following is a list of all the models available in the `jac_misc` package.

- [Jaseci Misc Package `(jac_misc)`](#jaseci-misc-package-jac_misc)
  - [Clustering Modules](#clustering-modules)
    - [Actions](#actions)
    - [Example Jac Usage](#example-jac-usage)
  - [Translator Modules](#translator-modules)
    - [Actions](#actions-1)
    - [Example Jac Usage:](#example-jac-usage-1)
  - [PDF Extractor Modules](#pdf-extractor-modules)
    - [Actions](#actions-2)
    - [Example Jac Usage](#example-jac-usage-2)

## Clustering Modules

Module `cluster` implemented for clustering text document into similar clusters. This is a example program to cluster documents with jaseci `cluster` module. We will use input as list of raw text documents and will produce cluster labels for each text documents.

### Actions

* `get_umap`: Reducing the dimension of data while preserving the relationship between data points to identify clusters easier.
    * Input
        * `text_embeddings` (list): list of text embeddings should pass here.
        * `n_neighbors` (int): number of neighbors to consider.
        * `min_dist` (float): minimum distance between clusters.
        * `n_components` (int): the dimensionality of the reduced data.
        * `random_state`(int): pre-producability of the algorithm.

    * Returns: multidimensional array of reduced features.

* `get_cluster_labels`: To get list of possible cluster labels
    * Input
        * `embeddings`(list): This accept list of embedded text features.
        * `algorithm` (String): Algorithm for clustering.
        * `min_samples` (int): The minimum number of data points in a cluster is represented here. Increasing this will reduces number of clusters
        * `min_cluster_size` (int): This represents how conservative you want your clustering should be. Larger values more data points will be considered as noise

    * Returns: list of labels.


### Example Jac Usage

**Input data file `text_cluster.json`**
```json
  [
    "still waiting card",
    "countries supporting",
    "card still arrived weeks",
    "countries accounts support",
    "provide support countries",
    "waiting week card still coming",
    "track card process delivery",
    "countries getting support",
    "know get card lost",
    "send new card",
    "still received new card",
    "info card delivery",
    "new card still come",
    "way track delivery card",
    "countries currently support"]
```

```jac
walker text_cluster_example{
    can file.load_json;
    can use.encode;
    can cluster.get_umap;
    can cluster.get_cluster_labels;

    has text, encode, final_features, labels;

    text = file.load_json("text_cluster.json");
    encode = use.encode(text);
    final_features = cluster.get_umap(encode,2);

    labels = cluster.get_cluster_labels(final_features,"hbdscan",2,2);
    std.out(labels);

}
```

For a complete example visit [here](jac_misc/cluster/README.md)

## Translator Modules

Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.

### Actions

* `translator` : Module `translator` uses the `mbart-large-50-many-to-many` to perform multilingual translation. It can translate from 50 languages to 50 languages.
  * Alternate name:
  * Input:
    * `text` - Text to be translated. Type: `Union[List[str], str]`
    * `src_lang` - Source language of the text. Type: `str`
    * `tgt_lang` - Target language of the text. Type: `str`
  * Return: Return type of the action is `List[str]`.


### Example Jac Usage:

Example JAC Code to translate text from Hindi to English:

```jac
walker test_translate_hindi_eng {
    can translator.translate;
    report translator.translate("नमस्ते, आप कैसे हैं?", "hi_IN", "en_XX"); # Returns ["Hello, how are you?"]
}
```
Example JAC Code to translate text from English to German:
```jac
walker test_translate_eng_german {
    can translator.translate;
    report translator.translate("Hello, how are you?", "en_XX", "de_DE"); # Returns ["Hallo, wie geht es dir?"]
}
```
For a complete example visit [here](jac_misc/translator/README.md)

## PDF Extractor Modules

`pdf_ext` module implemented for the Topical Change Detection in Documents via Embeddings of Long Sequences.

### Actions

* `extract_pdf`: gets different topics in the context provided, given a threshold
    * Input
        * `url`(String): gets the pdf from URL
        * `path`(Float): gets the pdf from local path
        * `metadata`(Bool): to display available metadata of PDF
    * Returns: a json with number of pages the pdf had and content

### Example Jac Usage

```jac
walker pdf_ext_example {
    has url = "http://www.africau.edu/images/default/sample.pdf";
    has metadata = true;
    can pdf_ext.extract_pdf;

    # Getting the dat from PDF
    resp_data = pdf_ext.extract_pdf(url=url,
    metadata=metadata);
    std.out(resp_data);
}
```

For a complete example visit [here](jac_misc/pdf_ext/README.md)