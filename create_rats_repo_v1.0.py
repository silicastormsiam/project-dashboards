import os
from github import Github
from datetime import datetime

# Metadata
# File Name: create_rats_repo_v1.0.py
# Version: 1.0
# Owner: Andrew John Holland
# Purpose: Create the silicastormsiam/rats repository on GitHub
# Change Log (Last 4):
#   - Version 1.0, 23-07-2025: Initial script to create RATS repository

# Configuration
GITHUB_TOKEN = "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"
REPO_NAME = "rats"
ORG_NAME = "silicastormsiam"
log_file = "project_log.txt"

def create_repository(client, org_name, repo_name):
    try:
        user = client.get_user()
        if user.login == org_name:
            repo = user.create_repo(
                name=repo_name,
                description="RATS - Recruitment Application Tracking System for SilicaStormSiam",
                private=False,
                auto_init=True,
                license_template="mit"
            )
            print(f"Created repository: {org_name}/{repo_name}")
            with open(log_file, "a") as f:
                f.write(f"Created repository: {org_name}/{repo_name} on {datetime.now().strftime('%d-%m-%Y %H:%M +07')}\n")
            return repo
        else:
            print(f"Error: Authenticated user {user.login} does not match {org_name}")
            return None
    except Exception as e:
        print(f"Failed to create repository: {str(e)}")
        return None

def main():
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return
    client = Github(GITHUB_TOKEN)
    repo = create_repository(client, ORG_NAME, REPO_NAME)
    if repo:
        print(f"Repository {ORG_NAME}/{REPO_NAME} created successfully")
    else:
        print(f"Failed to create repository {ORG_NAME}/{REPO_NAME}")

if __name__ == "__main__":
    main()
