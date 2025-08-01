import yaml
from app_utils.logger import set_logger


yaml_logger = set_logger(__name__)

def load_config(config_path: str = "config/config.yaml") -> dict:
    global config
    '''
    Load YAML config file from the specified path.

    Args:
        config path (str): Path to YAML File.

    Returns:
        dict: Parsed YAML content.
    
    '''
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            yaml_logger.debug(f"Loaded config from {config_path}")
            return config
    except FileNotFoundError:
        yaml_logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        yaml_logger.error(f'YAML Parsing error in {config_path}')
        raise

def override_config(key, value):
    global config
    if config is None:
        load_config()
    config[key] = value
    