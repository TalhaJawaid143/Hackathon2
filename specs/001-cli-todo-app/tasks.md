# Tasks: In-Memory Command-Line Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src directory structure with __init__.py files
- [X] T002 Create tests directory structure with __init__.py files
- [X] T003 [P] Create main.py file in src/ with basic application structure
- [X] T004 [P] Create models.py file in src/ for Task data model
- [X] T005 [P] Create todo_manager.py file in src/ for business logic
- [X] T006 [P] Create cli.py file in src/ for command line interface

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Task dataclass in src/models.py with id, title, description, status attributes
- [X] T008 Implement Task validation in src/models.py (title length, non-empty, special chars)
- [X] T009 Create TodoManager class in src/todo_manager.py with in-memory storage (list)
- [X] T010 Implement ID generation in TodoManager (auto-incrementing starting from 1)
- [X] T011 Create custom exception classes in src/todo_manager.py for error handling
- [X] T012 Implement 10,000 task limit enforcement in TodoManager
- [X] T013 Create CLI command parsing functionality in src/cli.py
- [X] T014 Implement basic CLI loop structure in src/main.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with title and optional description to the todo list

**Independent Test**: The application should allow a user to add a task with a title and optional description, and the task should appear in the list with a unique ID and "pending" status.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T015 [P] [US1] Unit test for Task creation in tests/test_models.py
- [X] T016 [P] [US1] Unit test for add_task functionality in tests/test_todo_manager.py

### Implementation for User Story 1

- [X] T017 [US1] Implement add_task method in TodoManager class in src/todo_manager.py
- [X] T018 [US1] Add validation for title requirements in add_task method
- [X] T019 [US1] Implement command parsing for 'add' command in src/cli.py
- [X] T020 [US1] Implement 'add' command handler in src/cli.py
- [X] T021 [US1] Connect 'add' command to TodoManager in src/main.py
- [X] T022 [US1] Add error handling for add command in src/cli.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Enable users to view all tasks with their ID, status indicator, title, and description

**Independent Test**: The application should display all tasks with their ID, status indicator, title, and description in a clear, readable format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US2] Unit test for list_tasks functionality in tests/test_todo_manager.py
- [X] T024 [P] [US2] Unit test for task display formatting in tests/test_cli.py

### Implementation for User Story 2

- [X] T025 [US2] Implement list_tasks method in TodoManager class in src/todo_manager.py
- [X] T026 [US2] Implement task display formatting in src/cli.py
- [X] T027 [US2] Implement 'list' command handler in src/cli.py
- [X] T028 [US2] Connect 'list' command to TodoManager in src/main.py
- [X] T029 [US2] Handle empty task list case with appropriate message

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Enable users to mark tasks as complete or incomplete to track progress

**Independent Test**: The application should allow a user to change the status of a task between "pending" and "complete".

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T030 [P] [US5] Unit test for mark_complete functionality in tests/test_todo_manager.py
- [X] T031 [P] [US5] Unit test for mark_incomplete functionality in tests/test_todo_manager.py

### Implementation for User Story 5

- [X] T032 [US5] Implement mark_complete method in TodoManager class in src/todo_manager.py
- [X] T033 [US5] Implement mark_incomplete method in TodoManager class in src/todo_manager.py
- [X] T034 [US5] Implement 'complete' command handler in src/cli.py
- [X] T035 [US5] Implement 'incomplete'/'pending' command handler in src/cli.py
- [X] T036 [US5] Connect 'complete' command to TodoManager in src/main.py
- [X] T037 [US5] Connect 'incomplete'/'pending' command to TodoManager in src/main.py

**Checkpoint**: All user stories 1, 2, and 5 should now be independently functional

---

## Phase 6: User Story 3 - Update Task Details (Priority: P2)

**Goal**: Enable users to update task titles and/or descriptions as needed

**Independent Test**: The application should allow a user to update the title and/or description of an existing task without affecting other properties.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T038 [P] [US3] Unit test for update_task functionality in tests/test_todo_manager.py

### Implementation for User Story 3

- [X] T039 [US3] Implement update_task method in TodoManager class in src/todo_manager.py
- [X] T040 [US3] Implement 'update' command handler in src/cli.py
- [X] T041 [US3] Connect 'update' command to TodoManager in src/main.py
- [X] T042 [US3] Add validation for update command in src/cli.py

**Checkpoint**: All user stories 1, 2, 3, and 5 should now be independently functional

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks that are no longer needed

**Independent Test**: The application should remove a specified task from the list and ensure it no longer appears when listing tasks.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T043 [P] [US4] Unit test for delete_task functionality in tests/test_todo_manager.py

### Implementation for User Story 4

- [X] T044 [US4] Implement delete_task method in TodoManager class in src/todo_manager.py
- [X] T045 [US4] Implement 'delete' command handler in src/cli.py
- [X] T046 [US4] Connect 'delete' command to TodoManager in src/main.py
- [X] T047 [US4] Add error handling for delete command in src/cli.py

**Checkpoint**: All user stories 1, 2, 3, 4, and 5 should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T048 [P] Add type hints throughout all modules in src/
- [X] T049 [P] Add docstrings to all classes and methods in src/
- [X] T050 Implement help command functionality in src/cli.py
- [X] T051 Implement quit/exit command functionality in src/main.py
- [X] T052 Add performance validation to ensure operations complete in under 1 second
- [X] T053 Add comprehensive error handling and user-friendly messages throughout
- [X] T054 [P] Create unit tests for all functionality in tests/
- [X] T055 Run quickstart.md validation to ensure all commands work as expected
- [X] T056 Final integration testing of complete workflow (add → list → update → complete → delete)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task creation in tests/test_models.py"
Task: "Unit test for add_task functionality in tests/test_todo_manager.py"

# Launch all implementation for User Story 1 together:
Task: "Implement add_task method in TodoManager class in src/todo_manager.py"
Task: "Add validation for title requirements in add_task method"
Task: "Implement command parsing for 'add' command in src/cli.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 5
   - Developer D: User Story 3
   - Developer E: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence