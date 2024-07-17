from TextObject import TextObject
from TextPreprocessor import TextPreprocessor

import os
import json

def test_processing():
    text = TextObject(language='en')
    text.text = "This is a test sentence. This is another test sentence."
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 12
    assert len(text.lemmas) == 12
    assert len(text.vectors) == 12

    try:
        os.mkdir("test")
    except:
        pass

    text.serialize("test/test_text.json")

    with open("test/test_text.json", 'r') as f:
        data = json.load(f)


    assert data['tokens'] == text.tokens
    assert data['lemmas'] == text.lemmas
    assert data['pos'] == text.pos


    text = TextObject(language='de')
    text.text = "Das ist ein Test Satz. Das ist noch ein Test Satz."
    preprocessor = TextPreprocessor()
    preprocessor.process_text(text)
    assert text.has_tokens() == True
    assert len(text.tokens) == 13
    assert len(text.lemmas) == 13
    assert len(text.vectors) == 13

    try:
        os.mkdir("test")
    except:
        pass

    text.serialize("test/test_text_de.json")

    with open("test/test_text_de.json", 'r') as f:
        data = json.load(f)


    assert data['tokens'] == text.tokens
    assert data['lemmas'] == text.lemmas
    assert data['pos'] == text.pos
