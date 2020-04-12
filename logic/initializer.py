from ..game.profession import PROFESSION_LIST, Profession

class Initializer:
    def __init__(self):
        self.initialized = False

    def init(self):
        if not self.initialized:
            self.initialized = True
            load_professions_from_json()


def load_professions_from_json():
    base_path = '../assets/professions/'
    full_path = os.path.join(os.getcwd(), base_path)
    for prof_file in os.listdir(full_path):
        if prof_file.endswith('.json'):
            profession = json.load(open(os.path.join(full_path, prof_file)))
            if profession["TPR-Type"] != "profession":
                raise Exception()
                # TODO: Implement custom load exception
            name = profession["name"]
            description = profession["description"]
            base_attributes = profession["base_attributes"]
            actions = profession["actions"]
            PROFESSION_LIST[name] = Profession(name, description, base_attributes, actions)
    if len(PROFESSION_LIST) != 6:
        raise Exception()
        # TODO: Implement custom load exception
