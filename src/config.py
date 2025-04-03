import os
import json


class Config:

    @staticmethod
    def load_config(filename):
        project_dir = os.path.dirname(os.getcwd())
        filepath = os.path.join(project_dir, "TextReteller", "config", filename)
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
