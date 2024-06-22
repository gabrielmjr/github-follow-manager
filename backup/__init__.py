import csv
import json
import os.path
import utils
from pathlib import Path


class BackupManager:
    instance = None

    def __init__(self):
        self.backup_dir = None
        self.create_backup_dir()

    def create_backup_dir(self):
        self.backup_dir = (f'{Path(__file__).parent.resolve().absolute()}' +
                           '/resources/backups')
        if not os.path.isdir(self.backup_dir):
            os.mkdir(self.backup_dir)

    def write_backup_to_csv(self, followers, target):
        with open(self.backup_dir + f'/{utils.current_time()}.{target}.csv', 'w') as csc_file:
            writer = csv.writer(csc_file)
            writer.writerow(followers)

    def write_backup_to_json(self, followers, target):
        with open(self.backup_dir + f'/{utils.current_time()}.{target}.json', 'w') as json_file:
            json_users = json.dumps(followers)
            json_file.write(json_users)

    @staticmethod
    def get_instance():
        if not isinstance(BackupManager.instance, BackupManager):
            BackupManager.instance = BackupManager()
        return BackupManager.instance
