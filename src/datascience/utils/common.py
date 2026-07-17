import os
from os import path
from pathlib import Path
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
from box.exceptions import BoxValueError


@ensure_annotations
def read_yaml(path_to_yaml: str) -> ConfigBox:
    """Reads a yaml file and returns a ConfigBox object.

    Args:
        path_to_yaml (str): Path to the yaml file.

    Returns:
        ConfigBox: ConfigBox Type
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates a list of directories.

    Args:
        path_to_directories (list): List of directories to be created.
        verbose (bool, optional): Whether to log the creation of each directory. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves data to a json file.

    Args:
        path (Path): Path to the json file.
        data (dict): Data to be saved.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads data from a json file.

    Args:
        path (Path): Path to the json file.

    Returns:
        ConfigBox: ConfigBox Type
    """
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data to a binary file using joblib.

    Args:
        data (Any): Data to be saved.
        path (Path): Path to the binary file.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads data from a binary file using joblib.

    Args:
        path (Path): Path to the binary file.
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data
