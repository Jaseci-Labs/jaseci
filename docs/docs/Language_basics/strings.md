# Jaseci String Methods

In this section, the table below displays all of the **string** methods available in Jaseci for manipulating strings. These methods provide a comprehensive and efficient way to work with strings in your application.

| Op | Args | Description |
|----------|----------|----------|
| .str::upper | none |  |
| .str::lower | none |  |
| .str::title | none |  |
| .str::capitalize | none |  |
| .str::swap_case | none |  |
| .str::is_alnum | none |  |
| .str::is_digit | none |  |
| .str::is_title | none |  |
| .str::is_upper | none |  |
| .str::is_lower | none |  |
| .str::is_space | none |  |
| .str::load_json | none |  |
| .str::count | substr, start, end | Returns the number of occurrences of a sub-string in the given string. Start and end specify 
range of indices to search |
| .str::find | substr, start, end | Returns the index of first occurrence of the substring (if found). If not found, it returns -1. Start and end specify range of indices to
search. |
| .str::split | optional (separator,maxsplit) | Breaks up a string at the specified separator for
maxsplit number of times and returns a list of
strings. Default separators is ‘ ’ and maxsplit
is unlimited. |
| .str::join | params | Join elements of the sequence (params) separated by the string separator that calls the join function. |
| .str::startswith |  |  |
| .str::endswith |  |  |
| .str::replace |  |  |
| .str::strip | optional |  |
| .str::lstrip | optional |  |
| .str::rstrip | optional |  |
