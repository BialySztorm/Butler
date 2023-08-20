import subprocess

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
    with open(file_path, "r") as file:
        for line in file:
            key, value = line.strip().split(":=")
            Config[key] = value
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
