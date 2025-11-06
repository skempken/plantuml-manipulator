"""Tests for the PlantUML parser module."""

import pytest
from pathlib import Path

from plantuml_manipulator.parser import (
    PlantUMLParser,
    DiagramStructure,
    Participant,
    Group,
    parse_file,
)


class TestPlantUMLParser:
    """Test cases for PlantUMLParser class."""

    @pytest.fixture
    def parser(self):
        """Create a parser instance for tests."""
        return PlantUMLParser()

    @pytest.fixture
    def fixtures_dir(self):
        """Path to test fixtures."""
        return Path(__file__).parent / "fixtures"

    def test_parser_initialization(self, parser):
        """Test that parser initializes correctly."""
        assert parser is not None

    def test_parse_simple_file(self, parser, fixtures_dir):
        """Test parsing a simple PlantUML file."""
        file_path = fixtures_dir / "simple.puml"
        structure = parser.parse_file(file_path)
        assert structure is not None
        assert structure.file_path == file_path

    def test_find_participants(self, parser):
        """Test finding participant declarations."""
        lines = [
            "@startuml",
            'participant "User" as User',
            'participant "System" as System #orange',
            "@enduml",
        ]
        participants = parser.find_participants(lines)
        assert len(participants) == 2
        assert participants[0].name == "User"
        assert participants[1].color == "orange"  # Color is captured without #

    def test_find_groups(self, parser):
        """Test finding group blocks."""
        lines = [
            "@startuml",
            "group Process Request",
            "    User -> System: Request",
            "end group",
            "@enduml",
        ]
        groups = parser.find_groups(lines)
        assert len(groups) == 1
        assert groups[0].name == "Process Request"

    def test_nested_groups(self, parser):
        """Test parsing nested groups."""
        lines = [
            "group Outer",
            "    group Inner",
            "        System -> System: Process",
            "    end",
            "end",
        ]
        groups = parser.find_groups(lines)
        assert len(groups) == 2

    def test_get_indent_level(self, parser):
        """Test indent level calculation."""
        assert parser.get_indent_level("no indent") == 0
        assert parser.get_indent_level("    4 spaces") == 4
        assert parser.get_indent_level("        8 spaces") == 8

    def test_is_group_start(self, parser):
        """Test group start detection."""
        assert parser.is_group_start("group Process Request")
        assert parser.is_group_start("    group Indented")
        assert not parser.is_group_start("end group")
        assert not parser.is_group_start("User -> System")

    def test_is_group_end(self, parser):
        """Test group end detection."""
        assert parser.is_group_end("end")
        assert parser.is_group_end("end group")
        assert parser.is_group_end("    end")
        assert not parser.is_group_end("group Start")

    def test_parse_file_convenience_function(self, fixtures_dir):
        """Test the convenience parse_file function."""
        file_path = str(fixtures_dir / "simple.puml")
        structure = parse_file(file_path)
        assert structure is not None


class TestParticipant:
    """Test cases for Participant dataclass."""

    def test_participant_creation(self):
        """Test creating a Participant."""
        p = Participant(name="User", alias="User", color="#blue", line_number=5)
        assert p.name == "User"
        assert p.alias == "User"
        assert p.color == "#blue"
        assert p.line_number == 5


class TestGroup:
    """Test cases for Group dataclass."""

    def test_group_creation(self):
        """Test creating a Group."""
        g = Group(
            name="Process Request",
            start_line=10,
            end_line=15,
            content=["User -> System: Request"],
            indent_level=0,
        )
        assert g.name == "Process Request"
        assert g.start_line == 10
        assert g.end_line == 15
        assert len(g.content) == 1


class TestDiagramStructure:
    """Test cases for DiagramStructure dataclass."""

    def test_structure_creation(self):
        """Test creating a DiagramStructure."""
        structure = DiagramStructure(
            file_path=Path("test.puml"),
            participants=[],
            groups=[],
            raw_lines=[],
            has_start_tag=True,
            has_end_tag=True,
        )
        assert structure.file_path == Path("test.puml")
        assert len(structure.participants) == 0
        assert structure.has_start_tag is True
