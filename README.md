# GitHub Follow Manager

***Build state:***
 ![](https://github.com/gabrielmjr/reciprometer/actions/workflows/python-package.yml/badge.svg)

## Description

Does people who you're following must follow you also? well, this repository is for you. This repository can also help you to manage your followers and users who you are following in CLI.
<br/>
This is a project that was made in Python and you can use it to:
1. - [x] See everyone who're following you.
2. - [x] See everyone who you're following.
3. - [ ] Follow all users with their username saved in a JSON or CSV(Auth token required).
4. - [x] Unfollow all users (Auth token required).
5. - [ ] Follow only who are following you (Auth token required).
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


3. Open up the `github-follow-manager` folder and install all the required libraries as followed:

        cd github-follow-manager
        pip install -r (or --requirement) requirements.txt
   The above code will install all required libraries to execute the program, in this case is only the [requests](https://pypi.org/project/requests) library, after the installation of this library you can go to next step.

4. Run the `main.py` file as followed:

       python main.py
   
5. Congratulation, you've setup your environment and runned the GitHub Follow Manager, there will be instructions to use, the program is terminal friendly, there's usage menu that makes it easy to use.
<br/>

## Additional
If you are facing some issue related to the GitHub Follow Manager, you can open an issue, else if you can, clone the source code, improve or refactor it and make a pull request, if it be useful, then I'll merge.

<br/>

## License   
Copyright 2024 Gabriel MJr

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0
