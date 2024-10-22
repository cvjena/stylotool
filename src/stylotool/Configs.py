import os
import logging
import json

model_list = [
        "chiasmus_de.pkl",
        "metaphor_de.torch",
        ]

def get_model_path():
    user_path = os.path.expanduser("~")
    config_path = os.path.join(user_path, ".config/freestylo/")
    config_file = os.path.join(config_path, "config.json")
    if not os.path.exists(config_file):

        os.makedirs(config_path, exist_ok=True)
        with open(config_file, "w") as f:
            json.dump(
                    {"model_path": os.path.join(user_path, ".freestylo/models/")},
                    f, 
                    indent=4)

    with open(config_file, "r") as f:
        config = json.load(f)

    model_path = config["model_path"]




