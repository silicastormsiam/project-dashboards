import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: manage_rats_tasks_v1.0.py
# Version: 1.0
# Owner: Andrew John Holland
# Purpose: Create and update tasks for RATS project on GitHub Project board using PMBOK process groups
# Change Log (Last 4):
#   - Version 1.0, 23-07-2025: Initial script for RATS project tasks

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO_NAME = "silicastormsiam/rats"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gXy"  # Verify for projects/3
TOKEN = "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"
log_file = "project_log.txt"

tasks = [
    {"title": "Create/update profiles on 9 platforms", "status": "Executing"},
    {"title": "Configure job alerts for IT roles", "status": "Executing"},
    {"title": "Verify platform profiles and alerts", "status": "Monitoring and Controlling"},
    {"title": "Set up email consolidation process", "status": "Executing"},
    {"title": "Validate database fields", "status": "Monitoring and Controlling"},
    {"title": "Create dashboard", "status": "Executing"},
    {"title": "Process daily job alerts", "status": "Executing"},
    {"title": "Deploy system and train user", "status": "Closing"},
    {"title": "Create a Daily Checklist - RATS", "status": "Planning"}
]

def create_issue(client, repo_name, title):
    mutation = """
    mutation {
      createIssue(input: {
        repositoryId: "%s",
        title: "%s",
        body: "Created for RATS project using PMBOK process groups"
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
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    existing_titles = get_existing_issues(client, REPO_NAME)
    for task in tasks:
        if task["title"] in existing_titles:
            print(f"Skipping existing issue: {task['title']}")
        else:
            issue_id = create_issue(client, REPO_NAME, task["title"])
            if issue_id:
                if add_issue_to_project(client, PROJECT_ID, issue_id):
                    print(f"Created and assigned: {task['title']}")
                    with open(log_file, "a") as f:
                        f.write(f"Created and assigned: {task['title']} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
                else:
                    print(f"Failed to add {task['title']} to project")
    status_field_id, status_options = get_status_field_id(PROJECT_ID)
    if not status_field_id or not status_options:
        print("Failed to get Status field ID or options")
        return
    item_ids = get_project_item_ids(PROJECT_ID)
    print(f"Project item IDs: {item_ids}")
    for task in tasks:
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
