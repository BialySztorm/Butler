import os
import sys
import keyboard
import re
import Butler_build
from Butler_github import github, download_files_from_latest_release
from Butler_jira import jira
from Butler_lib import itch, discord, TColors, read_env_file


class Main:
    # Constructor method for initializing class variables
    def __init__(self):
        self._selected_index = 0
        self._selected_view = 0
        self._selected_platform = ""
        self._selected_version = ""
        self._selected_releases = []
        self._error = ""
        self._version = ""
        if len(sys.argv) > 2:
            self._menu_options = [
                "Butler",
                "Windows",
                "Linux",
                "Mac",
                "All at once",
                "Exit"
            ]
        else:
            self._menu_options = [
                "Windows",
                "Linux",
                "Mac",
                "All at once",
                "Exit"
            ]
        self._version_options = [
            "update minor",
            "update major",
            "update patch",
            "don't change",
            "go back"
        ]
        self._release_options = [
            "itch.io",
            "discord",
            "github",
            "jira",
            "submit",
            "go back"
        ]

    # Reset method to reset class variables
    def reset(self):
        self._selected_index = 0
        self._selected_view = 0
        self._selected_platform = ""
        self._selected_version = ""
        self._selected_releases = []
        self._version = ""

    # **************
    # * Version
    # **************

    # Method to increment the version based on the index
    def _increment_version(self, index_to_change):
        parts = self._version.split('.')

        if 0 <= index_to_change < len(parts):
            parts[index_to_change] = str(int(parts[index_to_change]) + 1)

            for i in range(index_to_change + 1, len(parts)):
                parts[i] = '0'

            self._version = '.'.join(parts)
        elif index_to_change != len(parts):
            print(TColors.WARNING+f"Nr: {index_to_change} is a wrong version index"+TColors.END)

    # **************
    # * Platforms
    # **************

    # Method to release a version with the specified body and platform
    def release(self, body, platform):
        Config = read_env_file()
        # ? Itch
        if "itch.io" in self._selected_releases:
            itch(self._version, Config["ITCH_SITE_NAME"], platform)
        # ? Discord
        if "discord" in self._selected_releases:
            discord(self._version, Config["DISCORD_HOOK"], platform, self._selected_releases, body)
        # ? Github
        if "github" in self._selected_releases:
            github(Config["PROJECT_NAME"], self._version, {platform}, body, True, False, None)
        # ? Jira
        if "jira" in self._selected_releases:
            jira(self._version, body)

    # Method to release a version for Butler
    def butler(self, body):
        Config = read_env_file()
        # ? Github
        if "github" in self._selected_releases:
            Butler_build.Create()
            github(Config["PROJECT_NAME"], self._version, {"Build"}, body, False, False, None)
            Butler_build.Remove()
        # ? Discord
        if "discord" in self._selected_releases:
            discord(self._version, Config["DISCORD_HOOK"], "Build", self._selected_releases, body)
        # ? Itch
        if "itch.io" in self._selected_releases:
            download_files_from_latest_release(["Butler-win.exe", "Butler-mac", "Butler-linux"], Config["GITHUB_API_TOKEN"])
            itch(self._version, Config["ITCH_SITE_NAME"], "Windows", "Build/")
            itch(self._version, Config["ITCH_SITE_NAME"], "Mac", "Build/")
            itch(self._version, Config["ITCH_SITE_NAME"], "Linux", "Build/")
            Butler_build.Remove()

    # **************
    # * UI
    # **************

    # Static method to clear the screen
    @staticmethod
    def _clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Static method to display a menu with options
    @staticmethod
    def _display_menu(menu_options, selected_index, prefix: str = None, suffix: str = None, selected_indexes=None):
        if selected_indexes is None:
            selected_indexes = []
        print(TColors.BOLD+"\n")
        print("  ______              _              ")
        print(" (____  \\         _  | |             ")
        print("  ____)  )_   _ _| |_| | _____  ____ ")
        print(" |  __  (| | | (_   _) || ___ |/ ___)")
        print(" | |__)  ) |_| | | |_| || ____| |    ")
        print(" |______/|____/   \\__)\\_)_____)_|    ")
        print("                        by WhiteStorm")
        print(f"{TColors.END}\n\n{TColors.HEADER}{prefix}{TColors.END}\n")
        # Display menu options with formatting based on selection and indices
        for index, option in enumerate(menu_options):
            if option in selected_indexes:
                print(TColors.OK_BLUE, end="")
            if index == selected_index:
                print(f"    [{index + 1}] -> {option}")
            else:
                print(f"     {index + 1}    {option}")
            print(TColors.END, end="")
        print(suffix)

    # **************
    # * Main loop
    # **************

    # Main loop of the program
    def MainLoop(self):

        while True:
            # Clear the screen
            self._clear_screen()
            # Display menu based on the selected view
            if self._selected_view == 0:
                # Display platform selection menu
                self._display_menu(self._menu_options, self._selected_index, prefix="Select platform to release on:", suffix=self._error)
                menu_len = len(self._menu_options)
            elif self._selected_view == 1:
                try:
                    # Read the current version from 'Butler_version.txt' file
                    with open("Butler_version.txt", "r") as file:
                        self._version = file.read()
                except Exception as e:
                    print(TColors.FAIL+"Error occurred when trying to open Butler_version.txt"+TColors.END)
                    print(TColors.WARNING+f"Exception: {e}"+TColors.END)
                    sys.exit(int(re.search(r'\[Errno (\d+)\]', str(e)).group(1)))
                # Display version selection menu
                self._display_menu(self._version_options, self._selected_index, prefix="Current Version is: v"+self._version, suffix=self._error+f"\nSelected platform: {self._selected_platform}")
                menu_len = len(self._version_options)
            elif self._selected_view == 2:
                # Display app release options menu
                self._display_menu(self._release_options, self._selected_index, prefix="Select app you wanna release to:", suffix=self._error +
                                   f"\nSelected platform: {self._selected_platform}, Selected version operation: {self._selected_version}", selected_indexes=self._selected_releases)
                menu_len = len(self._release_options)
            elif self._selected_view == 3:
                # Display description input menu
                self._display_menu([], 0, suffix="Type description you wanna parse to release:", prefix=self._error +
                                   f"\nSelected platform: {self._selected_platform}, Selected version operation: {self._selected_version}")

            # Handle user input for menu navigation
            if self._selected_view < 3:
                key_event = keyboard.read_event(suppress=True)
                if key_event.event_type == keyboard.KEY_DOWN:
                    self._error = ""
                    if key_event.name == "w":
                        self._selected_index = (self._selected_index - 1) % menu_len
                    elif key_event.name == "s":
                        self._selected_index = (self._selected_index + 1) % menu_len
                    elif key_event.name == "up":
                        self._selected_index = (self._selected_index - 1) % menu_len
                    elif key_event.name == "down":
                        self._selected_index = (self._selected_index + 1) % menu_len
                    elif key_event.name == "enter":
                        if self._selected_view == 0:
                            # Process platform selection
                            selected_option = self._menu_options[self._selected_index]
                            self._selected_index = 0
                            print(f"Selected: {selected_option}")
                            if selected_option == "Exit":
                                break
                            self._selected_view = 1
                            self._selected_platform = selected_option
                        elif self._selected_view == 1:
                            # Process version selection
                            selected_option = self._version_options[self._selected_index]
                            self._selected_index = 0
                            if selected_option == "go back":
                                self._selected_view = 0
                                self._selected_version = ""
                            else:
                                self._selected_view = 2
                                self._selected_version = selected_option
                        elif self._selected_view == 2:
                            # Process app release selection
                            selected_option = self._release_options[self._selected_index]
                            if selected_option == "go back":
                                self._selected_index = 0
                                self._selected_view = 1
                                self._selected_releases = []
                            elif selected_option == "submit":
                                if self._selected_releases:
                                    self._selected_view = 3
                                else:
                                    self._error = TColors.WARNING + "\nApp not selected\n" + TColors.END
                            else:
                                if selected_option in self._selected_releases:
                                    self._selected_releases.remove(selected_option)
                                else:
                                    self._selected_releases.append(selected_option)
            else:
                # Input and process description for release
                body = input()
                self._increment_version(self._version_options.index(self._selected_version))

                try:
                    # Release based on platform and version
                    if self._selected_platform == "Butler":
                        self.butler(body)
                    elif self._selected_platform in {"Windows", "Linux", "Mac"}:
                        self.release(body, self._selected_platform)
                    elif self._selected_platform == "All at once":
                        self.release(body, "Windows")
                        self.release(body, "Linux")
                        self.release(body, "Mac")

                    # Save the new version to 'Butler_version.txt' file
                    with open("Butler_version.txt", "w") as file:
                        file.write(self._version)

                except Exception as e:
                    print(TColors.FAIL+"Error when uploading"+TColors.END)
                    print(TColors.WARNING+f"Exception: {e}"+TColors.END)

                input("Press enter to continue...")
                self.reset()


# Entry point of the script
if __name__ == "__main__":
    obj = Main()
    obj.MainLoop()
