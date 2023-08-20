import requests, locale
from requests.auth import HTTPBasicAuth
from datetime import datetime
from Butler_constants import  TColors, Config

def get_current_date_formatted():
    current_date = datetime.now()
    
    # Ustawienie języka i lokalizacji na język urządzenia
    locale.setlocale(locale.LC_TIME, "")
    
    formatted_date = current_date.strftime("%d/%b/%Y")
    return formatted_date

def increment_version(version_string):
    try:
        major, minor, patch = map(int, version_string.split('.'))
        new_patch = patch + 1
        new_version = f"{major}.{minor}.{new_patch}"
        return new_version
    except ValueError:
        print("Invalid version format. Expected format: X.Y.Z")
        return None

def find_different_elements(list1, list2):
    unique_elements = []
    
    for item in list1:
        if item not in list2:
            unique_elements.append(item)
    
    for item in list2:
        if item not in list1:
            unique_elements.append(item)
    
    return unique_elements

def create_jira_version(base_url, project_key, api_token, version_name, version_description):
    print("Creating new jira release")
    date = get_current_date_formatted()
    # print(date)

    url = f"{base_url}/rest/api/2/version"
    payload = {
        "name": version_name,
        "project": project_key,
        "description": version_description,
        "userStartDate": date,
        "archived": False,
        "released": False
    }
    
    auth = HTTPBasicAuth("andrzejmmm1@gmail.com", api_token)
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers, auth=auth)
    
    if response.status_code == 201:
        print(TColors.OKGREEN+"Version created successfully in Jira."+TColors.ENDC)
    else:
        print(TColors.FAIL+"Failed to create new version in Jira."+TColors.ENDC)
        print(TColors.WARNING+"Response:", response.text+TColors.ENDC)
        print(TColors.WARNING+"Response code:", response.status_code+TColors.ENDC)

def update_latest_release(project_key, base_url, username, password, version_name, release_date, version_description, released=False):
    print("Updating latest jira release")
    try:
        versions_url = f"{base_url}/rest/api/2/project/{project_key}/versions"
        auth = HTTPBasicAuth(username, password)
        response = requests.get(versions_url, auth=auth)

        if response.status_code == 200:
            versions = response.json()
            
            if versions:

                released_versions = [ver for ver in versions if ver.get("released", True)]
                # print(released_versions[-1]["name"])
                not_released_versions = find_different_elements(versions, released_versions)
                if not_released_versions: 
                    latest_version = max(not_released_versions, key=lambda x: x.get("startDate", ""))
                    latest_version_id = latest_version["id"]

                    update_url = f"{base_url}/rest/api/2/version/{latest_version_id}"
                    headers = {"Content-Type": "application/json"}
                    data = {
                        "name": version_name,
                        "released": released,
                        "description": version_description,
                        "userReleaseDate":release_date
                    }

                    update_response = requests.put(update_url, json=data, headers=headers, auth=auth)
                    if update_response.status_code == 200:
                        print(TColors.OKGREEN+"Latest version updated successfully."+TColors.ENDC)
                    else:
                        print(TColors.FAIL+"Failed to update latest version."+TColors.ENDC)
                        print(TColors.WARNING+"Response:", update_response.text+TColors.ENDC)
                else:
                    print(TColors.WARNING+"No released versions found for the project."+TColors.ENDC)
            else:
                print(TColors.WARNING+"No versions found for the project."+TColors.ENDC)
        else:
            print(TColors.FAIL+"Failed to retrieve versions."+TColors.ENDC)
            print(TColors.WARNING+"Response:", response.text+TColors.ENDC)
    except Exception as e:
        print(TColors.FAIL+"An error occurred:", e+TColors.ENDC)

def get_latest_project_version(project_key, auth_username, auth_password, base_url):
    url = f"{base_url}/rest/api/2/project/{project_key}/versions"
    
    auth = HTTPBasicAuth(auth_username, auth_password)
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        versions = response.json()
        if versions:
            latest_version = max(versions, key=lambda version: version.get("startDate"))
            return latest_version
        else:
            print(TColors.WARNING+"No versions found for the project."+TColors.ENDC)
    else:
        print(TColors.FAIL+"Failed to retrieve versions for the project."+TColors.ENDC)
        print(TColors.WARNING+"Response:", response.text+TColors.ENDC)
        print(TColors.WARNING+"Response code:", response.status_code+TColors.ENDC)

def jira(version, body):
    # Wywołanie funkcji z odpowiednimi argumentami
    # print(Config)

    update_latest_release(Config["JIRA_PROJECT_KEY"],Config["JIRA_BASE_URL"],Config["JIRA_USER"],Config["JIRA_API_TOKEN"], f"v{version}", get_current_date_formatted(), body,True)

    version = increment_version(version)

    create_jira_version(
        base_url=Config["JIRA_BASE_URL"],  # Zastąp adresem swojej instancji Jira
        project_key=Config["JIRA_PROJECT_KEY"],  # Zastąp kluczem swojego projektu w Jira
        api_token=Config["JIRA_API_TOKEN"], # Twój osobisty token dostępu do API Jira
        version_name=f"v{version}-draft",  # Nazwa nowego release
        version_description="draft"  # Opis nowego release
    )
    # print(get_latest_project_version(Config["JIRA_PROJECT_KEY"], "andrzejmmm1@gmail.com", Config["JIRA_API_TOKEN"], Config["JIRA_BASE_URL"]))