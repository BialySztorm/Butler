import os
import sys
import keyboard
import re
import Butler_build
from Butler_github import github
from Butler_jira import jira
from Butler_lib import itch, discord, TColors, read_env_file


class Main:

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

    def _increment_version(self, index_to_change):
        # Rozbij obecną wersję na części
        parts = self._version.split('.')

        # Sprawdź, czy podany indeks jest prawidłowy
        if 0 <= index_to_change < len(parts):
            # Zwiększ wartość na danym indeksie
            parts[index_to_change] = str(int(parts[index_to_change]) + 1)

            # Wyzeruj kolejne wartości po danym indeksie
            for i in range(index_to_change + 1, len(parts)):
                parts[i] = '0'

            # Złącz części z powrotem w nową wersję
            self._version = '.'.join(parts)
        else:
            print(TColors.WARNING+f"Nr: {index_to_change} is a wrong version index"+TColors.END)

    # **************
    # * Platforms
    # **************

    def release(self, currVersion, body, apps, platform):
        Config = read_env_file()
        # ? Itch
        if "itch.io" in apps:
            itch(currVersion, Config["ITCH_SITE_NAME"], platform)
        # ? Discord
        if "discord" in apps:
            discord(currVersion, Config["DISCORD_HOOK"], platform, apps, body)
        # ? Github
        if "github" in apps:
            github(Config["PROJECT_NAME"], currVersion, {platform}, body, True, False, None)
        # ? Jira
        if "jira" in apps:
            jira(currVersion, body)

    def butler(self, currVersion, body):
        Config = read_env_file()
        # ? Github
        Butler_build.Create()
        github(Config["PROJECT_NAME"], currVersion, {"Build"}, body, False, False, None)
        Butler_build.Remove()

    # **************
    # * UI
    # **************

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _display_menu(self, menu_options, selected_index, prefix=None, suffix=None, selected_indexes=None):
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

    def MainLoop(self):

        while True:
            self._clear_screen()
            if self._selected_view == 0:
                self._display_menu(self._menu_options, self._selected_index, prefix="Select platform to release on:", suffix=self._error)
                menu_len = len(self._menu_options)
            elif self._selected_view == 1:
                try:
                    with open("Butler_version.txt", "r") as file:
                        self._version = file.read()
                except Exception as e:
                    print(TColors.FAIL+"Error occurred when trying to open Butler_version.txt"+TColors.END)
                    print(TColors.WARNING+f"Exception: {e}"+TColors.END)
                    sys.exit(int(re.search(r'\[Errno (\d+)\]', str(e)).group(1)))
                self._display_menu(self._version_options, self._selected_index, prefix="Current Version is: v"+self._version, suffix=self._error+f"\nSelected platform: {self._selected_platform}")
                menu_len = len(self._version_options)
            elif self._selected_view == 2:
                self._display_menu(self._release_options, self._selected_index, prefix="Select app you wanna release to:", suffix=self._error +
                                   f"\nSelected platform: {self._selected_platform}, Selected version operation: {self._selected_version}", selected_indexes=self._selected_releases)
                menu_len = len(self._release_options)
            elif self._selected_view == 3:
                self._display_menu([], 0, suffix="Type description you wanna parse to release:", prefix=self._error +
                                   f"\nSelected platform: {self._selected_platform}, Selected version operation: {self._selected_version}")

            if self._selected_view < 3:
                key_event = keyboard.read_event(suppress=True)
                if key_event.event_type == keyboard.KEY_DOWN:
                    self.error = ""
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
                            selected_option = self._menu_options[self._selected_index]
                            self._selected_index = 0
                            print(f"Selected: {selected_option}")
                            if selected_option == "Exit":
                                break
                            self._selected_view = 1
                            self._selected_platform = selected_option
                        elif self._selected_view == 1:
                            selected_option = self._version_options[self._selected_index]
                            self._selected_index = 0
                            if selected_option == "go back":
                                self._selected_view = 0
                                self._selected_version = ""
                            else:
                                self._selected_view = 2
                                self._selected_version = selected_option
                        elif self._selected_view == 2:
                            selected_option = self._release_options[self._selected_index]
                            if selected_option == "go back":
                                self._selected_index = 0
                                self._selected_view = 1
                                self._selected_releases = []
                            elif selected_option == "submit":
                                if self._selected_releases:
                                    self._selected_view = 3
                                else:
                                    error = TColors.WARNING + "\nApp not selected\n" + TColors.END
                            else:
                                if selected_option in self._selected_releases:
                                    self._selected_releases.remove(selected_option)
                                else:
                                    self._selected_releases.append(selected_option)
            else:
                body = input()
                self._increment_version(self._version_options.index(self._selected_version))

                try:
                    if self._selected_platform == "Butler":
                        self.butler(self._version, body)
                    elif self._selected_platform in {"Windows", "Linux", "Mac"}:
                        self.release(self._version, body, self._selected_releases, self._selected_platform)
                    elif self._selected_platform == "All at once":
                        self.release(self._version, body, self._selected_releases, "Windows")
                        self.release(self._version, body, self._selected_releases, "Linux")
                        self.release(self._version, body, self._selected_releases, "Mac")

                    # save new version
                    with open("Butler_version.txt", "w") as file:
                        file.write(self._version)

                except Exception as e:
                    print(TColors.FAIL+"Error when uploading"+TColors.END)
                    print(TColors.WARNING+f"Exception: {e}"+TColors.END)

                input("Press enter to continue...")
                self.reset()


if __name__ == "__main__":
    obj = Main()
    obj.MainLoop()
