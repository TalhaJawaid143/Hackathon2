# Data Model: In-Memory Command-Line Todo Application

## Task Entity

### Attributes
- **id**: `int` - Unique auto-incrementing integer identifier (starting from 1)
- **title**: `str` - Non-empty string (required), length 1-200 characters, no special control characters
- **description**: `str` - Optional string (can be empty)
- **status**: `str` - Either "pending" or "complete" (default: "pending")

### Relationships
- None (standalone entity)

### Validation Rules
- ID must be unique and auto-incrementing
- Title must be 1-200 characters long
- Title must not contain special control characters
- Title must not be empty
- Status must be either "pending" or "complete"
- Description can be empty

### State Transitions
- Default state: "pending" when task is created
- Can transition from "pending" to "complete" via complete operation
- Can transition from "complete" to "pending" via incomplete/pending operation

## In-Memory Storage Model

### Structure
- **tasks**: `List[Task]` - A list containing all Task objects
- **next_id**: `int` - Counter for the next available ID (starts at 1)

### Constraints
- Maximum of 10,000 tasks in memory (per spec FR-017)
- IDs must remain unique and sequential
- No persistence to disk (in-memory only)

### Operations
- Add task: Append to the tasks list, assign next available ID
- Retrieve tasks: Access by index or iterate through the list
- Update task: Modify attributes of a specific task object
- Delete task: Remove from the tasks list
- Find task: Search by ID through the list