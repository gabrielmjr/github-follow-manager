def getOnlyNames(json_response):
    names = []
    for user in json_response:
        names.append(user['login'])
    return names
