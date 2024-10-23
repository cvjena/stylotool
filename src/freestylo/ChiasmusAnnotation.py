from freestylo.TextObject import TextObject
from freestylo.Configs import get_model_path
import numpy as np

"""
This class is used to find chiasmus candidates in a text.
It uses the TextObject class to store the text and its annotations.
"""
class ChiasmusAnnotation:
    """
    Constructor for the ChiasmusAnnotation class.
    @param text: TextObject stores the text and its annotations
    @param window_size: int size of the window to search for chiasmus candidates
    """
    def __init__(self, text : TextObject, window_size=30):
        self.text = text
        text.annotations.append(self)
        self.window_size = window_size
        self.candidates = []
        self.denylist = []
        self.allowlist = []
        self.neglist = []
        self.poslist = []
        self.conjlist = []
        self.type = "chiasmus"
        self.model = None


    """
    This method finds chiasmus candidates in the text.
    It uses the window_size to search for candidates.
    """
    def find_candidates(self):
        pos = self.text.pos

        outer_matches = []
        for i in range(len(pos)):
            outer_matches += self._find_matches(i, i + self.window_size)

        for match in outer_matches:
            A, A_ = match
            start_inner = A + 1
            inner_matches = self._find_matches(start_inner, A_)
            for B, B_ in inner_matches:
                self.candidates.append(ChiasmusCandidate(A, B, B_, A_))

    def load_classification_model(self, model_path):
        import pickle
        with open(get_model_path(model_path), "rb") as f:
            self.model = pickle.load(f)

    def serialize(self) -> list:
        candidates = []
        for c in self.candidates:
            candidates.append({
        "ids": c.ids,
        "A": c.A,
        "B": c.B,
        "B_": c.B_,
        "A_": c.A_,
        "score": c.score})
        return candidates

        
        
    
    """
    This method finds matches in the pos list of the text.
    It uses the start and end index to search for matches.
    @param start: int start index of the search
    @param end: int end index of the search
    @return list of matches
    """
    def _find_matches(self, start : int, end : int) -> list:
        pos = self.text.pos

        #if end > len(pos):
        #    end = len(pos)

        #if end < start+3:
        #    return []

        if not self._check_pos(pos[start]):
            return []
        matches = []
        for i in range(start+1, end):
            try:
                if pos[start] == pos[i]:
                    matches.append((start, i))
            except IndexError:
                pass
        return matches

    """
    This method checks if a pos is in the allowlist or not in the denylist.
    @param pos: str pos to check
    @return bool True if pos is in allowlist or not in denylist, False otherwise
    """
    def _check_pos(self, pos):
        if len(self.allowlist) > 0 and pos not in self.allowlist:
            return False
        if len(self.denylist) > 0 and pos in self.denylist:
            return False
        return True

    """
    This method checks if the text has chiasmus candidates.
    @return bool True if there are candidates, False otherwise
    """
    def has_candidates(self):
        return len(self.candidates) > 0

    """
    This method scores the chiasmus candidates.
    """
    def score_candidates(self):
        features = []
        for candidate in self.candidates:
            features.append(self.get_features(candidate))
        if self.model is None:
            print("Load Chiasmus Model before scoring the candidates")
            return False
        features = np.stack(features)
        scores = self.model.decision_function(features)
        for score, candidate in zip(scores, self.candidates):
            candidate.score = score
        return True

    """
    This method ranks a chiasmus candidate.
    @param candidate: ChiasmusCandidate candidate to rank
    """
    def score_candidate(self, candidate):

        features = get_features(candidate)

    def get_features(self, candidate):
        dubremetz_features = self.get_dubremetz_features(candidate)
        lexical_features = self.get_lexical_features(candidate)
        semantic_features = self.get_semantic_features(candidate)
        return np.concatenate((dubremetz_features, lexical_features, semantic_features))

    def get_dubremetz_features(self, candidate):

        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        tokens_main = [tokens[i] for i in range(candidate.A, candidate.A_+1)]
        lemmas_main = [lemmas[i] for i in range(candidate.A, candidate.A_+1)]
        pos_main = [pos[i] for i in range(candidate.A, candidate.A_+1)]
        dep_main = [dep[i] for i in range(candidate.A, candidate.A_+1)]
        vectors_main = [vectors[i] for i in range(candidate.A, candidate.A_+1)]

        neglist = self.neglist
        poslist = self.poslist
        conjlist = self.conjlist

        hardp_list = ['.', '(', ')', "[", "]"] 
        softp_list = [',', ';']

        features = []

         # Basic

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[0]+1 : candidate.ids[1] ]: num_punct+=1
            if h in tokens[ candidate.ids[2]+1 : candidate.ids[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[0]+1 : candidate.ids[1] ]: num_punct+=1
            if h in tokens[ candidate.ids[2]+1 : candidate.ids[3] ]: num_punct+=1
        features.append(num_punct)

        num_punct = 0
        for h in hardp_list:
            if h in tokens[ candidate.ids[1]+1 : candidate.ids[2] ]: num_punct+=1
        features.append(num_punct)

        rep_a1 = -1
        if lemmas[candidate.ids[0]] == lemmas[candidate.ids[3]]:
            rep_a1 -= 1
        rep_a1 += lemmas.count(lemmas[candidate.ids[0]])
        features.append(rep_a1)

        rep_b1 = -1
        if lemmas[candidate.ids[1]] == lemmas[candidate.ids[2]]:
            rep_b1 -= 1
        rep_b1 += lemmas.count(lemmas[candidate.ids[1]])
        features.append(rep_b1)

        rep_b2 = -1
        if lemmas[candidate.ids[1]] == lemmas[candidate.ids[2]]:
            rep_b2 -= 1
        rep_b2 += lemmas.count(lemmas[candidate.ids[2]])
        features.append(rep_b2)

        rep_a2 = -1
        if lemmas[candidate.ids[0]] == lemmas[candidate.ids[3]]:
            rep_a2 -= 1
        rep_a2 += lemmas.count(lemmas[candidate.ids[3]])
        features.append(rep_b2)

        # Size

        diff_size = abs((candidate.ids[1]-candidate.ids[0]) - (candidate.ids[3]-candidate.ids[2]))
        features.append(diff_size)

        toks_in_bc = candidate.ids[3]-candidate.ids[1]
        features.append(toks_in_bc)

        # Similarity

        exact_match = ([" ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])] == [" ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])])
        features.append(exact_match)

        same_tok = 0
        for l in lemmas[candidate.ids[0]+1 : candidate.ids[1]]:
            if l in lemmas[candidate.ids[2]+1 : candidate.ids[3]]: same_tok += 1
        features.append(same_tok)

        sim_score = same_tok / (candidate.ids[1]-candidate.ids[0])
        features.append(sim_score)

        num_bigrams = 0
        t1 = " ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])
        t2 = " ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])
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
        t1 = " ".join(tokens[candidate.ids[0]+1 : candidate.ids[1]])
        t2 = " ".join(tokens[candidate.ids[2]+1 : candidate.ids[3]])
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
        t1 = set(tokens[candidate.ids[0]+1:candidate.ids[1]])
        t2 = set(tokens[candidate.ids[2]+1:candidate.ids[3]])
        for t in t1:
            if t in t2: same_cont += 1
        features.append(same_cont)

        # Lexical clues

        conj = 0
        for c in conjlist:
            if c in tokens[candidate.ids[1]+1:candidate.ids[2]]+lemmas[candidate.ids[1]+1:candidate.ids[2]]:
                conj = 1
        features.append(conj)


        neg = 0
        for n in neglist:
            if n in tokens[candidate.ids[1]+1:candidate.ids[2]]+lemmas[candidate.ids[1]+1:candidate.ids[2]]:
                neg = 1
        features.append(neg)


        # Dependency score

        if dep[candidate.ids[1]] == dep[candidate.ids[3]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate.ids[0]] == dep[candidate.ids[2]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate.ids[1]] == dep[candidate.ids[2]]:
            features.append(1)  
        else: 
            features.append(0)

        if dep[candidate.ids[0]] == dep[candidate.ids[3]]:
            features.append(1)  
        else: 
            features.append(0)

        features = np.array(features)
        return features

    def get_lexical_features(self, candidate):
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        lemmas_main = [lemmas[i] for i in candidate.ids]


        neglist = self.neglist
        poslist = self.poslist

        features = []

        
        for i in range(len(lemmas_main)):
            for j in range(i+1, len(lemmas_main)):
                if lemmas_main[i] == lemmas_main[j]:
                    features.append(1)
                else:
                    features.append(0)

        features = np.array(features)
        return features

    def get_semantic_features(self, candidate):
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        vectors_main = [vectors[i] for i in candidate.ids]


        features = []
        for i in range(len(vectors_main)):
            for j in range(i+1, len(vectors_main)):
                features.append(cosine_similarity(vectors_main[i], vectors_main[j]))

        features = np.array(features)
        return features



def cosine_similarity(vec1, vec2):
    result = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    if np.isnan(result):
        result = 0
    return result


class ChiasmusCandidate:
    def __init__(self, A, B, B_, A_):
        self.ids = [A, B, B_, A_]
        self.A = A
        self.B = B
        self.B_ = B_
        self.A_ = A_
        self.score = None

    def __str__(self):
        return f"{self.A} {self.B} {self.B_} {self.A_}"


