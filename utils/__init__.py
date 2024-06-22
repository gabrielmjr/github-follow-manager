import time


def current_time():
    return time.time()


def get_only_names(json_response):
    names = []
    for user in json_response:
        names.append(user['login'])
    return names


def get_token(labels):
    print(labels.loaded_labels['enter_your_token'])
    return str(input(">>> "))
