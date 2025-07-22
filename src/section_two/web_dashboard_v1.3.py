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
PROJECT_NUMBER = "5"  # Project number for Project Dashboards on GitHub
TOKEN = os.getenv("GITHUB_TOKEN")
log_file = "project_log.txt"  # Adjusted for local execution; update to /var/www/dashboard on VPS

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
