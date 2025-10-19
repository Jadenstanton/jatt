# Just another task tracker

## Installation

```pip install git+https://github.com/jadenstanton/jatt.git```

## Usage

```shell
# Adding a new task
jatt add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
jatt update 1 "Buy groceries and cook dinner"
jatt delete 1

# Marking a task as in progress or done
jatt mark-in-progress 1
jatt mark-done 1

# Listing all tasks
jatt list

# Listing tasks by status
jatt list done
jatt list todo
jatt list in-progress
```
