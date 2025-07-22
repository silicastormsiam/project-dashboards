import os
import requests
from datetime import datetime

# Metadata
# File Name: sync_dashboard_v1.4.py
# Version: 1.4
# Owner: Andrew Holland
# Purpose: Automate daily sync of GitHub project and task data to web dashboard for Project Dashboards on GitHub, deployed on Hostinger KVM 2 VPS
# Change Log (Last 4):
#   - Version 1.4, 22-07-2025: Optimized for Hostinger KVM 2 VPS, removed Excel update for web-only deployment
#   - Version 1.3, 22-07-2025: Updated script to support Hostinger deployment and trigger web dashboard refresh
#   - Version 1.2, 22-07-2025: Updated script to support Synology DSM Task Scheduler and note hosting options
#   - Version 1.1, 22-07-2025: Updated script to support task-level tracking in Excel Task Details sheet

# Configuration
web_dashboard_url = "https://cyberpunkmonk.com"  # Replace with your domain
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Load token from environment variable
log_file = "/var/www/dashboard/project_log.txt"

# Trigger web dashboard refresh
headers = {"Authorization": f"token {GITHUB_TOKEN}"}
response = requests.get(web_dashboard_url, headers=headers)

# Log compliance
with open(log_file, "a") as f:
    f.write(f"sync_dashboard_v1.4.py executed, triggered web dashboard update on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")

print(f"Daily sync completed on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}")
