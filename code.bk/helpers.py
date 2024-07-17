import spacy


def get_spacy_model(model_name):
    """
    Check if the model is available in the spacy library. If not, download it.
    """
    if model_name not in spacy.util.get_installed_models():
        print(f"Downloading {model_name}...")
        spacy.cli.download(model_name)
        print(f"Done!")
    return spacy.load(model_name)

