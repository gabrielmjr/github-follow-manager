import csv
import json
import os.path
import pathlib

import executor.github_request
from executor import labels as lb
from executor import configs as confs
import time
from util import utils


class Executor:
    ACTION_FOLLOWERS = 0
    ACTION_FOLLOWING = 1

    def __init__(self):
        self.headers = None
        self.url = None
        self.language = self.current_page = 1
        self.github_requests = None
        self.backup_dir = None
        self.create_backup_dir()
        self.configs = confs.Configurations.get_instance()
        self.labels = None
        self.execute()

    def create_backup_dir(self):
        self.backup_dir = (f'{pathlib.Path(__file__).parent.resolve().absolute()}' +
                           '/resources/backups')
        if not os.path.isdir(self.backup_dir):
            os.mkdir(self.backup_dir)

    def execute(self):
        self.labels = lb.LabelsManager.get_instance(self.configs.get_language())
        self.github_requests = executor.github_request.GithubRequest(self.configs.get_username())
        self.handle_inputs()

    def handle_inputs(self):
        while True:
            self.current_page = 1
            for label in self.labels.get_menu():
                print(label['text'])
            command = int(input(">>> "))
            if command == 1:
                self.print_followers(False)
            if command == 2:
                self.print_following(False)
            if command == 4:
                self.unfollow_everyone()
            if command == 6:
                self.start_followers_backup_process()
            if command == 7:
                self.start_following_backup_process()

    def print_followers(self, is_in_pagination):
        followers = []
        print(f"{self.labels.loaded_labels['listing_followers']}\n")
        temp_followers = utils.get_only_names(self.github_requests
                                              .get_followers_at(self.current_page))
        if len(temp_followers) == 0:
            print(self.labels.loaded_labels['empty_page'])
            return
        for follower in temp_followers:
            if follower not in followers:
                followers.append(follower)
        for i in range(40 * (self.current_page - 1), 40 * self.current_page):
            try:
                print(list(followers)[i])
            except IndexError:
                return
        if not is_in_pagination:
            print(10 * '-')
            self.start_pagination(Executor.ACTION_FOLLOWERS)

    def print_following(self, is_in_pagination):
        following = []
        print(f"{self.labels.loaded_labels['listing_following']}\n")
        temp_following = utils.get_only_names(
            self.github_requests.get_following_at(self.current_page))
        if len(temp_following) == 0:
            print(self.labels.loaded_labels['empty_page'])
            return
        for _following in temp_following:
            if _following not in following:
                following.append(_following)
        for i in range(40 * (self.current_page - 1), 40 * self.current_page):
            try:
                print(following[i])
            except IndexError:
                return
        if not is_in_pagination:
            print(10 * '-')
            self.start_pagination(Executor.ACTION_FOLLOWING)

    def start_pagination(self, action):
        must_stop = False
        while True:
            if not must_stop:
                pass
            else:
                break
            print(self.labels.loaded_labels['pagination']['on'])
            for menu in self.labels.loaded_labels['pagination_menu']:
                print(menu['text'])
            command = int(input(">>> "))
            if action == Executor.ACTION_FOLLOWERS:
                if command == 1:
                    self.current_page = self.current_page + 1
                    self.print_followers(True)
                elif command == 2:
                    if self.current_page == 1:
                        print(self.labels.loaded_labels['already_in_the_beginning'])
                        continue
                    self.current_page = self.current_page - 1
                    self.print_followers(True)
                elif command == 3:
                    self.print_followers(True)
            if action == Executor.ACTION_FOLLOWING:
                if command == 1:
                    self.current_page = self.current_page + 1
                self.print_following(True)
            elif command == 2:
                if self.current_page == 1:
                    print(self.labels.loaded_labels['already_in_the_beginning'])
                    continue
                self.current_page = self.current_page - 1
                self.print_following(True)
            elif command == 3:
                self.print_following(True)
            elif command == 0:
                print(self.labels.loaded_labels['pagination']['off'])
                self.current_page = 1
                break
            else:
                print(self.labels.loaded_labels['command_not_found'])

    def unfollow_everyone(self):
        following = []
        print(self.labels.loaded_labels['enter_your_token'])
        auth_token = str(input(">>> "))
        self.current_page = 1
        while True:
            temp_following = utils.get_only_names(
                self.github_requests.get_following_at(self.current_page))
            if len(temp_following) == 0:
                self.unfollow_users(following, auth_token)
                break
            following = following + temp_following
            self.current_page = self.current_page + 1

    def unfollow_users(self, users, auth_token):
        are_everyone_unfollowed = True
        for user in users:
            if not self.github_requests.unfollow(user, auth_token):
                are_everyone_unfollowed = False
        if are_everyone_unfollowed:
            print(self.labels.loaded_labels['unfollowed_everyone'])
        else:
            print(self.labels.loaded_labels['error']['unknown'])

    def start_followers_backup_process(self):
        followers = []
        self.current_page = 1
        while True:
            temp_followers = utils.get_only_names(
                self.github_requests.get_followers_at(self.current_page))
            if len(temp_followers) == 0:
                self.save_users(followers, 'followers')
                break
            followers = followers + temp_followers
            self.current_page += 1

    def start_following_backup_process(self):
        following = []
        self.current_page = 1
        while True:
            temp_followings = utils.get_only_names(
                self.github_requests.get_following_at(self.current_page))
            if len(temp_followings) == 0:
                self.save_users(following, 'following')
                break
            following = following + temp_followings
            self.current_page += 1

    def save_users(self, followers, target):
        for save_option in self.labels.loaded_labels['save_options']:
            print(save_option['label'])
        command = int(input(">>> "))
        if command == 1:
            self.write_backup_to_csv(followers, target)
        if command == 2:
            self.write_backup_to_json(followers, target)

    def write_backup_to_csv(self, followers, target):
        with open(self.backup_dir + f'/{self.current_time()}.{target}.csv', 'w') as csc_file:
            writer = csv.writer(csc_file)
            writer.writerow(followers)

    def write_backup_to_json(self, followers, target):
        with open(self.backup_dir + f'/{self.current_time()}.{target}.json', 'w') as json_file:
            json_users = json.dumps(followers)
            json_file.write(json_users)

    @staticmethod
    def current_time():
        return time.time()


if __name__ == '__main__':
    Executor()
