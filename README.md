# GitHub Follow Manager

***Build state:***
 ![](https://github.com/gabrielmjr/reciprometer/actions/workflows/python-package.yml/badge.svg)

## Description

Does people who you're following must follow you also? well, this repository is for you. This repository can also help you to manage your followers and users who you are following in CLI.
<br/>
This is a project that was made in Python and you can use it to:
1. - [x] See everyone who're following you.
2. - [x] See everyone who you're following.
3. - [ ] Follow all users with their username saved in a JSON or CSV (Restore the backup of feature 7) (Auth token required).
4. - [x] Unfollow all users (Auth token required).
5. - [x] Follow only who are following you (Auth token required).
6. - [x] Make a backup of your followers in a JSON or CSV.
7. - [x] Make a backup of everyone who you are following in a JSON or CSV.

<br/>

> [!Note]
> 1. This program asks you an github username, this field can be filled by any github username and will works well because github API is opened for everyone.
> 2. To use the follow [3] and unfollow [4] funtions, you'll need to add your github Authentication Token, you'll be instructed when run the program.

<br/>

## How to use?

> [!Important]
> To use the GitHub Follow Manager, you've to be with Python (3) installed in your environment, if you don't have it installed, you can download it from the [official site](https://www.python.org/downloads/), alternativery you can [follow this tutorial](https://kinsta.com/knowledgebase/install-python/) or google `how to install python in <the OS name intalled on your machine>` and follow the instructions.

1. Clone the git project using:
  > [!Note]
  > After first release, you'll have option of download the stable release source code and then run the script instead of clonning it.


       git clone https://github.com/gabrielmjr/github-follow-manager

2. Open up the `github-follow-manager` folder

       cd github-follow-manager

3. Create a new Python Virtual Environment (venv) and activate it
> [!Note]
> Only create a new virtual environment after clone the project.
  
       python -m venv .venv 

4. Start the environment
 
       source .venv/bin/activate

5. Install all the required libraries as followed:

       pip install --requirement requirements.txt
   The above code will install all required libraries to execute the program, in this case is only the [requests](https://pypi.org/project/requests) library, after the installation of this library you can go to next step.


6. Run the `main.py` file as followed:

       python main.py
   
7. Congratulation, you've setup your environment and ran the GitHub Follow Manager, there will be instructions to use, the program is terminal friendly, there's usage menu that makes it easy to use.
<br/>

>[!Important]
> To use some follow/unfollow option, you will be requested to enter your [Github Fine Grained Personal Token with](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) Account permission > Followers > read and write access. [click here](https://github.com/settings/personal-access-tokens/new) to create a new.

>[!Note]
> The program just makes request to the [Github API](https://docs.github.com/en/rest/users?apiVersion=2022-11-28), nothing else, it only stores the username and the prefered language in a json located in 'project parent dir'/resources/configs,json, due to security reasons, the Token you provides the app during the execution when prompted are never stored nor shared, that's why you will be always prompted to enter the token to perform some action that requires it (such as follow/unfollow features).

>[!Note] 
> In subsequent times, to run the program, follow the step 2, then 4 and finally 6.

## Additional
If you are facing some issue related to the GitHub Follow Manager, you can open an issue, else if you can, clone the source code, improve or refactor it and make a pull request, if it be useful, then I'll merge.

## License   
```Copyright 2024 Gabriel MJr```.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
            http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
