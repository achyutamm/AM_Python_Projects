import yaml

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
    return config_data
