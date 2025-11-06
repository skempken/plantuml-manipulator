# PlantUML Manipulator

A command-line tool for structured manipulation of PlantUML sequence diagrams. Perform batch operations like inserting blocks after groups, adding participants, and validating diagram structures across multiple files.

## Features

- **Batch Operations**: Insert code blocks into multiple PlantUML files at once
- **Smart Participant Management**: Add participants at the correct position in declaration lists
- **Validation**: Check if diagrams contain required structures (groups, participants)
- **Reporting**: Generate overviews of groups, participants, and diagram structures
- **Safe Execution**: Dry-run mode, backup creation, and skip-if-exists logic
- **Filtering**: Target specific files based on existing participants or groups

## Quick Start

```bash
# Insert a block after a specific group in multiple files
python -m plantuml_manipulator insert-after \
  --pattern "diagrams/*.puml" \
  --after-group "Process request" \
  --block-file snippets/validation.puml \
  --dry-run

# Add a participant to multiple files
python -m plantuml_manipulator add-participant \
  --pattern "diagrams/*.puml" \
  --participant 'participant "API" as API #orange' \
  --after-participant "Frontend" \
  --skip-if-exists "API"

# Validate diagram structures
python -m plantuml_manipulator validate \
  --pattern "diagrams/*.puml" \
  --require-group "Validation" \
  --require-participant "API" \
  --report-format table
```

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/plantuml-manipulator.git
cd plantuml-manipulator

# Install dependencies
pip install -r requirements.txt

# Install as package (optional)
pip install -e .
```

## Use Cases

### 1. Implementing a New Business Rule Across Multiple Processes

You need to add a new validation step to 10+ process diagrams:

```bash
# Create the snippet
cat > snippets/new-validation.puml << 'EOF'
group Perform validation
    System -> System: Check prerequisites
    System -> ValidationService: Validate request
    ValidationService --> System: Validation result
end group
EOF

# Insert into all relevant files
python -m plantuml_manipulator insert-after \
  --pattern "processes/*.puml" \
  --after-group "Process request" \
  --block-file snippets/new-validation.puml \
  --skip-if-exists "Perform validation" \
  --backup \
  --verbose
```

### 2. Ensuring Consistency Across Diagrams

Check if all commission-relevant processes include the required structures:

```bash
python -m plantuml_manipulator validate \
  --pattern "processes/*.puml" \
  --require-group "Commission check" \
  --require-participant "CommissionService" \
  --only-if-has-participant "PaymentService" \
  --report-format table
```

### 3. Adding a New System to Affected Processes

A new system needs to be integrated into multiple processes:

```bash
# Add participant
python -m plantuml_manipulator add-participant \
  --pattern "processes/*.puml" \
  --participant 'participant "NewSystem" as NewSystem #orange' \
  --after-participant "OldSystem" \
  --skip-if-exists "NewSystem"

# Add integration block
python -m plantuml_manipulator insert-after \
  --pattern "processes/*.puml" \
  --after-group "Process data" \
  --block-file snippets/new-system-integration.puml
```

## Documentation

- **[Specification](docs/specification.md)**: Complete technical specification with algorithms and data structures
- **[API Reference](docs/api-reference.md)**: Detailed command reference and options
- **[Claude Skill](docs/claude-skill.md)**: Integration guide for Claude Code
- **[Examples](examples/README.md)**: Real-world usage examples

## Commands

### insert-after

Insert a code block after a specific group:

```bash
python -m plantuml_manipulator insert-after \
  --pattern "*.puml" \
  --after-group "Group Name" \
  --block-file snippet.puml \
  --dry-run
```

### add-participant

Add a participant declaration:

```bash
python -m plantuml_manipulator add-participant \
  --pattern "*.puml" \
  --participant 'participant "Name" as Name #color' \
  --after-participant "ExistingParticipant"
```

### validate

Validate diagram structures:

```bash
python -m plantuml_manipulator validate \
  --pattern "*.puml" \
  --require-group "Required Group" \
  --report-format table
```

### report

Generate structure reports:

```bash
# List all groups
python -m plantuml_manipulator report groups --pattern "*.puml"

# List all participants
python -m plantuml_manipulator report participants --pattern "*.puml"

# Show structure of a single file
python -m plantuml_manipulator report structure --file diagram.puml
```

## Key Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Show changes without executing them |
| `--verbose` | Detailed output with progress information |
| `--backup` | Create .bak files before modifications |
| `--skip-if-exists TEXT` | Skip files that already contain TEXT |
| `--only-if-has-participant NAME` | Only process files with participant NAME |

## Development Status

**Current Status**: Specification and documentation complete, implementation pending.

This repository currently contains:
- ✅ Complete technical specification
- ✅ Comprehensive API documentation
- ✅ Claude Code skill integration
- ✅ Example workflows
- ⏳ Implementation (coming soon)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT License](LICENSE)

## Project Structure

```
plantuml-manipulator/
├── README.md                      # This file
├── LICENSE                        # MIT License
├── CONTRIBUTING.md                # Contribution guidelines
├── requirements.txt               # Python dependencies
├── setup.py                       # Package installation
├── docs/
│   ├── specification.md           # Technical specification
│   ├── api-reference.md           # Complete API reference
│   ├── claude-skill.md            # Claude Code integration
│   └── examples.md                # Usage examples
├── src/
│   └── plantuml_manipulator/
│       ├── __init__.py
│       ├── cli.py                 # Command-line interface
│       ├── parser.py              # PlantUML parsing
│       ├── manipulator.py         # Core manipulation logic
│       └── validator.py           # Validation logic
├── tests/
│   ├── test_parser.py
│   ├── test_manipulator.py
│   └── fixtures/                  # Test PlantUML files
└── examples/
    ├── snippets/                  # Example code blocks
    │   ├── validation.puml
    │   └── integration.puml
    └── sample-workflows.md        # Real-world examples
```

## Background

This tool was created to address the challenge of maintaining consistency across dozens of PlantUML sequence diagrams documenting business processes in an insurance system. When new compliance requirements or architectural changes affect multiple processes, manually editing each diagram is error-prone and time-consuming.

PlantUML Manipulator automates these repetitive operations while maintaining the readability and structure of the diagrams.

## Claude Code Integration

This tool includes a Claude Code skill that enables Claude to automatically use the tool for batch PlantUML operations. When you ask Claude to make repetitive changes to multiple diagrams, it can leverage this tool instead of manual editing.

See [docs/claude-skill.md](docs/claude-skill.md) for integration details.

## Roadmap

### Phase 1: Core Implementation
- [ ] Implement `insert-after` command
- [ ] Implement `add-participant` command
- [ ] Basic error handling
- [ ] Unit tests

### Phase 2: Validation & Reporting
- [ ] Implement `validate` command
- [ ] Implement `report` commands
- [ ] JSON output format
- [ ] Integration tests

### Phase 3: Robustness
- [ ] Backup system
- [ ] Comprehensive error messages
- [ ] Performance optimizations
- [ ] Full test coverage

### Phase 4: Advanced Features
- [ ] Interactive mode
- [ ] Configuration file support
- [ ] Plugin system for custom validators

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- See existing discussions
- Check the documentation in `docs/`

## Acknowledgments

Inspired by the need to maintain large documentation sets for complex business processes in the insurance domain.
