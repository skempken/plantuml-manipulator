"""PlantUML Parser - Parse and analyze PlantUML sequence diagrams.

This module provides functionality to parse PlantUML files and extract
structural information like groups, participants, and other elements.

See docs/specification.md for detailed algorithm descriptions.
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Participant:
    """Represents a participant in a PlantUML diagram."""

    name: str
    alias: str
    color: Optional[str] = None
    line_number: int = 0
    raw_line: str = ""


@dataclass
class Group:
    """Represents a group block in a PlantUML diagram."""

    name: str
    start_line: int
    end_line: int
    content: List[str]
    indent_level: int = 0


@dataclass
class DiagramStructure:
    """Represents the parsed structure of a PlantUML diagram."""

    file_path: Path
    participants: List[Participant]
    groups: List[Group]
    raw_lines: List[str]
    has_start_tag: bool = False
    has_end_tag: bool = False


class PlantUMLParser:
    """Parser for PlantUML sequence diagrams.

    This parser uses a line-based, state-machine approach to extract
    structural information from PlantUML files.

    Usage:
        parser = PlantUMLParser()
        structure = parser.parse_file("diagram.puml")
        print(f"Found {len(structure.groups)} groups")
    """

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse_file(self, file_path: Path) -> DiagramStructure:
        """Parse a PlantUML file and extract its structure.

        Args:
            file_path: Path to the PlantUML file

        Returns:
            DiagramStructure containing parsed information

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        raise NotImplementedError("Parser implementation pending - see docs/specification.md")

    def parse_lines(self, lines: List[str]) -> DiagramStructure:
        """Parse PlantUML content from a list of lines.

        Args:
            lines: List of lines from a PlantUML file

        Returns:
            DiagramStructure containing parsed information
        """
        raise NotImplementedError("Parser implementation pending - see docs/specification.md")

    def find_participants(self, lines: List[str]) -> List[Participant]:
        """Extract all participant declarations from lines.

        Args:
            lines: List of lines to search

        Returns:
            List of Participant objects
        """
        raise NotImplementedError("Parser implementation pending - see docs/specification.md")

    def find_groups(self, lines: List[str]) -> List[Group]:
        """Extract all group blocks from lines.

        Uses a state machine to track nested groups and their boundaries.

        Args:
            lines: List of lines to search

        Returns:
            List of Group objects
        """
        raise NotImplementedError("Parser implementation pending - see docs/specification.md")

    def get_indent_level(self, line: str) -> int:
        """Calculate the indentation level of a line.

        Args:
            line: The line to analyze

        Returns:
            Number of leading spaces/tabs
        """
        return len(line) - len(line.lstrip())

    def is_group_start(self, line: str) -> bool:
        """Check if a line starts a group block.

        Args:
            line: The line to check

        Returns:
            True if line starts with 'group'
        """
        return line.strip().startswith("group ")

    def is_group_end(self, line: str) -> bool:
        """Check if a line ends a group block.

        Args:
            line: The line to check

        Returns:
            True if line is 'end' or 'end group'
        """
        stripped = line.strip()
        return stripped == "end" or stripped == "end group"


def parse_file(file_path: str) -> DiagramStructure:
    """Convenience function to parse a PlantUML file.

    Args:
        file_path: Path to the PlantUML file

    Returns:
        DiagramStructure containing parsed information
    """
    parser = PlantUMLParser()
    return parser.parse_file(Path(file_path))
