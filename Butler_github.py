import shutil
import requests
import os
from Butler_constants import TColors, OsMapping, Config
from Butler_lib import get_repository_info
from tqdm import tqdm


# **************
# * Subprocesses
# **************

def create_github_release(repo_owner, repo_name, access_token, tag_name, commit, name, body, zip_paths=None, draft=True, prerelease=False):
    print("Creating release...")
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "tag_name": tag_name,
        "target_commitish": commit,
        "name": name,
        "body": body,
        "draft": draft,
        "prerelease": prerelease
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print(TColors.OKGREEN+"Release created successfully."+TColors.ENDC)
        if zip_paths:
            for zip_path in zip_paths:
                upload_release_asset(repo_owner, repo_name, access_token, response.json()["id"], zip_path)
    else:
        print(TColors.FAIL+"Failed to create release."+TColors.ENDC)
        print(response.text)


def check_release_exists(repo_owner, repo_name, access_token, release_name, asset_files):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases"
    headers = {
        "Authorization": f"token {access_token}"
    }

    response = requests.get(url, headers=headers)

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
        print(TColors.WARNING+f"No release with name {release_name} found."+TColors.ENDC)
        return False
    elif response.status_code == 404:
        print(TColors.WARNING+"No release found."+TColors.ENDC)
        return False
    else:
        print(TColors.FAIL+f"Error checking release existence: {response.status_code} - {response.text}"+TColors.ENDC)
        return False


def upload_release_asset(repo_owner, repo_name, access_token, release_id, asset_path):
    print(f"Uploading {asset_path}...")
    url = f"https://uploads.github.com/repos/{repo_owner}/{repo_name}/releases/{release_id}/assets?name={os.path.basename(asset_path)}"
    headers = {
        "Authorization": f"token {access_token}",
        "Content-Type": "application/zip"
    }

    total_size = os.path.getsize(asset_path)
    with open(asset_path, "rb") as asset_file, tqdm.wrapattr(asset_file, "read", total=total_size, unit="B", unit_scale=True, unit_divisor=1024) as asset_stream:
        response = requests.post(url, data=asset_stream, headers=headers)
        pbar.update(total_size - pbar.n)  # Set progress to 100% at the end
    if response.status_code == 201:
        print(TColors.OKGREEN+"Asset uploaded successfully."+TColors.ENDC)
    else:
        print(TColors.FAIL+"Failed to upload asset."+TColors.ENDC)
        print(response.text)


def delete_release_asset(repo_owner, repo_name, access_token, release_id, asset_name):
    print("Deleting duplicated asset (if exists)...")
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/{release_id}/assets"
    headers = {
        "Authorization": f"token {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assets = response.json()
        for asset in assets:
            if asset["name"] == asset_name:
                asset_id = asset["id"]
                delete_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/assets/{asset_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 204:
                    print(TColors.OKGREEN+f"Asset '{asset_name}' deleted successfully."+TColors.ENDC)
                else:
                    print(TColors.FAIL+f"Failed to delete asset '{asset_name}'."+TColors.ENDC)
                    print(delete_response.text)
                return
        print(TColors.WARNING+f"Asset '{asset_name}' not found in release."+TColors.ENDC)
    else:
        print(TColors.FAIL+"Failed to get release assets."+TColors.ENDC)
        print(response.text)


def create_zip_archive(src_dirs, zip_path):
    zips_paths = []
    for src_dir in src_dirs:
        if src_dir.lower() in OsMapping:
            zip_os = OsMapping[src_dir.lower()]
        else:
            zip_os = src_dir.lower()
        num_files = len(os.listdir(src_dir))
        print("Creating ZIP archive...")
        try:
            with tqdm(total=num_files, unit=" files", position=0, leave=True) as pbar:
                shutil.make_archive(zip_path+"-"+zip_os, "zip", src_dir)
                pbar.update(num_files - pbar.n)
        except:
            print(TColors.FAIL+f"Directory {src_dir} not exists"+TColors.ENDC)
            continue
        zips_paths.append(zip_path+"-"+zip_os+".zip")
        print(TColors.OKGREEN+"ZIP archive created."+TColors.ENDC)
    return zips_paths


def delete_zip_archive(src_dirs):
    for file_path in src_dirs:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(TColors.OKGREEN+f"File {file_path} has been removed."+TColors.ENDC)
        else:
            print(TColors.WARNING+f"File {file_path} does not exist."+TColors.ENDC)


# **************
# * Main function
# **************

def github(ProjectName: str, Version: str, Platforms: list[str], Body="", Draft=True, Prerelease=False, Commit: str = None, access_token=Config["GITHUB_API_TOKEN"]):
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
        print(TColors.FAIL+"Failed to get repository information."+TColors.ENDC)
        return

    if Commit:
        current_commit = Commit

    # access_token = get_access_token(TokenPath)
    # print(access_token)

    zips_paths = create_zip_archive(Platforms, ProjectName)
    print("Created files: "+", ".join(zips_paths))
    if not check_release_exists(repo_owner, repo_name, access_token, "v"+Version, zips_paths):
        create_github_release(repo_owner, repo_name, access_token, "v"+Version, current_commit, "v"+Version, Body, zips_paths, Draft, Prerelease)
    print("Tidying up...")
    delete_zip_archive(zips_paths)
    print(TColors.OKGREEN+"Github stuff is Done!"+TColors.ENDC)


# * Test run
# github("Familiada", "1.0.3", {"Windows"})
