import os
import json
from graphqlclient import GraphQLClient

# Configuration
GITHUB_API = "https://api.github.com/graphql"
USERNAME = "silicastormsiam"
PROJECT_NUMBER = 5
TOKEN = os.getenv("GITHUB_TOKEN")

client = GraphQLClient(GITHUB_API)
client.inject_token(f"Bearer {TOKEN}")

query = """
query {
  user(login: "%s") {
    projectV2(number: %s) {
      id
      title
      items(first: 10) {
        nodes {
          content {
            ... on Issue {
              title
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
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {str(e)}")
