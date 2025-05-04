# External Integration

This document outlines how the type checking system integrates with external tools like IDEs, editors, and CI/CD pipelines.

## Overview

The type checker needs strong integration points to be useful beyond compiler validation:

1. **Language Server Protocol** implementation for IDE integration
2. **Command-line interface** for CI/CD and script usage
3. **Python API** for programmatic access

## Language Server Protocol

```mermaid
sequenceDiagram
    participant Editor
    participant LSP as Language Server
    participant Analysis as Type Analysis Engine
    participant Project as Project Manager

    Editor->>LSP: Initialize
    LSP->>Project: Load Project
    Project->>Analysis: Build Type Information

    Editor->>LSP: Document Changed
    LSP->>Analysis: Incremental Analysis
    Analysis->>LSP: Diagnostics
    LSP->>Editor: Report Errors

    Editor->>LSP: Hover Request
    LSP->>Analysis: Get Type Information
    Analysis->>LSP: Type Details
    LSP->>Editor: Show Type Info

    Editor->>LSP: Completion Request
    LSP->>Analysis: Get Completions
    Analysis->>LSP: Completion Items
    LSP->>Editor: Show Completions

    style Editor fill:#2d333b,stroke:#30363d,color:#adbac7
    style LSP fill:#2d333b,stroke:#30363d,color:#adbac7
    style Analysis fill:#2d333b,stroke:#30363d,color:#adbac7
    style Project fill:#2d333b,stroke:#30363d,color:#adbac7
```

### LSP Implementation

```python
class JacLanguageServer:
    """Language server implementation for Jac."""

    def __init__(self):
        self.workspace = None
        self.documents = {}
        self.type_checker = None
        self.project_manager = None

    async def initialize(self, params):
        """Initialize the language server."""
        root_path = params.root_uri
        self.workspace = root_path
        self.project_manager = ProjectManager(root_path)
        self.type_checker = TypeChecker(self.project_manager)

        # Pre-analyze workspace
        await self.project_manager.initialize()
        await self.type_checker.initialize()

        return {
            "capabilities": {
                "textDocumentSync": {
                    "openClose": True,
                    "change": 2,  # Incremental updates
                },
                "completionProvider": {
                    "triggerCharacters": [".", ":", "["]
                },
                "hoverProvider": True,
                "definitionProvider": True,
                "referencesProvider": True,
                "documentSymbolProvider": True,
                "workspaceSymbolProvider": True,
                "codeActionProvider": True,
                "signatureHelpProvider": {
                    "triggerCharacters": ["(", ","]
                }
            }
        }

    async def text_document_did_change(self, params):
        """Handle document changes."""
        document_uri = params.text_document.uri
        changes = params.content_changes

        # Update document content
        if document_uri in self.documents:
            document = self.documents[document_uri]
            document.apply_changes(changes)
        else:
            # Should have been opened first, but handle gracefully
            document = Document(document_uri, changes[0].text)
            self.documents[document_uri] = document

        # Perform incremental analysis
        await self.analyze_document(document_uri)

    async def analyze_document(self, document_uri):
        """Analyze a document and report diagnostics."""
        document = self.documents[document_uri]

        # Perform type checking
        diagnostics = await self.type_checker.check_document(document)

        # Send diagnostics to client
        self.client.publish_diagnostics(document_uri, diagnostics)

    async def text_document_hover(self, params):
        """Handle hover requests."""
        document_uri = params.text_document.uri
        position = params.position

        if document_uri not in self.documents:
            return None

        document = self.documents[document_uri]

        # Get node at position
        node = self.project_manager.get_node_at_position(document, position)
        if not node:
            return None

        # Get type information
        type_info = await self.type_checker.get_type_info(node)
        if not type_info:
            return None

        return {
            "contents": {
                "kind": "markdown",
                "value": f"```jac\n{type_info}\n```"
            }
        }

    async def text_document_completion(self, params):
        """Handle completion requests."""
        document_uri = params.text_document.uri
        position = params.position

        if document_uri not in self.documents:
            return None

        document = self.documents[document_uri]

        # Get completions
        completions = await self.type_checker.get_completions(document, position)

        return {
            "isIncomplete": False,
            "items": completions
        }
```

## Command-Line Interface

```python
class JacTypeCheckCLI:
    """Command-line interface for Jac type checking."""

    def __init__(self):
        self.project_manager = None
        self.type_checker = None

    def parse_args(self):
        """Parse command-line arguments."""
        parser = argparse.ArgumentParser(description="Jac Type Checker")
        parser.add_argument("paths", nargs="+", help="Files or directories to check")
        parser.add_argument("--strict", action="store_true", help="Enable strict mode")
        parser.add_argument("--ignore-missing-imports", action="store_true", help="Ignore missing imports")
        parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
        return parser.parse_args()

    def run(self):
        """Run the type checker."""
        args = self.parse_args()

        # Initialize project and type checker
        self.project_manager = ProjectManager(".")

        options = TypeCheckOptions()
        options.mode = TypeCheckingMode.STRICT if args.strict else TypeCheckingMode.NORMAL
        options.ignore_missing_imports = args.ignore_missing_imports

        self.type_checker = TypeChecker(self.project_manager, options)

        # Check files
        for path in args.paths:
            if os.path.isdir(path):
                self.check_directory(path)
            else:
                self.check_file(path)

        # Print results
        if args.format == "json":
            self.print_json_results()
        else:
            self.print_text_results()

    def check_file(self, file_path):
        """Check a single file."""
        try:
            with open(file_path, "r") as f:
                source = f.read()

            # Parse and check the file
            diagnostics = self.type_checker.check_file(file_path, source)

            # Store results
            self.results[file_path] = diagnostics
        except Exception as e:
            print(f"Error checking {file_path}: {e}")

    def check_directory(self, dir_path):
        """Check all Jac files in a directory."""
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".jac"):
                    file_path = os.path.join(root, file)
                    self.check_file(file_path)
```

## Python API

```python
class TypeCheckAPI:
    """Public API for programmatic access to the type checker."""

    def __init__(self, project_root: str = ".", options: Optional[TypeCheckOptions] = None):
        self.project_manager = ProjectManager(project_root)
        self.options = options or TypeCheckOptions()
        self.type_checker = TypeChecker(self.project_manager, self.options)

    def initialize(self) -> None:
        """Initialize the type checker with project information."""
        self.project_manager.initialize()
        self.type_checker.initialize()

    def check_file(self, file_path: str, source: Optional[str] = None) -> list[TypeDiagnostic]:
        """Check a single file and return diagnostics."""
        return self.type_checker.check_file(file_path, source)

    def check_code(self, source: str, file_name: str = "<string>") -> list[TypeDiagnostic]:
        """Check source code snippet and return diagnostics."""
        return self.type_checker.check_file(file_name, source)

    def get_type_at_position(self, file_path: str, line: int, column: int) -> Optional[Type]:
        """Get the type of the expression at the given position."""
        return self.type_checker.get_type_at_position(file_path, line, column)

    def get_completions(self, file_path: str, line: int, column: int) -> list[CompletionItem]:
        """Get completion items at the given position."""
        return self.type_checker.get_completions_at_position(file_path, line, column)

    def get_definition(self, file_path: str, line: int, column: int) -> Optional[SourceLocation]:
        """Get the definition location of the symbol at the given position."""
        return self.type_checker.get_definition_at_position(file_path, line, column)
```

## IDE Features

The type checking system enables the following IDE features:

1. **Error checking**: Showing type errors in the editor
2. **Hover information**: Showing type information on hover
3. **Completion**: Suggesting available members and methods
4. **Go to definition**: Navigating to symbol definitions
5. **Find references**: Finding all usages of a symbol
6. **Code actions**: Providing quick fixes for type errors
7. **Symbol search**: Finding symbols in the workspace

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Type Check

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .
    - name: Run type checker
      run: |
        jac-typecheck --strict --format=json src/ > typecheck-results.json
    - name: Upload results
      uses: actions/upload-artifact@v2
      with:
        name: typecheck-results
        path: typecheck-results.json
```

## Next Steps

The external integration completes the implementation plan for the full type checking system. By providing robust integration points, the type checker becomes a valuable tool for developers across their entire workflow, from writing code to deploying applications.