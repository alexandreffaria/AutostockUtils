import os
from dotenv import load_dotenv

def load_environment_variables():
    """Load environment variables from .env file in the parent directory."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    load_dotenv(env_path)

def get_parent_directory(path: str, levels: int = 1) -> str:
    """
    Get the parent directory of the given path.
    
    Args:
    path (str): The starting path.
    levels (int): Number of levels to go up. Default is 1.

    Returns:
    str: The path of the parent directory.
    """
    for _ in range(levels):
        path = os.path.dirname(path)
    return path