# Library imports
import shutil
from pathlib import Path

# Local imports
from src.logger import debug


def createDirectoryIfNecessary(directory: Path) -> bool:
    if directory.exists():
        debug(f"Directory {directory} already exists - skipping.")
        return False

    directory.mkdir(parents=True)
    debug(f"Created directory: {directory}")
    return True


def readDictFromFileIfPossible(filepath) -> dict:
    dict = {}
    try:
        with open(filepath, "r") as f:
            dict = eval(f.read())
    except Exception as e:
        dict = {}
    debug(f"Cached dictionary: {dict}")
    return dict


def createFileWithContent(filepath: Path, content: str, force=False) -> bool:
    if filepath.exists() and not force:
        debug(f"File {filepath} already exists - skipping.")
        return False

    with open(filepath, "w") as f:
        f.write(content)
    debug(f"Created file: {filepath}")
    return True


def copyFileIfPossible(source: Path, destination: Path) -> bool:
    if destination.exists():
        debug(f"File {destination} already exists - skipping.")
        return False

    shutil.copy(source, destination)
    debug(f"Copied file {source} to {destination}")
    return True
