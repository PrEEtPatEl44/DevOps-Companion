from flask import Flask, jsonify, request
from app.automated_task_assignment import get_all_users, fetch_unassigned_tasks, get_work_item_counts_for_all_users, generate_gpt_task_assignment, update_work_item_assigned_to
from app.status_report import fetch_pending_tasks
from flask_cors import CORS
from app.stats import count_work_items_by_state, count_work_items_by_assignment, count_work_items_by_type
from app.project_plan import fetch_all_work_items,generate_ms_project_plan
from app.config import jwt_token, PROJECT_NAME
from app.risk import filter_risk_items
from helper.outlook import OutlookEmailSender
from app.status_report import organize_tasks_by_due_date
from helper.chatgpt import generate_gpt_email,generate_subject_line
from app.login import fetch_user_projects
app = Flask(__name__)
CORS(app)

@app.route('/api/automated_task_assignment/fetch_allusers', methods=['GET'])
def fetch_users():
    """
    Flask route to fetch and return all users as JSON.
    """
    users = get_all_users()
    if users:
        return jsonify(users)
    else:
        return jsonify({'error': 'Failed to fetch users from Azure DevOps'}), 500

@app.route('/api/automated_task_assignment/fetch_unassigned_tasks', methods=['GET'])
def fetch_tasks():
    """
    Flask route to fetch and return all unassigned tasks as JSON.
    """
    tasks = fetch_unassigned_tasks()
    if tasks:
        return jsonify(tasks)
    else:
        return jsonify({'error': 'Failed to fetch unassigned tasks from Azure DevOps'}), 500

@app.route('/api/automated_task_assignment/task_counts', methods=['GET'])
def fetch_task_counts():
    """
    Flask route to fetch the count of tasks assigned to each user.
    """
    task_counts = get_work_item_counts_for_all_users()
    if task_counts:
        return jsonify(task_counts)
    else:
        return jsonify({'error': 'Failed to fetch task counts for users'}), 500

@app.route('/api/automated_task_assignment/update_work_item/<int:work_item_id>/<user_email>', methods=['POST'])
def update_work_item(work_item_id, user_email):
    """
    Flask route to update the 'Assigned To' field of a work item.
    """
    if not work_item_id or not user_email:
        return jsonify({'error': 'Missing work_item_id or user_email'}), 400

    result = update_work_item_assigned_to(work_item_id, user_email)
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to update work item'}), 500
    
@app.route('/api/status_report/generate_gpt_task_assignment/<task_id>', methods=['POST'])
def generate_gpt_task_assignment_route(task_id):
    """
    Flask route to generate task assignments using GPT.
    """
    if not task_id:
        return jsonify({'error': 'Missing task_id parameter'}), 400
    
    try:
        assignments = generate_gpt_task_assignment(task_id, fetch_all_work_items())
        return jsonify(assignments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status_report/fetch_pending_tasks/<due_date>', methods=['POST'])
def fetch_pending_tasks_route(due_date):
    if not due_date:
        return jsonify({'error': 'Missing due_date parameter'}), 400

    tasks = fetch_pending_tasks(due_date)
    if tasks:
        return jsonify(tasks)
    else:
        return jsonify({'error': 'Failed to fetch pending tasks'}), 500

@app.route('/api/stats/count_work_items_by_state', methods=['GET'])
def count_work_items_by_state_route():


    counts = count_work_items_by_state()
    if counts:
        return jsonify(counts)
    else:
        return jsonify({'error': 'Failed to count work items by state'}), 500
    
@app.route('/api/stats/count_work_items_by_assignment', methods=['GET'])
def count_work_items_by_assignment_route():
    counts = count_work_items_by_assignment()
    if counts:
        return jsonify(counts)
    else:
        return jsonify({'error': 'Failed to count work items by assignment'}), 500
    
@app.route('/api/stats/count_work_items_by_type', methods=['GET'])
def count_work_items_by_type_route():
    counts = count_work_items_by_type()
    if counts:
        return jsonify(counts)
    else:
        return jsonify({'error': 'Failed to count work items by assignment'}), 500

@app.route('/api/receive-token', methods=['POST'])
def receive_token():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    jwt_token = data.get('access_token')
    
    if jwt_token:
        print(f"Received token: {jwt_token}")
        return jsonify({"message": "Token received successfully", "status": "success"}), 200
    else:
        return jsonify({"message": "No token provided", "status": "error"}), 400



@app.route('/api/automated_task_assignment/bulk_update', methods=['POST'])
def bulk_update():
    data = request.json  # Expecting a list of { taskId: email } pairs
    results = []
    
    for task in data:
        task_id = task.get('taskId')
        email = task.get('email')
        
        result = update_work_item_assigned_to(task_id, email)
        
        #success = True  # Assume success for demonstration

        if result:
            results.append({task_id: "Assigned"})
        else:
            results.append({task_id: "Failed"})
    
    return jsonify(results), 200

@app.route('/api/status_report/generate_gpt_task_assignment', methods=['POST'])
def generate_gpt_task_assignment_route_all():
    """
    Flask route to generate task assignments using GPT for single or multiple task IDs.
    """
    data = request.get_json()
    
   
    task_ids = data.get('task_id') or data.get('task_ids')
    if not task_ids:
        return jsonify({'error': 'Missing task_id or task_ids parameter'}), 400

    if isinstance(task_ids, str):
        task_ids = [task_ids]

    try:
        assignments = []
        for task_id in task_ids:
            task_assignment = generate_gpt_task_assignment(task_id, fetch_all_work_items())
            assignments.append({task_id: task_assignment})
        
        return jsonify(assignments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/risk/filter_risk_items', methods=['GET'])
def fetch_filter_risks():
    """
    Flask route to filter risk items.
    """
    risk_items = filter_risk_items()
    if risk_items:
        return jsonify(risk_items)
    else:
         jsonify({'error': 'Failed to filter risk items'}), 500       

@app.route('/api/email_sender/create_draft', methods=['POST'])
def create_draft():
    """
    API Endpoint to create a draft email using Microsoft Graph API.
    """
    data = request.get_json()
    subject = data.get('subject')
    body = data.get('body')
    to_recipients = data.get('to_recipients')
    access_token = data.get('access_token')
    attachments = data.get('attachments', None)

    if not subject or not body or not to_recipients:
        return jsonify({'error': 'Missing subject, body, or to_recipients parameter'}), 400

    # Assuming you fetch an access token for authentication
    #access_token = jwt_token  # You need to implement this function to fetch a valid token

    if not access_token:
        return jsonify({'error': 'Authentication failed. No access token provided.'}), 401

    try:
        # Instantiate the email sender
        email_sender = OutlookEmailSender(access_token)

        # Use the OutlookEmailSender's send_email method to create a draft
        draft_link = email_sender.send_email(subject, body, to_recipients, attachments)

        return jsonify({
            'message': 'Draft created successfully',
            'draft_link': draft_link
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/email_sender/generate_email_ai', methods=['POST'])
def generate_email_ai():
    """
    API Endpoint to generate an email using GPT-4.
    """
    data = request.get_json()
    to = data.get('to')
    to_name = data.get('to_name')
    from_ = data.get('from')
    from_name = data.get('from_name')
    context = data.get('context')
    
    if not to or not from_ or not context:
        return jsonify({'error': 'Missing to, from, or context parameter'}), 400

    try:
        email = generate_gpt_email(to, to_name, from_, from_name, context)
        subject = generate_subject_line(context)
        return jsonify({'email': email, 'subject': subject})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/generate_status_report_plan', methods=['GET'])
def generate_status_report_plan_route():
    """
    Flask route to generate a status report plan.
    """
    status_report_plan = organize_tasks_by_due_date()
    if status_report_plan:
        return jsonify(status_report_plan)
    else:
        return jsonify({'error': 'Failed to generate status report plan'}), 500

@app.route('/api/get_projects', methods=['GET'])
def get_projects_route():
    """
    Flask route to fetch and return all projects as JSON.
    """
    projects = fetch_user_projects(jwt_token)
    if projects:
        return jsonify(projects)
    else:
        return jsonify({'error': 'Failed to fetch projects from Azure DevOps'}), 500

@app.route('/api/switch_project', methods=['POST'])
def switch_project():
    """
    Flask route to switch the current project.
    """
    data = request.get_json()
    PROJECT_NAME = data.get('project')
    if not project_id:
        return jsonify({'error': 'Missing project_id parameter'}), 400

    # Perform the project switch operation here
    return jsonify({'message': f'Switched to project with ID: {project_id}'}), 200

if __name__ == '__main__':
    app.run(debug=True)

