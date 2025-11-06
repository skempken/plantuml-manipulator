"""PlantUML Manipulator - Core logic for modifying PlantUML diagrams.

This module provides functions to manipulate PlantUML sequence diagrams:
- Insert blocks after specific groups
- Add participants at correct positions
- Modify diagram structures programmatically

See docs/specification.md for detailed algorithm descriptions.
"""

from typing import List, Optional, Callable, Dict, Any
from pathlib import Path
import shutil
import glob as glob_module
from .parser import DiagramStructure, Group, Participant, PlantUMLParser
from .exceptions import GroupNotFoundError, ParticipantNotFoundError


class DiagramManipulator:
    """Core manipulation logic for PlantUML diagrams.

    This class provides methods to modify PlantUML diagrams while
    preserving structure and formatting.

    Usage:
        manipulator = DiagramManipulator()
        result = manipulator.insert_after_group(
            diagram, "Process Request", block_content
        )
    """

    def __init__(self):
        """Initialize the manipulator."""
        pass

    def insert_after_group(
        self,
        structure: DiagramStructure,
        group_name: str,
        block_lines: List[str],
    ) -> List[str]:
        """Insert a block of lines after a specific group.

        Args:
            structure: Parsed diagram structure
            group_name: Name of the group to insert after
            block_lines: Lines to insert

        Returns:
            Modified diagram as list of lines

        Raises:
            GroupNotFoundError: If group not found
        """
        # Find the target group
        target_group = None
        for group in structure.groups:
            if group.name == group_name:
                target_group = group
                break

        if target_group is None:
            raise GroupNotFoundError(f"Group '{group_name}' not found in diagram")

        # Insert position is after the end line of the group
        insert_pos = target_group.end_line + 1

        # Build the new lines list
        result = structure.raw_lines[:insert_pos].copy()

        # Add empty line before block for spacing
        result.append('')

        # Add the block lines
        result.extend(block_lines)

        # Add remaining lines
        result.extend(structure.raw_lines[insert_pos:])

        return result

    def add_participant(
        self,
        structure: DiagramStructure,
        participant_line: str,
        after_participant: Optional[str] = None,
    ) -> List[str]:
        """Add a participant declaration to the diagram.

        If after_participant is specified, inserts after that participant.
        Otherwise, adds at the end of the participant list.

        Args:
            structure: Parsed diagram structure
            participant_line: The participant declaration to add
            after_participant: Optional name of participant to insert after

        Returns:
            Modified diagram as list of lines

        Raises:
            ParticipantNotFoundError: If after_participant is specified but not found
        """
        result = structure.raw_lines.copy()

        if not structure.participants:
            # No participants yet - find a good position to add it
            # Typically after @startuml and title, before any interactions
            insert_pos = 0
            for i, line in enumerate(result):
                if line.strip().startswith('@startuml') or line.strip().startswith('title'):
                    insert_pos = i + 1
                elif line.strip() and not line.strip().startswith('title'):
                    # Found first non-title, non-startuml line
                    break

            result.insert(insert_pos, '')
            result.insert(insert_pos + 1, participant_line)
            return result

        # Find the insertion position
        insert_pos = None

        if after_participant:
            # Find the specified participant
            target_participant = None
            for p in structure.participants:
                if p.alias == after_participant or p.name == after_participant:
                    target_participant = p
                    break

            if target_participant is None:
                raise ParticipantNotFoundError(
                    f"Participant '{after_participant}' not found in diagram"
                )

            insert_pos = target_participant.line_number + 1
        else:
            # Add after the last participant
            last_participant = structure.participants[-1]
            insert_pos = last_participant.line_number + 1

        # Insert the new participant
        result.insert(insert_pos, participant_line)

        return result

    def remove_group(self, structure: DiagramStructure, group_name: str) -> List[str]:
        """Remove a group block from the diagram.

        Args:
            structure: Parsed diagram structure
            group_name: Name of the group to remove

        Returns:
            Modified diagram as list of lines

        Raises:
            ValueError: If group not found
        """
        raise NotImplementedError("Manipulator implementation pending - see docs/specification.md")

    def replace_group(
        self,
        structure: DiagramStructure,
        group_name: str,
        new_content: List[str],
    ) -> List[str]:
        """Replace the content of a group with new content.

        Args:
            structure: Parsed diagram structure
            group_name: Name of the group to replace
            new_content: New content for the group

        Returns:
            Modified diagram as list of lines

        Raises:
            ValueError: If group not found
        """
        raise NotImplementedError("Manipulator implementation pending - see docs/specification.md")

    def preserve_indentation(self, original_line: str, new_content: List[str]) -> List[str]:
        """Apply the indentation from original_line to all lines in new_content.

        Args:
            original_line: Line with indentation to preserve
            new_content: Content to apply indentation to

        Returns:
            Content with preserved indentation
        """
        indent = original_line[: len(original_line) - len(original_line.lstrip())]
        return [indent + line if line.strip() else line for line in new_content]


class FileProcessor:
    """Process multiple files with manipulation operations.

    Handles batch operations, dry-run mode, backups, and filtering.

    Usage:
        processor = FileProcessor(dry_run=True)
        results = processor.process_files(
            pattern="*.puml",
            operation=insert_operation
        )
    """

    def __init__(self, dry_run: bool = False, create_backup: bool = False, verbose: bool = False):
        """Initialize the file processor.

        Args:
            dry_run: If True, don't write changes
            create_backup: If True, create .bak files
            verbose: If True, print detailed progress
        """
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.verbose = verbose

    def process_files(
        self,
        pattern: str,
        operation: Callable[[DiagramStructure], List[str]],
        skip_if_exists: Optional[str] = None,
        only_if_has_participant: Optional[str] = None,
        only_if_has_group: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Process multiple files matching a pattern.

        Args:
            pattern: Glob pattern for files
            operation: Function to apply to each file
            skip_if_exists: Skip if file contains this text
            only_if_has_participant: Only process files with this participant
            only_if_has_group: Only process files with this group

        Returns:
            Dictionary with processing results
        """
        parser = PlantUMLParser()
        results = {
            'processed': [],
            'skipped': [],
            'errors': [],
            'total': 0
        }

        # Find matching files
        files = glob_module.glob(pattern, recursive=True)
        files = [Path(f) for f in files if Path(f).is_file()]
        results['total'] = len(files)

        if self.verbose:
            print(f"Found {len(files)} files matching pattern '{pattern}'")

        for file_path in files:
            try:
                # Parse the file
                structure = parser.parse_file(file_path)

                # Apply filters
                if skip_if_exists:
                    file_content = '\n'.join(structure.raw_lines)
                    if skip_if_exists in file_content:
                        if self.verbose:
                            print(f"Skipping {file_path}: contains '{skip_if_exists}'")
                        results['skipped'].append({
                            'file': str(file_path),
                            'reason': f"contains '{skip_if_exists}'"
                        })
                        continue

                if only_if_has_participant:
                    has_participant = any(
                        p.name == only_if_has_participant or p.alias == only_if_has_participant
                        for p in structure.participants
                    )
                    if not has_participant:
                        if self.verbose:
                            print(f"Skipping {file_path}: missing participant '{only_if_has_participant}'")
                        results['skipped'].append({
                            'file': str(file_path),
                            'reason': f"missing participant '{only_if_has_participant}'"
                        })
                        continue

                if only_if_has_group:
                    has_group = any(g.name == only_if_has_group for g in structure.groups)
                    if not has_group:
                        if self.verbose:
                            print(f"Skipping {file_path}: missing group '{only_if_has_group}'")
                        results['skipped'].append({
                            'file': str(file_path),
                            'reason': f"missing group '{only_if_has_group}'"
                        })
                        continue

                # Apply the operation
                modified_lines = operation(structure)

                # Create backup if requested
                if self.create_backup and not self.dry_run:
                    self.create_backup_file(file_path)

                # Write the modified content
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(modified_lines))
                    if self.verbose:
                        print(f"✓ Processed {file_path}")
                else:
                    if self.verbose:
                        print(f"[DRY RUN] Would process {file_path}")

                results['processed'].append(str(file_path))

            except Exception as e:
                error_msg = f"{file_path}: {str(e)}"
                if self.verbose:
                    print(f"✗ Error processing {file_path}: {str(e)}")
                results['errors'].append({
                    'file': str(file_path),
                    'error': str(e)
                })

        return results

    def create_backup_file(self, file_path: Path) -> None:
        """Create a backup of a file.

        Args:
            file_path: Path to file to backup
        """
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        shutil.copy2(file_path, backup_path)
        if self.verbose:
            print(f"Created backup: {backup_path}")
