# Quickstart Guide: In-Memory Command-Line Todo Application

## Running the Application

To run the todo application:

```bash
cd src
python main.py
```

## Available Commands

Once the application is running, you can use the following commands:

### Add a Task
```
add <title> | <description>
```
Example: `add Buy groceries | Milk, eggs, bread`

### List All Tasks
```
list
```
Displays all tasks with ID, status indicator ([ ] or [x]), title, and description if present.

### Update a Task
```
update <id> <new_title> | <new_description>
```
Example: `update 1 New title | New description`
You can update title, description, or both (use | separator)

### Delete a Task
```
delete <id>
```
Example: `delete 1`
Removes the task permanently.

### Mark Task as Complete
```
complete <id>
```
Example: `complete 1`
Marks the task as complete.

### Mark Task as Incomplete
```
incomplete <id>
```
or
```
pending <id>
```
Example: `incomplete 1` or `pending 1`
Marks the task as pending.

### Show Help
```
help
```
Shows the list of available commands.

### Quit the Application
```
quit
```
or
```
exit
```
Exits the application cleanly.

## Example Workflow

Here's a complete example of using the application:

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

## Error Handling

The application provides user-friendly error messages for invalid inputs:

- If you try to access a non-existent task ID: "Task with ID X not found"
- If you provide an invalid command: "Unknown command: <command>. Type 'help' for available commands."
- If you don't provide required arguments: "Invalid command format. See 'help' for usage."
- If title exceeds 200 characters: "Title too long. Maximum 200 characters allowed."