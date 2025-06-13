import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure DevOps Configuration
ORG_NAME = os.getenv('AZURE_DEVOPS_ORG_NAME', 'preet442727')  # Default Azure DevOps organization name
PROJECT_NAME = os.getenv('AZURE_DEVOPS_PROJECT_NAME', "TestProjectKenn")  # Default Azure DevOps project name
PAT = os.getenv('AZURE_DEVOPS_PAT')  # Azure DevOps Personal Access Token
JWT_TOKEN = os.getenv('AZURE_DEVOPS_JWT_TOKEN')  # JWT Token for authentication

# Base URLs
AZURE_DEVOPS_GRAPH_API_URL = f"https://vssps.dev.azure.com/{ORG_NAME}/_apis/graph"
AZURE_DEVOPS_REST_API_URL = f"https://dev.azure.com/{ORG_NAME}/{PROJECT_NAME}/_apis"

# Getters
def get_org_name():
    return ORG_NAME

def get_project_name():
    return PROJECT_NAME

def get_pat():
    return PAT

def get_jwt_token():
    return JWT_TOKEN

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
    print(PROJECT_NAME)

def set_pat(value):
    global PAT
    PAT = value

def set_jwt_token(value):
    global JWT_TOKEN
    JWT_TOKEN = value