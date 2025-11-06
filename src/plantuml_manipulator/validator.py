"""PlantUML Validator - Validate diagram structures and generate reports.

This module provides functionality to:
- Validate that diagrams contain required elements
- Generate reports about diagram structures
- Check consistency across multiple diagrams

See docs/specification.md for detailed algorithm descriptions.
"""

from typing import List, Dict, Optional, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import json
import glob as glob_module

from .parser import DiagramStructure, PlantUMLParser


class ValidationStatus(Enum):
    """Status of a validation check."""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class ValidationResult:
    """Result of a validation check."""

    file_path: Path
    status: ValidationStatus
    checks_passed: int
    checks_failed: int
    messages: List[str]
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


@dataclass
class ValidationReport:
    """Aggregated validation results for multiple files."""

    total_files: int
    files_passed: int
    files_failed: int
    files_skipped: int
    results: List[ValidationResult]


class DiagramValidator:
    """Validator for PlantUML sequence diagrams.

    Usage:
        validator = DiagramValidator()
        result = validator.validate_structure(
            structure,
            required_groups=["Process Request"],
            required_participants=["API"]
        )
    """

    def __init__(self):
        """Initialize the validator."""
        self.parser = PlantUMLParser()

    def validate_structure(
        self,
        structure: DiagramStructure,
        required_groups: Optional[List[str]] = None,
        required_participants: Optional[List[str]] = None,
        forbidden_groups: Optional[List[str]] = None,
    ) -> ValidationResult:
        """Validate the structure of a diagram.

        Args:
            structure: Parsed diagram structure
            required_groups: Groups that must be present
            required_participants: Participants that must be present
            forbidden_groups: Groups that must not be present

        Returns:
            ValidationResult with check results
        """
        messages = []
        warnings = []
        checks_passed = 0
        checks_failed = 0

        # Check required groups
        if required_groups:
            group_names = [g.name for g in structure.groups]
            for required_group in required_groups:
                if required_group in group_names:
                    messages.append(f"✓ Found required group: {required_group}")
                    checks_passed += 1
                else:
                    messages.append(f"✗ Missing required group: {required_group}")
                    checks_failed += 1

        # Check required participants
        if required_participants:
            participant_names = [p.name for p in structure.participants]
            participant_aliases = [p.alias for p in structure.participants]
            for required_participant in required_participants:
                if required_participant in participant_names or required_participant in participant_aliases:
                    messages.append(f"✓ Found required participant: {required_participant}")
                    checks_passed += 1
                else:
                    messages.append(f"✗ Missing required participant: {required_participant}")
                    checks_failed += 1

        # Check forbidden groups
        if forbidden_groups:
            group_names = [g.name for g in structure.groups]
            for forbidden_group in forbidden_groups:
                if forbidden_group in group_names:
                    messages.append(f"✗ Found forbidden group: {forbidden_group}")
                    checks_failed += 1
                else:
                    messages.append(f"✓ Forbidden group not present: {forbidden_group}")
                    checks_passed += 1

        # Determine overall status
        if checks_failed > 0:
            status = ValidationStatus.FAIL
        elif checks_passed > 0:
            status = ValidationStatus.PASS
        else:
            status = ValidationStatus.SKIPPED

        return ValidationResult(
            file_path=structure.file_path,
            status=status,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            messages=messages,
            warnings=warnings
        )

    def validate_file(
        self,
        file_path: Path,
        required_groups: Optional[List[str]] = None,
        required_participants: Optional[List[str]] = None,
    ) -> ValidationResult:
        """Validate a PlantUML file.

        Args:
            file_path: Path to file to validate
            required_groups: Groups that must be present
            required_participants: Participants that must be present

        Returns:
            ValidationResult with check results
        """
        structure = self.parser.parse_file(file_path)
        return self.validate_structure(structure, required_groups, required_participants)

    def validate_multiple_files(
        self,
        pattern: str,
        required_groups: Optional[List[str]] = None,
        required_participants: Optional[List[str]] = None,
        only_if_has_participant: Optional[str] = None,
        only_if_has_group: Optional[str] = None,
    ) -> ValidationReport:
        """Validate multiple files matching a pattern.

        Args:
            pattern: Glob pattern for files
            required_groups: Groups that must be present
            required_participants: Participants that must be present
            only_if_has_participant: Only validate files with this participant
            only_if_has_group: Only validate files with this group

        Returns:
            ValidationReport with aggregated results
        """
        files = glob_module.glob(pattern, recursive=True)
        files = [Path(f) for f in files if Path(f).is_file()]

        results = []
        files_passed = 0
        files_failed = 0
        files_skipped = 0

        for file_path in files:
            try:
                structure = self.parser.parse_file(file_path)

                # Apply filters
                should_skip = False
                if only_if_has_participant:
                    has_participant = any(
                        p.name == only_if_has_participant or p.alias == only_if_has_participant
                        for p in structure.participants
                    )
                    if not has_participant:
                        should_skip = True

                if only_if_has_group:
                    has_group = any(g.name == only_if_has_group for g in structure.groups)
                    if not has_group:
                        should_skip = True

                if should_skip:
                    result = ValidationResult(
                        file_path=file_path,
                        status=ValidationStatus.SKIPPED,
                        checks_passed=0,
                        checks_failed=0,
                        messages=["File skipped due to filter criteria"],
                        warnings=[]
                    )
                    files_skipped += 1
                else:
                    result = self.validate_structure(structure, required_groups, required_participants)
                    if result.status == ValidationStatus.PASS:
                        files_passed += 1
                    elif result.status == ValidationStatus.FAIL:
                        files_failed += 1
                    else:
                        files_skipped += 1

                results.append(result)

            except Exception as e:
                # If parsing fails, treat as validation failure
                result = ValidationResult(
                    file_path=file_path,
                    status=ValidationStatus.FAIL,
                    checks_passed=0,
                    checks_failed=1,
                    messages=[f"Error parsing file: {str(e)}"],
                    warnings=[]
                )
                results.append(result)
                files_failed += 1

        return ValidationReport(
            total_files=len(files),
            files_passed=files_passed,
            files_failed=files_failed,
            files_skipped=files_skipped,
            results=results
        )


class ReportGenerator:
    """Generate reports about diagram structures.

    Usage:
        generator = ReportGenerator()
        report = generator.list_groups(pattern="*.puml")
        print(report)
    """

    def __init__(self):
        """Initialize the report generator."""
        self.parser = PlantUMLParser()

    def list_groups(self, pattern: str, format: str = "table") -> str:
        """List all groups found in files matching pattern.

        Args:
            pattern: Glob pattern for files
            format: Output format (table, json, csv)

        Returns:
            Formatted report as string
        """
        files = glob_module.glob(pattern, recursive=True)
        files = [Path(f) for f in files if Path(f).is_file()]

        all_groups = []
        for file_path in files:
            try:
                structure = self.parser.parse_file(file_path)
                for group in structure.groups:
                    all_groups.append({
                        'file': str(file_path),
                        'group': group.name,
                        'start_line': group.start_line + 1,  # 1-indexed for humans
                        'end_line': group.end_line + 1,
                        'indent_level': group.indent_level
                    })
            except Exception as e:
                pass  # Skip files that can't be parsed

        if format == "json":
            return json.dumps(all_groups, indent=2)
        elif format == "csv":
            if not all_groups:
                return "file,group,start_line,end_line,indent_level\n"
            lines = ["file,group,start_line,end_line,indent_level"]
            for item in all_groups:
                lines.append(f"{item['file']},{item['group']},{item['start_line']},{item['end_line']},{item['indent_level']}")
            return "\n".join(lines)
        else:  # table
            if not all_groups:
                return "No groups found."
            lines = []
            lines.append(f"{'File':<40} {'Group':<30} {'Lines':<15} {'Indent':<10}")
            lines.append("-" * 95)
            for item in all_groups:
                file_short = item['file'][-37:] if len(item['file']) > 40 else item['file']
                group_short = item['group'][:27] + "..." if len(item['group']) > 30 else item['group']
                line_range = f"{item['start_line']}-{item['end_line']}"
                lines.append(f"{file_short:<40} {group_short:<30} {line_range:<15} {item['indent_level']:<10}")
            return "\n".join(lines)

    def list_participants(self, pattern: str, format: str = "table") -> str:
        """List all participants found in files matching pattern.

        Args:
            pattern: Glob pattern for files
            format: Output format (table, json, csv)

        Returns:
            Formatted report as string
        """
        files = glob_module.glob(pattern, recursive=True)
        files = [Path(f) for f in files if Path(f).is_file()]

        all_participants = []
        for file_path in files:
            try:
                structure = self.parser.parse_file(file_path)
                for participant in structure.participants:
                    all_participants.append({
                        'file': str(file_path),
                        'name': participant.name,
                        'alias': participant.alias,
                        'color': participant.color or '',
                        'line_number': participant.line_number + 1
                    })
            except Exception as e:
                pass  # Skip files that can't be parsed

        if format == "json":
            return json.dumps(all_participants, indent=2)
        elif format == "csv":
            if not all_participants:
                return "file,name,alias,color,line_number\n"
            lines = ["file,name,alias,color,line_number"]
            for item in all_participants:
                lines.append(f"{item['file']},{item['name']},{item['alias']},{item['color']},{item['line_number']}")
            return "\n".join(lines)
        else:  # table
            if not all_participants:
                return "No participants found."
            lines = []
            lines.append(f"{'File':<40} {'Name':<25} {'Alias':<15} {'Color':<10} {'Line':<10}")
            lines.append("-" * 100)
            for item in all_participants:
                file_short = item['file'][-37:] if len(item['file']) > 40 else item['file']
                name_short = item['name'][:22] + "..." if len(item['name']) > 25 else item['name']
                lines.append(f"{file_short:<40} {name_short:<25} {item['alias']:<15} {item['color']:<10} {item['line_number']:<10}")
            return "\n".join(lines)

    def show_structure(self, file_path: Path, format: str = "tree") -> str:
        """Show the structure of a single file.

        Args:
            file_path: Path to file
            format: Output format (tree, json)

        Returns:
            Formatted structure as string
        """
        structure = self.parser.parse_file(file_path)

        if format == "json":
            data = {
                'file': str(file_path),
                'has_start_tag': structure.has_start_tag,
                'has_end_tag': structure.has_end_tag,
                'participants': [
                    {
                        'name': p.name,
                        'alias': p.alias,
                        'color': p.color,
                        'line_number': p.line_number + 1
                    }
                    for p in structure.participants
                ],
                'groups': [
                    {
                        'name': g.name,
                        'start_line': g.start_line + 1,
                        'end_line': g.end_line + 1,
                        'indent_level': g.indent_level
                    }
                    for g in structure.groups
                ]
            }
            return json.dumps(data, indent=2)
        else:  # tree
            lines = []
            lines.append(f"📄 {file_path}")
            lines.append("")
            lines.append("Participants:")
            if structure.participants:
                for p in structure.participants:
                    color_info = f" #{p.color}" if p.color else ""
                    lines.append(f"  • {p.name} (as {p.alias}){color_info} [line {p.line_number + 1}]")
            else:
                lines.append("  (none)")

            lines.append("")
            lines.append("Groups:")
            if structure.groups:
                for g in structure.groups:
                    indent = "  " * (g.indent_level // 2 + 1)
                    lines.append(f"{indent}📦 {g.name} [lines {g.start_line + 1}-{g.end_line + 1}]")
            else:
                lines.append("  (none)")

            return "\n".join(lines)

    def generate_matrix(self, pattern: str) -> str:
        """Generate a matrix showing which files contain which groups.

        Args:
            pattern: Glob pattern for files

        Returns:
            Matrix as formatted string
        """
        files = glob_module.glob(pattern, recursive=True)
        files = [Path(f) for f in files if Path(f).is_file()]

        # Collect all groups across all files
        file_groups = {}
        all_group_names = set()

        for file_path in files:
            try:
                structure = self.parser.parse_file(file_path)
                group_names = [g.name for g in structure.groups]
                file_groups[str(file_path)] = group_names
                all_group_names.update(group_names)
            except Exception as e:
                file_groups[str(file_path)] = []

        # Sort group names for consistent output
        sorted_groups = sorted(all_group_names)

        if not sorted_groups:
            return "No groups found in any files."

        # Build the matrix
        lines = []
        header = f"{'File':<40} " + " ".join(f"{g[:8]:<10}" for g in sorted_groups)
        lines.append(header)
        lines.append("-" * len(header))

        for file_path, groups in file_groups.items():
            file_short = file_path[-37:] if len(file_path) > 40 else file_path
            row = f"{file_short:<40} "
            for group in sorted_groups:
                mark = "✓" if group in groups else "·"
                row += f"{mark:<10} "
            lines.append(row)

        return "\n".join(lines)


def validate_file(
    file_path: str,
    required_groups: Optional[List[str]] = None,
    required_participants: Optional[List[str]] = None,
) -> ValidationResult:
    """Convenience function to validate a file.

    Args:
        file_path: Path to file to validate
        required_groups: Groups that must be present
        required_participants: Participants that must be present

    Returns:
        ValidationResult
    """
    validator = DiagramValidator()
    return validator.validate_file(Path(file_path), required_groups, required_participants)
