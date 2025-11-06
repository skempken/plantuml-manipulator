"""PlantUML Parser - Parse and analyze PlantUML sequence diagrams.

This module provides functionality to parse PlantUML files and extract
structural information like groups, participants, and other elements.

See docs/specification.md for detailed algorithm descriptions.
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
import re


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
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Remove newlines but keep empty lines
        lines = [line.rstrip('\n\r') for line in lines]

        structure = self.parse_lines(lines)
        structure.file_path = file_path

        return structure

    def parse_lines(self, lines: List[str]) -> DiagramStructure:
        """Parse PlantUML content from a list of lines.

        Args:
            lines: List of lines from a PlantUML file

        Returns:
            DiagramStructure containing parsed information
        """
        # Check for @startuml and @enduml tags
        has_start_tag = any(line.strip().startswith('@startuml') for line in lines)
        has_end_tag = any(line.strip().startswith('@enduml') for line in lines)

        # Extract participants and groups
        participants = self.find_participants(lines)
        groups = self.find_groups(lines)

        structure = DiagramStructure(
            file_path=Path(),  # Will be set by parse_file
            participants=participants,
            groups=groups,
            raw_lines=lines,
            has_start_tag=has_start_tag,
            has_end_tag=has_end_tag
        )

        return structure

    def find_participants(self, lines: List[str]) -> List[Participant]:
        """Extract all participant declarations from lines.

        Args:
            lines: List of lines to search

        Returns:
            List of Participant objects
        """
        participants = []
        # Pattern: participant "Name" as Alias [#color]
        # Handles variations like: participant Name as Alias, participant "Name" as Alias #color
        pattern = re.compile(
            r'^\s*participant\s+(?:"([^"]+)"|(\S+))\s+as\s+(\w+)(?:\s+#(\w+))?'
        )

        for i, line in enumerate(lines):
            match = pattern.match(line)
            if match:
                # Group 1 is quoted name, group 2 is unquoted name
                name = match.group(1) if match.group(1) else match.group(2)
                alias = match.group(3)
                color = match.group(4) if match.group(4) else None

                participant = Participant(
                    name=name,
                    alias=alias,
                    color=color,
                    line_number=i,
                    raw_line=line
                )
                participants.append(participant)

        return participants

    def find_groups(self, lines: List[str]) -> List[Group]:
        """Extract all group blocks from lines.

        Uses a state machine to track nested groups and their boundaries.

        Args:
            lines: List of lines to search

        Returns:
            List of Group objects
        """
        groups = []
        group_stack = []  # Stack to track nested groups

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Check for group start
            if self.is_group_start(line):
                # Extract group name (everything after "group ")
                group_name = stripped[6:].strip()  # Remove "group " prefix
                indent_level = self.get_indent_level(line)

                # Create group entry
                group_info = {
                    'name': group_name,
                    'start_line': i,
                    'indent_level': indent_level,
                    'content': []
                }
                group_stack.append(group_info)

            # Check for group end
            elif self.is_group_end(line):
                if group_stack:
                    # Pop the most recent group
                    group_info = group_stack.pop()

                    # Create Group object
                    group = Group(
                        name=group_info['name'],
                        start_line=group_info['start_line'],
                        end_line=i,
                        content=group_info['content'],
                        indent_level=group_info['indent_level']
                    )
                    groups.append(group)

            # If we're inside a group, add line to its content
            elif group_stack:
                # Add to the innermost group
                group_stack[-1]['content'].append(line)

        return groups

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
