# PlantUML Manipulator Claude Skill

This directory contains the Claude Code skill definition for PlantUML Manipulator.

## What is This?

This skill teaches Claude Code how to automatically use the PlantUML Manipulator tool for batch operations on PlantUML sequence diagrams.

## Files

- `SKILL.md` - Main skill documentation that Claude reads to understand when and how to use the tool

## Installation

To install this skill for Claude Code:

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy or symlink this directory
cp -r docs/skill ~/.claude/skills/plantuml-manipulator

# Or create a symlink for development (recommended)
ln -s $(pwd)/docs/skill ~/.claude/skills/plantuml-manipulator
```

## Verification

After installation, verify the skill is available:

```bash
ls -la ~/.claude/skills/plantuml-manipulator/SKILL.md
```

## Usage

Once installed, Claude will automatically recognize when to use the PlantUML Manipulator tool for:
- Batch insertions of code blocks
- Adding participants to multiple files
- Validating diagram structures
- Reporting on existing structures

For more information, see the main [Claude Skill Documentation](../claude-skill.md).

## Development

When developing the tool, use a symlink instead of copying:

```bash
ln -s $(pwd)/docs/skill ~/.claude/skills/plantuml-manipulator-dev
```

This allows immediate testing of skill documentation changes without needing to copy files.
