import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: update_sss_tasks_v1.1.py
# Version: 1.1
# Owner: Andrew John Holland
# Purpose: Update task statuses on SSS-Project Dashboard using PMBOK process groups
# Change Log (Last 4):
#   - Version 1.1, 23-07-2025: Corrected syntax errors by removing Markdown markers
#   - Version 1.0, 23-07-2025: Initial script for updating SSS-Project Dashboard tasks

# Configuration
GITHUB_API = "https://api.github.com/graphql"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Verify for projects/2
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"

tasks_to_update = [
    {"title": "Install Python and dependencies on VPS", "status": "Executing"},
    {"title": "Configure NGINX and SSL for cyberpunkmonk.com", "status": "Executing"},
    {"title": "Set up cron job for sync_dashboard_v1.4.py", "status": "Executing"},
    {"title": "Define dashboard requirements", "status": "Executing"},
    {"title": "Develop Plotly Dash dashboard code", "status": "Executing"},
    {"title": "Integrate GitHub API for data", "status": "Executing"},
    {"title": "Deploy dashboard on cyberpunkmonk.com", "status": "Executing"},
    {"title": "Define Section Three scope", "status": "Executing"},
    {"title": "Configure /volume1/GitHub/ shared folder", "status": "Closing"},
    {"title": "Add SSH deploy key to GitHub", "status": "Closing"},
    {"title": "Install Git Server", "status": "Executing"},
    {"title": "Set up Synology sync script", "status": "Executing"},
    {"title": "Initialize Synology bare repository", "status": "Executing"},
    {"title": "Create GitHub repository backup", "status": "Executing"},
    {"title": "AIFU - Artificial Intelligence Future Uncovered YouTube Channel", "status": "Closing"},
    {"title": "RATS - Recruitment Application Tracking System", "status": "Executing"},
    {"title": "Homelab Hardware Development: Create internal inventory with IPs and ports", "status": "Initiating"},
    {"title": "Homelab Hardware Development: Create public inventory without sensitive data", "status": "Initiating"},
    {"title": "CPM - Chatbot Project Management", "status": "Planning"}
]

def get_status_field_id(project_id):
    print("Fetching status field ID...")
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
        print(f"GraphQL result: {result}")
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return None, None
        fields = result.get("data", {}).get("node", {}).get("fields", {}).get("nodes", [])
        for field in fields:
            if field.get("name") == "Status":
                print(f"Found Status field: {field['id']}")
                return field["id"], {option["name"]: option["id"] for option in field["options"]}
        print("Failed to find Status field")
        return None, None
    except Exception as e:
        print(f"Failed to get status field ID: {str(e)}")
        return None, None

def get_project_item_ids(project_id):
    print("Fetching project item IDs...")
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return {}
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
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
    try:
        result = json.loads(client.execute(query))
        print(f"GraphQL result: {result}")
        if "errors" in result:
            print(f"GraphQL errors fetching project items: {result['errors']}")
            return {}
        items = result.get("data", {}).get("node", {}).get("items", {}).get("nodes", [])
        return {item["content"]["title"]: item["id"] for item in items if "title" in item["content"]}
    except Exception as e:
        print(f"Failed to fetch project item IDs: {str(e)}")
        return {}

def update_task_status(project_id, item_id, status_field_id, status_option_id, title):
    print(f"Updating status for {title} to {status_option_id}...")
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return False
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
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
    try:
        result = json.loads(client.execute(mutation))
        print(f"GraphQL result for {title}: {result}")
        if "errors" in result:
            print(f"GraphQL errors updating status for {title}: {result['errors']}")
            return False
        if result.get("data", {}).get("updateProjectV2ItemFieldValue"):
            print(f"Updated status for {title} to {status_option_id}")
            return True
        return False
    except Exception as e:
        print(f"Failed to update status for {title}: {str(e)}")
        return False

def main():
    status_field_id, status_options = get_status_field_id(PROJECT_ID)
    if not status_field_id or not status_options:
        print("Failed to get Status field ID or options")
        return
    item_ids = get_project_item_ids(PROJECT_ID)
    print(f"Project item IDs: {item_ids}")
    for task in tasks_to_update:
        item_id = item_ids.get(task["title"])
        status_option_id = status_options.get(task["status"])
        if not item_id:
            print(f"Project item not found: {task['title']}")
            continue
        if not status_option_id:
            print(f"Status option not found: {task['status']} for {task['title']}")
            continue
        if update_task_status(PROJECT_ID, item_id, status_field_id, status_option_id, task["title"]):
            with open(log_file, "a") as f:
                f.write(f"Updated status for {task['title']} to {task['status']} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
