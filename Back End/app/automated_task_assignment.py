import logging
import requests
from requests.auth import HTTPBasicAuth
from app.config import AZURE_DEVOPS_GRAPH_API_URL, PAT, AZURE_DEVOPS_REST_API_URL

def get_all_users():
    """
    Fetch and clean all users from Azure DevOps Graph API.
    """
    url = f'{AZURE_DEVOPS_GRAPH_API_URL}/users?api-version=7.1-preview.1'
    auth = HTTPBasicAuth('', PAT)  # Empty username, PAT as the password
    try:
        response = requests.get(url, auth=auth)
        logging.debug(f'Response Status Code: {response.status_code}')
        if response.status_code == 200:
            raw_data = response.json()
            cleaned_data = clean_user_data(raw_data)
            return {"count": len(cleaned_data), "users": cleaned_data}
        else:
            logging.error(f'Failed to fetch data from Azure DevOps: {response.status_code}')
            logging.error(f'Response Content: {response.content.decode()}')
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return None


def clean_user_data(raw_data):
    """
    Clean and structure user data from the raw API response.
    """
    users = raw_data.get("value", [])
    cleaned_users = []

    for user in users:
        cleaned_users.append({
            "displayName": user.get("displayName", "N/A"),
            "domain": user.get("domain", "N/A"),
            "mailAddress": user.get("mailAddress", "N/A"),
            "principalName": user.get("principalName", "N/A"),
        })

    return cleaned_users

    
def fetch_unassigned_tasks():
    """
    Fetch unassigned tasks from Azure DevOps using WIQL.
    """
    url = f'{AZURE_DEVOPS_REST_API_URL}/wit/wiql?api-version=7.1-preview.2'
    auth = HTTPBasicAuth('', PAT)  # Empty username, PAT as the password

    # Define the WIQL query
    query = {
        "query": """
        SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo]
        FROM WorkItems
        WHERE [System.AssignedTo] = ''
        ORDER BY [System.ChangedDate] DESC
        """
    }

    try:
        # Send POST request to execute the WIQL query
        response = requests.post(url, auth=auth, json=query)
        logging.debug(f'WIQL Query URL: {url}')
        logging.debug(f'WIQL Query Payload: {query}')
        logging.debug(f'Response Status Code: {response.status_code}')
        logging.debug(f'Response Content: {response.content.decode()}')
        
        if response.status_code == 200:
            # Extract work item IDs from the response
            work_item_refs = response.json().get('workItems', [])
            work_item_ids = [item['id'] for item in work_item_refs]
            logging.debug(f'Fetched Work Item IDs: {work_item_ids}')
            
            # Fetch full details for each work item in batches of 200
            all_work_items = []
            for i in range(0, len(work_item_ids), 200):
                batch_ids = work_item_ids[i:i+200]
                details_url = f"{AZURE_DEVOPS_REST_API_URL}/wit/workitemsbatch?api-version=7.1-preview.1"
                details_payload = {"ids": batch_ids}
                details_response = requests.post(details_url, auth=auth, json=details_payload)
                logging.debug(f'Details URL: {details_url}')
                logging.debug(f'Details Payload: {details_payload}')
                logging.debug(f'Details Response Status Code: {details_response.status_code}')
                logging.debug(f'Details Response Content: {details_response.content.decode()}')
                
                if details_response.status_code == 200:
                    all_work_items.extend(details_response.json().get('value', []))
                else:
                    logging.error(f'Failed to fetch work item details: {details_response.status_code}')
                    logging.error(f'Response Content: {details_response.content.decode()}')
                    return None
            
            return {"workItems": all_work_items}
        else:
            logging.error(f'Failed to execute WIQL query: {response.status_code}')
            logging.error(f'Response Content: {response.content.decode()}')
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return None

def get_work_item_count_for_user(user_email):
    """
    Get the count of work items assigned to a specific user from Azure DevOps.
    """
    url = f'{AZURE_DEVOPS_REST_API_URL}/wit/wiql?api-version=7.1-preview.2'
    auth = HTTPBasicAuth('', PAT)  # Empty username, PAT as the password

    # Define the WIQL query
    query = {
        "query": f"""
        SELECT [System.Id]
        FROM WorkItems
        WHERE [System.AssignedTo] = '{user_email}'
        """
    }

    try:
        # Execute the WIQL query
        response = requests.post(url, auth=auth, json=query)
        logging.debug(f'WIQL Query URL: {url}')
        logging.debug(f'WIQL Query Payload: {query}')
        logging.debug(f'Response Status Code: {response.status_code}')
        logging.debug(f'Response Content: {response.content.decode()}')
        
        if response.status_code == 200:
            work_items = response.json().get('workItems', [])
            return len(work_items)
        else:
            logging.error(f'Failed to fetch work item count for {user_email}: {response.status_code}')
            logging.error(f'Response Content: {response.content.decode()}')
            return 0
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed for {user_email}: {e}')
        return 0


def get_work_item_counts_for_all_users():
    """
    Get the work item count for all users retrieved from Azure DevOps.
    """
    # Get all users
    users_data = get_all_users()
    if not users_data or "users" not in users_data:
        logging.error('Failed to fetch users data.')
        return None

    users = users_data["users"]
    user_task_counts = {}

    # Loop through each user and fetch their work item count
    for user in users:
        user_email = user.get("mailAddress")
        if not user_email:
            logging.debug(f'Skipping user {user["displayName"]} (no email address).')
            continue

        task_count = get_work_item_count_for_user(user_email)
        user_task_counts[user_email] = {
            "displayName": user["displayName"],
            "taskCount": task_count
        }

    return user_task_counts

