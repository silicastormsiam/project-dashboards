import requests
import os
from datetime import datetime

# Metadata
# File Name: manage_project_board_v1.0.py
# Version: 1.0
# Owner: Andrew Holland
# Purpose: Automate task creation and updates on GitHub Project board for Project Dashboards on GitHub
# Change Log (Last 4):
#   - Version 1.0, 22-07-2025: Initial script to create and assign tasks to PMBOK process group columns
#   - (No prior changes; older changes archived in memory and available on request)

# Configuration
GITHUB_API = "https://api.github.com"
REPO = "silicastormsiam/project-dashboards"
PROJECT_NUMBER = "[PROJECT_NUMBER]"  # Replace with new project number
TOKEN = os.getenv("GITHUB_TOKEN")  # Load token from environment variable
log_file = "/var/www/dashboard/project_log.txt"

# Task definitions
tasks = [
    {
        "title": "Install Python and dependencies on VPS",
        "body": "Install Python, Dash, Gunicorn, NGINX, and Certbot on Hostinger KVM 2 VPS.",
        "label": "Section One",
        "column": "Executing",
        "due_date": "27-07-2025"
    },
    {
        "title": "Configure NGINX and SSL for cyberpunkmonk.com",
        "body": "Set up NGINX reverse proxy and SSL with Certbot for dashboard.",
        "label": "Section One",
        "column": "Executing",
        "due_date": "29-07-2025"
    },
    {
        "title": "Set up cron job for sync_dashboard_v1.4.py",
        "body": "Configure daily cron job for dashboard updates.",
        "label": "Section One",
        "column": "Executing",
        "due_date": "31-07-2025"
    },
    {
        "title": "Define dashboard requirements",
        "body": "Document dashboard requirements (e.g., GitHub API integration, visualizations).",
        "label": "Section Two",
        "column": "Planning",
        "due_date": "27-07-2025"
    },
    {
        "title": "Develop Plotly Dash dashboard code",
        "body": "Code Plotly Dash application for project and task visualization.",
        "label": "Section Two",
        "column": "Executing",
        "due_date": "31-07-2025"
    },
    {
        "title": "Integrate GitHub API for data",
        "body": "Implement GitHub API to fetch project board data.",
        "label": "Section Two",
        "column": "Executing",
        "due_date": "01-08-2025"
    },
    {
        "title": "Deploy dashboard on cyberpunkmonk.com",
        "body": "Deploy Plotly Dash app on Hostinger VPS.",
        "label": "Section Two",
        "column": "Executing",
        "due_date": "02-08-2025"
    },
    {
        "title": "Define Section Three scope",
        "body": "Placeholder for future project scope.",
        "label": "Section Three",
        "column": "Initiating",
        "due_date": "TBD"
    }
]

def get_column_id(column_name, headers):
    response = requests.get(f"{GITHUB_API}/projects/{PROJECT_NUMBER}/columns", headers=headers)
    columns = response.json()
    for column in columns:
        if column["name"] == column_name:
            return column["id"]
    return None

def create_issue(task, headers):
    issue_data = {
        "title": task["title"],
        "body": task["body"],
        "labels": [task["label"]]
    }
    response = requests.post(f"{GITHUB_API}/repos/{REPO}/issues", headers=headers, json=issue_data)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        print(f"Failed to create issue: {task['title']}, {response.text}")
        return None

def assign_issue_to_column(issue_id, column_id, headers):
    response = requests.post(f"{GITHUB_API}/projects/columns/{column_id}/cards", headers=headers, json={"content_id": issue_id, "content_type": "Issue"})
    if response.status_code != 201:
        print(f"Failed to assign issue {issue_id} to column {column_id}: {response.text}")

def main():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    for task in tasks:
        column_id = get_column_id(task["column"], headers)
        if column_id:
            issue_id = create_issue(task, headers)
            if issue_id:
                assign_issue_to_column(issue_id, column_id, headers)
                print(f"Created and assigned: {task['title']} to {task['column']}")
    
    with open(log_file, "a") as f:
        f.write(f"manage_project_board_v1.0.py executed, created tasks on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
