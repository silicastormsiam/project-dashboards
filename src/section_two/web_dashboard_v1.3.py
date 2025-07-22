import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests
import os
from datetime import datetime

# Metadata
# File Name: web_dashboard_v1.3.py
# Version: 1.3
# Owner: Andrew Holland
# Purpose: Dynamic web dashboard for Project Dashboards on GitHub, deployed on Hostinger KVM 2 VPS at cyberpunkmonk.com, displaying section-based project data
# Change Log (Last 4):
#   - Version 1.3, 22-07-2025: Updated to display section-based data (VPS Configuration, Dashboard Creation, TBD)
#   - Version 1.2, 22-07-2025: Added domain-specific metadata and professional footer
#   - Version 1.1, 22-07-2025: Optimized for Hostinger deployment, added styling and task table
#   - Version 1.0, 22-07-2025: Initial Plotly Dash web dashboard created

# Initialize Dash app
app = dash.Dash(__name__, title="Andrew Holland's Project Dashboard")

# GitHub API configuration
GITHUB_API = "https://api.github.com"
USERNAME = "silicastormsiam"
PROJECT_NUMBER = "[PROJECT_NUMBER]"  # Replace with new project number
TOKEN = os.getenv("GITHUB_TOKEN")  # Load token from environment variable

def fetch_github_data():
    headers = {"Authorization": f"token {TOKEN}"}
    api_url = f"{GITHUB_API}/users/{USERNAME}/projects/{PROJECT_NUMBER}/columns"
    response = requests.get(api_url, headers=headers)
    columns = response.json()
    
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
        
        for column in columns:
            column_name = column["name"]
            cards_url = column["cards_url"]
            cards_response = requests.get(cards_url, headers=headers)
            cards = cards_response.json()
            card_count = len(cards)
            
            # Filter tasks by section (based on task title or labels)
            for card in cards:
                task_title = card.get("note", "")
                task_updated = datetime.strptime(card["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y %H:%M +07")
                if card.get("content_url"):
                    issue_response = requests.get(card["content_url"], headers=headers)
                    issue = issue_response.json()
                    task_title = issue["title"]
                    task_updated = datetime.strptime(issue["updated_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y %H:%M +07")
                
                # Assign tasks to sections based on title keywords
                if "VPS" in task_title or "Hostinger" in task_title or "NGINX" in task_title or "SSL" in task_title:
                    if section["name"] == "Section One: VPS Configuration":
                        section_tasks.append([section["name"], task_title, column_name, task_updated])
                elif "dashboard" in task_title.lower() or "Plotly" in task_title or "web" in task_title.lower():
                    if section["name"] == "Section Two: Dashboard Creation":
                        section_tasks.append([section["name"], task_title, column_name, task_updated])
                elif "Section Three" in task_title:
                    if section["name"] == "Section Three: TBD":
                        section_tasks.append([section["name"], task_title, column_name, task_updated])
            
            # Count tasks per process group
            if section["name"] == "Section One: VPS Configuration" and ("VPS" in column["name"] or "Hostinger" in column["name"]):
                if column_name == "Initiating":
                    initiating_count = card_count
                elif column_name == "Planning":
                    planning_count = card_count
                elif column_name == "Executing":
                    executing_count = card_count
                elif column_name == "Monitoring and Controlling":
                    monitoring_count = card_count
                elif column_name == "Closing":
                    closing_count = card_count
            elif section["name"] == "Section Two: Dashboard Creation" and ("dashboard" in column["name"].lower() or "Plotly" in column["name"]):
                if column_name == "Initiating":
                    initiating_count = card_count
                elif column_name == "Planning":
                    planning_count = card_count
                elif column_name == "Executing":
                    executing_count = card_count
                elif column_name == "Monitoring and Controlling":
                    monitoring_count = card_count
                elif column_name == "Closing":
                    closing_count = card_count
        
        section_data.append([section["name"], initiating_count, planning_count, executing_count, monitoring_count, closing_count])
        task_data.extend(section_tasks)
    
    section_df = pd.DataFrame(section_data, columns=["Section Name", "Initiating", "Planning", "Executing", "Monitoring and Controlling", "Closing"])
    task_df = pd.DataFrame(task_data, columns=["Section Name", "Task Title", "Process Group", "Last Updated"])
    
    return section_df, task_df

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
    
    with open("/var/www/dashboard/project_log.txt", "a") as f:
        f.write(f"web_dashboard_v1.3.py updated dashboard with section data on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
    
    return section_fig, task_data

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
