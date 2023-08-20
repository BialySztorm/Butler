import os, shutil

class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def Create():
    """
    Copy selected files to the specified build folder.
    """
    print("Copying files to build...")
    selected_files = {"Butler_github.py", "Butler_jira.py", "Butler.py", "Butler_version.txt", "README.md"}

    # Create the build folder if it doesn't exist
    if not os.path.exists("Build"):
        os.makedirs("Build")

    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join("Build", file_name)
        shutil.copy(file_path, destination_path)
    print(TColors.OKGREEN+"All files copied."+TColors.ENDC)


def Remove():
    """
    Remove the specified build folder and its contents.
    """
    print("Deleting files from build...")
    if os.path.exists("Build"):
        shutil.rmtree("Build")
    print(TColors.OKGREEN+"All files deleted."+TColors.ENDC)