"""
Main entry point for the In-Memory Command-Line Todo Application.

This module initializes the application components and runs the main CLI loop.
"""
from todo_manager import TodoManager
from cli import TodoCLI


def main():
    """Main function to run the todo application."""
    print("Welcome to the Todo Application!")
    print("Type 'help' for available commands.")
    
    todo_manager = TodoManager()
    cli = TodoCLI(todo_manager)
    
    cli.run()


if __name__ == "__main__":
    main()