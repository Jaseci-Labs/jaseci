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
??? ebnf-snippet
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
??? ebnf-snippet
    ```yaml linenums="19"
    --8<-- "jaclang/compiler/jac.lark:19:30"
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
??? ebnf-snippet
    ```yaml linenums="33"
    --8<-- "jaclang/compiler/jac.lark:33:49"
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
??? ebnf-snippet
    ```yaml linenums="52"
    --8<-- "jaclang/compiler/jac.lark:52:57"
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
??? ebnf-snippet
    ```yaml linenums="60"
    --8<-- "jaclang/compiler/jac.lark:60:72"
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
??? ebnf-snippet
    ```yaml linenums="75"
    --8<-- "jaclang/compiler/jac.lark:75:86"
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
??? ebnf-snippet
    ```yaml linenums="89"
    --8<-- "jaclang/compiler/jac.lark:89:90"
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
??? ebnf-snippet
    ```yaml linenums="93"
    --8<-- "jaclang/compiler/jac.lark:93:93"
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
??? ebnf-snippet
    ```yaml linenums="96"
    --8<-- "jaclang/compiler/jac.lark:96:96"
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
??? ebnf-snippet
    ```yaml linenums="99"
    --8<-- "jaclang/compiler/jac.lark:99:99"
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
??? ebnf-snippet
    ```yaml linenums="102"
    --8<-- "jaclang/compiler/jac.lark:102:119"
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
??? ebnf-snippet
    ```yaml linenums="122"
    --8<-- "jaclang/compiler/jac.lark:122:149"
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
??? ebnf-snippet
    ```yaml linenums="152"
    --8<-- "jaclang/compiler/jac.lark:152:154"
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
??? ebnf-snippet
    ```yaml linenums="157"
    --8<-- "jaclang/compiler/jac.lark:157:157"
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
??? ebnf-snippet
    ```yaml linenums="160"
    --8<-- "jaclang/compiler/jac.lark:160:161"
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
??? ebnf-snippet
    ```yaml linenums="164"
    --8<-- "jaclang/compiler/jac.lark:164:167"
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
??? ebnf-snippet
    ```yaml linenums="170"
    --8<-- "jaclang/compiler/jac.lark:170:171"
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
??? ebnf-snippet
    ```yaml linenums="174"
    --8<-- "jaclang/compiler/jac.lark:174:184"
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
??? ebnf-snippet
    ```yaml linenums="187"
    --8<-- "jaclang/compiler/jac.lark:187:187"
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
??? ebnf-snippet
    ```yaml linenums="190"
    --8<-- "jaclang/compiler/jac.lark:190:190"
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
??? ebnf-snippet
    ```yaml linenums="193"
    --8<-- "jaclang/compiler/jac.lark:193:193"
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
??? ebnf-snippet
    ```yaml linenums="196"
    --8<-- "jaclang/compiler/jac.lark:196:197"
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
??? ebnf-snippet
    ```yaml linenums="200"
    --8<-- "jaclang/compiler/jac.lark:200:202"
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
??? ebnf-snippet
    ```yaml linenums="205"
    --8<-- "jaclang/compiler/jac.lark:205:209"
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
??? ebnf-snippet
    ```yaml linenums="212"
    --8<-- "jaclang/compiler/jac.lark:212:214"
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
??? ebnf-snippet
    ```yaml linenums="217"
    --8<-- "jaclang/compiler/jac.lark:217:219"
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
??? ebnf-snippet
    ```yaml linenums="222"
    --8<-- "jaclang/compiler/jac.lark:222:222"
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
??? ebnf-snippet
    ```yaml linenums="225"
    --8<-- "jaclang/compiler/jac.lark:225:225"
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
??? ebnf-snippet
    ```yaml linenums="228"
    --8<-- "jaclang/compiler/jac.lark:228:228"
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
??? ebnf-snippet
    ```yaml linenums="231"
    --8<-- "jaclang/compiler/jac.lark:231:231"
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
??? ebnf-snippet
    ```yaml linenums="234"
    --8<-- "jaclang/compiler/jac.lark:234:234"
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
??? ebnf-snippet
    ```yaml linenums="237"
    --8<-- "jaclang/compiler/jac.lark:237:237"
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
??? ebnf-snippet
    ```yaml linenums="240"
    --8<-- "jaclang/compiler/jac.lark:240:240"
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
??? ebnf-snippet
    ```yaml linenums="243"
    --8<-- "jaclang/compiler/jac.lark:243:243"
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
??? ebnf-snippet
    ```yaml linenums="246"
    --8<-- "jaclang/compiler/jac.lark:246:246"
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
??? ebnf-snippet
    ```yaml linenums="249"
    --8<-- "jaclang/compiler/jac.lark:249:252"
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
??? ebnf-snippet
    ```yaml linenums="255"
    --8<-- "jaclang/compiler/jac.lark:255:255"
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
??? ebnf-snippet
    ```yaml linenums="258"
    --8<-- "jaclang/compiler/jac.lark:258:258"
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
??? ebnf-snippet
    ```yaml linenums="261"
    --8<-- "jaclang/compiler/jac.lark:261:261"
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
??? ebnf-snippet
    ```yaml linenums="264"
    --8<-- "jaclang/compiler/jac.lark:264:264"
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
??? ebnf-snippet
    ```yaml linenums="267"
    --8<-- "jaclang/compiler/jac.lark:267:284"
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
??? ebnf-snippet
    ```yaml linenums="287"
    --8<-- "jaclang/compiler/jac.lark:287:288"
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
??? ebnf-snippet
    ```yaml linenums="291"
    --8<-- "jaclang/compiler/jac.lark:291:291"
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
??? ebnf-snippet
    ```yaml linenums="294"
    --8<-- "jaclang/compiler/jac.lark:294:294"
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
??? ebnf-snippet
    ```yaml linenums="297"
    --8<-- "jaclang/compiler/jac.lark:297:297"
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
??? ebnf-snippet
    ```yaml linenums="300"
    --8<-- "jaclang/compiler/jac.lark:300:300"
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
??? ebnf-snippet
    ```yaml linenums="303"
    --8<-- "jaclang/compiler/jac.lark:303:303"
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
??? ebnf-snippet
    ```yaml linenums="306"
    --8<-- "jaclang/compiler/jac.lark:306:309"
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
??? ebnf-snippet
    ```yaml linenums="312"
    --8<-- "jaclang/compiler/jac.lark:312:326"
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
??? ebnf-snippet
    ```yaml linenums="329"
    --8<-- "jaclang/compiler/jac.lark:329:332"
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
??? ebnf-snippet
    ```yaml linenums="335"
    --8<-- "jaclang/compiler/jac.lark:335:335"
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
??? ebnf-snippet
    ```yaml linenums="338"
    --8<-- "jaclang/compiler/jac.lark:338:338"
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
??? ebnf-snippet
    ```yaml linenums="341"
    --8<-- "jaclang/compiler/jac.lark:341:341"
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
??? ebnf-snippet
    ```yaml linenums="344"
    --8<-- "jaclang/compiler/jac.lark:344:344"
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
??? ebnf-snippet
    ```yaml linenums="347"
    --8<-- "jaclang/compiler/jac.lark:347:347"
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
??? ebnf-snippet
    ```yaml linenums="350"
    --8<-- "jaclang/compiler/jac.lark:350:350"
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
??? ebnf-snippet
    ```yaml linenums="353"
    --8<-- "jaclang/compiler/jac.lark:353:353"
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
??? ebnf-snippet
    ```yaml linenums="356"
    --8<-- "jaclang/compiler/jac.lark:356:361"
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
??? ebnf-snippet
    ```yaml linenums="364"
    --8<-- "jaclang/compiler/jac.lark:364:368"
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
??? ebnf-snippet
    ```yaml linenums="371"
    --8<-- "jaclang/compiler/jac.lark:371:396"
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
??? ebnf-snippet
    ```yaml linenums="399"
    --8<-- "jaclang/compiler/jac.lark:399:420"
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
??? ebnf-snippet
    ```yaml linenums="423"
    --8<-- "jaclang/compiler/jac.lark:423:430"
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
??? ebnf-snippet
    ```yaml linenums="433"
    --8<-- "jaclang/compiler/jac.lark:433:442"
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
??? ebnf-snippet
    ```yaml linenums="445"
    --8<-- "jaclang/compiler/jac.lark:445:450"
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
??? ebnf-snippet
    ```yaml linenums="453"
    --8<-- "jaclang/compiler/jac.lark:453:462"
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
??? ebnf-snippet
    ```yaml linenums="465"
    --8<-- "jaclang/compiler/jac.lark:465:475"
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
??? ebnf-snippet
    ```yaml linenums="478"
    --8<-- "jaclang/compiler/jac.lark:478:650"
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
??? ebnf-snippet
    ```yaml linenums="653"
    --8<-- "jaclang/compiler/jac.lark:653:664"
    ```
**Description**

--8<-- "examples/reference/f_string_tokens.md"

