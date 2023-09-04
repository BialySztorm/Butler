import shutil
import requests
import os
from Butler_lib import TColors, OsMapping, read_env_file
from Butler_lib import get_repository_info
from tqdm import tqdm


# **************
# * Subprocesses
# **************

# Function to create a GitHub release
def create_github_release(repo_owner, repo_name, access_token, tag_name, commit, name, body, zip_paths=None, draft=True, prerelease=False):
    print("Creating release...")
    # Define the URL and headers for the GitHub API request
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
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

def github(ProjectName: str, Version: str, Platforms: list[str], Body="", Draft=True, Prerelease=False, Commit: str = None, access_token=read_env_file()["GITHUB_API_TOKEN"]):
    """
    Manage github releases.

    Parameters:
        ProjectName (str): Name of project
        Version (str): Version of release
        Platforms list(str): List of platforms to add assets
        Body (str): Body of release
        Draft (bool): Add as release?
        Prerelease (bool): Add as prerelease?
        Commit (str): Commit or branch id
        TokenPath (str): Path to github token
    """
    repo_owner, repo_name, current_commit = get_repository_info()
    if not repo_owner or not repo_name:
        print(TColors.FAIL+"Failed to get repository information."+TColors.END)
        return

    if Commit:
        current_commit = Commit

    zips_paths = create_zip_archive(Platforms, ProjectName)
    print("Created files: "+", ".join(zips_paths))
    if not check_release_exists(repo_owner, repo_name, access_token, "v"+Version, zips_paths):
        create_github_release(repo_owner, repo_name, access_token, "v"+Version, current_commit, "v"+Version, Body, zips_paths, Draft, Prerelease)
    print("Tidying up...")
    delete_zip_archive(zips_paths)
    print(TColors.OK_GREEN+"Github stuff is Done!"+TColors.END)


# * Test run
# github("Familiada", "1.0.3", {"Windows"})
