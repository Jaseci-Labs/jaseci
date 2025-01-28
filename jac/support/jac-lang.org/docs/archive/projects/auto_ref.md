# Self Syncing Jac Language Reference

## Goal

The goal of this project is to create the official Complete Jac Language Reference. This work will include the creation of example code that covers the syntax and semantics of the language and some automation to keep it updated and synced with the codebase. There will be 2 important pieces of automation for the reference, first in generating the linked code blocks to the official language grammar in addition to automated testing of code examples.

## Description

The grammar for the language (`jac.lark`) is complete and serves as a source of truth spec for all valid Jac programs. It is sectioned off into logical documentable sections. We will call these “ref sections” throughout this document. For example,

```
// Enumerations
enum: enum_def
     | enum_decl

enum_decl: KW_ENUM access_tag? NAME inherited_archs? (enum_block | SEMI)
enum_def: arch_to_enum_chain enum_block

// Enumeration Bodies
enum_block: LBRACE ((enum_stmt COMMA)* enum_stmt)? RBRACE

enum_stmt: NAME EQ expression
         | NAME
         | py_code_block
```

Here we have 2 sections one for enumerations the other for the bodies of enumerations in Jac.

The reference will also be organized in corresponding sections. For each section, we will create separate md documents that include the documentation for each section.

```bash
enums.md
enum_bodies.md
```

The contents of these files will include the relevant documentation for each ref section and linked code blocks to standalone code for both the Jac and Python-equivalent versions of the example.

> FYI
> A linked code block looks like:
>
```
### Module Elements
``yaml linenums="10"
--.8<-- "jaclang/jac/jac.lark:10:17"
``
```
> Except without the dot in front of the 8.


All code example for ref sections will be housed in a `examples/reference` directory in the examples folder of jaclang. The md file themselves will live in a `.../docs/reference` folder of the current documentation.

## Automation

These files will serve as modules that will be automatically assembled into a single file called `complete_ref.md` that will include all of the sections of the reference together.

A function will be added to the lang_tools package in jaclang that will do this assembling while also generating the correct inlined sections of `jac.lark`.


For example for the section:

``` linenums="1"
--8<-- "jaclang/jac/jac.lark::27"
```

Would generate:

```
## Base Module structure
``yaml linenums="2"
--.8<-- "jaclang/jac/jac.lark:2:19"
``
--.8<-- ".../docs/reference/module.md"

## Import/Include Statements
``yaml linenums="20"
--.8<-- "jaclang/jac/jac.lark:20:27"
``
--.8<-- ".../docs/reference/impt_incl.md"
```

The comments structure above each of the ref sections will be extended to support this i.e.,
```
// Base Module structure
```

should become

```
// Base Module structure
// doc: module.md
```

and

```
// Import/Include Statements
// doc: impt_incl.md
```

for example.

The automation function in the lang_tools package will parse these headers from `jac.lark` to drive the assembly of doc files generation of the full reference's md file.

## Constraints

- Jac and python versions are needed for each example
- Both programs should run and produce the same output
- Ultimately there will be automated testes for the correctness of these programs

## Concrete Steps

* [TeamRise] First in `examples/reference` we need to have a single `.jac` file for each section in addition to a single `.py` file for each example, the programs should logically produce the same output.

    * The Jac example only have to pass parse errors.
    * The python should produce expected output.
    * If the example is Jac-only, create a python file with our naming convention, however have it just `print("Jac only feature")`
    * Reach Goal: 30 sections, both jac and python.

* PR into Kug's branch
* Kug and team tests the jac_ref generation
* Homogenize all examples and file names
* Update targets file
* Push branch
* Write auto test that all py files run in reference (see test_language.py)



* [MarsNinja] Automated testing infrastructure to run both jac programs and python programs to check outputs match

* ... reference gen infra.
