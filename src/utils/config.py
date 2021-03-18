from pathlib import Path
import os

import yaml


class Config:

    def __init__(self, file_name):
        path = Path(os.getcwd().split('src')[0]).joinpath('config') / file_name
        with open(path) as file:
            self.data = yaml.load(file, Loader=yaml.Loader)

    def __getitem__(self, item):
        return self.data[item]


CONFIG = Config('config.yaml')