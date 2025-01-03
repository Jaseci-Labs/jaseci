# Jac Language Reference

--8<-- "examples/reference/introduction.md"

## Base Module structure
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/base_module_structure.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/base_module_structure.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="2"
    --8<-- "jaclang/compiler/jac.lark:2:16"
    ```
**Description**

--8<-- "examples/reference/base_module_structure.md"

## Import/Include Statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/import_include_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/import_include_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="19"
    --8<-- "jaclang/compiler/jac.lark:19:31"
    ```
**Description**

--8<-- "examples/reference/import_include_statements.md"

## Architypes
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/architypes.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/architypes.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="34"
    --8<-- "jaclang/compiler/jac.lark:34:50"
    ```
**Description**

--8<-- "examples/reference/architypes.md"

## Architype bodies
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/architype_bodies.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/architype_bodies.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="53"
    --8<-- "jaclang/compiler/jac.lark:53:58"
    ```
**Description**

--8<-- "examples/reference/architype_bodies.md"

## Enumerations
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/enumerations.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/enumerations.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="61"
    --8<-- "jaclang/compiler/jac.lark:61:73"
    ```
**Description**

--8<-- "examples/reference/enumerations.md"

## Abilities
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/abilities.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/abilities.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="76"
    --8<-- "jaclang/compiler/jac.lark:76:87"
    ```
**Description**

--8<-- "examples/reference/abilities.md"

## Global variables
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/global_variables.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/global_variables.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="90"
    --8<-- "jaclang/compiler/jac.lark:90:91"
    ```
**Description**

--8<-- "examples/reference/global_variables.md"

## Free code
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/free_code.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/free_code.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="94"
    --8<-- "jaclang/compiler/jac.lark:94:94"
    ```
**Description**

--8<-- "examples/reference/free_code.md"

## Inline python
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/inline_python.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/inline_python.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="97"
    --8<-- "jaclang/compiler/jac.lark:97:97"
    ```
**Description**

--8<-- "examples/reference/inline_python.md"

## Tests
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/tests.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/tests.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="100"
    --8<-- "jaclang/compiler/jac.lark:100:100"
    ```
**Description**

--8<-- "examples/reference/tests.md"

## Implementations
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/implementations.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/implementations.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="103"
    --8<-- "jaclang/compiler/jac.lark:103:120"
    ```
**Description**

--8<-- "examples/reference/implementations.md"

## Codeblocks and Statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/codeblocks_and_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/codeblocks_and_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="123"
    --8<-- "jaclang/compiler/jac.lark:123:150"
    ```
**Description**

--8<-- "examples/reference/codeblocks_and_statements.md"

## If statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/if_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/if_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="153"
    --8<-- "jaclang/compiler/jac.lark:153:155"
    ```
**Description**

--8<-- "examples/reference/if_statements.md"

## While statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/while_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/while_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="158"
    --8<-- "jaclang/compiler/jac.lark:158:158"
    ```
**Description**

--8<-- "examples/reference/while_statements.md"

## For statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/for_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/for_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="161"
    --8<-- "jaclang/compiler/jac.lark:161:162"
    ```
**Description**

--8<-- "examples/reference/for_statements.md"

## Try statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/try_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/try_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="165"
    --8<-- "jaclang/compiler/jac.lark:165:168"
    ```
**Description**

--8<-- "examples/reference/try_statements.md"

## Match statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="171"
    --8<-- "jaclang/compiler/jac.lark:171:172"
    ```
**Description**

--8<-- "examples/reference/match_statements.md"

## Match patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="175"
    --8<-- "jaclang/compiler/jac.lark:175:185"
    ```
**Description**

--8<-- "examples/reference/match_patterns.md"

## Match litteral patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_litteral_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_litteral_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="188"
    --8<-- "jaclang/compiler/jac.lark:188:188"
    ```
**Description**

--8<-- "examples/reference/match_litteral_patterns.md"

## Match singleton patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_singleton_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_singleton_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="191"
    --8<-- "jaclang/compiler/jac.lark:191:191"
    ```
**Description**

--8<-- "examples/reference/match_singleton_patterns.md"

## Match capture patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_capture_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_capture_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="194"
    --8<-- "jaclang/compiler/jac.lark:194:194"
    ```
**Description**

--8<-- "examples/reference/match_capture_patterns.md"

## Match sequence patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_sequence_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_sequence_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="197"
    --8<-- "jaclang/compiler/jac.lark:197:198"
    ```
**Description**

--8<-- "examples/reference/match_sequence_patterns.md"

## Match mapping patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_mapping_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_mapping_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="201"
    --8<-- "jaclang/compiler/jac.lark:201:203"
    ```
**Description**

--8<-- "examples/reference/match_mapping_patterns.md"

## Match class patterns
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/match_class_patterns.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/match_class_patterns.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="206"
    --8<-- "jaclang/compiler/jac.lark:206:210"
    ```
**Description**

--8<-- "examples/reference/match_class_patterns.md"

## Context managers
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/context_managers.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/context_managers.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="213"
    --8<-- "jaclang/compiler/jac.lark:213:215"
    ```
**Description**

--8<-- "examples/reference/context_managers.md"

## Global and nonlocal statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/global_and_nonlocal_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/global_and_nonlocal_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="218"
    --8<-- "jaclang/compiler/jac.lark:218:220"
    ```
**Description**

--8<-- "examples/reference/global_and_nonlocal_statements.md"

## Data spatial typed context blocks
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/data_spatial_typed_context_blocks.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/data_spatial_typed_context_blocks.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="223"
    --8<-- "jaclang/compiler/jac.lark:223:223"
    ```
**Description**

--8<-- "examples/reference/data_spatial_typed_context_blocks.md"

## Return statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/return_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/return_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="226"
    --8<-- "jaclang/compiler/jac.lark:226:226"
    ```
**Description**

--8<-- "examples/reference/return_statements.md"

## Yield statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/yield_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/yield_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="229"
    --8<-- "jaclang/compiler/jac.lark:229:229"
    ```
**Description**

--8<-- "examples/reference/yield_statements.md"

## Raise statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/raise_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/raise_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="232"
    --8<-- "jaclang/compiler/jac.lark:232:232"
    ```
**Description**

--8<-- "examples/reference/raise_statements.md"

## Assert statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/assert_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/assert_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="235"
    --8<-- "jaclang/compiler/jac.lark:235:235"
    ```
**Description**

--8<-- "examples/reference/assert_statements.md"

## Check statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/check_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/check_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="238"
    --8<-- "jaclang/compiler/jac.lark:238:238"
    ```
**Description**

--8<-- "examples/reference/check_statements.md"

## Delete statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/delete_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/delete_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="241"
    --8<-- "jaclang/compiler/jac.lark:241:241"
    ```
**Description**

--8<-- "examples/reference/delete_statements.md"

## Report statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/report_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/report_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="244"
    --8<-- "jaclang/compiler/jac.lark:244:244"
    ```
**Description**

--8<-- "examples/reference/report_statements.md"

## Control statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/control_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/control_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="247"
    --8<-- "jaclang/compiler/jac.lark:247:247"
    ```
**Description**

--8<-- "examples/reference/control_statements.md"

## Data spatial Walker statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/data_spatial_walker_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/data_spatial_walker_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="250"
    --8<-- "jaclang/compiler/jac.lark:250:253"
    ```
**Description**

--8<-- "examples/reference/data_spatial_walker_statements.md"

## Visit statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/visit_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/visit_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="256"
    --8<-- "jaclang/compiler/jac.lark:256:256"
    ```
**Description**

--8<-- "examples/reference/visit_statements.md"

## Revisit statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/revisit_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/revisit_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="259"
    --8<-- "jaclang/compiler/jac.lark:259:259"
    ```
**Description**

--8<-- "examples/reference/revisit_statements.md"

## Disengage statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/disengage_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/disengage_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="262"
    --8<-- "jaclang/compiler/jac.lark:262:262"
    ```
**Description**

--8<-- "examples/reference/disengage_statements.md"

## Ignore statements
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/ignore_statements.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/ignore_statements.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="265"
    --8<-- "jaclang/compiler/jac.lark:265:265"
    ```
**Description**

--8<-- "examples/reference/ignore_statements.md"

## Assignments
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/assignments.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/assignments.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="268"
    --8<-- "jaclang/compiler/jac.lark:268:285"
    ```
**Description**

--8<-- "examples/reference/assignments.md"

## Expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="288"
    --8<-- "jaclang/compiler/jac.lark:288:289"
    ```
**Description**

--8<-- "examples/reference/expressions.md"

## Walrus assignments
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/walrus_assignments.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/walrus_assignments.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="292"
    --8<-- "jaclang/compiler/jac.lark:292:292"
    ```
**Description**

--8<-- "examples/reference/walrus_assignments.md"

## Lambda expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/lambda_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/lambda_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="295"
    --8<-- "jaclang/compiler/jac.lark:295:295"
    ```
**Description**

--8<-- "examples/reference/lambda_expressions.md"

## Pipe expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/pipe_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/pipe_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="298"
    --8<-- "jaclang/compiler/jac.lark:298:298"
    ```
**Description**

--8<-- "examples/reference/pipe_expressions.md"

## Pipe back expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/pipe_back_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/pipe_back_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="301"
    --8<-- "jaclang/compiler/jac.lark:301:301"
    ```
**Description**

--8<-- "examples/reference/pipe_back_expressions.md"

## Elvis expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/elvis_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/elvis_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="304"
    --8<-- "jaclang/compiler/jac.lark:304:304"
    ```
**Description**

--8<-- "examples/reference/elvis_expressions.md"

## Bitwise expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/bitwise_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/bitwise_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="307"
    --8<-- "jaclang/compiler/jac.lark:307:310"
    ```
**Description**

--8<-- "examples/reference/bitwise_expressions.md"

## Logical and compare expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/logical_and_compare_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/logical_and_compare_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="313"
    --8<-- "jaclang/compiler/jac.lark:313:327"
    ```
**Description**

--8<-- "examples/reference/logical_and_compare_expressions.md"

## Arithmetic expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/arithmetic_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/arithmetic_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="330"
    --8<-- "jaclang/compiler/jac.lark:330:333"
    ```
**Description**

--8<-- "examples/reference/arithmetic_expressions.md"

## Connect expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/connect_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/connect_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="336"
    --8<-- "jaclang/compiler/jac.lark:336:336"
    ```
**Description**

--8<-- "examples/reference/connect_expressions.md"

## Atomic expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/atomic_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/atomic_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="339"
    --8<-- "jaclang/compiler/jac.lark:339:339"
    ```
**Description**

--8<-- "examples/reference/atomic_expressions.md"

## Atomic pipe back expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/atomic_pipe_back_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/atomic_pipe_back_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="342"
    --8<-- "jaclang/compiler/jac.lark:342:342"
    ```
**Description**

--8<-- "examples/reference/atomic_pipe_back_expressions.md"

## Data spatial spawn expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/data_spatial_spawn_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/data_spatial_spawn_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="345"
    --8<-- "jaclang/compiler/jac.lark:345:345"
    ```
**Description**

--8<-- "examples/reference/data_spatial_spawn_expressions.md"

## Unpack expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/unpack_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/unpack_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="348"
    --8<-- "jaclang/compiler/jac.lark:348:348"
    ```
**Description**

--8<-- "examples/reference/unpack_expressions.md"

## References (unused)
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/references_(unused).jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/references_(unused).py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="351"
    --8<-- "jaclang/compiler/jac.lark:351:351"
    ```
**Description**

--8<-- "examples/reference/references_(unused).md"

## Data spatial calls
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/data_spatial_calls.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/data_spatial_calls.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="354"
    --8<-- "jaclang/compiler/jac.lark:354:354"
    ```
**Description**

--8<-- "examples/reference/data_spatial_calls.md"

## Subscripted and dotted expressions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/subscripted_and_dotted_expressions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/subscripted_and_dotted_expressions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="357"
    --8<-- "jaclang/compiler/jac.lark:357:365"
    ```
**Description**

--8<-- "examples/reference/subscripted_and_dotted_expressions.md"

## Function calls
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/function_calls.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/function_calls.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="368"
    --8<-- "jaclang/compiler/jac.lark:368:372"
    ```
**Description**

--8<-- "examples/reference/function_calls.md"

## Atom
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/atom.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/atom.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="375"
    --8<-- "jaclang/compiler/jac.lark:375:400"
    ```
**Description**

--8<-- "examples/reference/atom.md"

## Collection values
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/collection_values.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/collection_values.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="403"
    --8<-- "jaclang/compiler/jac.lark:403:424"
    ```
**Description**

--8<-- "examples/reference/collection_values.md"

## Tuples and Jac Tuples
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/tuples_and_jac_tuples.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/tuples_and_jac_tuples.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="427"
    --8<-- "jaclang/compiler/jac.lark:427:434"
    ```
**Description**

--8<-- "examples/reference/tuples_and_jac_tuples.md"

## Data Spatial References
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/data_spatial_references.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/data_spatial_references.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="437"
    --8<-- "jaclang/compiler/jac.lark:437:446"
    ```
**Description**

--8<-- "examples/reference/data_spatial_references.md"

## Special Comprehensions
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/special_comprehensions.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/special_comprehensions.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="449"
    --8<-- "jaclang/compiler/jac.lark:449:454"
    ```
**Description**

--8<-- "examples/reference/special_comprehensions.md"

## Names and references
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/names_and_references.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/names_and_references.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="457"
    --8<-- "jaclang/compiler/jac.lark:457:466"
    ```
**Description**

--8<-- "examples/reference/names_and_references.md"

## Builtin types
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/builtin_types.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/builtin_types.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="469"
    --8<-- "jaclang/compiler/jac.lark:469:479"
    ```
**Description**

--8<-- "examples/reference/builtin_types.md"

## Lexer Tokens
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/lexer_tokens.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/lexer_tokens.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="482"
    --8<-- "jaclang/compiler/jac.lark:482:654"
    ```
**Description**

--8<-- "examples/reference/lexer_tokens.md"

## f-string tokens
**Code Example**
=== "Jac"
    ```jac linenums="1"
    --8<-- "examples/reference/f_string_tokens.jac"
    ```
=== "Python"
    ```python linenums="1"
    --8<-- "examples/reference/f_string_tokens.py"
    ```
??? example "Jac Grammar Snippet"
    ```yaml linenums="657"
    --8<-- "jaclang/compiler/jac.lark:657:668"
    ```
**Description**

--8<-- "examples/reference/f_string_tokens.md"

