from thinc.api import Logistic
import check_configs
import helpers
import numpy as np
import os
from tqdm import tqdm
import pickle
import json


from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import average_precision_score



class ChiasmusDetector:
    def __init__(self, language = "de", remove_duplicates):
        self.language = language
        self.remove_duplicates = remove_duplicates # TODO
        self.config = check_configs.get_config()[language]
        self.spacy_model_name = self.config["spacy model"]
        self.max_phrase_length = 30
        self.context = 5

        self.nlp = helpers.get_spacy_model(self.spacy_model_name)

        try:
            self.model_file = self.config["chiasmus model file"]
        except:
            self.model_file = "chiasmus_default.pkl"
        self.model_file = os.path.join(check_configs.get_data_path(), self.model_file)


    def __call__(self, text, top=-1):
        """
        Detects Chiasmus phrases in the text.
        :param text: text to be processed
        :param top: number of top candidates to be returned, -1 for all
        :return: list of Chiasmus phrases
        """

        print("processing text...")
        tokens, pos, lemmas, dep, vectors = self.process_text(text)
        print("done")

        print("finding candidates...")
        candidates = self.get_candidates(pos)
        print(f"{len(candidates)} candidates found")
        print("done")

        if len(candidates) == 0:
            return []


        features = []
        print("calculating features...")
        for candidate in tqdm(candidates):
            features.append(self.get_features(candidate, tokens, pos, lemmas, dep, vectors))
        print("done")

        print("loading model...")
        with open(self.model_file, 'rb') as f:
            model = pickle.load(f)
        print("done")
        
        print("predicting...")
        score = model.decision_function(features)
        print("done")

        print("sorting...")
        indices = np.argsort(score)[::-1]
        candidates = [candidates[i] for i in indices]
        score = [float(score[i]) for i in indices]
        print("done")

        cdict = self.candidates_to_dict(candidates, tokens, pos, lemmas, dep, vectors, score)
        if top > 0:
            cdict = cdict[:top]
        return cdict


    def candidates_to_dict(self, candidates, tokens, pos, lemmas, dep, vectors, score):
        """
        Converts the list of candidates into a dictionary list.
        """

        candidates_return = []
        for i in range(len(candidates)):
            s = max(0, candidates[i][0]-self.context)
            e = min(len(tokens), candidates[i][3]+self.context)
            candidate = {}
            candidate['candidate'] = candidates[i]
            candidate['score'] = score[i]
            candidate['main tokens'] = [tokens[c] for c in candidates[i]]
            candidate['main pos'] = [pos[c] for c in candidates[i]]
            candidate['tokens'] = tokens[s:e]
            candidate['pos'] = pos[s:e]
            candidate['lemmas'] = lemmas[s:e]
            candidate['dep'] = dep[s:e]
            candidates_return.append(candidate)
        return candidates_return

    def process_text(self, text):
        """
        Tokenizes the text into words.
        """

        processed = self.nlp(text)
        tokens = [token.text for token in processed]
        pos = [token.pos_ for token in processed]
        lemmas = [token.lemma_ for token in processed]
        dep = [token.dep_ for token in processed]
        vectors = [token.vector for token in processed]

        return tokens, pos, lemmas, dep, vectors


    def get_candidates(self, pos):
        """
        Returns a list of potential Chiasmus phrases.
        """
        
        candidates = []
        for A in range(len(pos)-3):
            if pos[A] in self.config["chiasmus pos exclude"]:
                continue
            max_d = min(len(pos), A+self.max_phrase_length)
            for D in range(A + 3, max_d):
                if not pos[A] == pos[D]:
                    continue
                for B in range(A + 1, D):
                    if pos[B] in self.config["chiasmus pos exclude"]:
                        continue
                    for C in range(B + 1, D-1):
                        if not pos[B] == pos[C]:
                            continue
                        candidates.append([A, B, C, D])
        return candidates

    def get_features(self, candidate, tokens, pos, lemmas, dep, vectors):
        return np.concatenate([
            self.get_dubremetz_features(candidate, tokens, pos, dep, lemmas, vectors),
            ])


    def global_to_local(self, values, candidate):
        s = max(0, candidate[0]-self.context)
        e = min(len(values), candidate[3]+self.context)

        values_r = values[s:e]
        candidate_r = [c-s for c in candidate]
        return values_r, candidate_r


    def get_dubremetz_features(self, candidate_global, tokens_global, pos_global, lemmas_global, dep_global, vectors_global):


        tokens, candidate = self.global_to_local(tokens_global, candidate_global)
        pos, candidate = self.global_to_local(pos_global, candidate_global)
        lemmas, candidate = self.global_to_local(lemmas_global, candidate_global)
        dep, candidate = self.global_to_local(dep_global, candidate_global)
        vectors, candidate = self.global_to_local(vectors_global, candidate_global)


        try:
            neglist = self.config["negations"]
        except:
            neglist = []
        try:
            conjlist = self.config["conjugations"]
        except:
            conjlist = []

        features = []

        
        hardp_list = ['.', '(', ')', "[", "]"] 
        softp_list = [',', ';']

         # Basic

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate[0]+1 : candidate[1] ]: num_punct+=1
            if h in tokens[ candidate[2]+1 : candidate[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate[0]+1 : candidate[1] ]: num_punct+=1
            if h in tokens[ candidate[2]+1 : candidate[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate[1]+1 : candidate[2] ]: num_punct+=1
        features.append(num_punct)

        rep_a1 = -1
        if lemmas[candidate[0]] == lemmas[candidate[3]]:
            rep_a1 -= 1
        rep_a1 += lemmas.count(lemmas[candidate[0]])
        features.append(rep_a1)

        rep_b1 = -1
        if lemmas[candidate[1]] == lemmas[candidate[2]]:
            rep_b1 -= 1
        rep_b1 += lemmas.count(lemmas[candidate[1]])
        features.append(rep_b1)

        rep_b2 = -1
        if lemmas[candidate[1]] == lemmas[candidate[2]]:
            rep_b2 -= 1
        rep_b2 += lemmas.count(lemmas[candidate[2]])
        features.append(rep_b2)

        rep_a2 = -1
        if lemmas[candidate[0]] == lemmas[candidate[3]]:
            rep_a2 -= 1
        rep_a2 += lemmas.count(lemmas[candidate[3]])
        features.append(rep_b2)

        # Size

        diff_size = abs((candidate[1]-candidate[0]) - (candidate[3]-candidate[2]))
        features.append(diff_size)

        toks_in_bc = candidate[3]-candidate[1]
        features.append(toks_in_bc)

        # Similarity

        exact_match = ([" ".join(tokens[candidate[0]+1 : candidate[1]])] == [" ".join(tokens[candidate[2]+1 : candidate[3]])])
        features.append(exact_match)

        same_tok = 0
        for l in lemmas[candidate[0]+1 : candidate[1]]:
            if l in lemmas[candidate[2]+1 : candidate[3]]: same_tok += 1
        features.append(same_tok)

        sim_score = same_tok / (candidate[1]-candidate[0])
        features.append(sim_score)

        num_bigrams = 0
        t1 = " ".join(tokens[candidate[0]+1 : candidate[1]])
        t2 = " ".join(tokens[candidate[2]+1 : candidate[3]])
        s1 = set()
        s2 = set()
        for t in range(len(t1)-1):
            bigram = t1[t:t+2]
            s1.add(bigram)
        for t in range(len(t2)-1):
            bigram = t2[t:t+2]
            s2.add(bigram)
        for b in s1:
            if b in s2: num_bigrams += 1
        bigrams_normed = (num_bigrams/max(len(s1)+1, len(s2)+1))
        features.append(bigrams_normed)

        num_trigrams = 0
        t1 = " ".join(tokens[candidate[0]+1 : candidate[1]])
        t2 = " ".join(tokens[candidate[2]+1 : candidate[3]])
        s1 = set()
        s2 = set()
        for t in range(len(t1)-2):
            trigram = t1[t:t+3]
            s1.add(trigram)
        for t in range(len(t2)-2):
            trigram = t2[t:t+3]
            s2.add(trigram)
        for t in s1:
            if t in s2: num_trigrams += 1
        trigrams_normed = (num_trigrams/max(len(s1)+1, len(s2)+1))
        features.append(trigrams_normed)

        same_cont = 0
        t1 = set(tokens[candidate[0]+1:candidate[1]])
        t2 = set(tokens[candidate[2]+1:candidate[3]])
        for t in t1:
            if t in t2: same_cont += 1
        features.append(same_cont)

        # Lexical clues

        conj = 0
        for c in conjlist:
            if c in tokens[candidate[1]+1:candidate[2]]+lemmas[candidate[1]+1:candidate[2]]:
                conj = 1
        features.append(conj)


        neg = 0
        for n in neglist:
            if n in tokens[candidate[1]+1:candidate[2]]+lemmas[candidate[1]+1:candidate[2]]:
                neg = 1
        features.append(neg)


        # Dependency score

        if dep[candidate[1]] == dep[candidate[3]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate[0]] == dep[candidate[2]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate[1]] == dep[candidate[2]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate[0]] == dep[candidate[3]]:
            features.append(1)  
        else: 
            features.append(0)

        # Return
        return np.asarray(features)


def train_model(training_file = "", language = "de"):
    """
    Trains the default model.
    """

    training_folder = "chiasmus_training"
    # create the training folder if it does not exist
    if not os.path.exists(training_folder):
        os.makedirs(training_folder)


    if training_file == "":
        # download the training data
        from urllib.request import urlretrieve
        json_file = os.path.join(training_folder, 'train.json')
        urlretrieve(
            "https://raw.githubusercontent.com/cvjena/chiasmus-annotations/main/data/data.json",
            json_file)

        data = json.load(open(json_file))
    else:
        data = json.load(open(training_file))


    cd = ChiasmusDetector(language = language)
    cd.context = 10



    # get the features
    features = []
    y = []
    positive_annotations = ['a', 'fa', 'c', 'fc']
    for d in tqdm(data):
        tokens = d['tokens']
        lemmas = d['lemmas']
        pos = d['pos']
        dep = d['dep']
        candidate = [i-d['cont_ids'][0] for i in d['ids']]

        #vectors = [cd.nlp([t][0]).vector for t in tokens]
        vectors = []
        features.append(cd.get_features(candidate, tokens, pos, lemmas, dep, vectors))
        y.append(1 if d['annotation'] in positive_annotations else 0)

        
    model = make_pipeline(
            StandardScaler(),
            LogisticRegression(
                class_weight = "balanced",
                max_iter = 1000,
                C = 1
                )
            )


    model.fit(features, y)
    scores = average_precision_score(y, model.predict(features))
    print("training summary:")
    print("average precision: ", scores)


    # save the model
    model_file = os.path.join(check_configs.get_data_path(), "chiasmus_default.pkl")
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    print("model saved to", model_file)


    # delete all files in the training folder
    # for f in os.listdir(training_folder):
    #     os.remove(os.path.join(training_folder, f))
    # # delete the training folder
    # if os.path.exists(training_folder):
    #     os.rmdir(training_folder)




def main():
    """
    Runs the program.
    """
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true', help='train model')
    parser.add_argument('--lang', type=str, default="de", help='language')
    parser.add_argument('--data', type=str, default="", help='training data json')
    args = parser.parse_args()

    if args.train:
        train_model(args.data, args.lang)
        return


    text = 'Lang ist der Tag, die Nacht ist kurz'
    cd = ChiasmusDetector("de")
    print(json.dumps(cd(text), indent=4))

if __name__ == '__main__':
    train_model()
    main()
