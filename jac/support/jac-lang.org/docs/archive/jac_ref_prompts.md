**General**

You are writing documentation for programming language called Jac. The title, grammar snippet, and jac program of a section is below:

Title:

Grammar:

Jac Code:

(no note version: Write a very short section of documentation focused on the Jac Code in a technical tone (no salesy language) for this.)

Write a very short section of documentation in a technical tone (no salesy language) for this based on the Notes below. Don't include any code snippets in your response.

Notes:


**Introduction**


* This document serves as a reference guide to the jac language, a formal specification of the langauge, and a test suite of the language.
* This reference covers the full implementation of the Jac language and is hard synced and tested against the official repo of the language, grammar snippets and code examples are automatically generated from the actual grammar and test cases of the language.
* Basically only the descriptions can ever be out of date. I'm really happy about this property of this documentaiton, I know you can tell.
* The goal of this document is to be the defacto tool to use whenever you wonder to yourself "Hrm, how do I code X in Jac again?"

**Base Module Structure Notes**

* A module in Jac corresponds to a module in Python.
* Jac is a bit stricter on how docstrings can be used, 1 for every module at the top and 1 for each element within a module.
* If there is only 1 docstring before the first element in a module it is assumed to be the module level docstring
* Elements include the familar stuff from python such as functions and classes (in this case called architype in the grammar), however there are some novel elements that we go into later.
* The code example illustrates a module with a few elements in it.
* Note that Jac requires type annotations in the function signatures to support and strongly encourage type safety.
* Note that in Jac any free floating module level code must be wrapped with a `with entry {}` for clarity and cleanliness

**Import/Include Statements**

* Imports statements are similar to python with a few key differences
* In  the example we see the imports of regular python with the usage of `:py` and jac files with `:jac`
* the python imports work exactly as you would expect, you can freely import python modules anywhere in a jac program
* the Jac imports work similary except they apply to `.jac` files.
* note that the import froms use import from, this was a style change for readability

**