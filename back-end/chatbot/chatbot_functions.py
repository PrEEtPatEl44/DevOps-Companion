from app.automated_task_assignment import get_all_users, calculate_priority_score, validate_and_parse_json, get_work_item_counts_for_all_users, update_work_item_assigned_to
from app.config import AZURE_DEVOPS_REST_API_URL, PAT, PROJECT_NAME, ORG_NAME, jwt_token
from helper.outlook import OutlookEmailSender
from app.project_plan import fetch_all_work_items
import os
from app.risk import filter_risk_items

def update_work_item_assigned(work_item_id, user_email):
    """
    Updates the assigned user of a work item.

    Args:
        work_item_id (int): The ID of the work item to be updated.
        user_email (str): The email of the user to assign the work item to.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    return  update_work_item_assigned_to(work_item_id, user_email)

def send_email_outlook(subject, body, to_recipients):
    """
    Send an email using Outlook API.
    """
    # Get an access token
    access_token = jwt_token
    if not access_token:
        return None

    # Send the email
    sender = OutlookEmailSender(access_token)
    print("Sending email")
    return sender.send_mail(subject=subject, body=body, to_recipients=to_recipients)

def fetch_emails_outlook():
    """
    Fetch emails from the user's inbox.
    """
    access_token = jwt_token
    if not access_token:
        return None

    # Fetch emails
    sender = OutlookEmailSender(access_token)
    return sender.fetch_emails()

def book_meeting_outlook(subject, start_time, end_time, attendees, location=None, body=None):
    """
    Book a meeting using the Outlook API.
    """
    access_token = jwt_token
    if not access_token:
        return None

    # Book the meeting
    sender = OutlookEmailSender(access_token)
    return sender.book_meeting(subject, start_time, end_time, attendees, location, body)

def get_all_work_items_devops():
    """
    Get all work items from the Azure DevOps project.
    """
    return fetch_all_work_items()

def get_all_risk_items_devops():
    """
    Get all risk items from the Azure DevOps project.
    """
    return filter_risk_items()

def get_all_users_devops():
    """
    Get all users from the Azure DevOps project.
    """
    return get_work_item_counts_for_all_users()

def get_total_priority_by_user_devops():
    """
    Get the total priority score for each user.
    """
    all_tasks = fetch_all_work_items()
    all_users = get_all_users()
    if isinstance(all_tasks, dict) and "workItems" in all_tasks:
        tasks = all_tasks["workItems"]
    else:
        tasks = []

    tasks = [validate_and_parse_json(task) for task in tasks]

    user_priority = {user: 0 for user in all_users}
    for task in tasks:
        user = task.get("assignedTo")
        if user in user_priority:
            user_priority[user] += calculate_priority_score(task)

    return user_priority
