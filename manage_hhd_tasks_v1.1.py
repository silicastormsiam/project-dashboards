import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: manage_hhd_tasks_v1.1.py
# Version: 1.1
# Owner: Andrew John Holland
# Purpose: Create and update tasks for Homelab Hardware Development (HHD) project on GitHub Project board using PMBOK 5 process groups, designed for Daily Checklist
# Change Log (Last 4):
#   - Version 1.1, 23-07-2025: Aligned tasks with HHD specifics, improved status mapping, configured PMBOK groups for checklist
#   - Version 1.0, 23-07-2025: Initial script for HHD project tasks

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO_NAME = "silicastormsiam/homelab-hardware"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gXz"  # Verify this matches projects/4/views/1
TOKEN = os.getenv("GITHUB_TOKEN")
LOG_FILE = "project_log.txt"

# HHD-specific tasks mapped to PMBOK process groups
tasks = [
    {"title": "Project Initiation - Define Homelab Inventory Project", "pmbok_group": "Initiating"},
    {"title": "Plan Inventory Management - Develop Homelab Inventory - Original", "pmbok_group": "Planning"},
    {"title": "Plan Inventory Management - Develop Homelab Inventory - Skeleton", "pmbok_group": "Planning"},
    {"title": "Implement Inventory - Update Homelab Inventory - Original", "pmbok_group": "Executing"},
    {"title": "Implement Inventory - Update Homelab Inventory - Skeleton", "pmbok_group": "Executing"},
    {"title": "Deploy Inventory to GitHub", "pmbok_group": "Executing"},
    {"title": "Monitor Inventory Updates - Audit Security and Accuracy", "pmbok_group": "Monitoring and Controlling"},
    {"title": "Control Changes - Track Inventory Revisions", "pmbok_group": "Monitoring and Controlling"},
    {"title": "Close Inventory Project - Finalize and Document", "pmbok_group": "Closing"}
]

def create_issue(client, repo_name, title, pmbok_group):
    mutation = """
    mutation {
      createIssue(input: {
        repositoryId: "%s",
        title: "%s",
        body: "Task for Homelab Hardware Development (HHD) project, aligned with PMBOK %s process. Daily Checklist Item."
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
    if "errors" in repo_result:
        print(f"Error fetching repository ID: {repo_result['errors']}")
        return None
    repo_id = repo_result["data"]["repository"]["id"]
    result = json.loads(client.execute(mutation % (repo_id, title, pmbok_group)))
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

def get_status_field_id(client, project_id):
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
    result = json.loads(client.execute(query))
    if "errors" in result:
        print(f"Error fetching status field: {result['errors']}")
        return None, None
    fields = result.get("data", {}).get("node", {}).get("fields", {}).get("nodes", [])
    for field in fields:
        if field.get("name") == "Status":
            return field["id"], {option["name"]: option["id"] for option in field["options"]}
    print("Status field not found. Please ensure your board has a 'Status' field or adjust the script with your column names.")
    return None, None

def get_project_item_ids(client, project_id):
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          items(first: 100) {
            nodes {
              id
              content {
                ... on Issue {
                  title
                }
              }
            }
          }
        }
      }
    }
    """ % project_id
    result = json.loads(client.execute(query))
    if "errors" in result:
        print(f"Error fetching project items: {result['errors']}")
        return {}
    return {item["content"]["title"]: item["id"] for item in result.get("data", {}).get("node", {}).get("items", {}).get("nodes", []) if "title" in item["content"]}

def update_task_status(client, project_id, item_id, status_field_id, status_option_id, title):
    mutation = """
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "%s",
        itemId: "%s",
        fieldId: "%s",
        value: { singleSelectOptionId: "%s" }
      }) {
        projectV2Item {
          id
        }
      }
    }
    """ % (project_id, item_id, status_field_id, status_option_id)
    result = json.loads(client.execute(mutation))
    if "errors" in result:
        print(f"Error updating status for {title}: {result['errors']}")
        return False
    print(f"Updated status for {title} to {status_option_id}")
    return True

def log_action(action, task_title, status=None):
    with open(LOG_FILE, "a") as f:
        f.write(f"{action}: {task_title} {'(Status: ' + status + ')' if status else ''} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

def main():
    if not TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set. Set it with 'export GITHUB_TOKEN=your_token' before running for Daily Checklist.")
        return
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    # Fetch existing issues to avoid duplicates
    existing_titles = get_existing_issues(client, REPO_NAME)
    print(f"Existing issues: {existing_titles}")

    # Create new issues and add to project
    for task in tasks:
        if task["title"] not in existing_titles:
            issue_id = create_issue(client, REPO_NAME, task["title"], task["pmbok_group"])
            if issue_id:
                if add_issue_to_project(client, PROJECT_ID, issue_id):
                    print(f"Created and added: {task['title']} (PMBOK: {task['pmbok_group']})")
                    log_action("Created and added", task["title"], task["pmbok_group"])
                else:
                    print(f"Failed to add {task['title']} to project")
            else:
                print(f"Failed to create issue: {task['title']}")
        else:
            print(f"Skipping existing issue: {task['title']}")

    # Update task statuses based on PMBOK group mapping
    status_field_id, status_options = get_status_field_id(client, PROJECT_ID)
    if not status_field_id or not status_options:
        print("Cannot proceed: Status field ID or options not found. Please configure your board with PMBOK-compatible statuses or map them manually.")
        return
    print(f"Available status options: {status_options}")

    # Map PMBOK groups to potential board statuses (adjust based on your board)
    pmbok_to_board_status = {
        "Initiating": next((k for k, v in status_options.items() if "To Do" in k), "To Do"),
        "Planning": next((k for k, v in status_options.items() if "In Progress" in k), "In Progress"),
        "Executing": next((k for k, v in status_options.items() if "In Progress" in k), "In Progress"),
        "Monitoring and Controlling": next((k for k, v in status_options.items() if "In Review" in k), "In Review"),
        "Closing": next((k for k, v in status_options.items() if "Done" in k), "Done")
    }
    print(f"PMBOK to board status mapping: {pmbok_to_board_status}")

    item_ids = get_project_item_ids(client, PROJECT_ID)
    print(f"Project item IDs: {item_ids}")

    for task in tasks:
        item_id = item_ids.get(task["title"])
        if item_id:
            board_status = pmbok_to_board_status.get(task["pmbok_group"])
            status_option_id = status_options.get(board_status)
            if status_option_id:
                if update_task_status(client, PROJECT_ID, item_id, status_field_id, status_option_id, task["title"]):
                    log_action("Updated status", task["title"], board_status)
            else:
                print(f"Status option {board_status} not found for {task['title']}")
        else:
            print(f"Item ID not found for {task['title']}")

if __name__ == "__main__":
    main()
