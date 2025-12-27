"""
Unit tests for the Task model in the In-Memory Command-Line Todo Application.
"""
import unittest
import sys
import os
# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from models import Task


class TestTask(unittest.TestCase):
    """Test cases for the Task dataclass."""
    
    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(id=1, title="Test Task", description="Test Description", status="pending")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, "pending")
    
    def test_task_creation_defaults(self):
        """Test creating a task with default values."""
        task = Task(id=1, title="Test Task")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, "pending")
    
    def test_task_title_validation_empty(self):
        """Test that creating a task with an empty title raises an error."""
        with self.assertRaises(ValueError):
            Task(id=1, title="", description="Test Description", status="pending")
    
    def test_task_title_validation_none(self):
        """Test that creating a task with a None title raises an error."""
        with self.assertRaises(ValueError):
            Task(id=1, title=None, description="Test Description", status="pending")
    
    def test_task_title_length_min(self):
        """Test that creating a task with a title of minimum length (1 char) is valid."""
        task = Task(id=1, title="A", description="Test Description", status="pending")
        self.assertEqual(task.title, "A")
    
    def test_task_title_length_max(self):
        """Test that creating a task with a title of maximum length (200 chars) is valid."""
        title = "A" * 200
        task = Task(id=1, title=title, description="Test Description", status="pending")
        self.assertEqual(task.title, title)
    
    def test_task_title_length_exceeds_max(self):
        """Test that creating a task with a title exceeding max length raises an error."""
        title = "A" * 201
        with self.assertRaises(ValueError):
            Task(id=1, title=title, description="Test Description", status="pending")
    
    def test_task_title_special_control_chars(self):
        """Test that creating a task with special control characters raises an error."""
        with self.assertRaises(ValueError):
            Task(id=1, title="Test\x01Task", description="Test Description", status="pending")
        
        with self.assertRaises(ValueError):
            Task(id=1, title="Test\x7fTask", description="Test Description", status="pending")
    
    def test_task_status_validation(self):
        """Test that only 'pending' and 'complete' are valid statuses."""
        # Valid statuses
        task1 = Task(id=1, title="Test Task", status="pending")
        task2 = Task(id=2, title="Test Task", status="complete")
        
        self.assertEqual(task1.status, "pending")
        self.assertEqual(task2.status, "complete")
        
        # Invalid status
        with self.assertRaises(ValueError):
            Task(id=3, title="Test Task", status="invalid")
    
    def test_task_repr(self):
        """Test the string representation of a task."""
        task = Task(id=1, title="Test Task", description="Test Description", status="pending")
        expected = "Task(id=1, title='Test Task', description='Test Description', status='pending')"
        self.assertEqual(repr(task), expected)


if __name__ == "__main__":
    unittest.main()