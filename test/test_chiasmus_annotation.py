import freestylo.ChiasmusAnnotation as ca
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp
import numpy as np
import os


def test_chiasmus_annotation():
    text = to.TextObject(
            text = """Wörter gibt es häufig, doch selten gibt es Beispiele.
Das ist noch ein Satz mit einem schönen Adjektiv.""",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)


    chiasmus = ca.ChiasmusAnnotation(
            text=text)
    chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
    chiasmus.find_candidates()
    chiasmus.load_classification_model(os.path.expanduser("chiasmus_de.pkl"))
    chiasmus.score_candidates()

    scores = [c.score for c in chiasmus.candidates]
    indices = np.argsort(scores)[::-1]

    best_candidate = chiasmus.candidates[indices[0]]
    best_tokens = " ".join(text.tokens[best_candidate.A:best_candidate.A_+1])
    assert(best_tokens == "Wörter gibt es häufig , doch selten gibt es Beispiele")

    assert(scores[indices[0]] > 0)
    assert(scores[indices[1]] < 0)

    


    for candidate in chiasmus.candidates:
        print(" ".join(text.tokens[candidate.A:candidate.A_+1]))
        print()
        print(" ".join(text.pos[candidate.A:candidate.A_+1]))
        print()
        print("tokens:", " ".join([text.tokens[i] for i in candidate.ids]))
        print("pos:", " ".join([text.pos[i] for i in candidate.ids]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")




if __name__ == "__main__":
    test_chiasmus_annotation()


