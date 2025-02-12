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
    --8<-- "jaclang/compiler/jac.lark:42:58"
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
    ```yaml linenums="61"
    --8<-- "jaclang/compiler/jac.lark:61:66"
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
    ```yaml linenums="69"
    --8<-- "jaclang/compiler/jac.lark:69:81"
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
    ```yaml linenums="84"
    --8<-- "jaclang/compiler/jac.lark:84:95"
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
    ```yaml linenums="98"
    --8<-- "jaclang/compiler/jac.lark:98:99"
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
    ```yaml linenums="102"
    --8<-- "jaclang/compiler/jac.lark:102:102"
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
    ```yaml linenums="105"
    --8<-- "jaclang/compiler/jac.lark:105:105"
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
    ```yaml linenums="108"
    --8<-- "jaclang/compiler/jac.lark:108:108"
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
    ```yaml linenums="111"
    --8<-- "jaclang/compiler/jac.lark:111:128"
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
    ```yaml linenums="131"
    --8<-- "jaclang/compiler/jac.lark:131:158"
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
    ```yaml linenums="161"
    --8<-- "jaclang/compiler/jac.lark:161:163"
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
    ```yaml linenums="166"
    --8<-- "jaclang/compiler/jac.lark:166:166"
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
    ```yaml linenums="169"
    --8<-- "jaclang/compiler/jac.lark:169:170"
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
    ```yaml linenums="173"
    --8<-- "jaclang/compiler/jac.lark:173:176"
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
    ```yaml linenums="179"
    --8<-- "jaclang/compiler/jac.lark:179:180"
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
    ```yaml linenums="183"
    --8<-- "jaclang/compiler/jac.lark:183:193"
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
    ```yaml linenums="196"
    --8<-- "jaclang/compiler/jac.lark:196:196"
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
    ```yaml linenums="199"
    --8<-- "jaclang/compiler/jac.lark:199:199"
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
    ```yaml linenums="202"
    --8<-- "jaclang/compiler/jac.lark:202:202"
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
    ```yaml linenums="205"
    --8<-- "jaclang/compiler/jac.lark:205:206"
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
    ```yaml linenums="209"
    --8<-- "jaclang/compiler/jac.lark:209:211"
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
    ```yaml linenums="214"
    --8<-- "jaclang/compiler/jac.lark:214:218"
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
    ```yaml linenums="221"
    --8<-- "jaclang/compiler/jac.lark:221:223"
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
    ```yaml linenums="226"
    --8<-- "jaclang/compiler/jac.lark:226:228"
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
    ```yaml linenums="231"
    --8<-- "jaclang/compiler/jac.lark:231:231"
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
    ```yaml linenums="234"
    --8<-- "jaclang/compiler/jac.lark:234:234"
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
    ```yaml linenums="237"
    --8<-- "jaclang/compiler/jac.lark:237:237"
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
    ```yaml linenums="240"
    --8<-- "jaclang/compiler/jac.lark:240:240"
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
    ```yaml linenums="243"
    --8<-- "jaclang/compiler/jac.lark:243:243"
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
    ```yaml linenums="246"
    --8<-- "jaclang/compiler/jac.lark:246:246"
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
    ```yaml linenums="249"
    --8<-- "jaclang/compiler/jac.lark:249:249"
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
    ```yaml linenums="252"
    --8<-- "jaclang/compiler/jac.lark:252:252"
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
    ```yaml linenums="255"
    --8<-- "jaclang/compiler/jac.lark:255:255"
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
    ```yaml linenums="258"
    --8<-- "jaclang/compiler/jac.lark:258:261"
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
    ```yaml linenums="264"
    --8<-- "jaclang/compiler/jac.lark:264:264"
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
    ```yaml linenums="267"
    --8<-- "jaclang/compiler/jac.lark:267:267"
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
    ```yaml linenums="270"
    --8<-- "jaclang/compiler/jac.lark:270:270"
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
    ```yaml linenums="273"
    --8<-- "jaclang/compiler/jac.lark:273:273"
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
    ```yaml linenums="276"
    --8<-- "jaclang/compiler/jac.lark:276:293"
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
    ```yaml linenums="296"
    --8<-- "jaclang/compiler/jac.lark:296:297"
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
    ```yaml linenums="300"
    --8<-- "jaclang/compiler/jac.lark:300:300"
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
    ```yaml linenums="303"
    --8<-- "jaclang/compiler/jac.lark:303:303"
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
    ```yaml linenums="306"
    --8<-- "jaclang/compiler/jac.lark:306:306"
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
    ```yaml linenums="309"
    --8<-- "jaclang/compiler/jac.lark:309:309"
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
    ```yaml linenums="312"
    --8<-- "jaclang/compiler/jac.lark:312:315"
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
    ```yaml linenums="318"
    --8<-- "jaclang/compiler/jac.lark:318:332"
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
    ```yaml linenums="335"
    --8<-- "jaclang/compiler/jac.lark:335:338"
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
    ```yaml linenums="341"
    --8<-- "jaclang/compiler/jac.lark:341:341"
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
    ```yaml linenums="344"
    --8<-- "jaclang/compiler/jac.lark:344:344"
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
    ```yaml linenums="347"
    --8<-- "jaclang/compiler/jac.lark:347:347"
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
    ```yaml linenums="350"
    --8<-- "jaclang/compiler/jac.lark:350:350"
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
    ```yaml linenums="353"
    --8<-- "jaclang/compiler/jac.lark:353:353"
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
    ```yaml linenums="356"
    --8<-- "jaclang/compiler/jac.lark:356:356"
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
    ```yaml linenums="359"
    --8<-- "jaclang/compiler/jac.lark:359:359"
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
    ```yaml linenums="362"
    --8<-- "jaclang/compiler/jac.lark:362:370"
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
    ```yaml linenums="373"
    --8<-- "jaclang/compiler/jac.lark:373:377"
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
    ```yaml linenums="380"
    --8<-- "jaclang/compiler/jac.lark:380:405"
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
    ```yaml linenums="408"
    --8<-- "jaclang/compiler/jac.lark:408:429"
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
    ```yaml linenums="432"
    --8<-- "jaclang/compiler/jac.lark:432:439"
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
    ```yaml linenums="442"
    --8<-- "jaclang/compiler/jac.lark:442:451"
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
    ```yaml linenums="454"
    --8<-- "jaclang/compiler/jac.lark:454:459"
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
    ```yaml linenums="462"
    --8<-- "jaclang/compiler/jac.lark:462:471"
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
    ```yaml linenums="474"
    --8<-- "jaclang/compiler/jac.lark:474:500"
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
    ```yaml linenums="503"
    --8<-- "jaclang/compiler/jac.lark:503:526"
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
    ```yaml linenums="529"
    --8<-- "jaclang/compiler/jac.lark:529:715"
    ```
**Description**

--8<-- "examples/reference/lexer_tokens.md"

