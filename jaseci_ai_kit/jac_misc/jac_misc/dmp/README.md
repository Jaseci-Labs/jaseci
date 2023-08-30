# Jaseci Diff-Match-Patch Action Library
## Overview
This is an action library for the Jaseci AI kit that allows developers to utilize functions such as diff, match, or patch to synchronize and produce plain text output within their applications.  
The three main tools, as mentioned before, are:
1. Diff: Allows the developer to compare two texts and return a list of differences.
2. Match: Allows for location and accuracy-based weighting of a traditional search operation, allowing developers to search for the best match within a document.
3. Patch: Allows developers to apply a list of patches to a document even if the underlying text does not match.  

All of the following actions utilize a function from [Google's diff-match-patch library](https://github.com/google/diff-match-patch) which provides a common API for the public functions in a variety of languages including C, C++, Python, Java, and more.

The full description and documentation of this library can be found [here](https://github.com/google/diff-match-patch/wiki).

## Function Documentation
## Diff:
### `get_diff`
    Arguments:
        text1: str
        text2: str
        timeout: float = 1.0
    
    Return: 
        Files's diff (list)

    Usage: 
        Finding the differences between too files

    Notes:
        The "timeout" argument allows the user to specify how long the diff's exploration phase is allowed 
        to take (in seconds). Setting this value to 0 allows the diff to run indefinitely and to conclusion, 
        producing the most optimal diff. If the operation times out, a valid diff list will still be produced. 
        The first element of each tuple in the list specifies if it is an insertion (1), a deletion (-1) or 
        an equality (0). The second element specifies the affected text.

### `semantic_clean`
    Arguments:
        diff: list

    Return: 
        human-readable diff: list

    Usage:
        Making a human-readable list of differences between two files, removing coincidental differences that 
        clutter the report.

### `efficient_clean`
    Arguments:
        diff: list
        cost: int = 4

    Return:
        Machine-efficient diff: list

    Usage:
        Making a list of differences that can be read in a machine-efficient manner.

    Notes:
        The "cost" argument is set to determine the cost of adding extra characters to a diff. If the cost is 4, 
        this means that if expanding the length of a diff by 3 characters can remove one edit, then that 
        optimization will reduce the total cost

### `get_lvsht`
    Arguments:
        diff: list

    Return:
        Levenshtein distance: int

    Usage:
        Used to calculate the levenshtein distance of a diff report - the number of inserted, deleted, or 
        substituted characters

### `get_html`
    Arguments:
        diff: list

    Return:
        HTML document: str

    Usage:
        Used to convert a difference list into a pretty HTML document

## Match:
### `get_match`:
    Arguments:
        text: str
        pattern: str
        loc: int
        dist: int = 1000
        threshold: float = 0.5

    Return:
        Location of best match (int)

    Usage:
        Searches the input string for the best match of pattern given a starting location, search distance, 
        and accuracy threshold.

    Notes:
        The loc argument specifies a "best guess" of where in the full text the pattern will appear whereas 
        the dist argument specifies how far to search from the starting position for a match and the threshold 
        argument specifies how accurate the match has to be (within distance*threshold). The threshold must 
        be a float between 0 and 1. The get_match function will return -1 if no valid match is found.

    Examples:
        get_match(text="abc123abc", pattern="abc", loc=6)
        Would return 6 as a match of "abc" as the pattern is found at the 7th (index 6) character.

        get_match(text="abc123abc", pattern="abc", loc=4)
        Would return 6 as a match of "abc" because the pattern starting at character index 6 is closest.

        get_match(text="abc123abc", patterm="abc", loc=2)
        Would return 0 as a match of "abc" because the pattern starting at character index 0 is closest.

        get_match(text="abc123abc", pattern="abc", loc=5, dist=1)
        Would return -1 as there is no match of the pattern "abc" within 1*0.5 (dist*threshold) = 0.5 characters 
        of location 5.

        get_match(text="abc123abc", pattern="abc", loc=4, dist=4)
        Would return 6 as the second occurence of the pattern starting at index 6 is with 4*0.5 = 2 characters 
        of the starting location.

        get_match(text="abc123abc", pattern="abc", loc=4, dist=1000, threshold=0)
        Would return -1 because a threshold of 0 will always require the pattern to be found exactly at the 
        starting location.

## Patch
### `get_patch`
    Arguments:
        text1: str
        text2: str

    Return:
        List of patches (list)

    Usage:
        Create a list of patches that would allow two texts to be synchronized

### `get_patch`
    Arguments:
        diff: list

    Return:
        List of patches (list)

    Usage: 
        Create a list of patches based on the pre-computed differences between two texts

### `get_patch`
    Arguments:
        text1: str
        diff: list

    Return:
        List of patches (list)

    Usage:
        Create a list of patches based on the original text and a list of differences between the target text

    Notes:
        This method is preferred if the information is available

### `get_text`
    Arguments:
        patch: list

    Return:
        Patch text (str)

    Usage:
        Used to convert a list of patches to a single block of text that looks very similar to GNU diff/patch 
        format

### `text_to_patch`
    Arguments:
        text: str

    Return:
        List of patches (list)

    Usage:
        Used to convert a GNU diff/patch format text block to a list of patch objects

### `apply`
    Arguments:
        patch: list
        text1: str
        threshold: 0.5

    Return:
        Patched text and list of results (list)

    Usage:
        Used to apply a patch list to a specific text

    Notes:
        The returned results value is a boolean array that determines which patches were successfully applied. 
        Similar to the match threshold, the patch threshold determines how closely text for a major delete 
        must match. The threshold must be a float between 0 (exact match) and 1 (eveything matches). The 
        suggested value is the same as that for the match function.



