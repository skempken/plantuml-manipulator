# TODO: Remaining Tasks

## Documentation ✅ Complete

- [x] Main README.md
- [x] LICENSE (MIT)
- [x] CONTRIBUTING.md
- [x] requirements.txt / requirements-dev.txt
- [x] setup.py
- [x] docs/specification.md
- [x] docs/api-reference.md
- [x] docs/claude-skill.md
- [x] docs/skill/SKILL.md (Claude Code skill file)
- [x] .gitignore

## Fixes Needed ✅ Complete

- [x] Fix README.md references (docs/examples.md vs examples/README.md)
- [x] Create examples/snippets/integration.puml (referenced but missing)
- [x] Create tests/fixtures/ with example .puml files

## Source Code Structure ✅ Complete

- [x] src/plantuml_manipulator/__init__.py (basic version info)
- [x] src/plantuml_manipulator/cli.py (CLI structure with all commands)
- [x] src/plantuml_manipulator/parser.py (complete class structure)
- [x] src/plantuml_manipulator/manipulator.py (complete class structure)
- [x] src/plantuml_manipulator/validator.py (complete class structure)

## Test Structure ✅ Complete

- [x] tests/__init__.py (empty placeholder)
- [x] tests/test_parser.py (comprehensive test structure)
- [x] tests/test_manipulator.py (comprehensive test structure)
- [x] tests/test_validator.py (comprehensive test structure)
- [x] tests/fixtures/ (4 example .puml files: simple, with_groups, with_participants, complex)

## Examples ✅ Complete

- [x] examples/README.md
- [x] examples/snippets/validation.puml
- [x] examples/snippets/integration.puml

## Implementation

### Phase 1: Core Implementation ✅ Complete

- [x] PlantUMLParser implementation
  - [x] parse_file() - Parse PlantUML files
  - [x] parse_lines() - Parse content from lines
  - [x] find_participants() - Extract participant declarations
  - [x] find_groups() - Extract group blocks with nesting support
- [x] DiagramManipulator implementation
  - [x] insert_after_group() - Insert blocks after groups
  - [x] add_participant() - Add participant declarations
- [x] Custom exception classes (GroupNotFoundError, ParticipantNotFoundError, etc.)
- [x] Unit tests for parser (23 tests passing)
- [x] Unit tests for manipulator
- [x] Test fixtures and examples

### Phase 2: CLI & File Processing ✅ Complete

- [x] CLI implementation (cli.py)
  - [x] insert-after command
  - [x] add-participant command
  - [x] --dry-run and --verbose flags
- [x] FileProcessor implementation
  - [x] Batch file processing
  - [x] File filtering (only-if-has-participant, skip-if-exists, only-if-has-group)
  - [x] Backup functionality

### Phase 3: Validation & Reporting

- [ ] Validator implementation
- [ ] Report generation
- [ ] JSON output format

### Phase 4: Advanced Features

- [ ] remove_group() method
- [ ] replace_group() method
- [ ] Interactive mode
- [ ] Undo functionality

## Notes

- Tool should work universally for all PlantUML sequence diagrams
- All examples abstracted from specific project context
- Ready for open-source publication once implementation is complete
