"""Tests for the PlantUML manipulator module."""

import pytest
from pathlib import Path

from plantuml_manipulator.manipulator import DiagramManipulator, FileProcessor
from plantuml_manipulator.parser import DiagramStructure, Group, Participant


class TestDiagramManipulator:
    """Test cases for DiagramManipulator class."""

    @pytest.fixture
    def manipulator(self):
        """Create a manipulator instance for tests."""
        return DiagramManipulator()

    @pytest.fixture
    def sample_structure(self):
        """Create a sample diagram structure for tests."""
        return DiagramStructure(
            file_path=Path("test.puml"),
            participants=[
                Participant(name="User", alias="User", line_number=1),
                Participant(name="System", alias="System", line_number=2),
            ],
            groups=[
                Group(
                    name="Process Request",
                    start_line=5,
                    end_line=8,
                    content=["User -> System: Request"],
                ),
            ],
            raw_lines=["@startuml", 'participant "User" as User'],
        )

    def test_manipulator_initialization(self, manipulator):
        """Test that manipulator initializes correctly."""
        assert manipulator is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_insert_after_group(self, manipulator, sample_structure):
        """Test inserting a block after a group."""
        block = ["System -> System: Additional step"]
        result = manipulator.insert_after_group(sample_structure, "Process Request", block)
        assert result is not None
        assert isinstance(result, list)

    @pytest.mark.skip(reason="Implementation pending")
    def test_insert_after_nonexistent_group(self, manipulator, sample_structure):
        """Test that inserting after nonexistent group raises error."""
        block = ["System -> System: Step"]
        with pytest.raises(ValueError):
            manipulator.insert_after_group(sample_structure, "Nonexistent Group", block)

    @pytest.mark.skip(reason="Implementation pending")
    def test_add_participant(self, manipulator, sample_structure):
        """Test adding a participant."""
        participant_line = 'participant "API" as API #orange'
        result = manipulator.add_participant(sample_structure, participant_line, after_participant="System")
        assert result is not None
        assert isinstance(result, list)

    @pytest.mark.skip(reason="Implementation pending")
    def test_add_participant_at_end(self, manipulator, sample_structure):
        """Test adding a participant at the end."""
        participant_line = 'participant "NewService" as NewService'
        result = manipulator.add_participant(sample_structure, participant_line)
        assert result is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_remove_group(self, manipulator, sample_structure):
        """Test removing a group."""
        result = manipulator.remove_group(sample_structure, "Process Request")
        assert result is not None
        assert isinstance(result, list)

    @pytest.mark.skip(reason="Implementation pending")
    def test_replace_group(self, manipulator, sample_structure):
        """Test replacing group content."""
        new_content = ["User -> System: New request", "System --> User: New response"]
        result = manipulator.replace_group(sample_structure, "Process Request", new_content)
        assert result is not None

    def test_preserve_indentation(self, manipulator):
        """Test indentation preservation."""
        original = "    indented line"
        content = ["line 1", "line 2"]
        result = manipulator.preserve_indentation(original, content)
        assert result[0].startswith("    ")
        assert result[1].startswith("    ")


class TestFileProcessor:
    """Test cases for FileProcessor class."""

    @pytest.fixture
    def processor(self):
        """Create a file processor for tests."""
        return FileProcessor(dry_run=True, verbose=False)

    def test_processor_initialization(self):
        """Test file processor initialization."""
        processor = FileProcessor(dry_run=True, create_backup=True, verbose=True)
        assert processor.dry_run is True
        assert processor.create_backup is True
        assert processor.verbose is True

    @pytest.mark.skip(reason="Implementation pending")
    def test_process_files(self, processor, tmp_path):
        """Test processing multiple files."""

        def dummy_operation(structure):
            return structure.raw_lines

        result = processor.process_files(pattern="*.puml", operation=dummy_operation)
        assert result is not None
        assert isinstance(result, dict)

    @pytest.mark.skip(reason="Implementation pending")
    def test_create_backup_file(self, processor, tmp_path):
        """Test backup file creation."""
        test_file = tmp_path / "test.puml"
        test_file.write_text("@startuml\\n@enduml")

        backup_processor = FileProcessor(create_backup=True)
        backup_processor.create_backup_file(test_file)

        backup_file = tmp_path / "test.puml.bak"
        assert backup_file.exists()
