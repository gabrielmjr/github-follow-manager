import executor.github_request
from executor import labels as lb
from executor import configs as confs
from util import utils


class Executor:
    def __init__(self):
        self.headers = None
        self.url = None
        self.language = 1
        self.current_page = 1
        self.followers = []
        self.github_requests = None
        self.configs = confs.Configurations.get_instance()
        self.labels = None
        self.execute()

    def execute(self):
        self.labels = lb.LabelsManager.get_instance(self.configs.get_language())
        self.github_requests = executor.github_request.GithubRequest(self.configs.get_username())
        self.handle_inputs()

    def handle_inputs(self):
        while True:
            for label in self.labels.get_menu():
                print(label['text'])
            command = int(input(">>> "))
            if command == 1:
                self.print_followers(False)

    def print_followers(self, is_in_pagination):
        print("Listing all users that follows you.\n")
        temp_followers = utils.getOnlyNames(self.github_requests.get_followers_at(self.current_page))
        if len(temp_followers) == 0:
            print("Empty page.")
            return
        for follower in temp_followers:
            if follower not in self.followers:
                self.followers.append(follower)
        for i in range(40 * (self.current_page - 1), 40 * self.current_page):
            try:
                print(list(self.followers)[i])
            except IndexError:
                return
        if not is_in_pagination:
            print(10 * '-')
            self.start_pagination()

    def start_pagination(self):
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
            elif command == 0:
                print("Paging mode off")
                break
            else:
                print("Command not found")


if __name__ == '__main__':
    Executor()
