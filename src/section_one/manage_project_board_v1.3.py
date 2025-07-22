import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: manage_project_board_v1.3.py
# Version: 1.3
# Owner: Andrew Holland
# Purpose: Automate task creation and updates on GitHub Project board using GraphQL API
# Change Log (Last 4):
#   - Version 1.3, 22-07-2025: Enhanced error handling and skip existing tasks
#   - Version 1.2, 22-07-2025: Fixed token typo and added error handling
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience
#   - Version 1.0, 22-07-2025: Initial script using REST API (deprecated)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO = "silicastormsiam/project-dashboards"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Project ID for Project Dashboards on GitHub
REPO_ID = "R_kgDOPPbNSw"  # Repository ID for silicastormsiam/project-dashboards
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"  # Adjusted for local execution; update to /var/www/dashboard on VPS

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

def get_status_field_id(project_id):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return None, None
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          fields(first: 10) {
            nodes {
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """ % project_id
    
    try:
        result = json.loads(client.execute(query))
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return None, None
        fields = result.get("data", {}).get("node", {}).get("fields", {}).get("nodes", [])
        for field in fields:
            if field.get("name") == "Status":
                return field["id"], {option["name"]: option["id"] for option in field["options"]}
        print("Failed to find Status field")
        return None, None
    except Exception as e:
        print(f"Failed to get status field ID: {str(e)}")
        return None, None

def get_existing_issues():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return []
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      repository(owner: "silicastormsiam", name: "project-dashboards") {
        issues(first: 100) {
          nodes {
            title
          }
        }
      }
    }
    """
    
    try:
        result = json.loads(client.execute(query))
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return []
        return [issue["title"] for issue in result.get("data", {}).get("repository", {}).get("issues", {}).get("nodes", [])]
    except Exception as e:
        print(f"Failed to get existing issues: {str(e)}")
        return []

def create_issue_and_add_to_project(project_id, task, status_field_id, status_option_id):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return None
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    # Create issue
    mutation = """
    mutation {
      createIssue(input: {
        repositoryId: "%s"
        title: "%s"
        body: "%s"
        labels: ["%s"]
      }) {
        issue {
          id
        }
      }
    }
    """ % (REPO_ID, task["title"], task["body"], task["label"])
    
    try:
        result = json.loads(client.execute(mutation))
        if "errors" in result:
            print(f"GraphQL errors creating issue {task['title']}: {result['errors']}")
            return None
        issue_id = result.get("data", {}).get("createIssue", {}).get("issue", {}).get("id")
        if not issue_id:
            print(f"Failed to create issue: {task['title']}")
            return None
        
        # Add issue to project
        mutation = """
        mutation {
          addProjectV2ItemById(input: {
            projectId: "%s"
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
            print(f"GraphQL errors adding issue {task['title']} to project: {result['errors']}")
            return None
        item_id = result.get("data", {}).get("addProjectV2ItemById", {}).get("item", {}).get("id")
        if not item_id:
            print(f"Failed to add issue {task['title']} to project")
            return None
        
        # Set status field
        mutation = """
        mutation {
          updateProjectV2ItemFieldValue(input: {
            projectId: "%s"
            itemId: "%s"
            fieldId: "%s"
            value: { singleSelectOptionId: "%s" }
          }) {
            projectV2Item {
              id
            }
          }
        }
        """ % (project_id, item_id, status_field_id, status_option_id)
        
        try:
            result = json.loads(client.execute(mutation))
            if "errors" in result:
                print(f"GraphQL errors setting status for {task['title']}: {result['errors']}")
                return None
            if result.get("data", {}).get("updateProjectV2ItemFieldValue"):
                print(f"Created and assigned: {task['title']} to {task['column']}")
            return item_id
        except Exception as e:
            print(f"Failed to set status for {task['title']}: {str(e)}")
            return None
    except Exception as e:
        print(f"Failed to process task {task['title']}: {str(e)}")
        return None

def main():
    status_field_id, status_options = get_status_field_id(PROJECT_ID)
    if not status_field_id or not status_options:
        print("Failed to get Status field ID or options")
        return
    
    existing_issues = get_existing_issues()
    
    for task in tasks:
        if task["title"] in existing_issues:
            print(f"Skipping existing issue: {task['title']}")
            continue
        status_option_id = status_options.get(task["column"])
        if status_option_id:
            create_issue_and_add_to_project(PROJECT_ID, task, status_field_id, status_option_id)
    
    with open(log_file, "a") as f:
        f.write(f"manage_project_board_v1.3.py executed, created tasks on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
