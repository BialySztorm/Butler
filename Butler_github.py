import shutil
import requests
import os
from Butler_lib import TColors, OsMapping, read_env_file
from Butler_lib import get_repository_info
from tqdm import tqdm
import subprocess


# **************
# * Subprocesses
# **************

def create_github_release(repo_owner, repo_name, access_token, tag_name, commit, name, body, zip_paths=None, draft=True, prerelease=False, gpg_key_id=None):
    print("Creating release...")
    # Define the URL and headers for the GitHub API request
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"

    if gpg_key_id:
        sign_command = f'git commit -S -m "Release {tag_name}"'
        subprocess.run(sign_command, shell=True, check=True)

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    # Prepare data for the release request
    data = {
        "tag_name": tag_name,
        "target_commitish": commit,
        "name": name,
        "body": body,
        "draft": draft,
        "prerelease": prerelease
    }
    # Send a POST request to create the release
    response = requests.post(url, json=data, headers=headers)

    # Check the response status code and handle accordingly
    if response.status_code == 201:
        print(TColors.OK_GREEN+"Release created successfully."+TColors.END)
        if zip_paths:
            for zip_path in zip_paths:
                upload_release_asset(repo_owner, repo_name, access_token, response.json()["id"], zip_path)
    else:
        print(TColors.FAIL+"Failed to create release."+TColors.END)
        print(response.text)


# Function to check if a release with the same name exists
def check_release_exists(repo_owner, repo_name, access_token, release_name, asset_files):
    # Define the URL and headers for the GitHub API request
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    headers = {
        "Authorization": f"token {access_token}"
    }
    # Send a GET request to retrieve existing releases
    response = requests.get(url, headers=headers)

    # Check the response status code and handle accordingly
    if response.status_code == 200:
        releases = response.json()
        for release in releases:
            if release["name"] == release_name:
                release_id = release["id"]
                for asset_file in asset_files:
                    delete_release_asset(repo_owner, repo_name, access_token, release_id, asset_file)
                    upload_release_asset(repo_owner, repo_name, access_token, release_id, asset_file)
                print(f"Release with name {release_name} already exist.")
                return True
        print(TColors.WARNING+f"No release with name {release_name} found."+TColors.END)
        return False
    if response.status_code == 404:
        print(TColors.WARNING+"No release found."+TColors.END)
        return False

    print(TColors.FAIL+f"Error checking release existence: {response.status_code} - {response.text}"+TColors.END)
    return False


# Function to upload a release asset to GitHub
def upload_release_asset(repo_owner, repo_name, access_token, release_id, asset_path):
    print(f"Uploading {asset_path}...")
    # Define the URL and headers for uploading the release asset
    url = f"https://uploads.github.com/repos/{repo_owner}/{repo_name}/releases/{release_id}/assets?name={os.path.basename(asset_path)}"
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/zip"
    }
    # Get the total size of the asset for progress tracking
    total_size = os.path.getsize(asset_path)
    # Open and upload the asset file with progress tracking
    # skipcq: PTC-W6004
    with open(asset_path, "rb") as asset_file, tqdm.wrapattr(asset_file, "read", total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as asset_stream:
        response = requests.post(url, data=asset_stream, headers=headers)
    # Check the response status code and handle accordingly
    if response.status_code == 201:
        print(TColors.OK_GREEN+"Asset uploaded successfully."+TColors.END)
    else:
        print(TColors.FAIL+"Failed to upload asset."+TColors.END)
        print(response.text)


# Function to delete a release asset if it exists
def delete_release_asset(repo_owner, repo_name, access_token, release_id, asset_name):
    print("Deleting duplicated asset (if exists)...")
    # Define the URL and headers for deleting a release asset
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/{release_id}/assets"
    headers = {
        "Authorization": f"token {access_token}"
    }
    # Send a GET request to retrieve existing release assets
    response = requests.get(url, headers=headers)
    # Check the response status code and handle accordingly
    if response.status_code == 200:
        assets = response.json()
        for asset in assets:
            if asset["name"] == asset_name:
                asset_id = asset["id"]
                delete_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/assets/{asset_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 204:
                    print(TColors.OK_GREEN+f"Asset '{asset_name}' deleted successfully."+TColors.END)
                else:
                    print(TColors.FAIL+f"Failed to delete asset '{asset_name}'."+TColors.END)
                    print(delete_response.text)
                return
        print(TColors.WARNING+f"Asset '{asset_name}' not found in release."+TColors.END)
    else:
        print(TColors.FAIL+"Failed to get release assets."+TColors.END)
        print(response.text)


# Function to create a ZIP archive from specified source directories
def create_zip_archive(src_dirs, zip_path):
    zips_paths = []
    for src_dir in src_dirs:
        zip_os = OsMapping.get(src_dir, src_dir.lower())
        num_files = len(os.listdir(src_dir))
        print("Creating ZIP archive...")
        try:
            with tqdm(total=num_files, unit=" files", position=0, leave=True) as pbar:
                shutil.make_archive(zip_path+"-"+zip_os, "zip", src_dir)
                pbar.update(num_files - pbar.n)
        except Exception as e:
            print(TColors.FAIL+f"Directory {src_dir} not exists"+TColors.END)
            print(TColors.WARNING+f"Exception: {e}"+TColors.END)
            continue
        zips_paths.append(zip_path+"-"+zip_os+".zip")
        print(TColors.OK_GREEN+"ZIP archive created."+TColors.END)
    return zips_paths


# Function to delete ZIP archives
def delete_zip_archive(src_dirs):
    for file_path in src_dirs:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(TColors.OK_GREEN+f"File {file_path} has been removed."+TColors.END)
        else:
            print(TColors.WARNING+f"File {file_path} does not exist."+TColors.END)


# **************
# * Main function
# **************

def github(project_name: str, version: str, platforms: list[str], body="", draft=True, prerelease=False, commit: str = None, access_token=read_env_file()["GITHUB_API_TOKEN"], gpg_key=read_env_file()["GPG_KEY_ID"]):
    """
    Manage github releases.

    Parameters:
        project_name (str): Name of project
        version (str): version of release
        platforms list(str): List of platforms to add assets
        body (str): body of release
        draft (bool): Add as release?
        prerelease (bool): Add as prerelease?
        commit (str): commit or branch id
        access_token (str): string with access token
        gpg_key (str): GPG key to add
    """
    repo_owner, repo_name, current_commit = get_repository_info()
    if not repo_owner or not repo_name:
        print(TColors.FAIL+"Failed to get repository information."+TColors.END)
        return

    if commit:
        current_commit = commit

    # access_token = get_access_token(TokenPath)
    # print(access_token)

    zips_paths = create_zip_archive(platforms, project_name)
    print("Created files: "+", ".join(zips_paths))
    if not check_release_exists(repo_owner, repo_name, access_token, "v"+version, zips_paths):
        create_github_release(repo_owner, repo_name, access_token, "v"+version, current_commit, "v"+version, body, zips_paths, draft, prerelease)
    print("Tidying up...")
    delete_zip_archive(zips_paths)
    print(TColors.OK_GREEN+"Github stuff is Done!"+TColors.END)


def download_files_from_latest_release(selected_files: list[str], access_token: str = None):
    """
    Download files from the latest release.

    Parameters:
        selected_files (list(str)): List of files to download
        access_token (str): GitHub access token
    """
    # Get repository information
    repo_owner, repo_name, current_commit = get_repository_info()
    if not repo_owner or not repo_name:
        print(TColors.FAIL+"Failed to get repository information."+TColors.END)
        return
    # Get the latest release information
    releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    # Add the access token to the headers if it exists and get response
    if access_token:
        headers["Authorization"] = f"token {access_token}"
    response = requests.get(releases_url, headers=headers)

    if response.status_code != 200:
        print(TColors.FAIL+f"Failed to fetch the latest release information."+TColors.END)
        print(TColors.WARNING+f" Status code: {response.status_code}"+TColors.END)
        return
    # Get the assets from the response
    assets = response.json().get("assets", [])
    # Download the selected files
    for asset in assets:
        file_name = asset["name"]
        if file_name in selected_files:
            # Determine the destination directory based on the file name
            if "win" in file_name.lower():
                destination_dir = "Build/Windows"
            elif "linux" in file_name.lower():
                destination_dir = "Build/Linux"
            elif "mac" in file_name.lower():
                destination_dir = "Build/Mac"
            else:
                destination_dir = "Build/Other"
            download_path = os.path.join(destination_dir, file_name)
            print(f"Downloading {file_name} to {download_path}")
            # Download the file with progress tracking
            try:
                with requests.get(asset["browser_download_url"], stream=True) as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get('content-length', 0))
                    os.makedirs(destination_dir, exist_ok=True)

                    with open(download_path, 'wb') as file, tqdm(
                        desc=file_name,
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as progress_bar:
                        for data in response.iter_content(chunk_size=1024):
                            file.write(data)
                            progress_bar.update(len(data))
                    print(TColors.OK_GREEN+f"Downloaded {file_name}"+TColors.END)
            except Exception as e:
                print(TColors.FAIL+f"Failed to download {file_name}."+TColors.END)
                print(TColors.WARNING+f"Exception: {e}"+TColors.END)


# * Test run
# github("Familiada", "1.0.3", {"Windows"})
