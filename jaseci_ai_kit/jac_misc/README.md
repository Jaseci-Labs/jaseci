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
  - [Diff-Match-Patch Modules](#diff-match-patch-modules)
    - [Actions](#actions-3)
      - [Diff](#diff)
      - [Example Jac Usage](#example-jac-usage-3)
      - [Match](#match)
      - [Example Jac Usage](#example-jac-usage-4)
      - [Patch](#patch)
      - [Example Jac Usage](#example-jac-usage-5)


## Clustering Modules

Module `cluster` implemented for clustering text document into similar clusters. This is a example program to cluster documents with jaseci `cluster` module. We will use input as list of raw text documents and will produce cluster labels for each text documents.

### Actions

* `get_umap`: Redusing the dimention of data while preseving the relationship beween data points to identify clusters easier.
    * Input
        * `text_embeddings` (list): list of text embeddings should pass here.
        * `n_neighbors` (int): number of neighbors to consider.
        * `min_dist` (float): minimum distance between clusters.
        * `n_components` (int): the dimensionality of the reduced data.
        * `random_state`(int): preproducability of the algorithm.

    * Returns: multidimentional array of reduced features.

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
    "countries accounts suppor",
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

## Diff Match Patch Modules

Module `dmp` provides an action library piggybacking off of Google's `diff-match-patch` library to provide diffing, matching, and patching functionality.

### Actions

#### Diff

* `get_diff`: Computes a list of differences between two texts
  * Input
    * `text1`(String): gets the first text to be compared
    * `text2`(String): gets the second text to be compared
    * `timeout`(Float) = 1.0: provides the timeout value in seconds (0 for no timeout)
  * Returns: a list of differences between text1 and text2

* `semantic_clean`: Cleans a list of differences to make it human-readable
  * Input
    * `diff`(List): list of differences between two texts
  * Returns: A human-readable list of differences with coincidental differences removed

* `efficient_clean`: Cleans a list of differences to make it efficiently processed by a machine
  * Input
    * `diff`:(List): list of differences between two texts
    * `cost`:(Integer) = 4: cost of adding extra characters to a diff
  * Returns: A machine-efficient list of differences between two texts

* `get_lvsht`: Calculates the levenshtein distance of a difference list
  * Input:
    * `diff`(List): a list of differences between two texts
  * Returns: an integer representing the number of inserted, deleted, or substitutde characters in a difference list

* `get_html`: Converts a difference list into an HTML text block
  * Input:
    * `diff`(List): a list of differences between two texts
  * Returns: a text block of HTML code displaying the difference list

#### Example Jac Usage

```jac
  walker diff_example {
    has first_text = "Good dog";
    has second_text = "Bad dog";
    can diff.get_diff;
    can diff.semantic_clean;
    can diff.get_html;

    # Getting the list of differences
    diff_list = diff.get_diff(first_text, second_text);
    diff_list = diff.semantic_clean(diff_list);
    diff_html = diff.get_html(diff_list);
    std.out(diff_html);
  }
```

#### Match

* `get_match`
  * Input:
    * `text`(String): text to search for a match in
    * `pattern`(String): the pattern to search for within the text
    * `loc`(Integer): the starting location (character index) at which to start the search
    * `dist`(Integer) = 1000: the distance (in characters) to search for a match around the starting location
    * `threshold`(Float) = 0.5: the threshold for how accurate a match is (multiplied by distance)
  * Returns: the character index of the best found match or -1 if no valid match is found

#### Example Jac Usage

```jac
walker match_example {
  has search_text = "abc123abc";
  has search_pattern = "abc";
  has location = 4;
  can match.get_match;

  match_idx = match.get_match(search_text, search_pattern, location);
  std.out(match_idx);
}
```

#### Patch

* `get_patch`
  * Input
    * `text1`(String): first text to compare
    * `text2`(String): second text to compare  
    OR
    * `diff`(List): a list of differences between two texts  
    OR
    * `text1`(String): first text document
    * `diff`(List): a list of differences between text1 and another text
  * Returns: a list of patches to synchronzie two texts

* `get_text`
  * Input
    * `patch`(List): a list of patches
  * Returns: a text block of patches formatted similarly to GNU diff/patch

* `text_to_patch`
  * Input
    * `text`(String)
  * Returns: a list of patches converted from GNU diff/patch text format

* `apply`
  * Input
    * `patch`(List): the list of patches to apply
    * `text1`(String): the text to attempt to apply the patches to
    * `threshold`(Float) = 0.5: the delete threshold to determine how closely text must match in a major deletion. Must be between 0 and 1 inclusive.

#### Example Jac Usage

```jac
walker patch_example {
  has first_text = "Good dog goes for a walk";
  has second_text = "Bad dog barks at other dogs on a walk";
  can patch.get_patch;
  can patch.get_text;
  can patch.text_to_patch;
  can patch.apply;

  patch_list = patch.get_patch(first_text, second_text);
  # Meaningless patch -> text -> patch conversion
  patch_text = patch.get_text(patch_list);
  patch_list = patch.text_to_patch(patch_text);
  patched_text = patch.apply(patch_list, first_text);
  std.out(patched_text);
}
```

For a complete example visit [here](jac_misc/dmp/README.md)


