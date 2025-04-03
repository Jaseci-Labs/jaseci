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
    --8<-- "jaclang/compiler/jac.lark:2:12"
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
    ```yaml linenums="15"
    --8<-- "jaclang/compiler/jac.lark:15:27"
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
    ```yaml linenums="30"
    --8<-- "jaclang/compiler/jac.lark:30:46"
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
    ```yaml linenums="49"
    --8<-- "jaclang/compiler/jac.lark:49:54"
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
    ```yaml linenums="57"
    --8<-- "jaclang/compiler/jac.lark:57:69"
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
    ```yaml linenums="72"
    --8<-- "jaclang/compiler/jac.lark:72:83"
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
    ```yaml linenums="86"
    --8<-- "jaclang/compiler/jac.lark:86:87"
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
    ```yaml linenums="90"
    --8<-- "jaclang/compiler/jac.lark:90:90"
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
    ```yaml linenums="93"
    --8<-- "jaclang/compiler/jac.lark:93:93"
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
    ```yaml linenums="96"
    --8<-- "jaclang/compiler/jac.lark:96:96"
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
    ```yaml linenums="99"
    --8<-- "jaclang/compiler/jac.lark:99:116"
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
    ```yaml linenums="119"
    --8<-- "jaclang/compiler/jac.lark:119:146"
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
    ```yaml linenums="149"
    --8<-- "jaclang/compiler/jac.lark:149:151"
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
    ```yaml linenums="154"
    --8<-- "jaclang/compiler/jac.lark:154:154"
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
    ```yaml linenums="157"
    --8<-- "jaclang/compiler/jac.lark:157:158"
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
    ```yaml linenums="161"
    --8<-- "jaclang/compiler/jac.lark:161:164"
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
    ```yaml linenums="167"
    --8<-- "jaclang/compiler/jac.lark:167:168"
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
    ```yaml linenums="171"
    --8<-- "jaclang/compiler/jac.lark:171:181"
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
    ```yaml linenums="184"
    --8<-- "jaclang/compiler/jac.lark:184:184"
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
    ```yaml linenums="187"
    --8<-- "jaclang/compiler/jac.lark:187:187"
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
    ```yaml linenums="190"
    --8<-- "jaclang/compiler/jac.lark:190:190"
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
    ```yaml linenums="193"
    --8<-- "jaclang/compiler/jac.lark:193:194"
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
    ```yaml linenums="197"
    --8<-- "jaclang/compiler/jac.lark:197:199"
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
    ```yaml linenums="202"
    --8<-- "jaclang/compiler/jac.lark:202:206"
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
    ```yaml linenums="209"
    --8<-- "jaclang/compiler/jac.lark:209:211"
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
    ```yaml linenums="214"
    --8<-- "jaclang/compiler/jac.lark:214:216"
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
    ```yaml linenums="219"
    --8<-- "jaclang/compiler/jac.lark:219:219"
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
    ```yaml linenums="222"
    --8<-- "jaclang/compiler/jac.lark:222:222"
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
    ```yaml linenums="225"
    --8<-- "jaclang/compiler/jac.lark:225:225"
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
    ```yaml linenums="228"
    --8<-- "jaclang/compiler/jac.lark:228:228"
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
    ```yaml linenums="231"
    --8<-- "jaclang/compiler/jac.lark:231:231"
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
    ```yaml linenums="234"
    --8<-- "jaclang/compiler/jac.lark:234:234"
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
    ```yaml linenums="237"
    --8<-- "jaclang/compiler/jac.lark:237:237"
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
    ```yaml linenums="240"
    --8<-- "jaclang/compiler/jac.lark:240:240"
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
    ```yaml linenums="243"
    --8<-- "jaclang/compiler/jac.lark:243:243"
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
    ```yaml linenums="246"
    --8<-- "jaclang/compiler/jac.lark:246:249"
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
    ```yaml linenums="252"
    --8<-- "jaclang/compiler/jac.lark:252:252"
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
    ```yaml linenums="255"
    --8<-- "jaclang/compiler/jac.lark:255:255"
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
    ```yaml linenums="258"
    --8<-- "jaclang/compiler/jac.lark:258:258"
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
    ```yaml linenums="261"
    --8<-- "jaclang/compiler/jac.lark:261:261"
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
    ```yaml linenums="264"
    --8<-- "jaclang/compiler/jac.lark:264:281"
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
    ```yaml linenums="284"
    --8<-- "jaclang/compiler/jac.lark:284:285"
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
    ```yaml linenums="288"
    --8<-- "jaclang/compiler/jac.lark:288:288"
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
    ```yaml linenums="291"
    --8<-- "jaclang/compiler/jac.lark:291:291"
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
    ```yaml linenums="294"
    --8<-- "jaclang/compiler/jac.lark:294:294"
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
    ```yaml linenums="297"
    --8<-- "jaclang/compiler/jac.lark:297:297"
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
    ```yaml linenums="300"
    --8<-- "jaclang/compiler/jac.lark:300:303"
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
    ```yaml linenums="306"
    --8<-- "jaclang/compiler/jac.lark:306:320"
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
    ```yaml linenums="323"
    --8<-- "jaclang/compiler/jac.lark:323:326"
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
    ```yaml linenums="329"
    --8<-- "jaclang/compiler/jac.lark:329:329"
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
    ```yaml linenums="332"
    --8<-- "jaclang/compiler/jac.lark:332:332"
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
    ```yaml linenums="335"
    --8<-- "jaclang/compiler/jac.lark:335:335"
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
    ```yaml linenums="338"
    --8<-- "jaclang/compiler/jac.lark:338:338"
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
    ```yaml linenums="341"
    --8<-- "jaclang/compiler/jac.lark:341:341"
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
    ```yaml linenums="344"
    --8<-- "jaclang/compiler/jac.lark:344:344"
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
    ```yaml linenums="347"
    --8<-- "jaclang/compiler/jac.lark:347:347"
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
    ```yaml linenums="350"
    --8<-- "jaclang/compiler/jac.lark:350:358"
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
    ```yaml linenums="361"
    --8<-- "jaclang/compiler/jac.lark:361:365"
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
    ```yaml linenums="368"
    --8<-- "jaclang/compiler/jac.lark:368:393"
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
    ```yaml linenums="396"
    --8<-- "jaclang/compiler/jac.lark:396:417"
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
    ```yaml linenums="420"
    --8<-- "jaclang/compiler/jac.lark:420:427"
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
    ```yaml linenums="430"
    --8<-- "jaclang/compiler/jac.lark:430:439"
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
    ```yaml linenums="442"
    --8<-- "jaclang/compiler/jac.lark:442:447"
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
    ```yaml linenums="450"
    --8<-- "jaclang/compiler/jac.lark:450:459"
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
    ```yaml linenums="462"
    --8<-- "jaclang/compiler/jac.lark:462:488"
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
    ```yaml linenums="491"
    --8<-- "jaclang/compiler/jac.lark:491:514"
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
    ```yaml linenums="517"
    --8<-- "jaclang/compiler/jac.lark:517:702"
    ```
**Description**

--8<-- "examples/reference/lexer_tokens.md"

