import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: configure_project_columns_v1.1.py
# Version: 1.1
# Owner: Andrew Holland
# Purpose: Configure PMBOK process group columns on GitHub Project board using GraphQL API
# Change Log (Last 4):
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience; fixed headers parameter
#   - Version 1.0, 22-07-2025: Initial script using REST API (deprecated)
#   - (No prior changes; older changes archived in memory and available on request)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Project ID for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "/var/www/dashboard/project_log.txt"

def create_status_field(project_id):
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    mutation = """
    mutation {
      addProjectV2Field(input: {
        projectId: "%s"
        fieldType: SINGLE_SELECT
        name: "Status"
        settings: "{\"options\": [{\"name\": \"Initiating\"}, {\"name\": \"Planning\"}, {\"name\": \"Executing\"}, {\"name\": \"Monitoring and Controlling\"}, {\"name\": \"Closing\"}]}"
      }) {
        projectV2Field {
          id
          name
        }
      }
    }
    """ % project_id
    
    try:
        result = json.loads(client.execute(mutation))
        field_id = result.get("data", {}).get("addProjectV2Field", {}).get("projectV2Field", {}).get("id")
        if field_id:
            print(f"Created status field for project {project_id}")
        return field_id
    except Exception as e:
        print(f"Failed to create status field: {str(e)}")
        return None

def main():
    field_id = create_status_field(PROJECT_ID)
    if not field_id:
        print("Failed to configure PMBOK status field")
        return
    
    with open(log_file, "a") as f:
        f.write(f"configure_project_columns_v1.1.py executed, created PMBOK status field on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
