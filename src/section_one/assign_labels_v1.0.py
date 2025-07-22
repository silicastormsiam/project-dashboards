import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: assign_labels_v1.0.py
# Version: 1.0
# Owner: Andrew Holland
# Purpose: Assign labels to existing issues in the GitHub repository
# Change Log (Last 4):
#   - Version 1.0, 22-07-2025: Increased label query limit to 100 and added debug output

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO = "silicastormsiam/project-dashboards"
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"

# Task definitions with labels
tasks = [
    {"title": "Install Python and dependencies on VPS", "label": "Section One"},
    {"title": "Configure NGINX and SSL for cyberpunkmonk.com", "label": "Section One"},
    {"title": "Set up cron job for sync_dashboard_v1.4.py", "label": "Section One"},
    {"title": "Define dashboard requirements", "label": "Section Two"},
    {"title": "Develop Plotly Dash dashboard code", "label": "Section Two"},
    {"title": "Integrate GitHub API for data", "label": "Section Two"},
    {"title": "Deploy dashboard on cyberpunkmonk.com", "label": "Section Two"},
    {"title": "Define Section Three scope", "label": "Section Three"}
]

def get_label_ids():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return {}
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      repository(owner: "silicastormsiam", name: "project-dashboards") {
        labels(first: 100) {
          nodes {
            id
            name
          }
        }
      }
    }
    """
    
    try:
        result = json.loads(client.execute(query))
        if "errors" in result:
            print(f"GraphQL errors fetching labels: {result['errors']}")
            return {}
        labels = result.get("data", {}).get("repository", {}).get("labels", {}).get("nodes", [])
        label_dict = {label["name"]: label["id"] for label in labels}
        print(f"Retrieved labels: {list(label_dict.keys())}")
        return label_dict
    except Exception as e:
        print(f"Failed to fetch label IDs: {str(e)}")
        return {}

def get_issue_ids():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return {}
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      repository(owner: "silicastormsiam", name: "project-dashboards") {
        issues(first: 100) {
          nodes {
            id
            title
          }
        }
      }
    }
    """
    
    try:
        result = json.loads(client.execute(query))
        if "errors" in result:
            print(f"GraphQL errors fetching issues: {result['errors']}")
            return {}
        issues = result.get("data", {}).get("repository", {}).get("issues", {}).get("nodes", [])
        return {issue["title"]: issue["id"] for issue in issues}
    except Exception as e:
        print(f"Failed to fetch issue IDs: {str(e)}")
        return {}

def assign_label_to_issue(issue_id, label_id, title):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return False
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    mutation = """
    mutation {
      addLabelsToLabelable(input: {
        labelableId: "%s"
        labelIds: ["%s"]
      }) {
        labelable {
          ... on Issue {
            title
          }
        }
      }
    }
    """ % (issue_id, label_id)
    
    try:
        result = json.loads(client.execute(mutation))
        if "errors" in result:
            print(f"GraphQL errors assigning label to {title}: {result['errors']}")
            return False
        if result.get("data", {}).get("addLabelsToLabelable", {}).get("labelable"):
            print(f"Assigned label to issue: {title}")
            return True
        return False
    except Exception as e:
        print(f"Failed to assign label to {title}: {str(e)}")
        return False

def main():
    label_ids = get_label_ids()
    issue_ids = get_issue_ids()
    
    for task in tasks:
        issue_id = issue_ids.get(task["title"])
        label_id = label_ids.get(task["label"])
        if not issue_id:
            print(f"Issue not found: {task['title']}")
            continue
        if not label_id:
            print(f"Label not found: {task['label']} for {task['title']}")
            continue
        if assign_label_to_issue(issue_id, label_id, task["title"]):
            with open(log_file, "a") as f:
                f.write(f"Assigned label {task['label']} to issue {task['title']} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
