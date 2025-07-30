import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: manage_project_board_v1.3.py
# Version: 1.3
# Owner: Andrew John Holland
# Purpose: Add tasks to GitHub Project board using Projects V2
# Change Log (Last 4):
#   - Version 1.3, 23-07-2025: Added major SilicaStormSiam projects and Homelab tasks

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO_NAME = "silicastormsiam/project-dashboards"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Verify for projects/2
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"

tasks = [
    "Install Python and dependencies on VPS",
    "Configure NGINX and SSL for cyberpunkmonk.com",
    "Set up cron job for sync_dashboard_v1.4.py",
    "Define dashboard requirements",
    "Develop Plotly Dash dashboard code",
    "Integrate GitHub API for data",
    "Deploy dashboard on cyberpunkmonk.com",
    "Define Section Three scope",
    "Configure /volume1/GitHub/ shared folder",
    "Add SSH deploy key to GitHub",
    "Install Git Server",
    "Set up Synology sync script",
    "Initialize Synology bare repository",
    "Create GitHub repository backup",
    "AIFU - Artificial Intelligence Future Uncovered YouTube Channel",
    "RATS - Recruitment Application Tracking System",
    "Homelab Hardware Development: Create internal inventory with IPs and ports",
    "Homelab Hardware Development: Create public inventory without sensitive data",
    "CPM - Chatbot Project Management"
]

def create_issue(client, repo_name, title):
    mutation = """
    mutation {
      createIssue(input: {
        repositoryId: "%s",
        title: "%s",
        body: "Created for SSS-Project Dashboard"
      }) {
        issue {
          id
          title
        }
      }
    }
    """
    repo_query = """
    query {
      repository(owner: "%s", name: "%s") {
        id
      }
    }
    """ % (repo_name.split("/")[0], repo_name.split("/")[1])
    repo_result = json.loads(client.execute(repo_query))
    repo_id = repo_result["data"]["repository"]["id"]
    result = json.loads(client.execute(mutation % (repo_id, title)))
    if "errors" in result:
        print(f"Error creating issue {title}: {result['errors']}")
        return None
    return result["data"]["createIssue"]["issue"]["id"]

def add_issue_to_project(client, project_id, issue_id):
    mutation = """
    mutation {
      addProjectV2ItemById(input: {
        projectId: "%s",
        contentId: "%s"
      }) {
        item {
          id
        }
      }
    }
    """ % (project_id, issue_id)
    result = json.loads(client.execute(mutation))
    if "errors" in result:
        print(f"Error adding issue to project: {result['errors']}")
        return False
    return True

def get_existing_issues(client, repo_name):
    query = """
    query {
      repository(owner: "%s", name: "%s") {
        issues(first: 100, states: OPEN) {
          nodes {
            title
          }
        }
      }
    }
    """ % (repo_name.split("/")[0], repo_name.split("/")[1])
    result = json.loads(client.execute(query))
    if "errors" in result:
        print(f"Error fetching issues: {result['errors']}")
        return []
    return [issue["title"] for issue in result["data"]["repository"]["issues"]["nodes"]]

def main():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    existing_titles = get_existing_issues(client, REPO_NAME)
    for task in tasks:
        if task in existing_titles:
            print(f"Skipping existing issue: {task}")
            continue
        issue_id = create_issue(client, REPO_NAME, task)
        if issue_id:
            if add_issue_to_project(client, PROJECT_ID, issue_id):
                print(f"Created and assigned: {task}")
                with open(log_file, "a") as f:
                    f.write(f"Created and assigned: {task} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
            else:
                print(f"Failed to add {task} to project")

if __name__ == "__main__":
    main()
