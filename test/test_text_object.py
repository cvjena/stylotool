from freestylo.TextObject import TextObject
from freestylo.TextPreprocessor import TextPreprocessor
from freestylo.MGHPreprocessor import MGHPreprocessor

import os
import json

def test_processing():
    text = TextObject(text="This is a test sentence. This is another test sentence.", language='en')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 12
    assert len(text.lemmas) == 12
    assert len(text.vectors) == 12
    print(text.tokens)


    text = "Das ist ein Test Satz. Das ist noch ein Test Satz."
    text = TextObject(text=text, language='de')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 13
    assert len(text.lemmas) == 13
    assert len(text.vectors) == 13
    print(text.tokens)

    text = "Dô erbiten si der nahte und fuoren über Rîn"
    text = TextObject(text=text, language='mgh')
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert(len(text.tokens) == 9)
    assert(len(text.lemmas) == 9)
    assert(len(text.vectors) == 9)
    assert(text.has_tokens())
    assert(text.tokens[1] == "erbiten")
    assert(text.pos[1] == "VERB")
    print(text.tokens)



if __name__ == "__main__":
    test_processing()
