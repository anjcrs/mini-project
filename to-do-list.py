import datetime

tasks = {}

def add_task():
    task_name = input("Enter a new task: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    tasks[task_name] = {"due_date": due_date, "completed": False }

def view_task():
    for task, details in task.items():
        status: "Completed" if details["completed"] else "Not completed"
        print("Task: {task}, Due date: {details['due_date']}, Status: {status}")

def mark_completed():
    task_name = input("Enter task name: ")
    if task_name in tasks:
        tasks[task_name]["completed"] = True
        print("Task marked as completed!")
    else:
        print("Task not completed")

def delete_task():
    task_name = input("Enter task name: ")
    if task_name in tasks:
        del tasks[task_name]
        print("Task deleted!")
    else:
        print("Task not found!")

print("\n")
while True:
    print("1. Add task")
    print("2. View task")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("\n")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        view_task()
    elif choice == "3":
        mark_completed()
    elif choice == "4":
        delete_task()
    else:
        print("Invalid choice! Please try again.")
