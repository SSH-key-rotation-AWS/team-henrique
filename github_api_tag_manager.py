import requests


# Constants
BASE_URL = "https://api.github.com"
OWNER = "SSH-key-rotation-AWS"
REPO = "team-henrique"
TOKEN = "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"
CURRENT_TAG = ""

def get_latest_tag() -> str:
    '''Gets the latest tag from github so it can increment by one'''
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/tags"
    # Uses github PAT token for access
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tags = response.json()
        # Get the latest tag name
        latest_tag = tags[0]["name"]
        return latest_tag
    print(f"Error: {response.status_code} - {response.text}")
    return ""

def bump_tag():
    # Get the latest commit SHA
    commit_sha = get_latest_commit_sha()
    # Increment the tag version 
    version_parts = CURRENT_TAG.split(".")
    major, minor, patch = int(version_parts[0]), int(version_parts[1]), int(version_parts[2])
    new_tag_name = f"{major}.{minor}.{patch + 1}"
    # Create the new tag
    create_tag(new_tag_name, commit_sha)

def get_latest_commit_sha():
    '''Retrieves the latest commit sha which is needed for the Github API to get the latest tag'''
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/commits"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        # Get the latest commit SHA
        return commits[0]["sha"]
    print(f"Error: {response.status_code} - {response.text}")
    return None

def create_tag(tag_name, commit_sha):
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/git/refs"
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {
        "ref": f"refs/tags/{tag_name}",
        "sha": commit_sha
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        tag = response.json()
        print(f"Tag '{tag_name}' created successfully.")
    else:
        print(f"Error: {response.status_code} - {response.text}")
        
        
CURRENT_TAG = get_latest_tag()
bump_tag()