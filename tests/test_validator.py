"""Tests for the PlantUML validator module."""

import pytest
from pathlib import Path

from plantuml_manipulator.validator import (
    DiagramValidator,
    ReportGenerator,
    ValidationStatus,
    ValidationResult,
    ValidationReport,
    validate_file,
)
from plantuml_manipulator.parser import DiagramStructure, Group, Participant


class TestDiagramValidator:
    """Test cases for DiagramValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance for tests."""
        return DiagramValidator()

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
                Group(
                    name="Handle Response",
                    start_line=10,
                    end_line=13,
                    content=["System --> User: Response"],
                ),
            ],
            raw_lines=[],
        )

    def test_validator_initialization(self, validator):
        """Test that validator initializes correctly."""
        assert validator is not None
        assert validator.parser is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_structure_pass(self, validator, sample_structure):
        """Test validation that should pass."""
        result = validator.validate_structure(
            sample_structure, required_groups=["Process Request"], required_participants=["User"]
        )
        assert result.status == ValidationStatus.PASS
        assert result.checks_failed == 0

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_structure_fail(self, validator, sample_structure):
        """Test validation that should fail."""
        result = validator.validate_structure(
            sample_structure, required_groups=["Nonexistent Group"], required_participants=["NonexistentParticipant"]
        )
        assert result.status == ValidationStatus.FAIL
        assert result.checks_failed > 0

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_multiple_requirements(self, validator, sample_structure):
        """Test validation with multiple requirements."""
        result = validator.validate_structure(
            sample_structure,
            required_groups=["Process Request", "Handle Response"],
            required_participants=["User", "System"],
        )
        assert result is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_file(self, validator, tmp_path):
        """Test validating a file."""
        test_file = tmp_path / "test.puml"
        test_file.write_text("@startuml\\nparticipant User\\n@enduml")

        result = validator.validate_file(test_file, required_participants=["User"])
        assert result is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_multiple_files(self, validator, tmp_path):
        """Test validating multiple files."""
        # Create test files
        for i in range(3):
            test_file = tmp_path / f"test{i}.puml"
            test_file.write_text("@startuml\\n@enduml")

        pattern = str(tmp_path / "*.puml")
        report = validator.validate_multiple_files(pattern)
        assert report is not None
        assert isinstance(report, ValidationReport)


class TestReportGenerator:
    """Test cases for ReportGenerator class."""

    @pytest.fixture
    def generator(self):
        """Create a report generator for tests."""
        return ReportGenerator()

    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
        assert generator.parser is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_list_groups_table(self, generator, tmp_path):
        """Test listing groups in table format."""
        test_file = tmp_path / "test.puml"
        test_file.write_text("@startuml\\ngroup Test\\nend\\n@enduml")

        pattern = str(tmp_path / "*.puml")
        report = generator.list_groups(pattern, format="table")
        assert report is not None
        assert isinstance(report, str)

    @pytest.mark.skip(reason="Implementation pending")
    def test_list_groups_json(self, generator, tmp_path):
        """Test listing groups in JSON format."""
        pattern = str(tmp_path / "*.puml")
        report = generator.list_groups(pattern, format="json")
        assert report is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_list_participants(self, generator, tmp_path):
        """Test listing participants."""
        pattern = str(tmp_path / "*.puml")
        report = generator.list_participants(pattern, format="table")
        assert report is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_show_structure(self, generator, tmp_path):
        """Test showing file structure."""
        test_file = tmp_path / "test.puml"
        test_file.write_text("@startuml\\n@enduml")

        report = generator.show_structure(test_file, format="tree")
        assert report is not None

    @pytest.mark.skip(reason="Implementation pending")
    def test_generate_matrix(self, generator, tmp_path):
        """Test generating a coverage matrix."""
        pattern = str(tmp_path / "*.puml")
        matrix = generator.generate_matrix(pattern)
        assert matrix is not None


class TestValidationResult:
    """Test cases for ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating a ValidationResult."""
        result = ValidationResult(
            file_path=Path("test.puml"),
            status=ValidationStatus.PASS,
            checks_passed=5,
            checks_failed=0,
            messages=["All checks passed"],
        )
        assert result.status == ValidationStatus.PASS
        assert result.checks_passed == 5
        assert len(result.warnings) == 0


class TestValidationReport:
    """Test cases for ValidationReport dataclass."""

    def test_validation_report_creation(self):
        """Test creating a ValidationReport."""
        report = ValidationReport(
            total_files=10, files_passed=8, files_failed=2, files_skipped=0, results=[]
        )
        assert report.total_files == 10
        assert report.files_passed == 8


class TestConvenienceFunctions:
    """Test convenience functions."""

    @pytest.mark.skip(reason="Implementation pending")
    def test_validate_file_function(self, tmp_path):
        """Test the convenience validate_file function."""
        test_file = tmp_path / "test.puml"
        test_file.write_text("@startuml\\n@enduml")

        result = validate_file(str(test_file))
        assert result is not None
