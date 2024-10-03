import numpy as np
import torch
import SimilarityNN
from TextObject import TextObject

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
        self.model = torch.load(model_path).to(self.device)

    def get_vectors(self):
        adj_vectors = []
        noun_vectors = []
        for candidate in self.candidates:
            adj_vectors.append(self.text.vectors(candidate[0]))
            noun_vectors.append(self.text.vectors(candidate[1]))

        adj_vectors = np.array(adj_vectors)
        noun_vectors = np.array(noun_vectors)
        return adj_vectors, noun_vectors

    def score_candidates(self):
        adj_vectors, noun_vectors = self.get_vectors()
        adj_tensor = torch.tensor(adj_vectors, device=self.device)
        noun_tensor = torch.tensor(noun_vectors, device=self.device)
        assert(self.model is not None)
        adj_metaphor_tensor = self.model(adj_tensor)
        noun_metaphor_tensor = self.model(noun_tensor)
        scores = (torch.nn.CosineSimilarity()(adj_metaphor_tensor, noun_metaphor_tensor)+1)/2
        for score, candidate in zip(scores.item(), self.candidates):
            candidate.score = score

class MetaphorCandidate():
    def __init__(self, adj_id, noun_id):
        self.ids = [noun_id, adj_id]
        self.noun_id = noun_id
        self.adj_id = adj_id
        self.score = None

        







