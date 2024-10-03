
from TextObject import TextObject

"""
this class is used to find polysyndeton candidates in a text.
it uses the textobject class to store the text and its annotations.
"""

class PolysyndetonAnnotation:
    def __init__(self, text : TextObject, min_length=2, conj = ["and", "or", "but", "nor"], sentence_end_tokens=[".", "?", "!", ":", ";", "..."], punct_pos="PUNCT"):
        """
        Constructor for the PolysyndetonAnnotation class.
        @param text: TextObject stores the text and its annotations
        """

        self.text = text
        self.candidates = []
        self.min_length = min_length
        self.conj = conj
        self.sentence_end_tokens = sentence_end_tokens
        self.punct_pos = punct_pos

    def split_in_phrases(self):
        """
        This method splits the text into phrases.
        """
        
        phrases_in_sentences = []
        phrases = []
        current_sentence_start = 0
        current_phrase_start = 0
        for i, token in enumerate(self.text.tokens):
            if token in self.sentence_end_tokens:
                phrases.append([current_phrase_start, i])
                current_phrase_start = i+1
                current_sentence_start = i+1
                phrases_in_sentences.append(phrases)
                phrases = []
            elif token in self.conj and i-current_phrase_start > 2:
                phrases.append([current_phrase_start, i])
                current_phrase_start = i+1
        return phrases_in_sentences

    def find_last_word_in_phrase(self, phrase):
        """
        This method finds the last word in a phrase.
        @param phrase: list of integers, the phrase
        """
        for i in range(phrase[1], phrase[0], -1):
            if self.text.pos[i] != self.punct_pos:
                return i
        return phrase[1]

    def find_candidates(self):
        """
        This method finds polysyndeton candidates in the text.
        """
        candidates = []
        sentences = self.split_in_phrases()
        for sentence in sentences:
            current_candidate = PolysyndetonCandidate([], "")
            current_word = ""
            print(sentence)
            for phrase in sentence:
                #word = self.text.tokens[phrase[1]-1]
                word = self.text.tokens[self.find_last_word_in_phrase(phrase)]
                print(phrase, word)
                if word != current_candidate.word:
                    if len(current_candidate.ids) >= self.min_length:
                        candidates.append(current_candidate)
                    current_candidate = PolysyndetonCandidate([phrase], word)
                else:
                    current_candidate.ids.append(phrase)
        self.candidates = candidates

    def serialize(self) -> list:
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "score": c.score,
                "word": c.word})
        return candidates


class PolysyndetonCandidate():
    def __init__(self, ids, word):
        self.ids = ids
        self.word = word

    @property
    def score(self):
        return len(self.ids)
