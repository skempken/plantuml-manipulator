# Examples

This directory contains example snippets and workflows for PlantUML Manipulator.

## Directory Structure

```
examples/
├── README.md (this file)
├── snippets/          # Reusable PlantUML code blocks
│   ├── validation.puml
│   └── integration.puml
└── workflows/         # Complete workflow examples
    └── (to be added)
```

## Example Snippets

### snippets/validation.puml

A typical validation block that can be inserted into process diagrams:

```plantuml
group Perform Validation
    System -> System: Validate input
    System -> ValidationService: Check business rules
    ValidationService --> System: Validation result
    alt Validation successful
        System -> System: Continue processing
    else Validation failed
        System -> System: Handle validation error
        System --> User: Error message
    end
end group
```

**Usage:**
```bash
plantuml-manipulator insert-after \
  --pattern "processes/*.puml" \
  --after-group "Process Request" \
  --block-file examples/snippets/validation.puml
```

### snippets/integration.puml

Example of external system integration:

```plantuml
group Integrate with External System
    System -> ExternalAPI: Send request
    ExternalAPI -> ExternalAPI: Process
    ExternalAPI --> System: Response
    System -> System: Handle response
end group
```

## Common Workflows

### 1. Add Validation to Multiple Processes

```bash
# Step 1: Insert validation block
plantuml-manipulator insert-after \
  --pattern "processes/*.puml" \
  --after-group "Process Request" \
  --block-file examples/snippets/validation.puml \
  --skip-if-exists "Perform Validation" \
  --dry-run

# Step 2: Add ValidationService participant
plantuml-manipulator add-participant \
  --pattern "processes/*.puml" \
  --participant 'participant "ValidationService" as ValidationService #orange' \
  --after-participant "System" \
  --skip-if-exists "ValidationService"

# Step 3: Validate changes
plantuml-manipulator validate \
  --pattern "processes/*.puml" \
  --require-group "Perform Validation" \
  --require-participant "ValidationService"
```

### 2. Consistency Check Across Diagrams

```bash
# Check if all process diagrams follow standard structure
plantuml-manipulator validate \
  --pattern "processes/*.puml" \
  --require-group "Process Request" \
  --require-group "Handle Response" \
  --require-participant "System" \
  --report-format table
```

### 3. Generate Documentation

```bash
# Export structure of all diagrams for documentation
plantuml-manipulator report groups \
  --pattern "processes/*.puml" \
  --format json \
  --output docs/diagram-structure.json
```

## Creating Your Own Snippets

1. Create a valid PlantUML block
2. Save to `examples/snippets/your-snippet.puml`
3. Use with `--block-file`

**Template:**
```plantuml
group Your Group Name
    Participant1 -> Participant2: Action
    Participant2 --> Participant1: Response
end group
```

## Tips

- Keep snippets focused and reusable
- Use descriptive group names
- Include error handling in snippets
- Test snippets in a single file first
- Use `--dry-run` before applying to many files

## Contributing Examples

If you have useful snippets or workflows:
1. Add them to this directory
2. Update this README
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.
