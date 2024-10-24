import argparse
import json
import freestylo.ChiasmusAnnotation as ca
import freestylo.MetaphorAnnotation as ma
import freestylo.EpiphoraAnnotation as ea
import freestylo.PolysyndetonAnnotation as pa
import freestylo.AlliterationAnnotation as aa
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp

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
        elif annotation == "metaphor":
            add_metaphor_annotation(text, annotation_dict[annotation])
        elif annotation == "epiphora":
            add_epiphora_annotation(text, annotation_dict[annotation])

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

def add_metaphor_annotation(text, config):
    metaphor = ma.MetaphorAnnotation(text)
    metaphor.find_candidates()
    metaphor.load_model(config["model"])
    metaphor.score_candidates()

def add_epiphora_annotation(text, config):
    epiphora = ea.EpiphoraAnnotation(
            text = text,
            min_length = config["min_length"],
            conj = config["conj"],
            punct_pos = config["punct_pos"])
    epiphora.find_candidates()

def add_polysyndeton_annotation(text, config):
    polysyndeton = pa.PolysyndetonAnnotation(
            text = text,
            min_length = config["min_length"],
            conj = config["conj"],
            sentence_end_tokens = config["sentence_end_tokens"])
    polysyndeton.find_candidates()

def add_alliteration_annotation(text, config):
    alliteration = aa.AlliterationAnnotation(
            text = text,
            max_skip = config["max_skip"],
            min_length = config["min_length"])
    alliteration.find_candidates()

if __name__ == '__main__':
    main()
