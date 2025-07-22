import requests
import os
from datetime import datetime

# Metadata
# File Name: list_projects_v1.0.py
# Version: 1.0
# Owner: Andrew Holland
# Purpose: List all GitHub projects under user silicastormsiam to identify the project board for Project Dashboards on GitHub
# Change Log (Last 4):
#   - Version 1.0, 22-07-2025: Initial script to list user projects and their IDs
#   - (No prior changes; older changes archived in memory and available on request)

# Configuration
GITHUB_API = "https://api.github.com"
USERNAME = "silicastormsiam"
TOKEN = os.getenv("GITHUB_TOKEN")  # Load token from environment variable
log_file = "project_log.txt"  # Local log file

def list_projects():
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(f"{GITHUB_API}/users/{USERNAME}/projects", headers=headers)
    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            print(f"Project Name: {project['name']}, ID: {project['id']}, URL: {project['html_url']}")
        return projects
    else:
        print(f"Failed to list projects: {response.text}")
        return []

def main():
    projects = list_projects()
    with open(log_file, "a") as f:
        f.write(f"list_projects_v1.0.py executed, listed projects on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
