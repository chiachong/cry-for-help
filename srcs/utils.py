import yaml


def load_yaml(config: str) -> dict:
    """ Load project configurations from a .yaml file. """
    with open(config, 'r') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return config

