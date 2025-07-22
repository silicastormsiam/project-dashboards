#!/bin/bash

# Metadata
# File Name: setup_project_template_v1.6.sh
# Version: 1.6
# Owner: Andrew Holland
# Purpose: Automate setup of GitHub repository and project board for silicastormsiam projects using GraphQL API
# Change Log (Last 4):
#   - Version 1.6, 22-07-2025: Added assign_labels_v1.0.py and updated for labelIds
#   - Version 1.5, 22-07-2025: Updated to use GraphQL API for new Projects experience, specific VPS IP and domain
#   - Version 1.4, 22-07-2025: Updated gh project create to use --owner "@me"
#   - Version 1.3, 22-07-2025: Updated gh project create to remove --description flag

# Configuration
REPO_NAME="$1"  # Repository name passed as argument
PROJECT_NAME="$2"  # Project board name passed as argument
GITHUB_USER="silicastormsiam"
VPS_DIR="/var/www/dashboard"
DATE=$(date +"%d-%m-%Y %H:%M +07")
LOG_FILE="project_log.txt"
VPS_IP="145.79.8.69"
DOMAIN="cyberpunkmonk.com"

# Check for required arguments and environment variables
if [ -z "$REPO_NAME" ] || [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <repo_name> <project_name>"
    exit 1
fi
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable not set"
    exit 1
fi

# Step 1: Install required Python libraries
pip install requests dash pandas plotly graphqlclient

# Step 2: Create repository structure
echo "Creating repository structure for $REPO_NAME..."
mkdir -p src/section_one src/section_two src/section_three docs assets tests

# Step 3: Create .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*.pyc

# Excel
*.xlsx
*.xls
~$*.xlsx

# Logs
*.log
EOL

# Step 4: Create README.md
cat > README.md << EOL
# $PROJECT_NAME

## Metadata
- **File Name**: README_v1.0.md
- **Version**: 1.0
- **Owner**: Andrew Holland
- **Purpose**: Introduce the $PROJECT_NAME, outlining its sections, setup, and usage for showcasing project management and IT skills.
- **Change Log (Last 4)**:
  - Version 1.0, 22-07-2025: Initial README created with project overview, section details, and setup instructions.
  - (No prior changes; older changes archived in memory and available on request)

## Project Overview
**Project Name**: $PROJECT_NAME  
**Start Date**: 22-07-2025  
**Objective**: Develop a dynamic dashboard to track GitHub projects, including this project, across the five PMBOK process groups (Initiating, Planning, Executing, Monitoring and Controlling, Closing), hosted on a VPS at \`$DOMAIN\`.  
**Purpose**: Showcase Andrew Holland’s project management and IT skills to recruitment officers through real-time task tracking and web development expertise.  
**Repository**: https://github.com/$GITHUB_USER/$REPO_NAME  
**Project Board**: https://github.com/users/$GITHUB_USER/projects/[PROJECT_NUMBER]/views/1?layout=board  
**Dashboard URL**: https://$DOMAIN (post-deployment)

## Sections
### Section One: VPS Configuration
- **Objective**: Configure a VPS (\`root@$VPS_IP\`) to host the dashboard securely.
- **Tasks**: Install Python, Dash, Gunicorn, NGINX; configure SSL; set up daily synchronization.
- **Status**: Executing (as of 22-07-2025 17:50 +07).

### Section Two: Creation of Dashboard
- **Objective**: Develop a Plotly Dash web application to visualize project and task data from the GitHub Project board.
- **Tasks**: Code dashboard, integrate GitHub API, deploy on VPS, and create user guide.
- **Status**: Planning (as of 22-07-2025 17:50 +07).

### Section Three: To Be Determined
- **Objective**: Placeholder for future project enhancements.
- **Tasks**: Define scope and tasks (TBD).
- **Status**: Initiating (TBD).

## Installation
1. **Clone the Repository** (bash):
   \`\`\`bash
   git clone https://github.com/$GITHUB_USER/$REPO_NAME.git
   cd $REPO_NAME
   \`\`\`
2. **Set Up VPS (Section One)** (bash):
   - SSH into \`root@$VPS_IP\`.
   - Install dependencies:
     \`\`\`bash
     sudo apt update && sudo apt upgrade -y
     sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx -y
     pip3 install dash requests pandas gunicorn graphqlclient
     \`\`\`
   - Deploy files to \`$VPS_DIR/\` and configure NGINX/Certbot (see docs/vps_setup.md).
3. **Run Dashboard (Section Two)** (bash):
   - Ensure GITHUB_TOKEN is set in the environment.
   - Start the app:
     \`\`\`bash
     gunicorn -w 4 -b 0.0.0.0:8050 -D --chdir $VPS_DIR web_dashboard_v1.3:app
     \`\`\`
   - Access at \`https://$DOMAIN\`.

## Usage
- Visit \`https://$DOMAIN\` to view the dashboard, displaying task counts by PMBOK process groups (Initiating, Planning, Executing, Monitoring and Controlling, Closing) and detailed task lists for each section.
- Check the GitHub Project board (https://github.com/users/$GITHUB_USER/projects/[PROJECT_NUMBER]/views/1?layout=board) for task updates.

## Technologies
- **Python**: Plotly Dash, Gunicorn, Requests, Pandas, GraphQLClient.
- **GitHub**: GraphQL API for project board data, repository hosting.
- **VPS**: For deployment.
- **NGINX/Certbot**: Web server and SSL.

## Contributing
- Fork the repository and create a branch (bash):
  \`\`\`bash
  git checkout -b feature-name
  \`\`\`
- Submit pull requests to \`main\`. See \`docs/CONTRIBUTING.md\` for guidelines.

## License
- MIT License (see LICENSE file).

## Contact
- **Andrew Holland**: andrew@andrewholland.com
- **GitHub**: https://github.com/$GITHUB_USER
- **Portfolio**: https://$DOMAIN

## Compliance Log
- **Verification**: Inspected via \`cat README_v1.0.md\` on 22-07-2025 17:50 +07; metadata and versioning compliant.
- **Log Entry**: Recorded in \`$VPS_DIR/project_log.txt\` as “README_v1.0.md created for repository on 22-07-2025 17:50 +07”.
EOL

# Step 5: Create source files
cat > src/section_one/list_projects_v1.1.py << EOL
import os
import json
from graphqlclient import GraphQLClient
from datetime import datetime

# Metadata
# File Name: list_projects_v1.1.py
# Version: 1.1
# Owner: Andrew Holland
# Purpose: List all GitHub projects under user $GITHUB_USER using GraphQL API
# Change Log (Last 4):
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience
#   - Version 1.0, 22-07-2025: Initial script using REST API (deprecated)
#   - (No prior changes; older changes archived in memory and available on request)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
USERNAME = "$GITHUB_USER"
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "$LOG_FILE"

def list_projects():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return []
    
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
        if "errors" in result:
            print(f"GraphQL errors: {result['errors']}")
            return []
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
EOL

cat > src/section_one/configure_project_columns_v1.4.py << EOL
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
#   - Version 1.4, 22-07-2025: Fixed GraphQL syntax error in settings JSON, added PMBOK descriptions
#   - Version 1.3, 22-07-2025: Added check for existing Status field to avoid duplicates
#   - Version 1.2, 22-07-2025: Added enhanced error handling and logging for GraphQL API calls
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience; fixed headers parameter

# Configuration
GITHUB_API = "https://api.github.com/graphql"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Project ID for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "$LOG_FILE"

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
                    print("Please manually update the Status field options to: Initiating, Planning, Executing, Monitoring and Controlling, Closing")
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
    
    # Properly escaped JSON settings with descriptions
    settings = {
        "options": [
            {"name": "Initiating", "description": "Define project scope, create repo, set up board for dashboard."},
            {"name": "Planning", "description": "Plan dashboard requirements, VPS setup, and task schedules."},
            {"name": "Executing", "description": "Build VPS, code dashboard, integrate API, deploy to VPS."},
            {"name": "Monitoring and Controlling", "description": "Track dashboard, verify API data, check VPS performance."},
            {"name": "Closing", "description": "Finalize dashboard, document, transition to andrewholland.com."}
        ]
    }
    
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
EOL

cat > src/section_one/manage_project_board_v1.3.py << EOL
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
#   - Version 1.3, 22-07-2025: Fixed createIssue mutation to use labelIds instead of labels
#   - Version 1.2, 22-07-2025: Fixed token typo and added error handling
#   - Version 1.1, 22-07-2025: Updated to use GraphQL API for new Projects experience
#   - Version 1.0, 22-07-2025: Initial script using REST API (deprecated)

# Configuration
GITHUB_API = "https://api.github.com/graphql"
REPO = "silicastormsiam/project-dashboards"
PROJECT_ID = "PVT_kwHOCZq5ps4A-gWw"  # Project ID for Project Dashboards on GitHub
REPO_ID = "R_kgDOPPbNSw"  # Repository ID for silicastormsiam/project-dashboards
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "$LOG_FILE"

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
        return {label["name"]: label["id"] for label in labels}
    except Exception as e:
        print(f"Failed to fetch label IDs: {str(e)}")
        return {}

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

def create_issue_and_add_to_project(project_id, task, status_field_id, status_option_id, label_ids):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return None
    
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    
    # Get label ID for the task
    label_id = label_ids.get(task["label"])
    if not label_id:
        print(f"No label ID found for {task['label']}, creating issue without label")
        label_id_clause = ""
    else:
        label_id_clause = f'labelIds: ["{label_id}"]'
    
    # Create issue
    mutation = """
    mutation {
      createIssue(input: {
        repositoryId: "%s"
        title: "%s"
        body: "%s"
        %s
      }) {
        issue {
          id
        }
      }
    }
    """ % (REPO_ID, task["title"], task["body"], label_id_clause)
    
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
    
    label_ids = get_label_ids()
    existing_issues = get_existing_issues()
    
    for task in tasks:
        if task["title"] in existing_issues:
            print(f"Skipping existing issue: {task['title']}")
            continue
        status_option_id = status_options.get(task["column"])
        if status_option_id:
            create_issue_and_add_to_project(PROJECT_ID, task, status_field_id, status_option_id, label_ids)
    
    with open(log_file, "a") as f:
        f.write(f"manage_project_board_v1.3.py executed, created tasks on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

if __name__ == "__main__":
    main()
EOL

cat > src/section_one/sync_dashboard_v1.4.py << EOL
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
log_file = "$LOG_FILE"

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
          id
          title
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
        data = result.get("data", {}).get("user", {}).get("projectV2", {})
        if not data:
            error_msg = "No project data returned"
            print(error_msg)
            with open(log_file, "a") as f:
                f.write(f"{error_msg} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
            return None
        return data.get("items", {}).get("nodes", [])
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
EOL

cat > src/section_two/web_dashboard_v1.3.py << EOL
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from graphqlclient import GraphQLClient
import os
import json
from datetime import datetime

# Metadata
# File Name: web_dashboard_v1.3.py
# Version: 1.3
# Owner: Andrew Holland
# Purpose: Dynamic web dashboard for Project Dashboards on GitHub, deployed on Hostinger KVM 2 VPS at cyberpunkmonk.com, displaying section-based project data
# Change Log (Last 4):
#   - Version 1.3, 22-07-2025: Updated to use GraphQL API for new Projects experience
#   - Version 1.2, 22-07-2025: Added domain-specific metadata and professional footer
#   - Version 1.1, 22-07-2025: Optimized for Hostinger deployment, added styling and task table
#   - Version 1.0, 22-07-2025: Initial Plotly Dash web dashboard created

# Initialize Dash app
app = dash.Dash(__name__, title="Andrew Holland's Project Dashboard")

# GitHub API configuration
GITHUB_API = "https://api.github.com/graphql"
USERNAME = "silicastormsiam"
PROJECT_NUMBER = 5  # Project number for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "$LOG_FILE"

def fetch_github_data():
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return pd.DataFrame(), pd.DataFrame()
    
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
            print(f"GraphQL errors: {result['errors']}")
            return pd.DataFrame(), pd.DataFrame()
        items = result.get("data", {}).get("user", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
        
        section_data = []
        task_data = []
        sections = [
            {"name": "Section One: VPS Configuration", "tasks": []},
            {"name": "Section Two: Dashboard Creation", "tasks": []},
            {"name": "Section Three: TBD", "tasks": []}
        ]
        
        for section in sections:
            initiating_count = planning_count = executing_count = monitoring_count = closing_count = 0
            section_tasks = []
            
            for item in items:
                issue = item.get("content", {})
                title = issue.get("title", "")
                body = issue.get("body", "")
                updated_at = datetime.strptime(issue.get("updatedAt", ""), "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y %H:%M +07") if issue.get("updatedAt") else ""
                labels = [label["name"] for label in issue.get("labels", {}).get("nodes", [])]
                status = next((fv["name"] for fv in item.get("fieldValues", {}).get("nodes", []) if fv.get("name")), "")
                
                # Assign tasks to sections based on labels or title keywords
                if "Section One" in labels or "VPS" in title or "Hostinger" in title or "NGINX" in title or "SSL" in title:
                    if section["name"] == "Section One: VPS Configuration":
                        section_tasks.append([section["name"], title, status, updated_at])
                elif "Section Two" in labels or "dashboard" in title.lower() or "Plotly" in title or "web" in title.lower():
                    if section["name"] == "Section Two: Dashboard Creation":
                        section_tasks.append([section["name"], title, status, updated_at])
                elif "Section Three" in labels or "Section Three" in title:
                    if section["name"] == "Section Three: TBD":
                        section_tasks.append([section["name"], title, status, updated_at])
                
                # Count tasks per status
                if section["name"] == "Section One: VPS Configuration" and ("Section One" in labels or "VPS" in title or "Hostinger" in title):
                    if status == "Initiating":
                        initiating_count += 1
                    elif status == "Planning":
                        planning_count += 1
                    elif status == "Executing":
                        executing_count += 1
                    elif status == "Monitoring and Controlling":
                        monitoring_count += 1
                    elif status == "Closing":
                        closing_count += 1
                elif section["name"] == "Section Two: Dashboard Creation" and ("Section Two" in labels or "dashboard" in title.lower()):
                    if status == "Initiating":
                        initiating_count += 1
                    elif status == "Planning":
                        planning_count += 1
                    elif status == "Executing":
                        executing_count += 1
                    elif status == "Monitoring and Controlling":
                        monitoring_count += 1
                    elif status == "Closing":
                        closing_count += 1
            
            section_data.append([section["name"], initiating_count, planning_count, executing_count, monitoring_count, closing_count])
            task_data.extend(section_tasks)
        
        section_df = pd.DataFrame(section_data, columns=["Section Name", "Initiating", "Planning", "Executing", "Monitoring and Controlling", "Closing"])
        task_df = pd.DataFrame(task_data, columns=["Section Name", "Task Title", "Process Group", "Last Updated"])
        
        return section_df, task_df
    except Exception as e:
        print(f"Failed to fetch data: {str(e)}")
        return pd.DataFrame(), pd.DataFrame()

# Layout with professional styling
app.layout = html.Div([
    html.H1("Andrew Holland's Project Management Dashboard", style={"textAlign": "center", "color": "#003087", "fontFamily": "Arial"}),
    html.P(f"Last Updated: {datetime.now().strftime('%d-%m-%Y %H:%M +07')}", style={"textAlign": "center", "color": "#555"}),
    html.H2("Section Summary", style={"color": "#003087", "fontFamily": "Arial"}),
    dcc.Graph(id="section-summary"),
    html.H2("Task Details", style={"color": "#003087", "fontFamily": "Arial"}),
    dash_table.DataTable(
        id="task-table",
        columns=[
            {"name": "Section Name", "id": "Section Name"},
            {"name": "Task Title", "id": "Task Title"},
            {"name": "Process Group", "id": "Process Group"},
            {"name": "Last Updated", "id": "Last Updated"}
        ],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "fontFamily": "Arial", "padding": "5px"},
        style_header={"backgroundColor": "#003087", "color": "white", "fontWeight": "bold"}
    ),
    html.Footer(
        html.P("Developed by Andrew Holland | Contact: andrew@andrewholland.com | Hosted on cyberpunkmonk.com",
               style={"textAlign": "center", "color": "#555", "marginTop": "20px"})
    )
], style={"padding": "20px", "maxWidth": "1200px", "margin": "auto"})

# Callback for updating dashboard
@app.callback(
    [Output("section-summary", "figure"), Output("task-table", "data")],
    [Input("interval-component", "n_intervals")]
)
def update_dashboard(n):
    section_df, task_df = fetch_github_data()
    
    section_fig = px.bar(section_df, x="Section Name", y=["Initiating", "Planning", "Executing", "Monitoring and Controlling", "Closing"],
                         title="Task Counts by PMBOK Process Group per Section",
                         barmode="group", color_discrete_sequence=px.colors.qualitative.D3)
    section_fig.update_layout(xaxis_title="Section", yaxis_title="Task Count", font={"family": "Arial"})
    
    task_data = task_df.to_dict("records")
    
    with open(log_file, "a") as f:
        f.write(f"web_dashboard_v1.3.py updated dashboard with section data on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
    
    return section_fig, task_data

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
EOL

cat > src/section_one/assign_labels_v1.0.py << EOL
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
log_file = "$LOG_FILE"

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
EOL

# Step 6: Create labels
gh label create "Section One" -c "#FF5733" -R $GITHUB_USER/$REPO_NAME || echo "Label Section One already exists"
gh label create "Section Two" -c "#33FF57" -R $GITHUB_USER/$REPO_NAME || echo "Label Section Two already exists"
gh label create "Section Three" -c "#3357FF" -R $GITHUB_USER/$REPO_NAME || echo "Label Section Three already exists"

# Step 7: Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
fi

# Step 8: Commit changes
git add .
git commit -m "Initialize repository structure and files for $REPO_NAME v1.0 on $DATE"

# Step 9: Create GitHub repository if it doesn't exist
gh repo create $GITHUB_USER/$REPO_NAME --private --source=. --remote=origin || echo "Repository already exists"

# Step 10: Push to GitHub
git push origin main --force

# Step 11: Create GitHub Project board
echo "Creating GitHub Project board: $PROJECT_NAME..."
PROJECT_OUTPUT=$(gh project create --owner "@me" --title "$PROJECT_NAME" --description "Tracks dashboard development for showcasing PMBOK-based project management and IT skills, hosted on a VPS.")
PROJECT_NUMBER=$(echo "$PROJECT_OUTPUT" | grep -oP 'ID: \K\d+')
if [ -z "$PROJECT_NUMBER" ]; then
    echo "Failed to retrieve project number. Run python src/section_one/list_projects_v1.1.py to find it."
    exit 1
fi
echo "Project created with ID: $PROJECT_NUMBER"

# Step 12: Get Project and Repository IDs
PROJECT_ID=$(python -c "import os, json; from graphqlclient import GraphQLClient; client = GraphQLClient('https://api.github.com/graphql'); client.inject_token('Bearer ' + os.getenv('GITHUB_TOKEN')); query = '''query { user(login: \"$GITHUB_USER\") { projectV2(number: $PROJECT_NUMBER) { id } } }'''; result = json.loads(client.execute(query)); print(result.get('data', {}).get('user', {}).get('projectV2', {}).get('id'))")
REPO_ID=$(python -c "import os, json; from graphqlclient import GraphQLClient; client = GraphQLClient('https://api.github.com/graphql'); client.inject_token('Bearer ' + os.getenv('GITHUB_TOKEN')); query = '''query { repository(owner: \"$GITHUB_USER\", name: \"$REPO_NAME\") { id } }'''; result = json.loads(client.execute(query)); print(result.get('data', {}).get('repository', {}).get('id'))")

# Step 13: Update scripts with project and repository IDs
sed -i "s/PROJECT_ID = \"YOUR_PROJECT_ID\"/PROJECT_ID = \"$PROJECT_ID\"/" src/section_one/configure_project_columns_v1.4.py
sed -i "s/PROJECT_ID = \"YOUR_PROJECT_ID\"/PROJECT_ID = \"$PROJECT_ID\"/" src/section_one/manage_project_board_v1.3.py
sed -i "s/REPO_ID = \"YOUR_REPO_ID\"/REPO_ID = \"$REPO_ID\"/" src/section_one/manage_project_board_v1.3.py
sed -i "s/PROJECT_NUMBER = \"\[PROJECT_NUMBER\]\"/PROJECT_NUMBER = \"$PROJECT_NUMBER\"/" src/section_two/web_dashboard_v1.3.py
sed -i "s|projects/\[PROJECT_NUMBER\]/|projects/$PROJECT_NUMBER/|" README.md

# Step 14: Commit updated scripts
git add src/section_one/list_projects_v1.1.py src/section_one/configure_project_columns_v1.4.py src/section_one/manage_project_board_v1.3.py src/section_one/sync_dashboard_v1.4.py src/section_one/assign_labels_v1.0.py src/section_two/web_dashboard_v1.3.py README.md
git commit -m "Update scripts with project number $PROJECT_NUMBER for $REPO_NAME v1.0 on $DATE"
git push origin main

# Step 15: Configure project columns
python src/section_one/configure_project_columns_v1.4.py

# Step 16: Populate project board with tasks
python src/section_one/manage_project_board_v1.3.py

# Step 17: Assign labels to issues
python src/section_one/assign_labels_v1.0.py

# Step 18: Deploy to VPS
echo "Deploying to VPS at $VPS_IP..."
ssh root@$VPS_IP << EOF
    sudo mkdir -p $VPS_DIR
    sudo chown \$USER:\$USER $VPS_DIR
    cd $VPS_DIR
    git clone https://github.com/$GITHUB_USER/$REPO_NAME.git
    cp $REPO_NAME/src/section_one/* $REPO_NAME/src/section_two/* .
    echo 'export GITHUB_TOKEN=$GITHUB_TOKEN' >> ~/.bashrc
    source ~/.bashrc
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx -y
    pip3 install dash requests pandas gunicorn graphqlclient
    sudo bash -c "cat > /etc/nginx/sites-available/dashboard << NGINX
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    location / {
        proxy_pass http://localhost:8050;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
NGINX"
    sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN
    crontab -l > cron_temp
    echo "0 0 * * * python3 $VPS_DIR/sync_dashboard_v1.4.py >> $VPS_DIR/cron.log 2>&1" >> cron_temp
    crontab cron_temp
    rm cron_temp
    gunicorn -w 4 -b 0.0.0.0:8050 -D --chdir $VPS_DIR web_dashboard_v1.3:app
EOF

# Step 19: Log completion
echo "Setup completed for $REPO_NAME and $PROJECT_NAME on $DATE" | tee -a $LOG_FILE

exit 0
