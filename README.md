# Butler - Release helper script build with python
[![DeepSource](https://app.deepsource.com/gh/BialySztorm/Butler.svg/?label=active+issues&show_trend=true&token=DX7v_pziLLEoUSL7Od21Wqj-)](https://app.deepsource.com/gh/BialySztorm/Butler/?ref=repository-badge)

## Installation and usage

Simple drag all files to your build directory(all build files should be under child directory with platform name), complete the prerequisite for chosen platforms, if you are using python script comment things you don't gonna use and you are ready to go.

You can easy customize constants if you want in Butler_constants.py

To start the script paste in command line "python Butler.py", choose release platform, select the version change you wanna do, and next everything gonna do for you automatically.

## Prerequisite for binary file
1. itch:
 - [Butler](https://itchio.itch.io/butler) - Downloaded and added to PATH or in the same dir
 - ITCH_SITE_NAME:=[Site name](https://itch.io/docs/butler/pushing.html) in .env

2. Discord:
 - DISCORD_HOOK:=[Discord hook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in .env

3. Github releases:
 - GITHUB_API_TOKEN:=[Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in .env file or change definition wherever it is
 - starting script in git repository directory

4. Jira
 - place this information in .env: \
    JIRA_BASE_URL:=YOUR_JIRA_BASE_URL \
    JIRA_PROJECT_KEY:=PROJECT_KEY \
    JIRA_API_TOKEN:=JIRA_API_TOKEN \
    JIRA_USER:=JIRA_USERNAME_OR_EMAIL
## Prerequisite for python script

 - Downloaded [Python3](https://www.python.org/downloads/)
 - [keyboard](https://pypi.org/project/keyboard/), [os](https://docs.python.org/3/library/os.html) & [sys](https://docs.python.org/3/library/sys.html) python modules

1. itch:
 - [Butler](https://itchio.itch.io/butler) - Downloaded and added to PATH or in the same dir
 - ITCH_SITE_NAME:=[Site name](https://itch.io/docs/butler/pushing.html) in .env

2. Discord:
 - [requests](https://pypi.org/project/requests/) python module
 - DISCORD_HOOK:=[Discord hook](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) in .env

3. Github releases:
 - GITHUB_API_TOKEN:=[Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in .env file or change definition wherever it is
 - [subprocess](https://docs.python.org/3/library/subprocess.html), [shutil](https://docs.python.org/3/library/shutil.html), [requests](https://pypi.org/project/requests/) & [tqdm](https://pypi.org/project/tqdm/) python modules
 - starting script in git repository directory

4. Jira
 - place this information in .env: \
    JIRA_BASE_URL:=YOUR_JIRA_BASE_URL \
    JIRA_PROJECT_KEY:=PROJECT_KEY \
    JIRA_API_TOKEN:=JIRA_API_TOKEN \
    JIRA_USER:=JIRA_USERNAME_OR_EMAIL
 - [requests](https://pypi.org/project/requests/), [locale](https://docs.python.org/3/library/locale.html) & [datetime](https://docs.python.org/3/library/datetime.html) modules

| | |
|:-------------------------:|:-------------------------:|
| <img width="1604" alt="Screenshot_2023-08-21_092807" src="https://raw.githubusercontent.com/BialySztorm/Butler/main/.github/Screenshot_2023-08-21_092807.png"> | <img width="1604" alt="Screenshot_2023-08-21_092821" src="https://raw.githubusercontent.com/BialySztorm/Butler/main/.github/Screenshot_2023-08-21_092821.png"> |
| <img width="1604" alt="Screenshot_2023-08-21_092830" src="https://raw.githubusercontent.com/BialySztorm/Butler/main/.github/Screenshot_2023-08-21_092830.png"> | <img width="1604" alt="Screenshot_2023-08-21_093310" src="https://raw.githubusercontent.com/BialySztorm/Butler/main/.github/Screenshot_2023-08-21_093310.png"> |
