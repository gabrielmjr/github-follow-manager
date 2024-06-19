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
                self.start_backup_process()

    def print_followers(self, is_in_pagination):
        followers = []
        print("Listing all users that follows you.\n")
        temp_followers = utils.get_only_names(self.github_requests
                                              .get_followers_at(self.current_page))
        if len(temp_followers) == 0:
            print("Empty page.")
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
        print("Listing all users that you are following.\n")
        temp_following = utils.get_only_names(
            self.github_requests.get_following_at(self.current_page))
        if len(temp_following) == 0:
            print("Empty page.")
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
            print("Paging mode on")
            print("Enter 1 to go to the next page")
            print("Enter 2 to go to previewer page")
            print("Enter 3 to re-print this page")
            print("Enter 0 to exit paging mode")
            command = int(input(">>> "))
            if action == Executor.ACTION_FOLLOWERS:
                if command == 1:
                    self.current_page = self.current_page + 1
                    self.print_followers(True)
                elif command == 2:
                    if self.current_page == 1:
                        print("Already in the beginning")
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
                    print("Already in the beginning")
                    continue
                self.current_page = self.current_page - 1
                self.print_following(True)
            elif command == 3:
                self.print_following(True)
            elif command == 0:
                print("Paging mode off")
                self.current_page = 1
                break
            else:
                print("Command not found")

    def unfollow_everyone(self):
        following = []
        print("Enter your github auth token")
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
            print("Unfollowed everyone.")
        else:
            print("Something went wrong.")

    def start_backup_process(self):
        followers = []
        self.current_page = 1
        while True:
            temp_followers = utils.get_only_names(
                self.github_requests.get_followers_at(self.current_page))
            if len(temp_followers) == 0:
                self.save_users(followers)
                break
            followers = followers + temp_followers
            self.current_page = self.current_page + 1

    def save_users(self, followers):
        print("Enter 1 to save to a CSV.")
        print("Enter 2 to save to a JSON.")
        command = int(input(">>> "))
        if command == 1:
            self.write_backup_to_csv(followers)
        if command == 2:
            self.write_backup_to_json(followers)

    def write_backup_to_csv(self, followers):
        with open(self.backup_dir + f'/{self.current_time()}.csv', 'w') as csc_file:
            writer = csv.writer(csc_file)
            writer.writerow(followers)

    def write_backup_to_json(self, followers):
        with open(self.backup_dir + f'/{self.current_time()}.json', 'w') as json_file:
            json_users = json.dumps(followers)
            json_file.write(json_users)

    @staticmethod
    def current_time():
        return time.time()


if __name__ == '__main__':
    Executor()
