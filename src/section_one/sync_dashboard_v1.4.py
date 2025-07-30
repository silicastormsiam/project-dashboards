import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: sync_dashboard_v1.4.py
# Version: 1.4
# Owner: Andrew Holland
# Purpose: Synchronize GitHub Project board data with the dashboard, logging updates
# Change Log (Last 4):
#   - Version 1.4, 22-07-2025: Added detailed error logging for debugging
#   - (No prior versions; created for cron job synchronization)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
USERNAME = "silicastormsiam"
PROJECT_NUMBER = 5  # Project number for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"  # Adjusted for local execution; update to /var/www/dashboard on VPS

def fetch_project_data():
    if not TOKEN:
        error_msg = "Error: GITHUB_TOKEN is not set"
        print(error_msg)
        with open(log_file, "a") as f:
            f.write(f"{error_msg} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
        return None
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      user(login: "%s") {
        projectV2(number: %s) {
          items(first: 100) {
            nodes {
              content {
                ... on Issue {
                  title
                  body
                  labels(first: 10) {
                    nodes {
                      name
                    }
                  }
                  updatedAt
                }
              }
              fieldValues(first: 10) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """ % (USERNAME, PROJECT_NUMBER)
    
    try:
        result = json.loads(client.execute(query))
        if "errors" in result:
            error_msg = f"GraphQL errors: {result['errors']}"
            print(error_msg)
            with open(log_file, "a") as f:
                f.write(f"{error_msg} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
            return None
        data = result.get("data", {}).get("user", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
        if not data:
            error_msg = "No project data returned"
            print(error_msg)
            with open(log_file, "a") as f:
                f.write(f"{error_msg} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
            return None
        return data
    except Exception as e:
        error_msg = f"Failed to fetch project data: {str(e)}"
        print(error_msg)
        with open(log_file, "a") as f:
            f.write(f"{error_msg} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
        return None

def main():
    project_data = fetch_project_data()
    if not project_data:
        print("Failed to sync project data")
        return
    
    # Log successful sync
    with open(log_file, "a") as f:
        f.write(f"sync_dashboard_v1.4.py executed, synced project data on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
    print("Successfully synced project data")

if __name__ == "__main__":
    main()
