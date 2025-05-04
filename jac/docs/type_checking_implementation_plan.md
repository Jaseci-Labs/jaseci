# Type Checking Implementation Plan for Jac

This document outlines a step-by-step implementation plan for the new type checking system described in the architecture proposal.

## Phase 1: Basic Type System and Type Binder (2-3 weeks)

### Week 1: Type System Implementation
- [ ] Create the `types.py` module with the base type classes
- [ ] Implement primitive types (int, float, str, bool, etc.)
- [ ] Implement container types (list, dict, set, tuple)
- [ ] Implement function types
- [ ] Implement class types
- [ ] Add Jac-specific types (walker, node, edge, ability, enum)
- [ ] Write unit tests for the type system

### Week 2: Type Binder Implementation
- [ ] Create the `type_binder_pass.py` module
- [ ] Implement binding for literal values (int, float, str, bool)
- [ ] Implement binding for container literals (list, dict, set, tuple)
- [ ] Implement binding for variables and symbols
- [ ] Implement binding for function definitions
- [ ] Implement binding for class definitions
- [ ] Implement binding for Jac-specific constructs
- [ ] Write unit tests for the type binder

### Week 3: Integration with Compiler
- [ ] Update `schedules.py` to include the new type binder pass
- [ ] Update `program.py` to use the new type binder pass
- [ ] Create a simple end-to-end test for type binding
- [ ] Fix any issues that arise during integration
- [ ] Document the type system and type binder

## Phase 2: Type Evaluator and Checker (2-3 weeks)

### Week 4: Type Evaluator Implementation
- [ ] Create the `type_evaluator_pass.py` module
- [ ] Implement type evaluation for binary expressions
- [ ] Implement type evaluation for unary expressions
- [ ] Implement type evaluation for function calls
- [ ] Implement type evaluation for attribute access
- [ ] Implement type evaluation for indexing
- [ ] Implement type evaluation for Jac-specific expressions
- [ ] Write unit tests for the type evaluator

### Week 5: Type Checker Implementation
- [ ] Create the `type_checker_pass.py` module
- [ ] Implement type compatibility checking
- [ ] Implement assignment checking
- [ ] Implement function call argument checking
- [ ] Implement return type checking
- [ ] Implement operator compatibility checking
- [ ] Implement Jac-specific type checking rules
- [ ] Write unit tests for the type checker

### Week 6: Integration and Testing
- [ ] Update `schedules.py` to include the new type evaluator and checker passes
- [ ] Update `program.py` to use the new passes
- [ ] Create comprehensive end-to-end tests for type checking
- [ ] Fix any issues that arise during integration
- [ ] Document the type evaluator and checker

## Phase 3: Advanced Features and Error Reporting (2-3 weeks)

### Week 7: Error Reporting Enhancements
- [ ] Improve error messages for type mismatches
- [ ] Add suggestions for fixing type errors
- [ ] Implement error recovery to continue type checking after errors
- [ ] Add location information to error messages
- [ ] Create a test suite for error reporting

### Week 8: Advanced Type Features
- [ ] Implement support for generics
- [ ] Implement support for type aliases
- [ ] Implement support for union types
- [ ] Implement support for optional types
- [ ] Implement support for callable types
- [ ] Write unit tests for advanced type features

### Week 9: Jac-Specific Type Features
- [ ] Implement special type checking for walker-node interactions
- [ ] Implement special type checking for edge operations
- [ ] Implement special type checking for ability calls
- [ ] Implement special type checking for enum values
- [ ] Write unit tests for Jac-specific type features

## Phase 4: Mypy Removal and Final Integration (2-3 weeks)

### Week 10: Parallel Testing
- [ ] Run both mypy and the new type checker in parallel
- [ ] Compare results and fix discrepancies
- [ ] Ensure all existing type checks pass with the new system
- [ ] Create a comprehensive test suite for the new type checker

### Week 11: Mypy Removal
- [ ] Remove `JacTypeCheckPass` and related code
- [ ] Remove `FuseTypeInfoPass` and related code
- [ ] Remove mypy dependencies from the codebase
- [ ] Update any code that relied on mypy-specific features
- [ ] Ensure all tests pass without mypy

### Week 12: Final Integration and Documentation
- [ ] Perform final integration testing
- [ ] Optimize performance of the type checker
- [ ] Update all documentation to reflect the new type checking system
- [ ] Create user-facing documentation for type annotations and error messages
- [ ] Create developer documentation for extending the type system

## Milestones and Deliverables

### Milestone 1: Basic Type System (End of Week 3)
- Working type system with support for basic types
- Type binder that can associate types with AST nodes
- Integration with the compiler pipeline

### Milestone 2: Type Checking (End of Week 6)
- Type evaluator that can infer types for expressions
- Type checker that can verify type compatibility
- Integration with the compiler pipeline

### Milestone 3: Advanced Features (End of Week 9)
- Improved error reporting
- Support for advanced type features
- Support for Jac-specific type features

### Milestone 4: Final System (End of Week 12)
- Complete removal of mypy dependency
- Fully integrated type checking system
- Comprehensive documentation and test suite

## Risks and Mitigations

### Risk: Complexity of Type Inference
- **Mitigation**: Start with simple cases and gradually add support for more complex expressions. Use a phased approach to ensure each part works before moving on.

### Risk: Performance Issues
- **Mitigation**: Profile the type checker regularly and optimize critical paths. Consider incremental type checking for large codebases.

### Risk: Compatibility with Existing Code
- **Mitigation**: Run both type checkers in parallel during development to ensure compatibility. Create a comprehensive test suite that covers existing code patterns.

### Risk: Missing Edge Cases
- **Mitigation**: Create a thorough test suite that covers a wide range of type checking scenarios. Involve users in beta testing to identify edge cases.

## Conclusion

This implementation plan provides a structured approach to developing the new type checking system for Jac. By breaking the work into phases and weeks, it ensures steady progress and allows for regular evaluation and adjustment. The milestones provide clear targets for measuring progress, and the risk mitigation strategies help address potential challenges.

The end result will be a robust, efficient, and Jac-specific type checking system that eliminates the dependency on mypy and provides better integration with Jac's unique features.
