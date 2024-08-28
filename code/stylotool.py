import argparse
import json
import ChiasmusAnnotation as ca
import TextObject as to
import TextPreprocessor as tp

def main():
    parser = argparse.ArgumentParser(description="Stylometric analysis tool")
    parser.add_argument("--input", help="Input text file")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--config", help="Configuration file")
    args = parser.parse_args()

    # load config
    with open(args.config) as f:
        config = json.load(f)

    # Load text

    text = to.TextObject(
            textfile = args.input,
            language=config["language"])

    # Preprocess text
    preprocessor = tp.TextPreprocessor(language=config["language"])
    preprocessor.process_text(text)
    # Annotate
    annotation_dict = config["annotations"]
    for annotation in annotation_dict:
        if annotation == "chiasmus":
            add_chiasmus_annotation(text, annotation_dict[annotation])

    # Serialize results
    text.serialize(args.output)

def add_chiasmus_annotation(text, config):
    chiasmus = ca.ChiasmusAnnotation(
            text=text,
            window_size = config["window_size"])
    chiasmus.allowlist = config["allowlist"]
    chiasmus.denylist = config["denylist"]
    chiasmus.find_candidates()
    chiasmus.load_classification_model(config["model"])
    chiasmus.score_candidates()

if __name__ == '__main__':
    main()
