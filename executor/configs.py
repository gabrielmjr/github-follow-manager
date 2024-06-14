import json
from executor import labels as lb
from pathlib import Path


class Configurations:
    instance = None

    def __init__(self):
        self.configs = {
            'lang': '',
            'username': ''
        }
        self.labels = None
        self.setup_configurations()

    def ask_lang(self):
        print("""Enter 1 to continue in English.
            \rDigite 2 para continuar em lingua portuguesa:""")
        lang = int(input(">>> "))
        if lang == 1:
            self.configs['lang'] = 'en'
        elif lang == 2:
            self.configs['lang'] = 'pt'

    def ask_username(self):
        self.configs['username'] = str(input(self.labels.loaded_labels['others']['ask_name']))

    def setup_configurations(self):
        configs_path = Path(f"{Path(__file__).parent.resolve().absolute()}"
                            f"/../resources/configs.json")
        if configs_path.exists():
            with open(configs_path, 'r', encoding='utf-8') as configs:
                self.configs = json.loads(configs.read())
        else:
            print("The following configurations will be prompted once and stored in resources"
                  "/configs.json")
            self.ask_lang()
            self.labels = lb.LabelsManager.get_instance(self.configs['lang'])
            self.ask_username()
            with open(configs_path, 'w', encoding='utf-8') as configs:
                configs.write(json.dumps(self.configs))

    def get_language(self):
        return self.configs['lang']

    def get_username(self):
        return self.configs['username']

    @staticmethod
    def get_instance():
        if not isinstance(Configurations.instance, Configurations):
            Configurations.instance = Configurations()
        return Configurations.instance
