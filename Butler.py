import os, sys
import requests
from Butler_github import github
from Butler_jira import jira
# from Butler_build import Create, Remove
from Butler_constants import TColors, Config

# **************
# * Version
# **************

def version():
    f = open(os.path.join(sys.path[0], "Butler_version.txt"),"r")
    currVersion = f.read()
    print(TColors.HEADER+"Current version is: ",currVersion,"\n"+TColors.ENDC)
    print("[1] - update minor")
    print("[2] - update major")
    print("[3] - update patch")
    print("[0] - don't change\n")
    action = input("Type Option: ")
    print("\n")
    if action == '1':
        tmp = currVersion.split('.')
        tmp[0]=str(int(tmp[0])+1)
        currVersion = tmp[0]+".0.0"
    elif action == '2':
        tmp = currVersion.split('.')
        tmp[1]=str(int(tmp[1])+1)
        currVersion = tmp[0]+"."+tmp[1]+".0"
    elif action == '3':
        tmp = currVersion.split('.')
        tmp[2]=str(int(tmp[2])+1)
        currVersion = tmp[0]+"."+tmp[1]+"."+tmp[2]
    elif action != '0':
        return -1
    f.close()
    f = open(os.path.join(sys.path[0], "Butler_version.txt"),"w")
    f.write(currVersion)
    f.close()
    return currVersion
    

# **************
# * Platforms
# **************

def platform():
    print(TColors.HEADER+"Select platform for push build to\n"+TColors.ENDC)
    print("[1] - Windows")
    print("[2] - Linux")
    print("[3] - Mac")
    print("[4] - All at once")
    print("[0] - Exit")
    action = input("Type Option: ")
    return action
        


def windows(currVersion, body):
    #? Itch
    os.system("butler.exe push windows "+Config["ITCH_SITE_NAME"]+":win --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Windows channel"}        
    requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    github(Config["PROJECT_NAME"],currVersion,{"Windows"},body ,True,False,None)
    #? Jira
    jira(currVersion, body)

def linux(currVersion, body):  
    #? Itch
    os.system("butler.exe push linux "+Config["ITCH_SITE_NAME"]+":linux --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Linux channel"}        
    requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    github(Config["PROJECT_NAME"],currVersion,{"Linux"},body ,True,False,None)
    #? Jira
    jira(currVersion, body)

def mac(currVersion, body):
    #? Itch
    os.system("butler push mac "+Config["ITCH_SITE_NAME"]+":mac --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Mac channel"}        
    requests.post(Config["DISCORD_HOOK"], data=payload)
    #? Github
    github(Config["PROJECT_NAME"],currVersion,{"Mac"},body ,True,False,None)
    #? Jira
    jira(currVersion, body)

# def butler(currVersion, body):
#     #? Github
#     Create()
#     github(ProjectName,currVersion,{"Build"},body ,False,False,None,TokenPath)
#     Remove()

# **************
# * Main loop
# **************

if __name__ == "__main__":
    action = '-1'
    while(action!='0'):
        action = platform()
        if action == '0':
            continue
        body = input("Write text for release body:\n")
        # body = ""
        print("\n")
        if action == '1':
            windows(version(), body)
        elif action == '2':
            linux(version(), body) 
        elif action == '3':
            mac(version(), body)
        elif action == '4':
            windows(version(), body)
            linux(version(), body) 
            mac(version(), body)
        # elif action == '5':
        #     wait = input(TColors.WARNING+"Comment butler code then press Enter to continue."+TColors.ENDC)
        #     butler(version(), body)
        else:
            print(TColors.WARNING+"Wrong option"+TColors.ENDC)
        # print(version())
        wait = input(TColors.OKBLUE+"Press Enter to continue."+TColors.ENDC)
        os.system("cls")



