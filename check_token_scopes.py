import requests
import os

TOKEN = os.getenv("GITHUB_TOKEN")
headers = {"Authorization": f"Bearer {TOKEN}"}
response = requests.get("https://api.github.com/user", headers=headers)
scopes = response.headers.get("X-Oauth-Scopes", "")
print(f"Token scopes: {scopes}")
