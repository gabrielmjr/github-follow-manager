import requests


class GithubRequest:
    instance = None

    def __init__(self, username):
        self.username = username
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        self.url = f"https://api.github.com/users/{username}"
        pass

    def get_followers_at(self, page):
        return requests.get(self.url + f'/followers?per_page=40&page={page}', headers=self.headers).json()

    @staticmethod
    def get_instance(username):
        if not isinstance(GithubRequest.instance, GithubRequest):
            GithubRequest.instance = GithubRequest(username)
        return GithubRequest.instance
