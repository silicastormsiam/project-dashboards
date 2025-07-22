def update_task_status(project_id, item_id, status_field_id, status_option_id, title):
    if not TOKEN:
        print("Error: GITHUB_TOKEN is not set")
        return False
    client = GraphQLClient(GITHUB_API)
    client.inject_token(f"Bearer {TOKEN}")
    mutation = """
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "%s",
        itemId: "%s",
        fieldId: "%s",
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
            print(f"GraphQL errors updating status for {title}: {result['errors']}")
            return False
        if result.get("data", {}).get("updateProjectV2ItemFieldValue"):
            print(f"Updated status for {title} to {status_option_id}")
            return True
        return False
    except Exception as e:
        print(f"Failed to update status for {title}: {str(e)}")
        return False
