import yaml

def load_config_section(section:str, config_path:str="./config/config.yaml")->dict:
    '''
    Loads and returns a specific section from the YAML config.

    Args:
        section (str): Section name to retrieve (e.g. vectorstore, embedding).
        config_path (str): Path to the YAML config 
    Return:
        dict: Config section (Empty dict if not found.)
    '''
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get(section,{})