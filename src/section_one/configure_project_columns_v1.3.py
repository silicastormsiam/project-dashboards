import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: configure_project_columns_v1.4.py
# Version: 1.4
# Owner: Andrew Holland
# Purpose: Configure PMBOK process group columns on GitHub Project board using GraphQL API, handling existing fields
# Change Log (Last 4):
#   - Version 1.4, 22-07-2025: Fixed GraphQL syntax error in settings JSON and improved error handling
#   - Version 1.3, 22-07-2025: Added check for existing Status field to avoid duplicates
#   - Version 1.2, 22-07-2025: Added enhanced error handling and logging for GraphQL API calls
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience; fixed headers parameter

# Configuration
GITHUB_API = "https://api.github.com/graphql"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Project ID for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"  # Adjusted for local execution; update to /var/www/dashboard on VPS

def get_status_field_id(project_id):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return None
    
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
            return None
        fields = result.get("data", {}).get("node", {}).get("fields", {}).get("nodes", [])
        for field in fields:
            if field.get("name") == "Status":
                expected_options = {"Initiating", "Planning", "Executing", "Monitoring and Controlling", "Closing"}
                current_options = {option["name"] for option in field.get("options", [])}
                if expected_options.issubset(current_options):
                    print(f"Found existing Status field with ID {field['id']} and correct PMBOK options")
                    return field["id"]
                else:
                    print(f"Existing Status field found, but options do not match PMBOK: {current_options}")
                    return None
        print("No existing Status field found")
        return None
    except Exception as e:
        print(f"Failed to get status field ID: {str(e)}")
        return None

def create_status_field(project_id):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return None
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    # Properly escaped JSON settings
    settings = json.dumps({
        "options": [
            {"name": "Initiating"},
            {"name": "Planning"},
            {"name": "Executing"},
            {"name": "Monitoring and Controlling"},
            {"name": "Closing"}
        ]
    })
    
    mutation = """
    mutation {
      addProjectV2Field(input: {
        projectId: "%s"
        fieldType: SINGLE_SELECT
        name: "Status"
        settings: %s
      }) {
        projectV2Field {
          id
          name
        }
      }
    }
    """ % (project_id, json.dumps(settings))
    
    try:
        result = json.loads(client.execute(mutation))
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return None
        field_id = result.get("data", {}).get("addProjectV2Field", {}).get("projectV2Field", {}).get("id")
        if field_id:
            print(f"Created status field for project {project_id} with ID {field_id}")
        else:
            print("Failed to create status field: No field ID returned")
        return field_id
    except Exception as e:
        print(f"Failed to create status field: {str(e)}")
        return None

def main():
    field_id = get_status_field_id(PROJECT_ID)
    if field_id:
        print(f"Using existing Status field with ID {field_id}")
    else:
        field_id = create_status_field(PROJECT_ID)
        if not field_id:
            print("Failed to configure PMBOK status field")
            return
    
    with open(log_file, "a") as f:
        f.write(f"configure_project_columns_v1.4.py executed, configured PMBOK status field on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
