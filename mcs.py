# @AaghaFazal
# pkg install python
# pip install requests

import requests
import time

# Set your GitHub personal access token here
GITHUB_TOKEN = "Set your GitHub personal access token here"

# GitHub API URL for Codespaces
API_URL = "https://api.github.com/user/codespaces"

# Headers for authentication
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_codespaces():
    """Fetch the list of Codespaces and their statuses."""
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        return response.json().get("codespaces", [])  # Get the list of codespaces
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Codespaces: {e}")
        return []

def start_codespace(name):
    """Start a specific Codespace by its name."""
    start_url = f"{API_URL}/{name}/start"
    try:
        response = requests.post(start_url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        print(f"Codespace {name} started successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to start Codespace {name}: {e}")

def manage_codespaces():
    """Check Codespaces' statuses and restart if necessary."""
    while True:
        codespaces = get_codespaces()

        if not isinstance(codespaces, list):
            print("Error: Expected a list of Codespaces but got something else.")
            return

        if not codespaces:
            print("No Codespaces found or unable to fetch.")
            return

        for codespace in codespaces:
            if isinstance(codespace, dict):
                name = codespace.get("name")
                state = codespace.get("state")

                if name and state:
                    print(f"Codespace: {name}, Status: {state}")

                    # If the state is shutdown or stopped, start the Codespace
                    if state.lower() in ["shutdown", "stopped"]:
                        print(f"Codespace {name} is offline. Starting it...")
                        start_codespace(name)
                    else:
                        print(f"Codespace {name} is already running.")
                else:
                    print(f"Error: Missing name or state for a Codespace: {codespace}")
            else:
                print(f"Error: Unexpected item in the response: {codespace}")

        # Wait for 60 seconds before checking again
        time.sleep(60)

if __name__ == "__main__":
    manage_codespaces()
