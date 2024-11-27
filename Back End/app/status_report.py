import requests
from requests.auth import HTTPBasicAuth
from app.config import AZURE_DEVOPS_REST_API_URL, PAT
import logging

def fetch_pending_tasks(due_date):
    """
    Fetch work items from Azure DevOps that are not marked as done and have a due date past the specified date.
    
    Args:
        due_date (str): The date in YYYY-MM-DD format to filter tasks with due dates past this value.
    
    Returns:
        dict or None: A dictionary of work items or None in case of failure.
    """
    url = f'{AZURE_DEVOPS_REST_API_URL}/wit/wiql?api-version=7.1-preview.2'
    auth = HTTPBasicAuth('', PAT)  # Empty username, PAT as the password

    # Define the WIQL query
    query = {
        "query": f"""
        SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo], [Microsoft.VSTS.Scheduling.DueDate]
        FROM WorkItems
        WHERE [System.State] <> 'Done'
        AND [Microsoft.VSTS.Scheduling.DueDate] > '{due_date}'
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
