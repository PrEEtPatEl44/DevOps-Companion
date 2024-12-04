# Azure DevOps Configuration
ORG_NAME = 'preet442727'  # Default Azure DevOps organization name
PROJECT_NAME = "TestProjectKenn"  # Default Azure DevOps project name
#PAT = 'VJ2qQQgHniwwpMroZeGtayYSqnmVympa62s7oBOtc9DW0rJCjKo0JQQJ99AKACAAAAAAAAAAAAASAZDOE742'  # Default Azure DevOps Personal Access Token
PAT = "BTqqMvthD6mNT2nvg5Ck9XAxPIQ1DID0zgt5ngvMWDLwQnHaevtDJQQJ99ALACAAAAAvrSh0AAASAZDOUR3P"
jwt_token = 'eyJ0eXAiOiJKV1QiLCJub25jZSI6Ii1nVDQzQVJTcG5kYl80b0VGZ3poSXE4eElUM2Z6cVFmbkxua1RxWFFNUzgiLCJhbGciOiJSUzI1NiIsIng1dCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCIsImtpZCI6Inp4ZWcyV09OcFRrd041R21lWWN1VGR0QzZKMCJ9...'



# Getters
def get_org_name():
    return ORG_NAME

def get_project_name():
    return PROJECT_NAME

def get_pat():
    return PAT

def get_jwt_token():
    return jwt_token

def get_azure_devops_graph_api_url():
    return AZURE_DEVOPS_GRAPH_API_URL

def get_azure_devops_rest_api_url():
    return AZURE_DEVOPS_REST_API_URL

# Setters
def set_org_name(value):
    global ORG_NAME, AZURE_DEVOPS_GRAPH_API_URL, AZURE_DEVOPS_REST_API_URL
    ORG_NAME = value
    AZURE_DEVOPS_GRAPH_API_URL = f"https://vssps.dev.azure.com/{ORG_NAME}/_apis/graph"
    AZURE_DEVOPS_REST_API_URL = f"https://dev.azure.com/{ORG_NAME}/{PROJECT_NAME}/_apis"

def set_project_name(value):
    global PROJECT_NAME, AZURE_DEVOPS_REST_API_URL
    PROJECT_NAME = value
    AZURE_DEVOPS_REST_API_URL = f"https://dev.azure.com/{ORG_NAME}/{PROJECT_NAME}/_apis"
    print(AZURE_DEVOPS_REST_API_URL)
    print(PROJECT_NAME, )

def set_pat(value):
    global PAT
    PAT = value

def set_jwt_token(value):
    global jwt_token
    jwt_token = value
# Base URLs

AZURE_DEVOPS_GRAPH_API_URL = f"https://vssps.dev.azure.com/{get_org_name()}/_apis/graph"
AZURE_DEVOPS_REST_API_URL = f"https://dev.azure.com/{get_org_name()}/{get_project_name()}/_apis"