import os
import requests
import base64
import json

# Replace these with your repository and PAT information
repo_owner = "ManishaMiranda"
repo_name = "test-luminex"
pat = "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"

# GitHub API URL to list workflows
api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows"

# Set up headers with your PAT
headers = {
    "Authorization": f"token {pat}",
    "Accept": "application/vnd.github.v3+json"
}

payload = {
    "event_type": "deploy-aws-resources",
    "client_payload": {
        "instance_name": "value1",
        "ami_id": "value2",
        "instance_type": "value3"
    },
}

# Make a GET request to list workflows
response = requests.get(api_url, headers=headers, verify = False )

if response.status_code == 200:
    workflows = response.json()["workflows"]

    # Function to execute a workflow
    def execute_workflow(workflow_id):
        execution_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/dispatches"
        payload = {
            "ref": "main"
        }
        execution_response = requests.post(execution_url, headers=headers, data=json.dumps(payload))
        return execution_response.status_code

    # Execute all workflows
    for workflow in workflows:
        workflow_id = workflow["id"]
        workflow_name = workflow["name"]
        result = execute_workflow(workflow_id)
        print(f"Executed workflow '{workflow_name}' with result: {result}")

else:
    print(f"Failed to list workflows. Status code: {response.status_code}")
