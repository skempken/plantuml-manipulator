# Contributing to PlantUML Manipulator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/plantuml-manipulator.git
   cd plantuml-manipulator
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### 1. Create a Branch

Create a descriptive branch for your work:

```bash
git checkout -b feature/add-export-command
git checkout -b fix/group-parsing-bug
git checkout -b docs/improve-examples
```

### 2. Make Changes

- Follow the existing code style
- Add tests for new features
- Update documentation as needed
- Keep commits focused and atomic

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/plantuml_manipulator

# Run specific test file
pytest tests/test_parser.py
```

### 4. Format Code

```bash
# Format with black
black src/ tests/

# Check with mypy
mypy src/
```

### 5. Commit Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Add export command for JSON output

- Implement export subcommand
- Add JSON serialization for diagram structures
- Include tests and documentation"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/add-export-command
```

Then create a pull request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots/examples if relevant

## Code Style

### Python

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting (line length: 88)
- Use type hints for function signatures
- Write docstrings for public functions and classes

**Example:**

```python
def find_group_end_line(lines: List[str], group_name: str) -> Optional[int]:
    """
    Find the line number after the 'end group' statement for a given group.

    Args:
        lines: List of file lines
        group_name: Name of the group to find

    Returns:
        Line number after 'end group', or None if not found
    """
    # Implementation...
```

### Documentation

- Use Markdown for documentation files
- Include code examples in documentation
- Keep examples realistic and practical
- Update API reference when adding/changing commands

## Testing Guidelines

### Test Structure

```python
def test_insert_block_after_group():
    """Test inserting a block after a specific group."""
    # Arrange
    original_lines = [
        "group First Group",
        "    action",
        "end group",
        "",
        "group Second Group",
        "    action",
        "end group",
    ]
    block_lines = ["group New Group", "    new action", "end group"]

    # Act
    result = insert_block_after_group(original_lines, "First Group", block_lines)

    # Assert
    assert "group New Group" in result
    assert result.index("group New Group") > result.index("end group")
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Include integration tests for full workflows
- Add regression tests for fixed bugs

### Test Files

Place tests in `tests/` directory:

```
tests/
├── test_parser.py           # PlantUML parsing tests
├── test_manipulator.py      # Core manipulation tests
├── test_validator.py        # Validation tests
├── test_cli.py              # CLI integration tests
└── fixtures/
    ├── simple.puml          # Test input files
    ├── nested_groups.puml
    └── expected/            # Expected output files
        └── simple_modified.puml
```

## Adding New Commands

To add a new command (e.g., `merge`):

### 1. Design

- Document the command in an issue first
- Get feedback on the design
- Update specification if needed

### 2. Implementation

Create the command implementation:

```python
# src/plantuml_manipulator/commands/merge.py

from typing import List
from ..parser import PlantUMLFile

def merge_files(files: List[PlantUMLFile], output: str) -> None:
    """Merge multiple PlantUML files into one."""
    # Implementation...
```

### 3. CLI Integration

Add to CLI (`src/plantuml_manipulator/cli.py`):

```python
@click.command()
@click.option('--pattern', required=True)
@click.option('--output', required=True)
def merge(pattern: str, output: str):
    """Merge multiple PlantUML files into one."""
    # Implementation...
```

### 4. Tests

Add comprehensive tests:

```python
# tests/test_merge.py

def test_merge_simple_files():
    """Test merging two simple files."""
    # Test implementation...

def test_merge_with_duplicate_participants():
    """Test handling of duplicate participants."""
    # Test implementation...
```

### 5. Documentation

Update:
- `docs/api-reference.md` with command details
- `docs/examples.md` with usage examples
- `README.md` if it's a major feature

## Documentation

### API Reference

Keep `docs/api-reference.md` up-to-date with:
- All commands and options
- Parameter descriptions
- Return values and exit codes
- Example usage

### Examples

Add practical examples to `docs/examples.md`:
- Real-world use cases
- Common workflows
- Troubleshooting tips

### Specification

Update `docs/specification.md` when:
- Adding new algorithms
- Changing data structures
- Modifying parsing logic

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version)
- Example PlantUML files if possible

### Feature Requests

Include:
- Clear use case description
- Expected behavior
- Example usage (pseudo-code is fine)
- Why existing commands don't solve the problem

## Pull Request Process

1. **Ensure tests pass**: All tests must pass before merging
2. **Update documentation**: Keep docs in sync with code
3. **Add changelog entry**: Note your changes in CHANGELOG.md
4. **Request review**: Tag maintainers for review
5. **Address feedback**: Respond to review comments
6. **Squash commits**: Clean up commit history if requested

## Code Review Guidelines

### For Authors

- Keep PRs focused and reasonably sized
- Respond to feedback constructively
- Update PR based on review comments
- Mark conversations as resolved when addressed

### For Reviewers

- Be constructive and respectful
- Focus on code quality and maintainability
- Suggest improvements, don't demand perfection
- Approve when code meets project standards

## Release Process

(For maintainers)

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create release tag: `git tag -a v1.0.0 -m "Version 1.0.0"`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release
6. Publish to PyPI (if applicable)

## Questions?

- Check existing issues and discussions
- Open a new issue for questions
- Tag with `question` label

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to PlantUML Manipulator!
