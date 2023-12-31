import os
import shutil
from Butler_lib import TColors


# * Create build dir and copy needed files
def Create():
    """
    Copy selected files to the specified build folder.
    """
    print("Copying files to build...")
    selected_files = {"Butler_github.py", "Butler_jira.py", "Butler.py", "Butler_lib.py", "README.md"}

    # Create the build folder if it doesn't exist, else delete the current one and make empty
    if not os.path.exists("Build"):
        os.makedirs("Build")
    else:
        shutil.rmtree("Build")
        os.makedirs("Build")

    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join("Build", file_name)
        shutil.copy(file_path, destination_path)
    print(TColors.OK_GREEN+"All files copied."+TColors.END)


# * delete build files
def Remove():
    """
    Remove the specified build folder and its contents.
    """
    print("Deleting files from build...")
    if os.path.exists("Build"):
        shutil.rmtree("Build")
    print(TColors.OK_GREEN+"All files deleted."+TColors.END)
