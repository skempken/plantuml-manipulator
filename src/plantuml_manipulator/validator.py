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
        raise NotImplementedError("Validator implementation pending - see docs/specification.md")

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
        raise NotImplementedError("Validator implementation pending - see docs/specification.md")

    def validate_multiple_files(
        self,
        pattern: str,
        required_groups: Optional[List[str]] = None,
        required_participants: Optional[List[str]] = None,
        only_if_has_participant: Optional[str] = None,
    ) -> ValidationReport:
        """Validate multiple files matching a pattern.

        Args:
            pattern: Glob pattern for files
            required_groups: Groups that must be present
            required_participants: Participants that must be present
            only_if_has_participant: Only validate files with this participant

        Returns:
            ValidationReport with aggregated results
        """
        raise NotImplementedError("Validator implementation pending - see docs/specification.md")


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
        raise NotImplementedError("ReportGenerator implementation pending - see docs/specification.md")

    def list_participants(self, pattern: str, format: str = "table") -> str:
        """List all participants found in files matching pattern.

        Args:
            pattern: Glob pattern for files
            format: Output format (table, json, csv)

        Returns:
            Formatted report as string
        """
        raise NotImplementedError("ReportGenerator implementation pending - see docs/specification.md")

    def show_structure(self, file_path: Path, format: str = "tree") -> str:
        """Show the structure of a single file.

        Args:
            file_path: Path to file
            format: Output format (tree, json)

        Returns:
            Formatted structure as string
        """
        raise NotImplementedError("ReportGenerator implementation pending - see docs/specification.md")

    def generate_matrix(self, pattern: str) -> str:
        """Generate a matrix showing which files contain which groups.

        Args:
            pattern: Glob pattern for files

        Returns:
            Matrix as formatted string
        """
        raise NotImplementedError("ReportGenerator implementation pending - see docs/specification.md")


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
