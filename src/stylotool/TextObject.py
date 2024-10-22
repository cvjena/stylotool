import pickle
import json

class TextObject:
    def __init__(self, textfile=None, text=None, language=''):
        self.textfile = textfile
        self.language = language
        self.tokens = []
        self.pos = []
        self.lemmas = []
        self.dep = []
        self.vectors = []
        self.annotations = []
        self.token_offsets = []
        self.text = text

        if textfile is not None:
            try:
                with open(textfile, 'r') as f:
                    self.text = f.read()
            except FileNotFoundError:
                print("File not found, no textfile loaded")
        elif text is not None:
            self.text = text

    def save_as(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def serialize(self, filename):
        with open(filename, 'w') as f:
            annotations = {}
            for anno in self.annotations:
                annotations[anno.type] = anno.serialize()
            save_dict = {
                'text': self.text,
                'tokens': self.tokens,
                'pos': self.pos,
                'lemmas': self.lemmas,
                'dep': self.dep,
                'token_offsets': self.token_offsets,
                'annotations': annotations
            }
            with open(filename, 'w') as f:
                json.dump(save_dict, f, indent=4)


    def has_text(self):
        return len(self.text) > 0
    
    def has_tokens(self):
        return len(self.tokens) > 0

    def has_pos(self):
        return len(self.pos) > 0

    def has_lemmas(self):
        return len(self.lemmas) > 0

    def has_dep(self):
        return len(self.dep) > 0

    def has_vectors(self):
        return len(self.vectors) > 0

    def has_annotations(self):
        return len(self.annotations) > 0
