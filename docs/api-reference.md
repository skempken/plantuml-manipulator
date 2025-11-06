# API Reference

Complete command reference for PlantUML Manipulator.

## Global Options

| Option | Short | Description |
|--------|-------|-------------|
| `--dry-run` | `-d` | Show changes without executing |
| `--verbose` | `-v` | Detailed output |
| `--quiet` | `-q` | Only show errors |
| `--backup` | `-b` | Create .bak files before changes |
| `--force` | `-f` | Overwrite without confirmation |

## Commands

### insert-after

Insert a block after a specific group.

**Syntax:**
```bash
plantuml-manipulator insert-after [OPTIONS]
```

**Required Options:**
- `--pattern TEXT`: Glob pattern for files
- `--after-group TEXT`: Group name after which to insert
- `--block-file PATH`: File containing the block to insert

**Optional Options:**
- `--skip-if-exists TEXT`: Skip files already containing TEXT
- `--only-if-has-participant TEXT`: Only process files with this participant
- `--only-if-has-group TEXT`: Only process files with this group

**Example:**
```bash
plantuml-manipulator insert-after \
  --pattern "diagrams/*.puml" \
  --after-group "Process Request" \
  --block-file snippets/validation.puml \
  --skip-if-exists "Perform Validation" \
  --dry-run
```

### add-participant

Add a participant declaration to files.

**Syntax:**
```bash
plantuml-manipulator add-participant [OPTIONS]
```

**Required Options:**
- `--pattern TEXT`: Glob pattern for files
- `--participant TEXT`: Complete participant declaration
- `--after-participant TEXT`: Participant after which to insert

**Optional Options:**
- `--skip-if-exists TEXT`: Skip if participant exists
- `--before-participant TEXT`: Alternative to --after-participant

**Example:**
```bash
plantuml-manipulator add-participant \
  --pattern "diagrams/*.puml" \
  --participant 'participant "API" as API #orange' \
  --after-participant "Frontend" \
  --skip-if-exists "API"
```

### validate

Validate diagram structures.

**Syntax:**
```bash
plantuml-manipulator validate [OPTIONS]
```

**Required Options:**
- `--pattern TEXT`: Glob pattern for files
- At least one of:
  - `--require-group TEXT`: Group must exist
  - `--require-participant TEXT`: Participant must exist

**Optional Options:**
- `--report-format [table|json|csv]`: Output format (default: table)
- `--only-if-has-participant TEXT`: Only check these files

**Example:**
```bash
plantuml-manipulator validate \
  --pattern "diagrams/*.puml" \
  --require-group "Perform Validation" \
  --require-participant "API" \
  --report-format table
```

### report

Generate structure reports.

**Subcommands:**

#### report groups
List all groups in files.

```bash
plantuml-manipulator report groups \
  --pattern "diagrams/*.puml" \
  --format [table|json|csv]
```

#### report participants
List all participants in files.

```bash
plantuml-manipulator report participants \
  --pattern "diagrams/*.puml" \
  --format [table|json|csv]
```

#### report structure
Show detailed structure of a single file.

```bash
plantuml-manipulator report structure \
  --file "diagrams/user_login.puml"
```

## Pattern Syntax

The `--pattern` option uses Python glob syntax:

| Pattern | Matches | Example |
|---------|---------|---------|
| `*.puml` | All .puml in current dir | `test.puml` |
| `**/*.puml` | All .puml recursively | `dir/test.puml` |
| `dir/*.puml` | All .puml in dir/ | `dir/test.puml` |
| `06_*.puml` | Files starting with 06_ | `06_login.puml` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | No files found |
| 3 | No changes made (all skipped) |
| 4 | Validation failed |
| 5 | Parse error |

## Output Formats

### Verbose Mode

```
Processing: user_login.puml
  ✓ Found group "Process Request" at line 12
  → Inserting block at line 20
  ✓ File updated successfully
```

### JSON Output

```json
{
  "files_processed": 8,
  "files_modified": 8,
  "modifications": [
    {
      "file": "user_login.puml",
      "changes": [
        {"type": "insert_block", "line": 20}
      ]
    }
  ]
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PUML_DRY_RUN` | false | Enable dry-run mode |
| `PUML_VERBOSE` | false | Enable verbose mode |
| `PUML_BACKUP` | false | Enable backup mode |

## Common Workflows

### Add New Business Rule

```bash
# 1. Create snippet
cat > snippets/new-rule.puml << 'EOF'
group Apply New Rule
    System -> System: Check rule
    System -> Service: Execute rule
end group
EOF

# 2. Insert with dry-run
plantuml-manipulator insert-after \
  --pattern "diagrams/*.puml" \
  --after-group "Process Request" \
  --block-file snippets/new-rule.puml \
  --skip-if-exists "Apply New Rule" \
  --dry-run

# 3. Execute if OK
plantuml-manipulator insert-after \
  --pattern "diagrams/*.puml" \
  --after-group "Process Request" \
  --block-file snippets/new-rule.puml \
  --skip-if-exists "Apply New Rule" \
  --backup
```

### Consistency Check

```bash
plantuml-manipulator validate \
  --pattern "diagrams/*.puml" \
  --require-group "Perform Validation" \
  --report-format table
```

### Add New System

```bash
# 1. Add participant
plantuml-manipulator add-participant \
  --pattern "diagrams/*.puml" \
  --participant 'participant "NewSystem" as NewSystem #orange' \
  --after-participant "OldSystem" \
  --skip-if-exists "NewSystem"

# 2. Add integration
plantuml-manipulator insert-after \
  --pattern "diagrams/*.puml" \
  --after-group "Process Data" \
  --block-file snippets/new-system-integration.puml
```

For more details, see [specification.md](specification.md).
