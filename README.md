# Butler - Release helper script build with python

## Installation and usage

Simple drag all files to your build directory(all build files should be under child directory with platform name), complete the prerequisite for chosen platforms, comments things you don't gonna use and you are ready to go.

You can easy customize constants if you want in Butler.py

Start the script with command line, choose release platform, select the version change you wanna do, and next everything gonna do for you automatically.


## Prerequisite

 - Downloaded Python3
 - os & sys python modules

1. itch:
 - [Butler](https://itchio.itch.io/butler) - Downloaded and added to PATH
 - Site name in constants section in Butler.py

2. Discord:
 - requests python module
 - Discord hook in constants section in Butler.py

3. Github releases:
 - Personal Access Token in token.env file or change definition wherever it is
 - subprocess, shutil, requests & tqdm python modules
 - starting script in git repository directory