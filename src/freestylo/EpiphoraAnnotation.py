
from freestylo.TextObject import TextObject

"""
this class is used to find polysyndeton candidates in a text.
it uses the textobject class to store the text and its annotations.
"""

class EpiphoraAnnotation:
    def __init__(self, text : TextObject, min_length=2, conj = ["and", "or", "but", "nor"], punct_pos="PUNCT"):
        """
        Constructor for the EpiphoraAnnotation class.
        @param text: TextObject stores the text and its annotations
        """

        self.text = text
        self.candidates = []
        self.min_length = min_length
        self.conj = conj
        self.punct_pos = punct_pos

    def split_in_phrases(self):
        """
        This method splits the text into phrases.
        """
            
        phrases = []
        current_start = 0
        for i, token in enumerate(self.text.tokens):
            if token in self.conj or self.text.pos[i] == self.punct_pos:
                if i-current_start > 2:
                    phrases.append([current_start, i])
                    current_start = i+1
        phrases.append([current_start, len(self.text.tokens)])
        return phrases


    def find_candidates(self):
        """
        This method finds epiphora candidates in the text.
        """
        candidates = []
        current_candidate = EpiphoraCandidate([], "")
        phrases = self.split_in_phrases()
        for phrase in phrases:
            word = self.text.tokens[phrase[1]-1]
            if word != current_candidate.word:
                if len(current_candidate.ids) >= self.min_length:
                    candidates.append(current_candidate)
                current_candidate = EpiphoraCandidate([phrase], word)
            else:
                current_candidate.ids.append(phrase)
        self.candidates = candidates

    def serialize(self) -> list:
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "length": c.length,
                "word": c.word})
        return candidates


class EpiphoraCandidate():
    def __init__(self, ids, word):
        self.ids = ids
        self.word = word

    @property
    def score(self):
        return len(self.ids)
