import os, sys, keyboard
import requests
from Butler_github import github
from Butler_jira import jira
from Butler_build import Create, Remove
from Butler_constants import TColors, Config

# **************
# * Version
# **************

def increment_version(current_version, index_to_change):
    # Rozbij obecną wersję na części
    parts = current_version.split('.')
    
    # Sprawdź, czy podany indeks jest prawidłowy
    if 0 <= index_to_change < len(parts):
        # Zwiększ wartość na danym indeksie
        parts[index_to_change] = str(int(parts[index_to_change]) + 1)
        
        # Wyzeruj kolejne wartości po danym indeksie
        for i in range(index_to_change + 1, len(parts)):
            parts[i] = '0'
        
        # Złącz części z powrotem w nową wersję
        new_version = '.'.join(parts)
        return new_version
    else:
        return current_version  # Indeks nieprawidłowy
    

# **************
# * Platforms
# **************

def windows(currVersion, body, apps):
    #? Itch
    if "itch.io" in apps:
        os.system("butler.exe push windows "+Config["ITCH_SITE_NAME"]+":win --if-changed --userversion "+currVersion)
    #? Discord
    if "discord" in apps:
        payload = {"content":"Version: "+currVersion+" was pushed to itch on Windows channel"}        
        requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    if "github" in apps:
        github(Config["PROJECT_NAME"],currVersion,{"Windows"},body ,True,False,None)
    #? Jira
    if "jira" in apps:
        jira(currVersion, body)

def linux(currVersion, body, apps):  
    #? Itch
    if "itch.io" in apps:
        os.system("butler.exe push linux "+Config["ITCH_SITE_NAME"]+":linux --if-changed --userversion "+currVersion)
    #? Discord
    if "discord" in apps:
        payload = {"content":"Version: "+currVersion+" was pushed to itch on Linux channel"}        
        requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    if "github" in apps:
        github(Config["PROJECT_NAME"],currVersion,{"Linux"},body ,True,False,None)
    #? Jira
    if "jira" in apps:
        jira(currVersion, body)

def mac(currVersion, body, apps):
    #? Itch
    if "itch.io" in apps:
        os.system("butler push mac "+Config["ITCH_SITE_NAME"]+":mac --if-changed --userversion "+currVersion)
    #? Discord
    if "discord" in apps:
        payload = {"content":"Version: "+currVersion+" was pushed to itch on Mac channel"}        
        requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    if "github" in apps:
        github(Config["PROJECT_NAME"],currVersion,{"Mac"},body ,True,False,None)
    #? Jira
    if "jira" in apps:
        jira(currVersion, body)

def butler(currVersion, body):
    #? Github
    Create()
    github(Config["PROJECT_NAME"],currVersion,{"Build"},body ,False,False,None)
    Remove()

# **************
# * Main loop
# **************

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(menu_options, selected_index, prefix = "", suffix = "", selected_indexes = []):
    print(TColors.BOLD+"\n")
    print("  ______              _              ")
    print(" (____  \\         _  | |             ")
    print("  ____)  )_   _ _| |_| | _____  ____ ")
    print(" |  __  (| | | (_   _) || ___ |/ ___)")
    print(" | |__)  ) |_| | | |_| || ____| |    ")
    print(" |______/|____/   \\__)\\_)_____)_|    ")
    print("                        by WhiteStorm")
    print(f"{TColors.ENDC}\n\n{TColors.HEADER}{prefix}{TColors.ENDC}\n")
    for index, option in enumerate(menu_options):
        if option in selected_indexes:
            print(TColors.OKBLUE, end="")
        if index == selected_index:
            print(f"    [{index + 1}] -> {option}")
        else:
            print(f"     {index + 1}    {option}")
        print(TColors.ENDC, end="")
    print(suffix)

def main():

    if len(sys.argv)>1:
        menu_options = [
            "Butler",
            "Windows",
            "Linux",
            "Mac",
            "All at once",
            "Exit"
        ]
    else:
        menu_options = [
            "Windows",
            "Linux",
            "Mac",
            "All at once",
            "Exit"
        ]
    
    version_options = [
        "update minor",
        "update major",
        "update patch",
        "don't change",
        "go back"
    ]

    release_options = [
        "itch.io",
        "discord",
        "github",
        "jira",
        "submit",
        "go back"
    ]
    
    selected_index = 0
    selected_view = 0
    selected_platform = ""
    selected_version = ""
    selected_releases = []
    error = ""
    version = ""
    
    while True:
        clear_screen()
        if selected_view == 0:
            display_menu(menu_options, selected_index, prefix="Select platform to release on:", suffix=error)
            menu_len = len(menu_options)
        elif selected_view == 1:
            f = open(os.path.join(sys.path[0], "Butler_version.txt"),"r")
            version = f.read()
            f.close()
            display_menu(version_options, selected_index, prefix="Current Version is: v"+version, suffix=error+f"\nSelected platform: {selected_platform}")
            menu_len = len(version_options)
        elif selected_view == 2:
            display_menu(release_options, selected_index, prefix="Select app you wanna release to:", suffix=error+f"\nSelected platform: {selected_platform}, Selected version operation: {selected_version}", selected_indexes=selected_releases)
            menu_len = len(release_options)
        elif selected_view == 3:
            display_menu([], 0, suffix="Type description you wanna parse to release:", prefix=error+f"\nSelected platform: {selected_platform}, Selected version operation: {selected_version}")
        
        if selected_view<3:
            key_event = keyboard.read_event(suppress=True)
            if key_event.event_type == keyboard.KEY_DOWN:
                error=""
                if key_event.name == "w":
                    selected_index = (selected_index - 1) % menu_len
                elif key_event.name == "s":
                    selected_index = (selected_index + 1) % menu_len
                elif key_event.name == "up":
                    selected_index = (selected_index - 1) % menu_len
                elif key_event.name == "down":
                    selected_index = (selected_index + 1) % menu_len
                elif key_event.name == "enter":
                    if selected_view == 0:
                        selected_option = menu_options[selected_index]
                        selected_index = 0
                        print(f"Selected: {selected_option}")
                        if selected_option == "Exit":
                            break
                        else:
                            selected_view = 1
                            selected_platform = selected_option
                    elif selected_view == 1:
                        selected_option = version_options[selected_index]
                        selected_index = 0
                        if selected_option == "go back":
                            selected_view = 0
                            selected_version = ""
                        else:
                            selected_view = 2
                            selected_version = selected_option
                    elif selected_view == 2:
                        selected_option = release_options[selected_index]
                        if selected_option == "go back":
                            selected_index = 0
                            selected_view = 1
                            selected_releases = {}
                        elif selected_option == "submit":
                            if len(selected_releases):
                                selected_view = 3
                            else:
                                error =  TColors.WARNING+"\nApp not selected\n"+TColors.ENDC
                        else:
                            if selected_option in selected_releases:
                                selected_releases.remove(selected_option)
                            else:
                                selected_releases.append(selected_option)
        else:
            body = input()
            version = increment_version(version, version_options.index(selected_version))

            try:
                if selected_platform == "Butler":
                    butler(version,body)
                elif selected_platform == "Windows":   
                    windows(version,body,selected_releases)   
                elif selected_platform == "Linux":
                    linux(version,body,selected_releases)
                elif selected_platform == "Mac":
                    mac(version,body,selected_releases)
                elif selected_platform == "All at once":
                    windows(version,body,selected_releases)
                    linux(version,body,selected_releases)
                    mac(version,body,selected_releases)

                # save new version
                f = open(os.path.join(sys.path[0], "Butler_version.txt"),"w")
                f.write(version)
                f.close()

            except:
                print("Error when uploading")
            

            wait = input("Press enter to continue...")
            selected_index = 0
            selected_view = 0
            selected_platform = ""
            selected_version = ""
            selected_releases = []
            error = ""
                

if __name__ == "__main__":
    main()




