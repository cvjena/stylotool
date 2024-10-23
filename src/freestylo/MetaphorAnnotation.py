import numpy as np
import torch
import freestylo.SimilarityNN as SimilarityNN
from freestylo.TextObject import TextObject
from freestylo.Configs import get_model_path


# TODO: automatically select cuda device

class MetaphorAnnotation:
    def __init__(self, text):
        self.text = text
        text.annotations.append(self)
        self.candidates = []
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.type = "metaphor"
        self.model = None

    def find_candidates(self):
        pos = self.text.pos
        for i in range(len(pos)-1):
            if pos[i] == "ADJ" and pos[i+1] == "NOUN":
                self.candidates.append(MetaphorCandidate(i, i+1))

    def serialize(self) -> list:
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "adjective": c.adj_id,
                "noun": c.noun_id,
                "score": c.score})
        return candidates


    def load_model(self, model_path):
        model_path = get_model_path(model_path)
        self.model = SimilarityNN.SimilarityNN(300, 128, 1, 128, self.device)
        self.model.load_state_dict(torch.load(model_path, weights_only=True))
        self.model = self.model.to(self.device)
        self.model.eval()

    def get_vectors(self):
        adj_vectors = []
        noun_vectors = []
        for candidate in self.candidates:
            adj_vectors.append(self.text.vectors[candidate.ids[0]])
            noun_vectors.append(self.text.vectors[candidate.ids[1]])

        adj_vectors = np.array(adj_vectors)
        noun_vectors = np.array(noun_vectors)
        return adj_vectors, noun_vectors

    def score_candidates(self):
        adj_vectors, noun_vectors = self.get_vectors()
        adj_tensor = torch.tensor(adj_vectors, device=self.device).to(self.device)
        noun_tensor = torch.tensor(noun_vectors, device=self.device).to(self.device)
        assert(self.model is not None)
        adj_metaphor_tensor = self.model(adj_tensor)
        noun_metaphor_tensor = self.model(noun_tensor)
        #scores = 1-(torch.nn.CosineSimilarity()(adj_metaphor_tensor, noun_metaphor_tensor)+1)/2
        scores = cosine_distance(adj_metaphor_tensor, noun_metaphor_tensor)
        for score, candidate in zip(scores, self.candidates):
            candidate.score = score.item()

def cosine_distance(a, b):
    return 1 - torch.nn.functional.cosine_similarity(a, b)

class MetaphorCandidate():
    def __init__(self, adj_id, noun_id):
        self.ids = [adj_id, noun_id]
        self.noun_id = noun_id
        self.adj_id = adj_id
        self.score = None

        







