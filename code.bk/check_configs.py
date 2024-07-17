import os
import json


def get_config_path():
    if os.name == "posix":
        try:
            xdg = os.environ["XDG_CONFIG_HOME"]
        except:
            xdg = "~/.config"
            xdg = os.path.expanduser("~/.config")
        config_path = os.path.join(
                xdg,
                "stylotool")
        config_file = os.path.join(
                config_path,
                "config.json")
        return config_path, config_file
    else:
        print("This tool is currently only supported on POSIX systems.")
        return None


def get_standard_config():
    return {
            "de": {
                "language name": "German",
                "spacy model": "de_core_news_sm",
                "conjugations": ["und", "so", "weil", "weder", "noch", "aber", "für", "dennoch"],
                "negations": ["nein", "nicht", "niemals", "nichts"],
                "chiasmus pos exclude": ["CCONJ", "PUNCT", "SPACE", "ADP", "PART"]
                }
            }

def get_data_path():
    if os.name == "posix":
        try:
            xdg = os.environ["XDG_DATA_HOME"]
        except:
            xdg = os.path.expanduser("~/.local/share")
        data_path = os.path.join(
                xdg,
                "stylotool")
        # create path if it does not exist
        if not os.path.exists(data_path):
            print("Creating data path at {}".format(data_path))
            os.makedirs(data_path)
        return data_path
    else:
        print("This tool is currently only supported on POSIX systems.")
        return None

def get_config():
    _, config_file = get_config_path()
    check_config()
    return json.load(open(config_file))




def check_config():
    config_path, config_file = get_config_path()

    # check if config path exists
    if not os.path.exists(config_path):
        print(f"Config path does not exist: {config_path}")
        print("Creating config path...")
        os.makedirs(config_path)

    # check if config file exists
    if not os.path.exists(config_file):
        print(f"Config file does not exist: {config_file}")
        print("Creating config file...")
        standard_config = get_standard_config()
        with open(config_file, "w") as f:
            json.dump(standard_config, f, indent=4)

    

def main():
    pass

if __name__ == '__main__':
    main()
