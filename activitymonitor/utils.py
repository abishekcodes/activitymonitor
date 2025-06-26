import os

def env_bool_parser(name: str, default: bool = False) -> bool:
    value = os.getenv(name, str(default)).lower()
    return value in ('true', '1', 'yes')