import spacy
from freestylo.TextObject import TextObject
from freestylo.MGHPreprocessor import MGHPreprocessor

"""
This class is used to preprocess text.
It uses the TextObject class to store the text and its annotations.
"""
class TextPreprocessor:
    """
    Constructor for the TextPreprocessor class.
    @param language: str language of the text
    """
    def __init__(self, language='en'):
        if language == 'en':
            self.nlp = self.load_spacy_nlp('en_core_web_lg')
        elif language == 'de':
            self.nlp = self.load_spacy_nlp('de_core_news_lg')
        elif language == 'mgh':
            from MGHPreprocessor import MGHPreprocessor
            self.nlp = MGHPreprocessor()


    def load_spacy_nlp(self, model_name):
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
        return nlp


    """
    This method processes the text and stores the annotations in the TextObject.
    @param text: TextObject stores the text and its annotations
    """
    def process_text(self, text : TextObject):
        processed = self.nlp(text.text)
        try:
            text.tokens = [token.text for token in processed]
        except:
            print("No tokens available")

        try:    
            text.pos = [token.pos_ for token in processed]
        except:
            print("No POS available")

        try:
            text.lemmas = [token.lemma_ for token in processed]
        except:
            print("No lemmas available")

        try:
            text.dep = [token.dep_ for token in processed]
        except:
            print("No dependencies available")

        try:
            text.vectors = [token.vector for token in processed]
        except:
            print("No vectors available")

        try:
            text.token_offsets = [(token.idx, token.idx + len(token.text)) for token in processed]
        except:
            print("No token offsets available")


