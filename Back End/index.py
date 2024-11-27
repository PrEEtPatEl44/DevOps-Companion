from flask import Flask, jsonify
from app.automated_task_assignment import get_all_users, fetch_unassigned_tasks, get_work_item_counts_for_all_users, update_work_item_assigned_to
from app.status_report import fetch_pending_tasks
from flask_cors import CORS
from app.stats import count_work_items_by_state, count_work_items_by_assignment

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




if __name__ == '__main__':
    app.run(debug=True)

#/api/automated_task_assignment/update_work_item/1012/preet442727@outlook.com