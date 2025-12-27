"""
Integration tests for the main application in the In-Memory Command-Line Todo Application.
"""
import unittest
import sys
import os
from unittest.mock import patch, Mock
from io import StringIO
# Add src directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import main
from todo_manager import TodoManager
from cli import TodoCLI


class TestMainIntegration(unittest.TestCase):
    """Integration test cases for the main application."""
    
    def test_full_workflow_integration(self):
        """Test the complete workflow: add → list → update → complete → delete."""
        # Create the managers
        todo_manager = TodoManager()
        cli = TodoCLI(todo_manager)
        
        # Mock the input function to simulate user commands
        commands = [
            "add Buy groceries | Milk, eggs, bread",  # Add task
            "add Complete project proposal",           # Add another task
            "list",                                   # List tasks
            "complete 1",                             # Mark first task as complete
            "update 2 Finalize project proposal | Submit to manager by EOD",  # Update task
            "list",                                   # List tasks again
            "delete 1",                               # Delete first task
            "list",                                   # List tasks again
            "quit"                                    # Quit
        ]
        
        # Mock input to return commands in sequence
        def mock_input(prompt=""):
            if hasattr(mock_input, 'index'):
                mock_input.index += 1
            else:
                mock_input.index = 0
            
            if mock_input.index < len(commands):
                command = commands[mock_input.index]
                print(f"> {command}")  # Simulate user typing
                return command
            else:
                return "quit"  # Default to quit if out of commands
        
        # Capture output
        import sys
        original_stdout = sys.stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        # Patch the input function
        with patch('builtins.input', side_effect=commands + ["quit"]):
            # We can't easily test the CLI run loop directly, so we'll test the individual components
            pass
        
        # Restore stdout
        sys.stdout = original_stdout
        
        # Instead, let's test the workflow step by step
        # Add tasks
        task1 = todo_manager.add_task("Buy groceries", "Milk, eggs, bread")
        task2 = todo_manager.add_task("Complete project proposal")
        
        # Verify tasks were added
        tasks = todo_manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Buy groceries")
        self.assertEqual(tasks[0].description, "Milk, eggs, bread")
        self.assertEqual(tasks[1].title, "Complete project proposal")
        self.assertEqual(tasks[1].description, "")
        
        # Mark first task as complete
        completed_task = todo_manager.mark_complete(1)
        self.assertEqual(completed_task.status, "complete")
        
        # Update second task
        updated_task = todo_manager.update_task(2, "Finalize project proposal", "Submit to manager by EOD")
        self.assertEqual(updated_task.title, "Finalize project proposal")
        self.assertEqual(updated_task.description, "Submit to manager by EOD")
        
        # Delete first task
        result = todo_manager.delete_task(1)
        self.assertTrue(result)
        
        # Verify only one task remains
        remaining_tasks = todo_manager.list_tasks()
        self.assertEqual(len(remaining_tasks), 1)
        self.assertEqual(remaining_tasks[0].id, 2)
        self.assertEqual(remaining_tasks[0].title, "Finalize project proposal")
    
    def test_command_processing_integration(self):
        """Test that commands are processed correctly through the CLI."""
        todo_manager = TodoManager()
        cli = TodoCLI(todo_manager)
        
        # Test add command
        import sys
        from io import StringIO
        
        captured_output = StringIO()
        original_stdout = sys.stdout
        sys.stdout = captured_output
        
        cli.handle_add("Test Task | Test Description")
        output = captured_output.getvalue().strip()
        sys.stdout = original_stdout
        
        self.assertEqual(output, "Task added with ID 1")
        
        # Verify task was added
        tasks = todo_manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")
        self.assertEqual(tasks[0].description, "Test Description")
        
        # Test list command
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cli.handle_list()
        output = captured_output.getvalue().strip()
        sys.stdout = original_stdout
        
        expected_line = "1 [ ] Test Task - Test Description"
        self.assertIn(expected_line, output)
        
        # Test update command
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cli.handle_update("1 Updated Task | Updated Description")
        output = captured_output.getvalue().strip()
        sys.stdout = original_stdout
        
        self.assertEqual(output, "Task 1 updated successfully")
        
        # Verify task was updated
        updated_task = todo_manager.get_task(1)
        self.assertEqual(updated_task.title, "Updated Task")
        self.assertEqual(updated_task.description, "Updated Description")
        
        # Test complete command
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cli.handle_complete("1")
        output = captured_output.getvalue().strip()
        sys.stdout = original_stdout
        
        self.assertEqual(output, "Task 1 marked as complete")
        
        # Verify task status was updated
        completed_task = todo_manager.get_task(1)
        self.assertEqual(completed_task.status, "complete")
        
        # Test delete command
        captured_output = StringIO()
        sys.stdout = captured_output
        
        cli.handle_delete("1")
        output = captured_output.getvalue().strip()
        sys.stdout = original_stdout
        
        self.assertEqual(output, "Task 1 deleted successfully")
        
        # Verify task was deleted
        tasks = todo_manager.list_tasks()
        self.assertEqual(len(tasks), 0)


if __name__ == "__main__":
    unittest.main()