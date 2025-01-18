import utils

from backup import BackupManager
from preferences import Configurations, labels as lb
from request import GithubRequest
from utils import println


class Executor:
    ACTION_FOLLOWERS = 0
    ACTION_FOLLOWING = 1

    def __init__(self):
        self.current_page = 1
        self.github_requests = None
        self.configs = Configurations.get_instance()
        self.labels = None
        self.execute()

    def execute(self):
        self.labels = lb.LabelsManager.get_instance(self.configs.get_language())
        self.github_requests = GithubRequest(self.configs.get_username())
        self.handle_inputs()

    def handle_inputs(self):
        println()
        while True:
            self.current_page = 1
            for label in self.labels.get_menu():
                print(label['text'])
            command = int(input(">>> "))
            if command == 1:
                println()
                self.print_followers(False)
            if command == 2:
                println()
                self.print_following(False)
            if command == 4:
                println()
                self.unfollow_everyone()
            if command == 5:
                println()
                self.start_reciprocity()
            if command == 6:
                println()
                self.start_followers_backup_process()
            if command == 7:
                println()
                self.start_following_backup_process()

    def print_followers(self, is_in_pagination):
        println(f"{self.labels.loaded_labels['listing_followers']}\n")
        followers = utils.get_only_names(self.github_requests
                                         .get_followers_at(self.current_page))
        if len(followers) == 0:
            println(self.labels.loaded_labels['empty_page'])
        for i in range(0, 40):
            try:
                print(list(followers)[i])
            except IndexError:
                continue
        if not is_in_pagination:
            print(10 * '-')
            self.start_pagination(Executor.ACTION_FOLLOWERS)

    def print_following(self, is_in_pagination):
        println(f"{self.labels.loaded_labels['listing_following']}\n")
        following = utils.get_only_names(
            self.github_requests.get_following_at(self.current_page))
        if len(following) == 0:
            println(self.labels.loaded_labels['empty_page'])
            return
        for i in range(0, 40):
            try:
                print(following[i])
            except IndexError:
                continue
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
            if command == 0:
                print(self.labels.loaded_labels['pagination']['off'])
                self.current_page = 1
                break
            elif action == Executor.ACTION_FOLLOWERS:
                if 1 <= command <= 3:
                    self.handle_followers_command_in_pagination(command)
            elif action == Executor.ACTION_FOLLOWING:
                if 1 <= command <= 3:
                    self.handle_following_command_in_pagination(command)
            else:
                println(self.labels.loaded_labels['command_not_found'])

    def handle_followers_command_in_pagination(self, command):
        if command == 1:
            self.current_page = self.current_page + 1
            self.print_followers(True)
        elif command == 2:
            if self.current_page == 1:
                println(self.labels.loaded_labels['already_in_the_beginning'])
                return
            self.current_page = self.current_page - 1
            self.print_followers(True)
        elif command == 3:
            self.print_followers(True)

    def handle_following_command_in_pagination(self, command):
        if command == 1:
            self.current_page = self.current_page + 1
            self.print_following(True)
        elif command == 2:
            if self.current_page == 1:
                println(self.labels.loaded_labels['already_in_the_beginning'])
                return
            self.current_page = self.current_page - 1
            self.print_following(True)
        elif command == 3:
            self.print_following(True)

    def unfollow_everyone(self):
        auth_token = utils.get_token(self.labels)
        self.unfollow_users(self.get_all_following(), auth_token)

    def start_reciprocity(self):
        reciprocity_done = True
        auth_token = utils.get_token(self.labels)
        following = self.get_all_following()
        followers = self.get_all_followers()
        for flwing in following:
            if flwing not in followers:
                reciprocity_done = self.unfollow_user(flwing, auth_token)
        if reciprocity_done:
            println(self.labels.loaded_labels['unfollowed_everyone_wor_not_following'])
        else:
            println(self.labels.loaded_labels['error']['unknown'])

    def unfollow_users(self, users, auth_token):
        are_everyone_unfollowed = True
        for user in users:
            if not self.unfollow_user(user, auth_token):
                are_everyone_unfollowed = False
        if are_everyone_unfollowed:
            println(self.labels.loaded_labels['unfollowed_everyone'])
        else:
            println(self.labels.loaded_labels['error']['unknown'])

    def unfollow_user(self, user, token):
        return self.github_requests.unfollow(user, token)

    def start_followers_backup_process(self):
        self.save_users(self.get_all_followers(), 'followers')

    def get_all_followers(self):
        followers = []
        self.current_page = 1
        while True:
            temp_followers = utils.get_only_names(
                self.github_requests.get_followers_at(self.current_page))
            if len(temp_followers) == 0:
                return followers
            followers = followers + temp_followers
            self.current_page += 1

    def get_all_following(self):
        following = []
        self.current_page = 1
        while True:
            temp_followings = utils.get_only_names(
                self.github_requests.get_following_at(self.current_page))
            if len(temp_followings) == 0:
                return following
            following = following + temp_followings
            self.current_page += 1

    def start_following_backup_process(self):
        self.save_users(self.get_all_following(), 'following')

    def save_users(self, followers, target):
        for save_option in self.labels.loaded_labels['save_options']:
            print(save_option['text'])
        command = int(input(">>> "))
        if command == 1:
            BackupManager.instance.write_backup_to_csv(followers, target)
        if command == 2:
            BackupManager.instance.write_backup_to_json(followers, target)


if __name__ == '__main__':
    Executor()
