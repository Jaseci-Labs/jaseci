## Sort List Alphanumerically
List objects have a **sort()** method that will sort the list alphanumerically, ascending, by default:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Sort_list/jac_sort_list_alph.jac"
    ```

## Sort Descending
To sort descending, use the keyword argument **reverse = True**:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Sort_list/jac_sort_decending.jac"
    ```

## Customize Sort Function
You can define a custom function for sorting by using the keyword argument **key=function**.This function should return a numeric value, which will be used to determine the sorting order, with the lowest values appearing first.

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Sort_list/jac_sort_custome_sort.jac"
    ```

## Case Insensitive Sort
By default the **sort()** method is case sensitive, resulting in all capital letters being sorted before lower case letters:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Sort_list/jac_sort_case_insensitive.jac"
    ```

## Reverse Order
The **reverse()** method reverses the current sorting order of the elements:

**Code Example**
    ```jac linenums="1"
    --8<-- "examples/learning_section/jac_list/Sort_list/jac_sort_reverse.jac"
    ```