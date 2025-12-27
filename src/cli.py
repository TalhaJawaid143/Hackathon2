"""
Command Line Interface for the In-Memory Command-Line Todo Application.

This module handles command parsing, user input/output, and formatting.
"""
from todo_manager import TodoManager, TaskNotFoundError
from typing import Optional
import re


class TodoCLI:
    """
    Command Line Interface for the Todo Application.
    
    Handles user commands, parses input, and formats output.
    """
    
    def __init__(self, todo_manager: TodoManager):
        """
        Initialize the CLI with a TodoManager instance.
        
        Args:
            todo_manager: The TodoManager instance to interact with
        """
        self.todo_manager = todo_manager
        self.running = True
    
    def run(self):
        """Run the main CLI loop."""
        while self.running:
            try:
                command_input = input("> ").strip()
                if not command_input:
                    continue
                
                self.process_command(command_input)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break
    
    def process_command(self, command_input: str):
        """
        Process a user command.
        
        Args:
            command_input: The raw command string from the user
        """
        # Split the command and arguments
        parts = command_input.split(" ", 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Handle different commands
        if command == "add":
            self.handle_add(args)
        elif command == "list":
            self.handle_list()
        elif command == "update":
            self.handle_update(args)
        elif command == "delete":
            self.handle_delete(args)
        elif command == "complete":
            self.handle_complete(args)
        elif command in ["incomplete", "pending"]:
            self.handle_incomplete(args)
        elif command == "help":
            self.handle_help()
        elif command in ["quit", "exit"]:
            self.handle_quit()
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def handle_add(self, args: str):
        """
        Handle the 'add' command.
        
        Args:
            args: The arguments for the add command (title and optional description)
        """
        # Parse title and description using the pipe separator
        title, description = self._parse_title_description(args)
        
        if not title:
            print("Invalid command format. Usage: add <title> | <description> (description is optional)")
            return
        
        try:
            task = self.todo_manager.add_task(title, description)
            print(f"Task added with ID {task.id}")
        except Exception as e:
            print(f"Error adding task: {str(e)}")
    
    def handle_list(self):
        """Handle the 'list' command."""
        tasks = self.todo_manager.list_tasks()
        
        if not tasks:
            print("No tasks found")
            return
        
        for task in tasks:
            status_indicator = "[x]" if task.status == "complete" else "[ ]"
            description_part = f" - {task.description}" if task.description else ""
            print(f"{task.id} {status_indicator} {task.title}{description_part}")
    
    def handle_update(self, args: str):
        """
        Handle the 'update' command.
        
        Args:
            args: The arguments for the update command (id, new title, new description)
        """
        # Parse task ID, new title, and new description
        try:
            # Split by first space to get ID
            parts = args.split(" ", 1)
            if len(parts) < 2:
                print("Invalid command format. Usage: update <id> <new_title> | <new_description>")
                return
            
            task_id_str, rest = parts[0], parts[1]
            task_id = int(task_id_str)
            
            # Parse new title and description
            new_title, new_description = self._parse_title_description(rest)
            
            # Determine what to update
            update_title = new_title if new_title else None
            update_description = new_description if new_description else None
            
            # If both are None, it means we only got an ID
            if update_title is None and update_description is None:
                print("Invalid command format. Usage: update <id> <new_title> | <new_description>")
                return
            
            task = self.todo_manager.update_task(task_id, update_title, update_description)
            print(f"Task {task.id} updated successfully")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")
        except TaskNotFoundError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error updating task: {str(e)}")
    
    def handle_delete(self, args: str):
        """
        Handle the 'delete' command.
        
        Args:
            args: The arguments for the delete command (task ID)
        """
        try:
            task_id = int(args.strip())
            success = self.todo_manager.delete_task(task_id)
            
            if success:
                print(f"Task {task_id} deleted successfully")
            else:
                print(f"Task with ID {task_id} not found")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")
        except Exception as e:
            print(f"Error deleting task: {str(e)}")
    
    def handle_complete(self, args: str):
        """
        Handle the 'complete' command.
        
        Args:
            args: The arguments for the complete command (task ID)
        """
        try:
            task_id = int(args.strip())
            task = self.todo_manager.mark_complete(task_id)
            print(f"Task {task.id} marked as complete")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")
        except TaskNotFoundError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error marking task as complete: {str(e)}")
    
    def handle_incomplete(self, args: str):
        """
        Handle the 'incomplete' or 'pending' command.
        
        Args:
            args: The arguments for the incomplete command (task ID)
        """
        try:
            task_id = int(args.strip())
            task = self.todo_manager.mark_incomplete(task_id)
            print(f"Task {task.id} marked as pending")
        except ValueError:
            print("Invalid task ID. Please provide a valid number.")
        except TaskNotFoundError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error marking task as pending: {str(e)}")
    
    def handle_help(self):
        """Handle the 'help' command."""
        print("Available commands:")
        print("  add <title> | <description>    - Add a new task")
        print("  list                           - List all tasks")
        print("  update <id> <title> | <desc>   - Update a task")
        print("  delete <id>                    - Delete a task")
        print("  complete <id>                  - Mark task as complete")
        print("  incomplete <id> or pending <id> - Mark task as pending")
        print("  help                           - Show this help message")
        print("  quit or exit                   - Exit the application")
    
    def handle_quit(self):
        """Handle the 'quit' or 'exit' command."""
        print("Goodbye!")
        self.running = False
    
    def _parse_title_description(self, args: str) -> tuple[Optional[str], Optional[str]]:
        """
        Parse title and description from command arguments using the pipe separator.

        Args:
            args: The command arguments string

        Returns:
            A tuple of (title, description) where both can be None if not provided
        """
        # Handle the case where pipe is at the beginning
        if args.startswith("|"):
            # Everything after the pipe is the description, title is empty
            description = args[1:].strip()
            return "", description

        # Handle the case where pipe is at the end
        if args.endswith("|"):
            # Everything before the pipe is the title, description is empty
            title = args[:-1].strip()
            return title, ""

        # Handle the case with " | " in the middle
        if " | " in args:
            title, description = args.split(" | ", 1)
            return title.strip(), description.strip()
        else:
            # If no pipe separator, treat the entire string as the title
            return args.strip(), ""