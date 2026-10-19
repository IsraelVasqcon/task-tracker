# Task Tracker CLI

A command-line application developed in Python for creating, tracking, and managing tasks stored locally in a JSON file.

This project was created to practice Python programming, object-oriented programming, file handling, command-line argument processing, data validation, and version control with Git.

If you are reading this project in English, this project is dedicated to study purposes and to understanding more about programming. Most of the code is in Portuguese, however the code itself calls functions and methods in English because that's how the language understands better. Feel free to explore the functionalities of the project. Enjoi!

Features
The application allows users to:

Add new tasks
Update a task description
Delete tasks
Mark a task as in progress
Mark a task as completed
List all tasks
List pending tasks
List tasks in progress
List completed tasks
Automatically store data in JSON format
Handle invalid commands, arguments, and data
Technologies and Resources
Python
Python Standard Library
argparse for command processing
json for data persistence
dataclasses for task modeling
pathlib for file path handling
datetime for recording creation and update timestamps
Git for version control
GitHub for repository hosting
This project does not use any external frameworks or libraries.

Requirements
Python 3.10 or later
Terminal, Git Bash, PowerShell, or an equivalent command-line interface
To check the installed Python version:

python --version
On some Windows installations:

py --version
Project Structure;
task-tracker/
├── .gitignore
├── README.md
├── task_cli.py
└── tests.md
During the first execution, the application automatically creates:

tasks.json
The tasks.json file stores task data locally and is not committed to the repository.

How to Run
Clone the repository:

git clone REPOSITORY_URL
Navigate to the project directory:

cd task-tracker
Display the help menu:

python task_cli.py --help
You can also display help for a specific command:

python task_cli.py add --help
python task_cli.py update --help
python task_cli.py delete --help
Available Commands
Add a Task
python task_cli.py add "Buy groceries"
Expected output:

Task added successfully (ID: 1)
Every new task is initially created with the following status:

todo
Update a Task
python task_cli.py update 1 "Buy groceries and prepare dinner"
Expected output:

Task with ID 1 updated successfully.
The update changes the task description and the updatedAt field while preserving the ID, status, and creation date.

Delete a Task
python task_cli.py delete 1
Expected output:

Task with ID 1 deleted successfully: Buy groceries
Only the task matching the provided ID will be removed.

Mark a Task as In Progress
python task_cli.py mark-in-progress 1
Expected output:

Task with ID 1 marked as in progress.
The status will be changed to:

in-progress
Mark a Task as Completed
python task_cli.py mark-done 1
Expected output:

Task with ID 1 marked as completed.
The status will be changed to:

done
List All Tasks
python task_cli.py list
Example output:

--------------------------------------------------
ID:1
Description: Buy groceries
Status: todo
Created at: 2026-10-17T01:10:32.099745+00:00
Updated at: 2026-10-17T01:10:32.099745+00:00
--------------------------------------------------
List Pending Tasks
python task_cli.py list todo
List Tasks in Progress
python task_cli.py list in-progress
List Completed Tasks
python task_cli.py list done
Available Statuses
The application uses three task statuses:

# Status Meaning

todo: Pending task
in-progress: Task in progress
done: Completed task

Task Structure
Each task contains the following properties:

Property: Description
id: Numeric task identifier
description: Task description
status: Current task status
createdAt: Creation date and time
updatedAt: Date and time of the most recent update
Example record in tasks.json:

{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2026-10-17T01:10:32.099745+00:00",
  "updatedAt": "2026-10-17T01:10:32.099745+00:00"
}

Dates are stored in UTC using the ISO 8601 format.

JSON File Creation
If tasks.json does not exist, the application automatically creates the file with an empty list:

[]
The file content is validated when it is loaded. The application identifies situations such as:

Empty files
Malformed JSON
A root structure that is not a list
Tasks missing required fields
Duplicate IDs
Invalid dates
Unrecognized statuses
Internal Organization
The application is organized by responsibility.

Task
Represents a task and validates:

ID
Description
Status
Creation date
Update date
JsonTaskRepository
Responsible for:

Creating tasks.json
Loading data
Converting JSON records into task objects
Validating duplicate IDs
Saving changes
Protecting the write operation by using a temporary file
TaskService
Contains the business rules for:

Adding tasks
Updating tasks
Deleting tasks
Finding tasks
Changing task statuses
Listing and filtering tasks
Validating IDs and descriptions
CLI
The command-line interface uses argparse to:

Recognize commands
Process positional arguments
Convert IDs into integers
Generate help messages
Reject invalid commands and arguments
Error Handling
The application handles situations such as:

Empty descriptions
IDs equal to or less than zero
Non-numeric IDs
Tasks that do not exist
Updates that do not make any actual changes
Attempts to apply the same status again
Invalid filters
Inaccessible files
Corrupted JSON files
Duplicate IDs
Example:

python task_cli.py delete 999
Output:

Error: Task with ID 999 was not found.
ID Generation Decision
The next ID is calculated using the highest ID currently stored, plus 1.

Example:

Current IDs: 1, 2, and 4
Next ID: 5
If the task with the highest ID is deleted, that number may be reused when a new task is added

A future version may use persistent metadata or a database to prevent identifier reuse
------------------------------------------
Testing
------------------------------------------
The manual test scenarios are documented in
tests.md
The following scenarios were tested
------------------------------------------
Creating multiple tasks
ID generation
Updating task descriptions
Changing task statuses
Task filtering
Task deletion
Nonexistent IDs
Missing arguments
Invalid values
Empty descriptions
Accented characters and special characters
Automatic JSON file creation
Invalid JSON
Preservation of other records
Date field integrity
To validate the Python syntax

python -m py_compile task_cli.py
Complete Workflow Example
python task_cli.py add "Study Python"
python task_cli.py list
python task_cli.py mark-in-progress 1
python task_cli.py list in-progress
python task_cli.py update 1 "Study object-oriented programming in Python"
python task_cli.py mark-done 1
python task_cli.py list done
python task_cli.py delete 1
python task_cli.py list

Concepts Practiced
The following concepts were applied during development

Object-oriented programming
Classes and objects
Encapsulation
Abstraction
Single responsibility principle
Instance methods
Class methods
Static methods
Custom exceptions
Type annotations
List comprehensions
JSON serialization and deserialization
File handling
Positional arguments
Exit codes
Git and incremental commits
Debugging and manual testing
Current Version Limitations
Local storage using a single JSON file
No automated tests
No concurrency support for multiple simultaneous executions
Execution through python task_cli.py
IDs based on the highest currently stored identifier
Dates displayed directly in UTC
No database
Possible Future Improvements
Add automated tests using unittest
Split the application into separate modules
Install the application as a task-cli command
Add SQLite support
Add pagination and sorting to task listings
Add task description search
Convert dates to local time
Configure continuous integration
Distribute the application as a Python package
Lessons Learned
This project was developed as part of a Python and Git learning process.

In addition to implementing the functional requirements, the development process involved:

Incremental planning
Identifying and fixing indentation issues
Using tracebacks for troubleshooting
Input validation
Preventing code duplication
Refactoring
Creating commits for individual features
Reviewing files before publication
Author
Developed by Israel de Vasconcellos e Siqueira.

This project was created for learning purposes and software development practice.
