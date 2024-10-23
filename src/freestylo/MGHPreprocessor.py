import cltk
import numpy as np

from cltk.corpus.middle_high_german.alphabet import normalize_middle_high_german
from cltk.tag.pos import POSTag
from cltk.lemmatize.middle_high_german.backoff import BackoffMHGLemmatizer



class MGHPreprocessor:
    def __init__(self):
        self.text = ""
        pass

    # make class callable with ()
    def __call__(self, text):
        self.text = normalize_middle_high_german(text)

        tokens = []

        idx = 0
        pos_tagger = POSTag('middle_high_german')
        lemmatizer = BackoffMHGLemmatizer()
        # custom tokenizer, because I need the character index of the word
        while True:
            word, next_idx = self.get_next_word(self.text, idx)

            pos = pos_tagger.tag_tnt(word)[0][1]

            lemma = min(lemmatizer.lemmatize([word])[0][1], key=len)

            dep = ""

            vector = np.zeros(300)


            tokens.append(MGHToken(word, pos, lemma, dep, vector, idx))

            if next_idx is None:
                break
            idx = next_idx
        return tokens



    def get_next_word(self, text, idx):
        cursor = idx
        is_end = False 
        #find end of current word
        while cursor < len(text):
            try:
                if text[cursor] in [" ", "\n", "\t"]:
                    break
            except: # end of text
                is_end = True
                break
            cursor += 1

        end_word = cursor

        #find start of next word
        while cursor < len(text):
            try:
                if text[cursor] not in [" ", "\n", "\t"]:
                    break
            except:
                is_end = True
                break
            cursor += 1

        next_word = cursor

        if cursor == len(text):
            next_word = None

        word = text[idx:end_word]

        return word, next_word

class MGHToken:
    def __init__(self, text, pos, lemma, dep, vector, idx):
        self.text = text
        self.pos = pos
        self.lemma = lemma
        self.dep = dep
        self.vector = vector
        self.idx = idx

