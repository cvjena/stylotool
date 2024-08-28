import TextObject as to
import pickle
import os
import json
import spacy
import ChiasmusAnnotation as ca
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import average_precision_score
from tqdm import tqdm

def create_training_text_object():
    with open('../datasets/chiasmus-annotations/data/data.json', 'r') as f:
        data = json.load(f)



    text = to.TextObject()
    
    #self.textfile = textfile
    text.language = 'de'
    offsets = []
    offset = 0
    model_name = "de_core_news_lg"
    nlp = None
    while nlp is None:
        try:
            nlp = spacy.load(model_name)
        except:
            try:
                spacy.cli.download(model_name)
            except:
                print(f"ERROR: Could not download model {model_name}")
                exit(1)
    chiasmi = ca.ChiasmusAnnotation(text, 30)
    positive_annotations = ['a', 'fa', 'c', 'fc']
    features = []
    labels = []
    print("processing text")
    for example in tqdm(data):
        offsets.append(offset)
        text.tokens += example["tokens"]
        text.pos += example["pos"]
        text.lemmas += example["lemmas"]
        text.dep += example["dep"]
        vectors = [nlp(token).vector for token in example["tokens"]]
        text.vectors += vectors
        ids = [i-example["cont_ids"][0]+offset for i in example["ids"]]
        offset += len(example["tokens"])

        candidate = ca.ChiasmusCandidate(ids[0], ids[1], ids[2], ids[3])
        if example["annotation"] in positive_annotations:
            candidate.score = 1
        else:
            candidate.score = 0


        chiasmi.candidates.append(candidate)


    for candidate in tqdm(chiasmi.candidates):
        print(candidate.ids)
        features.append(chiasmi.get_features(candidate))
        labels.append(candidate.score)

    model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                class_weight = "balanced",
                max_iter = 1000,
                C = 1
                )
            )


    for f in features:
        print(f.shape)
    features = np.array(features)
    labels = np.array(labels)
    print("training model")
    print(features.shape)
    print(labels.shape)
    model.fit(features, labels)
    scores = average_precision_score(labels, model.predict(features))
    print("training summary:")
    print("average precision: ", scores)


    # save the model
    model_file = os.path.join("../models/chiasmus_de.pkl")
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    print("model saved to", model_file)



        



    #self.tokens = 
    #self.language = language
    #self.tokens = []
    #self.pos = []
    #self.lemmas = []
    #self.dep = []
    #self.vectors = []
    #self.annotations = {}
    #self.token_offsets = []
    #self.text = ""


def main():
    create_training_text_object()
if __name__ == "__main__":
    main()
