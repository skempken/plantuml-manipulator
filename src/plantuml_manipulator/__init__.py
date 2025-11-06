"""PlantUML Manipulator - Structured manipulation of PlantUML sequence diagrams."""

__version__ = "0.1.0-dev"
__author__ = "PlantUML Manipulator Contributors"

# Import main classes and functions
from .parser import (
    PlantUMLParser,
    DiagramStructure,
    Participant,
    Group,
    parse_file
)

from .manipulator import (
    DiagramManipulator,
    FileProcessor
)

from .exceptions import (
    PlantUMLManipulatorError,
    GroupNotFoundError,
    ParticipantNotFoundError,
    InvalidPlantUMLError
)

__all__ = [
    # Version info
    '__version__',
    '__author__',

    # Parser
    'PlantUMLParser',
    'DiagramStructure',
    'Participant',
    'Group',
    'parse_file',

    # Manipulator
    'DiagramManipulator',
    'FileProcessor',

    # Exceptions
    'PlantUMLManipulatorError',
    'GroupNotFoundError',
    'ParticipantNotFoundError',
    'InvalidPlantUMLError',
]
