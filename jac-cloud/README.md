# jac-cloud
`jac-cloud` is the cloud-native library for jac programs. `jac-cloud` automatically converts your jac program from a script-like local program to a production-readh server stack.

### Install
#### From pip
```bash
pip install jac-cloud
```
### From source (for contributors)
```bash
git clone https://github.com/Jaseci-Labs/jaseci.git
cd jaseci/jac-cloud
pip install -e .
```
#### Additional dependencies for contributors
```bash
pip install jaclang black pre-commit pytest flake8 flake8_import_order flake8_docstrings flake8_comprehensions flake8_bugbear flake8_annotations pep8_naming flake8_simplify mypy pytest
pre-commit install
```

### Quick Start
Simply replace `jac run` with `jac serve`. `jac serve` starts an API server with a set of API endpoints corresponding to the walkers in the jac program.

`jac serve main.jac`

### API Docs
Once starts, navigate to `/docs` to access the built-in API docs.

For additional details, check out [our documentation](https://www.jac-lang.org/learn/guide/).

test