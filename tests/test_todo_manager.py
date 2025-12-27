"""
Unit tests for the TodoManager in the In-Memory Command-Line Todo Application.
"""
import unittest
import sys
import os
# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from todo_manager import TodoManager, TaskNotFoundError, TaskLimitError, InvalidTaskError


class TestTodoManager(unittest.TestCase):
    """Test cases for the TodoManager class."""
    
    def setUp(self):
        """Set up a fresh TodoManager instance for each test."""
        self.manager = TodoManager()
    
    def test_add_task_valid(self):
        """Test adding a valid task."""
        task = self.manager.add_task("Test Task", "Test Description")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, "pending")
        
        # Verify the task was added to the list
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 1)
    
    def test_add_task_no_description(self):
        """Test adding a task without a description."""
        task = self.manager.add_task("Test Task")
        
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, "pending")
    
    def test_add_task_invalid_title_empty(self):
        """Test adding a task with an empty title raises an error."""
        with self.assertRaises(InvalidTaskError):
            self.manager.add_task("")
    
    def test_add_task_invalid_title_too_long(self):
        """Test adding a task with a title that's too long raises an error."""
        long_title = "A" * 201
        with self.assertRaises(InvalidTaskError):
            self.manager.add_task(long_title)
    
    def test_add_task_special_control_chars(self):
        """Test adding a task with special control characters in title raises an error."""
        with self.assertRaises(InvalidTaskError):
            self.manager.add_task("Test\x01Task")
        
        with self.assertRaises(InvalidTaskError):
            self.manager.add_task("Test\x7fTask")
    
    def test_list_tasks_empty(self):
        """Test listing tasks when there are no tasks."""
        tasks = self.manager.list_tasks()
        
        self.assertEqual(len(tasks), 0)
        self.assertEqual(tasks, [])
    
    def test_list_tasks_multiple(self):
        """Test listing multiple tasks."""
        task1 = self.manager.add_task("Task 1", "Description 1")
        task2 = self.manager.add_task("Task 2", "Description 2")
        task3 = self.manager.add_task("Task 3", "Description 3")
        
        tasks = self.manager.list_tasks()
        
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Task 1")
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[1].title, "Task 2")
        self.assertEqual(tasks[2].id, 3)
        self.assertEqual(tasks[2].title, "Task 3")
    
    def test_get_task_valid(self):
        """Test getting a valid task by ID."""
        added_task = self.manager.add_task("Test Task", "Test Description")
        
        retrieved_task = self.manager.get_task(1)
        
        self.assertEqual(added_task.id, retrieved_task.id)
        self.assertEqual(added_task.title, retrieved_task.title)
        self.assertEqual(added_task.description, retrieved_task.description)
        self.assertEqual(added_task.status, retrieved_task.status)
    
    def test_get_task_invalid_id(self):
        """Test getting a task with an invalid ID raises an error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task(999)
    
    def test_update_task_title_only(self):
        """Test updating only the title of a task."""
        task = self.manager.add_task("Original Title", "Original Description")
        
        updated_task = self.manager.update_task(1, new_title="New Title")
        
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "Original Description")
        self.assertEqual(updated_task.status, "pending")
    
    def test_update_task_description_only(self):
        """Test updating only the description of a task."""
        task = self.manager.add_task("Original Title", "Original Description")
        
        updated_task = self.manager.update_task(1, new_description="New Description")
        
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.title, "Original Title")
        self.assertEqual(updated_task.description, "New Description")
        self.assertEqual(updated_task.status, "pending")
    
    def test_update_task_both(self):
        """Test updating both title and description of a task."""
        task = self.manager.add_task("Original Title", "Original Description")
        
        updated_task = self.manager.update_task(1, new_title="New Title", new_description="New Description")
        
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")
        self.assertEqual(updated_task.status, "pending")
    
    def test_update_task_invalid_title(self):
        """Test updating a task with an invalid title raises an error."""
        task = self.manager.add_task("Original Title", "Original Description")
        
        with self.assertRaises(InvalidTaskError):
            self.manager.update_task(1, new_title="")
        
        with self.assertRaises(InvalidTaskError):
            self.manager.update_task(1, new_title="A" * 201)
    
    def test_update_task_invalid_id(self):
        """Test updating a task with an invalid ID raises an error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.update_task(999, new_title="New Title")
    
    def test_delete_task_valid(self):
        """Test deleting a valid task."""
        task = self.manager.add_task("Test Task", "Test Description")
        
        result = self.manager.delete_task(1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.list_tasks()), 0)
    
    def test_delete_task_invalid_id(self):
        """Test deleting a task with an invalid ID."""
        result = self.manager.delete_task(999)
        
        self.assertFalse(result)
        self.assertEqual(len(self.manager.list_tasks()), 0)
    
    def test_delete_task_after_adding_multiple(self):
        """Test deleting a task from a list with multiple tasks."""
        task1 = self.manager.add_task("Task 1", "Description 1")
        task2 = self.manager.add_task("Task 2", "Description 2")
        task3 = self.manager.add_task("Task 3", "Description 3")
        
        result = self.manager.delete_task(2)
        
        self.assertTrue(result)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 3)
    
    def test_mark_complete_valid(self):
        """Test marking a valid task as complete."""
        task = self.manager.add_task("Test Task", "Test Description")
        
        updated_task = self.manager.mark_complete(1)
        
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.status, "complete")
    
    def test_mark_complete_invalid_id(self):
        """Test marking a task as complete with an invalid ID raises an error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.mark_complete(999)
    
    def test_mark_incomplete_valid(self):
        """Test marking a valid task as incomplete."""
        task = self.manager.add_task("Test Task", "Test Description")
        
        # First mark as complete
        completed_task = self.manager.mark_complete(1)
        self.assertEqual(completed_task.status, "complete")
        
        # Then mark as incomplete
        updated_task = self.manager.mark_incomplete(1)
        
        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.status, "pending")
    
    def test_mark_incomplete_invalid_id(self):
        """Test marking a task as incomplete with an invalid ID raises an error."""
        with self.assertRaises(TaskNotFoundError):
            self.manager.mark_incomplete(999)
    
    def test_task_limit_enforcement(self):
        """Test that the task limit is enforced."""
        # Create a manager with a small limit for testing
        manager = TodoManager(max_tasks=2)
        
        # Add tasks up to the limit
        task1 = manager.add_task("Task 1", "Description 1")
        task2 = manager.add_task("Task 2", "Description 2")
        
        # Verify we can't add another task
        with self.assertRaises(TaskLimitError):
            manager.add_task("Task 3", "Description 3")
    
    def test_id_generation_sequential(self):
        """Test that IDs are generated sequentially."""
        task1 = self.manager.add_task("Task 1", "Description 1")
        task2 = self.manager.add_task("Task 2", "Description 2")
        task3 = self.manager.add_task("Task 3", "Description 3")
        
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        
        # Delete middle task and add another
        self.manager.delete_task(2)
        task4 = self.manager.add_task("Task 4", "Description 4")
        
        # ID should continue from the next available
        self.assertEqual(task4.id, 4)


if __name__ == "__main__":
    unittest.main()