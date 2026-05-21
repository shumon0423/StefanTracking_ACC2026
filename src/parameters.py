import yaml

def load_parameters(filename="config/parameters.yaml"):
    with open(filename, "r") as file:
        return yaml.safe_load(file)

params = load_parameters()
