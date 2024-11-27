from flask import Flask, jsonify
from flask_cors import CORS
from app.automated_task_assignment import get_all_users, fetch_unassigned_tasks, get_work_item_counts_for_all_users

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


if __name__ == '__main__':
    app.run(debug=True)
