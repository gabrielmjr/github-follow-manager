import executor.github_request
from executor import labels as lb
from executor import configs as confs
from util import utils


class Executor:
    def __init__(self):
        self.headers = None
        self.url = None
        self.language = 1
        self.github_requests = None
        self.configs = confs.Configurations.get_instance()
        self.labels = None
        self.execute()

    def handle_inputs(self):
        for label in self.labels.get_menu():
            print(label['text'])
        while True:
            command = int(input(">>> "))
            if command == 1:
                print("Listing all users that follows you.\n")
                for name in utils.getOnlyNames(self.github_requests.get_all_followers()):
                    print(name)

    def execute(self):
        self.labels = lb.LabelsManager.get_instance(self.configs.get_language())
        self.github_requests = executor.github_request.GithubRequest(self.configs.get_username())
        self.handle_inputs()


if __name__ == '__main__':
    Executor()
