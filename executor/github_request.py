import http.client

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

    def get_followers_at(self, page):
        return requests.get(self.url + f'/followers?per_page=40&page={page}',
                            headers=self.headers).json()

    def get_following_at(self, page):
        return requests.get(self.url + f'/following?per_page=40&page={page}',
                            headers=self.headers).json()

    def unfollow(self, user, auth_token):
        headers = dict(list(self.headers.items()) + list({"Authorization": "token " + auth_token}.items()))
        url = f'https://api.github.com/user/following/{user}'
        code = requests.delete(url, headers=headers).status_code
        if code == http.client.NO_CONTENT:
            return True
        return False

    @staticmethod
    def get_instance(username):
        if not isinstance(GithubRequest.instance, GithubRequest):
            GithubRequest.instance = GithubRequest(username)
        return GithubRequest.instance
