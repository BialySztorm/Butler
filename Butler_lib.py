import subprocess
import sys, re

# **************
# * Functions
# **************

# * Reading env file

def read_env_file(file_path):
    """
    Read the Jira environment file and return its contents as a dictionary.

    Parameters:
        file_path (str): Path to the Jira environment file.

    Returns:
        dict: A dictionary containing the Jira configuration.
    """
    Config = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split(":=")
                Config[key] = value
    except Exception as e:
        print('\033[91m'+"Error occurred when trying to open .env"+'\033[0m')
        print('\033[93m'+f"Exception: {e}"+'\033[0m')
        sys.exit(int(re.search(r'\[Errno (\d+)\]', str(e)).group(1)))
    return Config

# * Reading repository info

def get_repository_info():
    repo_info = subprocess.check_output(["git", "remote", "-v"], text=True).splitlines()
    for line in repo_info:
        if "origin" in line and "(fetch)" in line:
            parts = line.split()
            repo_url = parts[1]
            owner, repo_name = repo_url.split("/")[-2:]
            repo_name = repo_name.replace(".git", "")
            current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            return owner, repo_name, current_commit
    return None, None

# * Creting files

def create_clear_data_files():
    files_to_create = {
        "Butler_version.txt": "0.0.0",
        ".env": """JIRA_BASE_URL:= 
JIRA_PROJECT_KEY:= 
JIRA_API_TOKEN:= 
JIRA_USER:= 
ITCH_SITE_NAME:= 
PROJECT_NAME:= 
DISCORD_HOOK:= 
GITHUB_API_TOKEN:= """
    }
    
    for filename, content in files_to_create.items():
        try:
            with open(filename, "x") as file:
                file.write(content)
            print(f"Created {filename} with initial content.")
        except FileExistsError:
            print(f"{filename} already exists. Skipping creation.")

create_clear_data_files()