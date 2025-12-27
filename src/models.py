"""
Task data model for the In-Memory Command-Line Todo Application.

This module defines the Task dataclass with all required attributes and validation.
"""
from dataclasses import dataclass
import re


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id: Unique auto-incrementing integer identifier (starting from 1)
        title: Non-empty string (required), length 1-200 characters, no special control characters
        description: Optional string (can be empty)
        status: Either "pending" or "complete" (default: "pending")
    """
    id: int
    title: str
    description: str = ""
    status: str = "pending"
    
    def __post_init__(self):
        """Validate the task attributes after initialization."""
        # Validate title
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title must be a non-empty string")
        
        if len(self.title) < 1 or len(self.title) > 200:
            raise ValueError("Title must be between 1 and 200 characters")
        
        # Check for special control characters in title
        if re.search(r'[\x00-\x1f\x7f-\x9f]', self.title):
            raise ValueError("Title cannot contain special control characters")
        
        # Validate status
        if self.status not in ["pending", "complete"]:
            raise ValueError("Status must be either 'pending' or 'complete'")