import os, sys
import requests
from Butler_github import github

# **************
# * Constants
# **************

SiteName = "user/project"
ProjectName = "Project"
DiscordHook = ''
TokenPath = "token.env"

class TColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
    f = open(os.path.join(sys.path[0], "Butler-version.txt"),"w")
    f.write(currVersion)
    f.close()
    return currVersion
    

# **************
# * Platforms
# **************

def platform():
    print(TColors.HEADER+"Select platform for push build to itch\n"+TColors.ENDC)
    print("[1] - Windows")
    print("[2] - Linux")
    print("[3] - Mac")
    print("[4] - All at once")
    print("[0] - Exit")
    action = input("Type Option: ")
    return action
        


def windows(currVersion, body):
    #? Itch
    os.system("butler.exe pus1h windows "+SiteName+":win --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Windows channel"}        
    requests.post(DiscordHook, data=payload)
    #? Github
    github(ProjectName,currVersion,{"Windows"},body ,True,False,None,TokenPath)

def linux(currVersion, body):  
    #? Itch
    os.system("butler.exe push linux "+SiteName+":linux --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Linux channel"}        
    requests.post(DiscordHook, data=payload)
    #? Github
    github(ProjectName,currVersion,{"Linux"},body ,True,False,None,TokenPath)

def mac(currVersion, body):
    #? Itch
    os.system("butler push mac "+SiteName+":mac --if-changed --userversion "+currVersion)
    #? Discord
    payload = {"content":"Version: "+currVersion+" was pushed to itch on Mac channel"}        
    requests.post(DiscordHook, data=payload)
    #? Github
    github(ProjectName,currVersion,{"Mac"},body ,True,False,None,TokenPath)

# **************
# * Main loop
# **************


action = '-1'
while(action!='0'):
    action = platform()
    if action == '0':
        continue
    body = input("Write text for release body:\n")
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
    else:
        print(TColors.WARNING+"Wrong option"+TColors.ENDC)
    # print(version())
    wait = input(TColors.OKBLUE+"Press Enter to continue."+TColors.ENDC)
    os.system("cls")
