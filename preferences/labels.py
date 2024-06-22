import json
import pathlib


class LabelsManager:
    instance = None

    def __init__(self, lang):
        self.lang = lang
        self.loaded_labels = None
        self.load_labels()

    def read_labels(self):
        with open(f'{pathlib.Path(__file__).parent.resolve().absolute()}/../'
                  f'resources/{self.lang}/labels.json', encoding='utf-8') as json_data:
            json_label = json.load(json_data)
        return json_label

    def load_labels(self):
        self.loaded_labels = self.read_labels()

    def get_menu(self):
        return self.loaded_labels['menu']

    @staticmethod
    def get_instance(lang: str):
        if not isinstance(LabelsManager.instance, LabelsManager):
            LabelsManager.instance = LabelsManager(lang)
        return LabelsManager.instance
