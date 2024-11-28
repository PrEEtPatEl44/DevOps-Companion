import requests
import logging
from requests.auth import HTTPBasicAuth
from app.config import AZURE_DEVOPS_REST_API_URL, PAT, PROJECT_NAME

def fetch_all_work_items():
    """
    Fetch all work items from Azure DevOps for a given project.
    
    Parameters:
        azure_devops_url (str): Base URL for Azure DevOps REST API.
        project_name (str): Name of the Azure DevOps project.
        pat (str): Personal Access Token for authentication.
    
    Returns:
        dict: A dictionary with work items, or None if an error occurred.
    """
    url = f'{AZURE_DEVOPS_REST_API_URL}/wit/wiql?api-version=7.1-preview.2'
    
    auth = HTTPBasicAuth('', PAT)  # Empty username, PAT as the password

    # Define the WIQL query
    query = {
        "query": f"""
        SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo], [System.TeamProject]
        FROM WorkItems
        WHERE [System.TeamProject] = '{PROJECT_NAME}'
        ORDER BY [System.ChangedDate] DESC
        """
    }

    try:
        logging.debug(f'WIQL Query URL: {url}')
        logging.debug(f'WIQL Query Payload: {query}')

        # Send POST request to execute the WIQL query
        response = requests.post(url, auth=auth, json=query)
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
            
            # Clean up the data
            cleaned_work_items = [
                {
                    "id": item.get("id"),
                    "title": item.get("fields", {}).get("System.Title", ""),
                    "state": item.get("fields", {}).get("System.State", ""),
                    "assigned_to": item.get("fields", {}).get("System.AssignedTo", {}).get("displayName", ""),
                    "team_project": item.get("fields", {}).get("System.TeamProject", "")
                }
                for item in all_work_items
            ]
            return {"workItems": cleaned_work_items}
        else:
            logging.error(f'Failed to execute WIQL query: {response.status_code}')
            logging.error(f'Response Content: {response.content.decode()}')
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return None

