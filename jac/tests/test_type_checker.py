"""Test script for the type checking system."""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jaclang.compiler.program import JacProgram
from jaclang.compiler.passes.main import CompilerMode
from jaclang.compiler.passes.main.type_binder_pass import TypeBinderPass
from jaclang.compiler.passes.main.type_evaluator_pass import TypeEvaluatorPass
from jaclang.compiler.passes.main.type_checker_pass import TypeCheckerPass


def test_type_checker_with_example(example_path):
    """Test the type checking system with a Jac example file."""
    print(f"\nTesting type checking with {example_path}")
    print("=" * 80)

    # Create a JacProgram instance
    program = JacProgram()

    # Compile the example file
    module = program.compile(file_path=example_path, mode=CompilerMode.PARSE)

    # Run the type binder pass
    binder = TypeBinderPass(ir_in=module, prog=program)
    binder.run()

    # Run the type evaluator pass
    evaluator = TypeEvaluatorPass(ir_in=module, prog=program)
    evaluator.run()

    # Run the type checker pass
    checker = TypeCheckerPass(ir_in=module, prog=program)
    checker.run()

    # Print the results
    print(f"\nType binding results for {example_path}:")
    print("-" * 80)
    print(f"Bound {len(binder.type_map)} nodes to types")

    print(f"\nType evaluation results for {example_path}:")
    print("-" * 80)
    print(
        f"Evaluated {len(evaluator.type_map) - len(binder.type_map)} additional nodes"
    )

    print(f"\nType checking results for {example_path}:")
    print("-" * 80)
    if checker.errors:
        print(f"Found {len(checker.errors)} type errors:")
        for error in checker.errors:
            print(f"  - {error}")
    else:
        print("No type errors found!")

    print("\nTest completed successfully!")


def run_tests():
    """Run tests on multiple example files."""
    # Test with basic_class_pylike.jac
    test_type_checker_with_example(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "micro",
            "basic_class_pylike.jac",
        )
    )

    # Test with type_info.jac
    test_type_checker_with_example(
        os.path.join(
            os.path.dirname(__file__), "..", "examples", "micro", "type_info.jac"
        )
    )

    # Test with typed_filter_compr.jac
    test_type_checker_with_example(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "examples",
            "micro",
            "typed_filter_compr.jac",
        )
    )


if __name__ == "__main__":
    run_tests()
