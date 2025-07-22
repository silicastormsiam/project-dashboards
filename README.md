Project Dashboards on GitHub
Metadata

File Name: README_v1.1.md
Version: 1.1
Owner: Andrew Holland
Purpose: Introduce the Project Dashboards on GitHub, outlining its sections, setup, and usage for showcasing project management and IT skills.
Change Log (Last 4):
Version 1.1, 22-07-2025: Updated formatting for clarity and consistency.
Version 1.0, 22-07-2025: Initial README created with project overview, section details, and setup instructions.
(No prior changes; older changes archived in memory and available on request)



Project Overview
Project Name: Project Dashboards on GitHubStart Date: 22-07-2025Objective: Develop a dynamic dashboard to track GitHub projects, including this project, across the five PMBOK process groups (Initiating, Planning, Executing, Monitoring and Controlling, Closing), hosted on a Hostinger KVM 2 VPS at cyberpunkmonk.com (transitioning to andrewholland.com).Purpose: Showcase Andrew Holland’s project management and IT skills to recruitment officers through real-time task tracking and web development expertise.Repository: https://github.com/silicastormsiam/project-dashboardsProject Board: https://github.com/users/silicastormsiam/projects/[PROJECT_NUMBER]/views/1?layout=board (to be created)Dashboard URL: https://cyberpunkmonk.com (post-deployment)
Sections
Section One: Configuration of Hostinger.com VPS KVM 2

Objective: Configure a Hostinger KVM 2 VPS (root@145.79.8.69) to host the dashboard securely.
Tasks: Install Python, Dash, Gunicorn, NGINX; configure SSL; set up daily synchronization.
Status: Executing (as of 22-07-2025 11:36 +07).

Section Two: Creation of Dashboard

Objective: Develop a Plotly Dash web application to visualize project and task data from the GitHub Project board.
Tasks: Code dashboard, integrate GitHub API, deploy on VPS, and create user guide.
Status: Planning (as of 22-07-2025 11:36 +07).

Section Three: To Be Determined

Objective: Placeholder for future project enhancements.
Tasks: Define scope and tasks (TBD).
Status: Initiating (TBD).

Installation

Clone the Repository (bash):git clone https://github.com/silicastormsiam/project-dashboards.git
cd project-dashboards


Set Up VPS (Section One) (bash):
SSH into root@145.79.8.69.
Install dependencies:sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip nginx certbot python3-certbot-nginx -y
pip3 install dash requests pandas gunicorn


Deploy files to /var/www/dashboard/ and configure NGINX/Certbot (see docs/vps_setup.md).


Run Dashboard (Section Two) (bash):
Update GitHub token in src/section_two/web_dashboard_v1.3.py.
Start the app:gunicorn -w 4 -b 0.0.0.0:8050 -D --chdir /var/www/dashboard web_dashboard_v1.3:app


Access at https://cyberpunkmonk.com.



Usage

Visit https://cyberpunkmonk.com to view the dashboard, displaying task counts by PMBOK process group and detailed task lists for each section.
Check the GitHub Project board (https://github.com/users/silicastormsiam/projects/[PROJECT_NUMBER]/views/1?layout=board) for task updates.

Technologies

Python: Plotly Dash, Gunicorn, Requests, Pandas.
GitHub: API for project board data, repository hosting.
Hostinger: KVM 2 VPS for deployment.
NGINX/Certbot: Web server and SSL.

Contributing

Fork the repository and create a branch (bash):git checkout -b feature-name


Submit pull requests to main. See docs/CONTRIBUTING.md for guidelines.

License

MIT License (see LICENSE file).

Contact

Andrew Holland: andrew@andrewholland.com
GitHub: https://github.com/silicastormsiam
Portfolio: https://cyberpunkmonk.com (transitioning to https://andrewholland.com)

Compliance Log

Verification: Inspected via cat README_v1.1.md on 22-07-2025 11:36 +07; metadata and versioning compliant.
Log Entry: Recorded in /var/www/dashboard/project_log.txt as “README_v1.1.md updated with corrected formatting on 22-07-2025 11:36 +07”.
