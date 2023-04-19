#  Regex Actions Library

## Search for pattern in String

Searching for the first occurrence of a specific pattern or sequence of characters within a string.

Jac Example:

```jac
walker search{
    can regex.search;
    _string = "The rain in Spain";

    report regex.search("ai",_string);
}
```

Expected output

```json
"report": [
    {
      "span": [
        5,
        7
      ],
      "match": "ai"
    }
  ]
```

## Match begining of the string

Checks if there are any characters at the beginning of a string that match a specified regular expression pattern


Jac Example

```jac
walker match{
    can regex.match;
    _string = "The quick brown fox.";

    report regex.match("[A-Z]", _string);
}
```

Expected Output

```json
"report": [
    {
      "span": [
        0,
        1
      ],
      "match": "T"
    }
  ],
```

## Match full string.

Checks if a complete string matches a given regular expression pattern.

Jac Example

```jac
walker fullmatch{
    can regex.fullmatch;
    _string = "THEQUICKBROWNFOX";

    report regex.fullmatch("[A-Z]+", _string);
}
```

Expected output

```json
"report": [
    {
      "span": [
        0,
        16
      ],
      "match": "THEQUICKBROWNFOX"
    }
```

## Split string

Split string by the occurrences of pattern.

Jac Example

```jac
walker split{
    can regex.split;
    _string = "Words, words, words.";

    report regex.split("\W+", _string);
}
```

Expected Example

```json
"report": [
    [
      "Words",
      "words",
      "words",
      ""
    ]
  ],
```

## Find all occurances of the pattern

Finding all non-overlapping occurrences of a given pattern in a string.

Jac Example

```jac
walker findall{
    can regex.findall;
    _string = "set width=20 and height=10";

    report regex.findall("(\\w+)=(\\d+)", _string);
}
```

Expected Output

```json
"report": [
    [
      [
        "width",
        "20"
      ],
      [
        "height",
        "10"
      ]
    ]
  ]
```

## Search regex matches iteratively

Iteratevely search for non-overlapping match of the regular expression pattern in the string.

Jac Example

```jac
walker finditer{

    can regex.finditer;
    _string = "Blue Berries Blue Berries";

    report regex.finditer("Blue", _string);
}
```

Expected Output

```json
"report": [
    [
      {
        "span": [
          0,
          4
        ],
        "match": "Blue"
      },
      {
        "span": [
          13,
          17
        ],
        "match": "Blue"
      }
    ]
  ],
```

## Find and replace

Find non-overlapping occurrences of the regular expression pattern in the string, and replace each instance with the given substring

Jac Example

```jac
walker sub{
    can regex.sub;
    _string = "Account Number - 12345, Amount - 586.32";

    report regex.sub("[0-9]+", "NN", _string);
}
```

Expected Output

```json
"report": [
    "Account Number - NN, Amount - NN.NN"
  ]
```

## Find and Replace, returns the number of replacements

Find non-overlapping occurrences of the regular expression pattern in the string, and replace each instance with the given substring. Also returns the number of occurances of the pattern in the string.

Jac Example

```jac
walker subn{
    can regex.subn;
    _string = "Account Number - 12345, Amount - 586.32";

    report regex.subn("[0-9]+", "NN", _string);
}
```

Expected Output

```json
"report": [
    [
      "Account Number - NN, Amount - NN.NN",
      3
    ]
  ]
```

## Escape special characters in pattern.

Escape special characters in pattern. This is useful if you want to match an arbitrary literal string that may have regular expression metacharacters in it.

Jac Example

```jac
walker escape{

    can regex.escape;

    report regex.escape("https://www.jaseci.org");
}
```

Expected Output

```json
"report": [
    "https://www\\.jaseci\\.org"
  ]
```

## Clear the regular expression cache

Clear the regular expression cache

Jac Example

```Jac
walker purge{
    can regex.purge;
    report regex.purge();
}
```

Expected Output

```json
 "success": true,
  "report": [
    null
  ]
```