import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: list_projects_v1.1.py
# Version: 1.1
# Owner: Andrew Holland
# Purpose: List all GitHub projects under user silicastormsiam using GraphQL API
# Change Log (Last 4):
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience
#   - Version 1.0, 22-07-2025: Initial script using REST API (deprecated)
#   - (No prior changes; older changes archived in memory and available on request)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
USERNAME = "silicastormsiam"
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"

def list_projects():
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    query = """
    query {
      user(login: "%s") {
        projectsV2(first: 10) {
          nodes {
            number
            title
            url
            id
          }
        }
      }
    }
    """ % USERNAME
    
    try:
        result = json.loads(client.execute(query))
        projects = result.get("data", {}).get("user", {}).get("projectsV2", {}).get("nodes", [])
        for project in projects:
            print(f"Project Name: {project['title']}, Number: {project['number']}, ID: {project['id']}, URL: {project['url']}")
        return projects
    except Exception as e:
        print(f"Failed to list projects: {str(e)}")
        return []

def main():
    projects = list_projects()
    with open(log_file, "a") as f:
        f.write(f"list_projects_v1.1.py executed, listed projects on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
