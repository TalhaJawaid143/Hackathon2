# In-Memory Command-Line Todo Application

A console-based todo application that stores all tasks in memory with no persistence. The application provides CLI commands for adding, viewing, updating, deleting, and marking tasks as complete.

## Features

- Add tasks with title and optional description
- List all tasks with ID, status indicator, title, and description
- Update task titles and descriptions
- Delete tasks
- Mark tasks as complete or incomplete
- Help command for available commands
- Clean exit functionality

## Requirements

- Python 3.13+
- Standard library only (no external dependencies)

## Usage

1. Navigate to the src directory:
   ```bash
   cd src
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Use the available commands:
   - `add <title> | <description>` - Add a new task (description is optional)
   - `list` - List all tasks
   - `update <id> <new_title> | <new_description>` - Update a task
   - `delete <id>` - Delete a task
   - `complete <id>` - Mark task as complete
   - `incomplete <id>` or `pending <id>` - Mark task as pending
   - `help` - Show available commands
   - `quit` or `exit` - Exit the application

## Example Workflow

```
> add Buy groceries | Milk, eggs, bread
Task added with ID 1

> add Complete project proposal
Task added with ID 2

> list
1 [ ] Buy groceries - Milk, eggs, bread
2 [ ] Complete project proposal

> complete 1
Task 1 marked as complete

> update 2 Finalize project proposal | Submit to manager by EOD
Task 2 updated successfully

> list
1 [x] Buy groceries - Milk, eggs, bread
2 [ ] Finalize project proposal - Submit to manager by EOD

> quit
Goodbye!
```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

1. **Models Layer** (`models.py`): Contains the Task dataclass that represents the core entity
2. **Business Logic Layer** (`todo_manager.py`): Implements all task management operations
3. **CLI Layer** (`cli.py`): Handles command parsing, user input/output, and formatting
4. **Application Layer** (`main.py`): Orchestrates the CLI loop and connects all components

## Testing

Unit tests are located in the `tests/` directory. To run all tests:

```bash
cd tests
python -m unittest discover
```

## Constraints

- Maximum of 10,000 tasks in memory
- Title length must be between 1 and 200 characters
- No special control characters allowed in titles
- In-memory storage only (data is lost on exit)