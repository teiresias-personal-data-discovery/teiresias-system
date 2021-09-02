import os
from shutil import rmtree


def create_directory(path: str):
    try:
        os.mkdir(path)
        return 1
    except OSError as error:
        print(repr(error))
        return -1


def remove_directory(path: str):
    try:
        rmtree(path)
        return 1
    except OSError as error:
        print(repr(error))
        return -1


def clean_directory(path: str):
    try:
        for _, directories, files in os.walk(path):
            for directory in directories:
                rmtree(os.path.join(path, directory))
            for file in files:
                os.unlink(os.path.join(path, file))
        return 1
    except OSError as error:
        print(repr(error))
        return -1
