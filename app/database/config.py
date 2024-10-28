from configparser import ConfigParser
from typing import Dict, Optional, Any
from pathlib import Path

def get_absolute_path() -> str:
    base_dir = Path('../../database.ini')
    return str(base_dir)

def load_config(filename: str=get_absolute_path(), section: str='postgresql') -> Dict[str, Any]:
    '''
        filename : Gets the absolute path of the database.ini file
        section: The section of the file we intend to
    '''
    parser: ConfigParser = ConfigParser()
    try:
        with open(filename) as file:
            parser.read_file(file)
    except Exception as e:
        print(f'X unable to read file ==> {e}')
    config: Optional[Dict] = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename}")
    return config
