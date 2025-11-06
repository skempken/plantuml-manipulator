"""PlantUML Manipulator CLI - Command-line interface.

This module provides the Click-based CLI for the PlantUML Manipulator tool.

See docs/api-reference.md for detailed command documentation.
"""

import click
from pathlib import Path
from typing import Optional

from . import __version__
from .manipulator import DiagramManipulator, FileProcessor
from .parser import PlantUMLParser
from .validator import DiagramValidator, ReportGenerator, ValidationStatus


@click.group()
@click.version_option(version=__version__)
def main():
    """PlantUML Manipulator - Structured manipulation of PlantUML sequence diagrams.

    Perform batch operations like inserting blocks after groups, adding participants,
    and validating diagram structures across multiple files.

    Examples:

        # Insert a block after a group
        plantuml-manipulator insert-after --pattern "*.puml" \\
            --after-group "Process Request" --block-file snippet.puml --dry-run

        # Add a participant
        plantuml-manipulator add-participant --pattern "*.puml" \\
            --participant 'participant "API" as API' --after-participant "Frontend"

        # Validate structures
        plantuml-manipulator validate --pattern "*.puml" \\
            --require-group "Validation" --report-format table
    """
    pass


@main.command("insert-after")
@click.option("--pattern", required=True, help="Glob pattern for files to process")
@click.option("--after-group", required=True, help="Name of group to insert after")
@click.option("--block-file", required=True, type=click.Path(exists=True), help="File containing block to insert")
@click.option("--skip-if-exists", help="Skip files that already contain this text")
@click.option("--only-if-has-participant", help="Only process files with this participant")
@click.option("--only-if-has-group", help="Only process files with this group")
@click.option("--dry-run", is_flag=True, help="Show changes without executing")
@click.option("--backup", is_flag=True, help="Create .bak files before modification")
@click.option("--verbose", is_flag=True, help="Show detailed progress")
def insert_after(
    pattern: str,
    after_group: str,
    block_file: str,
    skip_if_exists: Optional[str],
    only_if_has_participant: Optional[str],
    only_if_has_group: Optional[str],
    dry_run: bool,
    backup: bool,
    verbose: bool,
):
    """Insert a code block after a specific group in multiple files.

    This command finds all files matching PATTERN, locates the group named
    AFTER_GROUP, and inserts the content from BLOCK_FILE after it.

    Examples:

        # Insert validation block after "Process Request"
        plantuml-manipulator insert-after \\
            --pattern "diagrams/**/*.puml" \\
            --after-group "Process Request" \\
            --block-file snippets/validation.puml \\
            --dry-run

        # Insert only in files that have a specific participant
        plantuml-manipulator insert-after \\
            --pattern "*.puml" \\
            --after-group "Initialize" \\
            --block-file setup.puml \\
            --only-if-has-participant "Database" \\
            --backup
    """
    # Read the block file
    block_path = Path(block_file)
    if not block_path.exists():
        click.echo(f"Error: Block file not found: {block_file}", err=True)
        raise SystemExit(1)

    with open(block_path, 'r', encoding='utf-8') as f:
        block_lines = [line.rstrip('\n\r') for line in f.readlines()]

    # Create manipulator and processor
    manipulator = DiagramManipulator()
    processor = FileProcessor(dry_run=dry_run, create_backup=backup, verbose=verbose)

    # Define the operation
    def operation(structure):
        return manipulator.insert_after_group(structure, after_group, block_lines)

    # Process files
    if verbose or dry_run:
        mode = "[DRY RUN] " if dry_run else ""
        click.echo(f"{mode}Inserting block after group '{after_group}'")
        click.echo(f"Pattern: {pattern}")
        click.echo(f"Block file: {block_file}")
        click.echo()

    results = processor.process_files(
        pattern=pattern,
        operation=operation,
        skip_if_exists=skip_if_exists,
        only_if_has_participant=only_if_has_participant,
        only_if_has_group=only_if_has_group,
    )

    # Print summary
    click.echo()
    click.echo("Summary:")
    click.echo(f"  Total files found: {results['total']}")
    click.echo(f"  Processed: {len(results['processed'])}")
    click.echo(f"  Skipped: {len(results['skipped'])}")
    click.echo(f"  Errors: {len(results['errors'])}")

    if results['errors']:
        click.echo()
        click.echo("Errors:", err=True)
        for error in results['errors']:
            click.echo(f"  {error['file']}: {error['error']}", err=True)
        raise SystemExit(1)


@main.command("add-participant")
@click.option("--pattern", required=True, help="Glob pattern for files to process")
@click.option("--participant", required=True, help="Participant declaration to add")
@click.option("--after-participant", help="Add after this participant")
@click.option("--skip-if-exists", help="Skip files that already contain this text")
@click.option("--only-if-has-group", help="Only process files with this group")
@click.option("--dry-run", is_flag=True, help="Show changes without executing")
@click.option("--backup", is_flag=True, help="Create .bak files before modification")
@click.option("--verbose", is_flag=True, help="Show detailed progress")
def add_participant(
    pattern: str,
    participant: str,
    after_participant: Optional[str],
    skip_if_exists: Optional[str],
    only_if_has_group: Optional[str],
    dry_run: bool,
    backup: bool,
    verbose: bool,
):
    """Add a participant declaration to multiple files.

    Examples:

        # Add a participant after another one
        plantuml-manipulator add-participant \\
            --pattern "*.puml" \\
            --participant 'participant "API" as API #orange' \\
            --after-participant "Frontend" \\
            --skip-if-exists "API"

        # Add to all files (at the end of participant list)
        plantuml-manipulator add-participant \\
            --pattern "*.puml" \\
            --participant 'participant "NewService" as NewService' \\
            --backup
    """
    # Create manipulator and processor
    manipulator = DiagramManipulator()
    processor = FileProcessor(dry_run=dry_run, create_backup=backup, verbose=verbose)

    # Define the operation
    def operation(structure):
        return manipulator.add_participant(structure, participant, after_participant)

    # Process files
    if verbose or dry_run:
        mode = "[DRY RUN] " if dry_run else ""
        click.echo(f"{mode}Adding participant: {participant}")
        if after_participant:
            click.echo(f"After participant: {after_participant}")
        click.echo(f"Pattern: {pattern}")
        click.echo()

    results = processor.process_files(
        pattern=pattern,
        operation=operation,
        skip_if_exists=skip_if_exists,
        only_if_has_group=only_if_has_group,
    )

    # Print summary
    click.echo()
    click.echo("Summary:")
    click.echo(f"  Total files found: {results['total']}")
    click.echo(f"  Processed: {len(results['processed'])}")
    click.echo(f"  Skipped: {len(results['skipped'])}")
    click.echo(f"  Errors: {len(results['errors'])}")

    if results['errors']:
        click.echo()
        click.echo("Errors:", err=True)
        for error in results['errors']:
            click.echo(f"  {error['file']}: {error['error']}", err=True)
        raise SystemExit(1)


@main.command("validate")
@click.option("--pattern", required=True, help="Glob pattern for files to validate")
@click.option("--require-group", multiple=True, help="Group that must be present (can be used multiple times)")
@click.option(
    "--require-participant", multiple=True, help="Participant that must be present (can be used multiple times)"
)
@click.option("--only-if-has-participant", help="Only validate files with this participant")
@click.option("--only-if-has-group", help="Only validate files with this group")
@click.option("--report-format", type=click.Choice(["table", "json", "simple"]), default="table", help="Output format")
@click.option("--verbose", is_flag=True, help="Show detailed validation results")
def validate(
    pattern: str,
    require_group: tuple,
    require_participant: tuple,
    only_if_has_participant: Optional[str],
    only_if_has_group: Optional[str],
    report_format: str,
    verbose: bool,
):
    """Validate that diagrams contain required structures.

    Examples:

        # Check if all files have required groups
        plantuml-manipulator validate \\
            --pattern "*.puml" \\
            --require-group "Process Request" \\
            --require-group "Handle Response"

        # Check specific files for participants
        plantuml-manipulator validate \\
            --pattern "payment/*.puml" \\
            --require-participant "PaymentService" \\
            --require-participant "Database" \\
            --report-format json
    """
    validator = DiagramValidator()

    # Convert tuples to lists
    required_groups = list(require_group) if require_group else None
    required_participants = list(require_participant) if require_participant else None

    if verbose:
        click.echo(f"Validating files matching pattern: {pattern}")
        if required_groups:
            click.echo(f"Required groups: {', '.join(required_groups)}")
        if required_participants:
            click.echo(f"Required participants: {', '.join(required_participants)}")
        click.echo()

    # Perform validation
    report = validator.validate_multiple_files(
        pattern=pattern,
        required_groups=required_groups,
        required_participants=required_participants,
        only_if_has_participant=only_if_has_participant,
        only_if_has_group=only_if_has_group
    )

    # Output results based on format
    if report_format == "json":
        import json
        data = {
            'summary': {
                'total_files': report.total_files,
                'files_passed': report.files_passed,
                'files_failed': report.files_failed,
                'files_skipped': report.files_skipped
            },
            'results': [
                {
                    'file': str(r.file_path),
                    'status': r.status.value,
                    'checks_passed': r.checks_passed,
                    'checks_failed': r.checks_failed,
                    'messages': r.messages,
                    'warnings': r.warnings
                }
                for r in report.results
            ]
        }
        click.echo(json.dumps(data, indent=2))
    elif report_format == "simple":
        for result in report.results:
            status_symbol = "✓" if result.status == ValidationStatus.PASS else "✗" if result.status == ValidationStatus.FAIL else "·"
            click.echo(f"{status_symbol} {result.file_path}")
    else:  # table
        click.echo()
        click.echo("Validation Results")
        click.echo("=" * 80)
        click.echo()

        for result in report.results:
            if result.status == ValidationStatus.SKIPPED and not verbose:
                continue

            status_symbol = "✓" if result.status == ValidationStatus.PASS else "✗" if result.status == ValidationStatus.FAIL else "·"
            click.echo(f"{status_symbol} {result.file_path}")

            if verbose or result.status == ValidationStatus.FAIL:
                for msg in result.messages:
                    click.echo(f"  {msg}")
                for warn in result.warnings:
                    click.echo(f"  ⚠ {warn}")
                click.echo()

        click.echo("=" * 80)
        click.echo(f"Total files: {report.total_files}")
        click.echo(f"Passed: {report.files_passed}")
        click.echo(f"Failed: {report.files_failed}")
        click.echo(f"Skipped: {report.files_skipped}")

    # Exit with error code if any validations failed
    if report.files_failed > 0:
        raise SystemExit(1)


@main.group("report")
def report():
    """Generate reports about diagram structures."""
    pass


@report.command("groups")
@click.option("--pattern", required=True, help="Glob pattern for files")
@click.option("--format", type=click.Choice(["table", "json", "csv"]), default="table", help="Output format")
def report_groups(pattern: str, format: str):
    """List all groups found in matching files.

    Examples:

        # Show all groups in table format
        plantuml-manipulator report groups --pattern "*.puml"

        # Export to JSON
        plantuml-manipulator report groups --pattern "*.puml" --format json
    """
    generator = ReportGenerator()
    output = generator.list_groups(pattern, format)
    click.echo(output)


@report.command("participants")
@click.option("--pattern", required=True, help="Glob pattern for files")
@click.option("--format", type=click.Choice(["table", "json", "csv"]), default="table", help="Output format")
def report_participants(pattern: str, format: str):
    """List all participants found in matching files.

    Examples:

        # Show all participants
        plantuml-manipulator report participants --pattern "*.puml"

        # Export to CSV
        plantuml-manipulator report participants --pattern "*.puml" --format csv
    """
    generator = ReportGenerator()
    output = generator.list_participants(pattern, format)
    click.echo(output)


@report.command("structure")
@click.option("--file", "file_path", required=True, type=click.Path(exists=True), help="File to analyze")
@click.option("--format", type=click.Choice(["tree", "json"]), default="tree", help="Output format")
def report_structure(file_path: str, format: str):
    """Show the structure of a single file.

    Examples:

        # Show structure as tree
        plantuml-manipulator report structure --file diagram.puml

        # Export structure as JSON
        plantuml-manipulator report structure --file diagram.puml --format json
    """
    generator = ReportGenerator()
    output = generator.show_structure(Path(file_path), format)
    click.echo(output)


if __name__ == "__main__":
    main()
