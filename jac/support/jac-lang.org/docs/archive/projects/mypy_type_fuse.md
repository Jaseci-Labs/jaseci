# Self Syncing Jac Language Reference

## Goal

The goal of this project is to have a deeper fusing between mypy's internal AST representation and the Jac AST. Mypy builds a library of dependant files and its own representation it build from python ASTs of those files. Currently, Jac will provide it's internal generated python AST to mypy and provide a callback function for error reporting that jac can provide an implementation for. In this next step, we'd like to have a deeper integration to mypy's internal representation by linking nodes to mypy's AST representation as well as errors inside mypy coverted to Jac's Alert type. We'd also like to understand more about mypy's internal representations and it's daemon mode to see what should be road-mapped on the Jac's side to better align it to mypy's operations to simplify implementations.

## Description


## Notes

* Validate ASTConverter in MYPY is seeing our Jac generated python ast nodes with the .jac_link field present.

* If that is the case, the .jac_link field is pointing to a Jac ast node, and we simply have to create a .gen.mypy_ast on jac nodes to point to the relevant mypy ast node. And we can add a jac_link on each mypy uni_node.

* Finally... we are going to take advantage of these links between ASTs to register type error properly through Jac's alert system.

