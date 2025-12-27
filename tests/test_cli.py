"""
Unit tests for the CLI module in the In-Memory Command-Line Todo Application.
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch
from io import StringIO
# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from cli import TodoCLI
from todo_manager import TodoManager


class TestTodoCLI(unittest.TestCase):
    """Test cases for the TodoCLI class."""
    
    def setUp(self):
        """Set up a fresh TodoCLI instance for each test."""
        self.todo_manager = TodoManager()
        self.cli = TodoCLI(self.todo_manager)
    
    def test_parse_title_description_with_pipe(self):
        """Test parsing title and description with pipe separator."""
        title, description = self.cli._parse_title_description("Buy groceries | Milk, eggs, bread")
        
        self.assertEqual(title, "Buy groceries")
        self.assertEqual(description, "Milk, eggs, bread")
    
    def test_parse_title_description_without_pipe(self):
        """Test parsing title without pipe separator (no description)."""
        title, description = self.cli._parse_title_description("Buy groceries")
        
        self.assertEqual(title, "Buy groceries")
        self.assertEqual(description, "")
    
    def test_parse_title_description_empty_description(self):
        """Test parsing title with empty description after pipe."""
        title, description = self.cli._parse_title_description("Buy groceries |")
        
        self.assertEqual(title, "Buy groceries")
        self.assertEqual(description, "")
    
    def test_parse_title_description_only_pipe(self):
        """Test parsing when only pipe is provided."""
        title, description = self.cli._parse_title_description("| Only description")
        
        self.assertEqual(title, "")
        self.assertEqual(description, "Only description")
    
    def test_handle_add_valid(self):
        """Test handling the add command with valid input."""
        # Capture print output
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_add("Buy groceries | Milk, eggs, bread")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task added with ID 1")
        
        # Verify task was added
        tasks = self.todo_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "Milk, eggs, bread")
        self.assertEqual(tasks[0].status, "pending")
    
    def test_handle_add_no_description(self):
        """Test handling the add command without description."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_add("Buy groceries")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task added with ID 1")
        
        # Verify task was added
        tasks = self.todo_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "")
    
    def test_handle_add_invalid_format(self):
        """Test handling the add command with invalid format."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_add("")  # Empty input
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Invalid command format", output)
    
    def test_handle_list_empty(self):
        """Test handling the list command when there are no tasks."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_list()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "No tasks found")
    
    def test_handle_list_with_tasks(self):
        """Test handling the list command with tasks."""
        # Add some tasks
        self.todo_manager.add_task("Task 1", "Description 1")
        task2 = self.todo_manager.add_task("Task 2", "Description 2")
        self.todo_manager.mark_complete(task2.id)  # Mark second task as complete
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_list()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        lines = output.split('\n')
        
        self.assertEqual(len(lines), 2)
        self.assertIn("1 [ ] Task 1 - Description 1", lines)
        self.assertIn("2 [x] Task 2 - Description 2", lines)
    
    def test_handle_update_valid(self):
        """Test handling the update command with valid input."""
        # Add a task first
        task = self.todo_manager.add_task("Original Title", "Original Description")
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_update("1 New Title | New Description")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task 1 updated successfully")
        
        # Verify task was updated
        updated_task = self.todo_manager.get_task(1)
        self.assertEqual(updated_task.title, "New Title")
        self.assertEqual(updated_task.description, "New Description")
    
    def test_handle_update_title_only(self):
        """Test handling the update command with only title."""
        # Add a task first
        task = self.todo_manager.add_task("Original Title", "Original Description")
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_update("1 New Title Only")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task 1 updated successfully")
        
        # Verify task was updated
        updated_task = self.todo_manager.get_task(1)
        self.assertEqual(updated_task.title, "New Title Only")
        self.assertEqual(updated_task.description, "Original Description")
    
    def test_handle_update_invalid_id(self):
        """Test handling the update command with invalid ID."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_update("999 New Title | New Description")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Task with ID 999 not found", output)
    
    def test_handle_delete_valid(self):
        """Test handling the delete command with valid input."""
        # Add a task first
        task = self.todo_manager.add_task("Task to delete", "Description")
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_delete("1")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task 1 deleted successfully")
        
        # Verify task was deleted
        tasks = self.todo_manager.list_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_handle_delete_invalid_id(self):
        """Test handling the delete command with invalid ID."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_delete("999")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task with ID 999 not found")
    
    def test_handle_complete_valid(self):
        """Test handling the complete command with valid input."""
        # Add a task first
        task = self.todo_manager.add_task("Task to complete", "Description")
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_complete("1")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task 1 marked as complete")
        
        # Verify task status was updated
        updated_task = self.todo_manager.get_task(1)
        self.assertEqual(updated_task.status, "complete")
    
    def test_handle_complete_invalid_id(self):
        """Test handling the complete command with invalid ID."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_complete("999")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Task with ID 999 not found", output)
    
    def test_handle_incomplete_valid(self):
        """Test handling the incomplete command with valid input."""
        # Add a task first and mark it as complete
        task = self.todo_manager.add_task("Task to incomplete", "Description")
        self.todo_manager.mark_complete(1)
        
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_incomplete("1")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertEqual(output, "Task 1 marked as pending")
        
        # Verify task status was updated
        updated_task = self.todo_manager.get_task(1)
        self.assertEqual(updated_task.status, "pending")
    
    def test_handle_incomplete_invalid_id(self):
        """Test handling the incomplete command with invalid ID."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_incomplete("999")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Task with ID 999 not found", output)
    
    def test_handle_help(self):
        """Test handling the help command."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.handle_help()
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Available commands:", output)
        self.assertIn("add <title> | <description>", output)
        self.assertIn("list", output)
        self.assertIn("update <id> <title> | <desc>", output)
        self.assertIn("delete <id>", output)
        self.assertIn("complete <id>", output)
        self.assertIn("incomplete <id> or pending <id>", output)
        self.assertIn("help", output)
        self.assertIn("quit or exit", output)
    
    def test_process_command_unknown(self):
        """Test processing an unknown command."""
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        self.cli.process_command("unknowncommand")
        
        # Restore stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip()
        self.assertIn("Unknown command: unknowncommand", output)


if __name__ == "__main__":
    unittest.main()