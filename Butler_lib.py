import subprocess
import sys
import re
import os
import requests

# **************
# * Constants
# **************

EnvironmentFilePath = ".env"


class TColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


OsMapping = {
    "Windows": "win",
    "Linux": "linux",
    "Mac": "mac"
}

# **************
# * Functions
# **************


# * Creating files

def create_clear_data_files():
    files_to_create = {
        "Butler_version.txt": "0.0.0",
        ".env": ("JIRA_BASE_URL:=None\n"
                 "JIRA_PROJECT_KEY:=None\n"
                 "JIRA_API_TOKEN:=None\n"
                 "JIRA_USER:=None\n"
                 "ITCH_SITE_NAME:=None\n"
                 "PROJECT_NAME:=None\n"
                 "DISCORD_HOOK:=None\n"
                 "GITHUB_API_TOKEN:=None"
                 )

    }

    for filename, content in files_to_create.items():
        try:
            with open(filename, "x") as file:
                file.write(content)
            print(f"Created {filename} with initial content.")
        except FileExistsError:
            print(f"{filename} already exists. Skipping creation.")


create_clear_data_files()


# * Reading env file
def read_env_file(file_path=EnvironmentFilePath):
    """
    Read the environment file and return its contents as a dictionary.

    Parameters:
        file_path (str): Path to the environment file.

    Returns:
        dict: A dictionary containing the configuration.
    """
    Config = {}
    try:
        # skipcq: PTC-W6004
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split(":=")
                Config[key] = value
    except Exception as e:
        print(TColors.FAIL+"Error occurred when trying to open .env"+TColors.END)
        print(TColors.WARNING+f"Exception: {e}"+TColors.END)
        sys.exit(int(re.search(r'\[Errno (\d+)\]', str(e)).group(1)))
    return Config


# * Reading repository info

def get_repository_info():
    # skipcq: BAN-B607
    repo_info = subprocess.check_output(["git", "remote", "-v"], text=True).splitlines()
    for line in repo_info:
        if "origin" in line and "(fetch)" in line:
            parts = line.split()
            repo_url = parts[1]
            owner, repo_name = repo_url.split("/")[-2:]
            repo_name = repo_name.replace(".git", "")
            # skipcq: BAN-B607
            current_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            return owner, repo_name, current_commit
    return None, None


# * Data validation

def is_version_format(string):
    pattern = r"^\d+\.\d+\.\d+$"
    return re.match(pattern, string) is not None


def is_user_game_format(string):
    pattern = r"^[a-z0-9\-_]+/[a-z0-9\-_]+$"
    return re.match(pattern, string) is not None


# * Other platforms release

def discord(currVersion, DiscordHook, Platform, Apps, Body):
    try:
        payload = {"content": f"Version: {currVersion} was pushed to {', '.join(Apps)} on {Platform} channel. {Body}"}
        requests.post(DiscordHook, data=payload)
        print(TColors.OK_GREEN+"Payload sent to discord."+TColors.END)
    except Exception as e:
        print(TColors.FAIL+"Error occurred when trying to send payload to discord."+TColors.END)
        print(TColors.WARNING+f"Exception: {e}"+TColors.END)


def itch(currVersion, ItchSiteName, Platform, Directory=None):
    os_mapping = {
        "Windows": "win",
        "Linux": "linux",
        "Mac": "mac"
    }
    if not is_version_format(currVersion):
        print(TColors.WARNING+"Wrong version format"+TColors.END)
    elif not is_user_game_format(ItchSiteName):
        print(TColors.WARNING+"Wrong itch site name format"+TColors.END)
    else:
        # skipcq: BAN-B605
        os.system(f"butler push {Directory+Platform} {ItchSiteName}:{os_mapping[Platform]} --if-changed --userversion {currVersion}")
