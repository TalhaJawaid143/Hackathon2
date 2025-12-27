"""
Todo Manager for the In-Memory Command-Line Todo Application.

This module implements the business logic for task management operations.
"""
from models import Task
from typing import List, Optional
import re


class TaskNotFoundError(Exception):
    """Exception raised when a task with a specific ID is not found."""
    pass


class TaskLimitError(Exception):
    """Exception raised when the task limit is exceeded."""
    pass


class InvalidTaskError(Exception):
    """Exception raised when a task is invalid."""
    pass


class TodoManager:
    """
    Manages the collection of tasks in memory.
    
    The TodoManager handles all task-related operations like adding, listing,
    updating, deleting, and marking tasks as complete/incomplete.
    """
    
    def __init__(self, max_tasks: int = 10000):
        """
        Initialize the TodoManager with an empty task list.
        
        Args:
            max_tasks: Maximum number of tasks allowed in memory (default: 10,000)
        """
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self.max_tasks = max_tasks
    
    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the list.
        
        Args:
            title: The task title (required)
            description: The task description (optional)
            
        Returns:
            The newly created Task object
            
        Raises:
            InvalidTaskError: If the title is invalid
            TaskLimitError: If the maximum number of tasks is reached
        """
        # Validate title
        if not title or not isinstance(title, str):
            raise InvalidTaskError("Title must be a non-empty string")
        
        if len(title) < 1 or len(title) > 200:
            raise InvalidTaskError("Title must be between 1 and 200 characters")
        
        # Check for special control characters in title
        if re.search(r'[\x00-\x1f\x7f-\x9f]', title):
            raise InvalidTaskError("Title cannot contain special control characters")
        
        # Check if we've reached the task limit
        if len(self.tasks) >= self.max_tasks:
            raise TaskLimitError(f"Maximum number of tasks ({self.max_tasks}) reached")
        
        # Create the new task
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            status="pending"
        )
        
        # Add to the list and increment the ID counter
        self.tasks.append(task)
        self.next_id += 1
        
        return task
    
    def list_tasks(self) -> List[Task]:
        """
        Get a list of all tasks.
        
        Returns:
            A list of all Task objects
        """
        return self.tasks
    
    def get_task(self, task_id: int) -> Task:
        """
        Get a specific task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object with the specified ID
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        
        raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def update_task(self, task_id: int, new_title: Optional[str] = None, 
                   new_description: Optional[str] = None) -> Task:
        """
        Update a task's title and/or description.
        
        Args:
            task_id: The ID of the task to update
            new_title: The new title (optional)
            new_description: The new description (optional)
            
        Returns:
            The updated Task object
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
            InvalidTaskError: If the new title is invalid
        """
        task = self.get_task(task_id)
        
        # Update title if provided
        if new_title is not None:
            if not new_title or not isinstance(new_title, str):
                raise InvalidTaskError("Title must be a non-empty string")
            
            if len(new_title) < 1 or len(new_title) > 200:
                raise InvalidTaskError("Title must be between 1 and 200 characters")
            
            # Check for special control characters in title
            if re.search(r'[\x00-\x1f\x7f-\x9f]', new_title):
                raise InvalidTaskError("Title cannot contain special control characters")
            
            task.title = new_title
        
        # Update description if provided
        if new_description is not None:
            task.description = new_description
        
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was successfully deleted, False otherwise
        """
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        
        return False
    
    def mark_complete(self, task_id: int) -> Task:
        """
        Mark a task as complete.
        
        Args:
            task_id: The ID of the task to mark as complete
            
        Returns:
            The updated Task object
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task(task_id)
        task.status = "complete"
        return task
    
    def mark_incomplete(self, task_id: int) -> Task:
        """
        Mark a task as incomplete (pending).
        
        Args:
            task_id: The ID of the task to mark as incomplete
            
        Returns:
            The updated Task object
            
        Raises:
            TaskNotFoundError: If no task with the given ID exists
        """
        task = self.get_task(task_id)
        task.status = "pending"
        return task