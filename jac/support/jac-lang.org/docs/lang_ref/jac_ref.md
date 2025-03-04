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
    --8<-- "jaclang/compiler/jac.lark:2:24"
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
    ```yaml linenums="27"
    --8<-- "jaclang/compiler/jac.lark:27:39"
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
    ```yaml linenums="42"
    --8<-- "jaclang/compiler/jac.lark:42:57"
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
    ```yaml linenums="60"
    --8<-- "jaclang/compiler/jac.lark:60:65"
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
    ```yaml linenums="68"
    --8<-- "jaclang/compiler/jac.lark:68:80"
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
    ```yaml linenums="83"
    --8<-- "jaclang/compiler/jac.lark:83:94"
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
    ```yaml linenums="97"
    --8<-- "jaclang/compiler/jac.lark:97:98"
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
    ```yaml linenums="101"
    --8<-- "jaclang/compiler/jac.lark:101:101"
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
    ```yaml linenums="104"
    --8<-- "jaclang/compiler/jac.lark:104:104"
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
    ```yaml linenums="107"
    --8<-- "jaclang/compiler/jac.lark:107:107"
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
    ```yaml linenums="110"
    --8<-- "jaclang/compiler/jac.lark:110:127"
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
    ```yaml linenums="130"
    --8<-- "jaclang/compiler/jac.lark:130:157"
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
    ```yaml linenums="160"
    --8<-- "jaclang/compiler/jac.lark:160:162"
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
    ```yaml linenums="165"
    --8<-- "jaclang/compiler/jac.lark:165:165"
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
    ```yaml linenums="168"
    --8<-- "jaclang/compiler/jac.lark:168:169"
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
    ```yaml linenums="172"
    --8<-- "jaclang/compiler/jac.lark:172:175"
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
    ```yaml linenums="178"
    --8<-- "jaclang/compiler/jac.lark:178:179"
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
    ```yaml linenums="182"
    --8<-- "jaclang/compiler/jac.lark:182:192"
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
    ```yaml linenums="195"
    --8<-- "jaclang/compiler/jac.lark:195:195"
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
    ```yaml linenums="198"
    --8<-- "jaclang/compiler/jac.lark:198:198"
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
    ```yaml linenums="201"
    --8<-- "jaclang/compiler/jac.lark:201:201"
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
    ```yaml linenums="204"
    --8<-- "jaclang/compiler/jac.lark:204:205"
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
    ```yaml linenums="208"
    --8<-- "jaclang/compiler/jac.lark:208:210"
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
    ```yaml linenums="213"
    --8<-- "jaclang/compiler/jac.lark:213:217"
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
    ```yaml linenums="220"
    --8<-- "jaclang/compiler/jac.lark:220:222"
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
    ```yaml linenums="225"
    --8<-- "jaclang/compiler/jac.lark:225:227"
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
    ```yaml linenums="230"
    --8<-- "jaclang/compiler/jac.lark:230:230"
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
    ```yaml linenums="233"
    --8<-- "jaclang/compiler/jac.lark:233:233"
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
    ```yaml linenums="236"
    --8<-- "jaclang/compiler/jac.lark:236:236"
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
    ```yaml linenums="239"
    --8<-- "jaclang/compiler/jac.lark:239:239"
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
    ```yaml linenums="242"
    --8<-- "jaclang/compiler/jac.lark:242:242"
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
    ```yaml linenums="245"
    --8<-- "jaclang/compiler/jac.lark:245:245"
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
    ```yaml linenums="248"
    --8<-- "jaclang/compiler/jac.lark:248:248"
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
    ```yaml linenums="251"
    --8<-- "jaclang/compiler/jac.lark:251:251"
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
    ```yaml linenums="254"
    --8<-- "jaclang/compiler/jac.lark:254:254"
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
    ```yaml linenums="257"
    --8<-- "jaclang/compiler/jac.lark:257:260"
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
    ```yaml linenums="263"
    --8<-- "jaclang/compiler/jac.lark:263:263"
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
    ```yaml linenums="266"
    --8<-- "jaclang/compiler/jac.lark:266:266"
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
    ```yaml linenums="269"
    --8<-- "jaclang/compiler/jac.lark:269:269"
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
    ```yaml linenums="272"
    --8<-- "jaclang/compiler/jac.lark:272:272"
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
    ```yaml linenums="275"
    --8<-- "jaclang/compiler/jac.lark:275:292"
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
    ```yaml linenums="295"
    --8<-- "jaclang/compiler/jac.lark:295:296"
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
    ```yaml linenums="299"
    --8<-- "jaclang/compiler/jac.lark:299:299"
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
    ```yaml linenums="302"
    --8<-- "jaclang/compiler/jac.lark:302:302"
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
    ```yaml linenums="305"
    --8<-- "jaclang/compiler/jac.lark:305:305"
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
    ```yaml linenums="308"
    --8<-- "jaclang/compiler/jac.lark:308:308"
    ```
**Description**

--8<-- "examples/reference/pipe_back_expressions.md"

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
    ```yaml linenums="311"
    --8<-- "jaclang/compiler/jac.lark:311:314"
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
    ```yaml linenums="317"
    --8<-- "jaclang/compiler/jac.lark:317:331"
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
    ```yaml linenums="334"
    --8<-- "jaclang/compiler/jac.lark:334:337"
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
    ```yaml linenums="340"
    --8<-- "jaclang/compiler/jac.lark:340:340"
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
    ```yaml linenums="343"
    --8<-- "jaclang/compiler/jac.lark:343:343"
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
    ```yaml linenums="346"
    --8<-- "jaclang/compiler/jac.lark:346:346"
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
    ```yaml linenums="349"
    --8<-- "jaclang/compiler/jac.lark:349:349"
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
    ```yaml linenums="352"
    --8<-- "jaclang/compiler/jac.lark:352:352"
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
    ```yaml linenums="355"
    --8<-- "jaclang/compiler/jac.lark:355:355"
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
    ```yaml linenums="358"
    --8<-- "jaclang/compiler/jac.lark:358:358"
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
    ```yaml linenums="361"
    --8<-- "jaclang/compiler/jac.lark:361:369"
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
    ```yaml linenums="372"
    --8<-- "jaclang/compiler/jac.lark:372:376"
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
    ```yaml linenums="379"
    --8<-- "jaclang/compiler/jac.lark:379:404"
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
    ```yaml linenums="407"
    --8<-- "jaclang/compiler/jac.lark:407:428"
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
    ```yaml linenums="431"
    --8<-- "jaclang/compiler/jac.lark:431:438"
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
    ```yaml linenums="441"
    --8<-- "jaclang/compiler/jac.lark:441:450"
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
    ```yaml linenums="453"
    --8<-- "jaclang/compiler/jac.lark:453:458"
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
    ```yaml linenums="461"
    --8<-- "jaclang/compiler/jac.lark:461:470"
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
    ```yaml linenums="473"
    --8<-- "jaclang/compiler/jac.lark:473:499"
    ```
**Description**

--8<-- "examples/reference/builtin_types.md"

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
    ```yaml linenums="502"
    --8<-- "jaclang/compiler/jac.lark:502:525"
    ```
**Description**

--8<-- "examples/reference/f_string_tokens.md"

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
    ```yaml linenums="528"
    --8<-- "jaclang/compiler/jac.lark:528:714"
    ```
**Description**

--8<-- "examples/reference/lexer_tokens.md"

