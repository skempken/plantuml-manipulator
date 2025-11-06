"""Custom exceptions for PlantUML Manipulator."""


class PlantUMLManipulatorError(Exception):
    """Base exception for all tool errors."""
    pass


class GroupNotFoundError(PlantUMLManipulatorError):
    """Raised when a group is not found in the diagram."""
    pass


class ParticipantNotFoundError(PlantUMLManipulatorError):
    """Raised when a participant is not found in the diagram."""
    pass


class InvalidPlantUMLError(PlantUMLManipulatorError):
    """Raised when the PlantUML syntax is invalid."""
    pass
