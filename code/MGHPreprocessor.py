#import cltk
import numpy as np


class MGHPreprocessor:
    def __init__(self):
        print("Not implemented yet")
        pass

    # make class callable with ()
    def __call__(self, text):
        self.text = text
        print("Not implemented yet")
        return [MGHToken(token) for token in text.split()]

class MGHToken:
    def __init__(self, text):
        self.text = text
        self.pos_ = ""
        self.lemma_ = ""
        self.dep_ = ""
        self.vector = np.zeros(300)
        self.idx = 0
