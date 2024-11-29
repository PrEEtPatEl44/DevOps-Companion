from app.project_plan import fetch_all_work_items
import logging
from  app.automated_task_assignment import calculate_priority_score,validate_and_parse_json
import logging
from datetime import datetime, timedelta
from helper.chatgpt import send_chat
def filter_risk_items():
    all_tasks = fetch_all_work_items()
    risk = []
    if isinstance(all_tasks, dict) and "workItems" in all_tasks:
        tasks = all_tasks["workItems"]
    else:
        logging.warning("all_tasks does not contain 'workItems', defaulting to empty list.")
        tasks = []

    tasks = [validate_and_parse_json(task) for task in tasks]

    now = datetime.now()
    seven_days_from_now = now + timedelta(days=7)
    
    for task in tasks:
        task["priority_score"] = calculate_priority_score(task)

    for task in tasks[:]:
        due_date_str = task.get("dueDate")
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                if now <= due_date <= seven_days_from_now:
                    risk.append(task)
                    tasks.remove(task)
            except ValueError:
                logging.warning(f"Invalid date format for task: {task}")
    
    if tasks:
        average_priority_score = sum(task["priority_score"] for task in tasks) / len(tasks)
        high_priority_tasks = [task for task in tasks if task["priority_score"] > average_priority_score]
        
        for task in high_priority_tasks:
            risk.append(task)
            tasks.remove(task)
    else:
        logging.warning("No tasks available to calculate average priority score.")
    
    schema = {
    "name": "item_list",
    "schema": {
        "type": "object",
        "properties": {
        "items": {
            "type": "array",
            "description": "A list of items containing structured information.",
            "items": {
            "type": "object",
            "properties": {
                "id": {
                "type": "number",
                "description": "Unique identifier for the item."
                },
                "title": {
                "type": "string",
                "description": "Title of the item."
                },
                "state": {
                "type": "string",
                "description": "Current state of the item."
                },
                "assigned_to": {
                "type": "string",
                "description": "User assigned to the item."
                },
                "team_project": {
                "type": "string",
                "description": "The project associated with the item."
                },
                "priority": {
                "type": "number",
                "description": "Priority level of the item."
                },
                "severity": {
                "type": "string",
                "description": "Severity level of the item."
                },
                "due_date": {
                "type": "string",
                "description": "Due date for the item."
                },
                "priority_score": {
                "type": "number",
                "description": "Calculated score based on priority."
                }
            },
            "required": [
                "id",
                "title",
                "state",
                "assigned_to",
                "team_project",
                "priority",
                "severity",
                "due_date",
                "priority_score"
            ],
            "additionalProperties": False
            }
        }
        },
        "required": [
        "items"
        ],
        "additionalProperties": False
    },
    "strict": True
    }

    prompt = (
    f"Analyze the following list of tasks: {all_tasks}. "
    f"Each task has a 'priority_score,' calculated based on its priority, severity, and the number of days until the due date. "
    f"Tasks with higher scores are considered more critical. The task list includes items with varying statuses ('new', 'in-progress', 'completed'). "
    f"Your goal is to identify and list the top 15 high-risk tasks based on the following criteria: "
    f"- Tasks with the highest priority scores. "
    f"- Tasks approaching their due dates, especially if their status is 'new' or 'in-progress'. "
    f"- Tasks that have a high priority_score, regardless of their status. "
    f"Do not include explanations or details outside the required schema."
    )
    

    return send_chat(prompt, context="Task assignment logic", schema=schema)

