import ChiasmusAnnotation as ca
import TextObject as to
import TextPreprocessor as tp
import numpy as np


def test_chiasmus_annotation():
    text = to.TextObject(
            textfile = "../datasets/tests/chiasmustest.txt",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)


    chiasmus = ca.ChiasmusAnnotation(
            text=text)
    chiasmus.allowlist = ["NOUN", "VERB", "ADJ", "ADV"]
    chiasmus.find_candidates()
    chiasmus.load_classification_model("../models/chiasmus_de.pkl")
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

    text.serialize("../datasets/tests/test_chiasmus_annotation.json")



if __name__ == "__main__":
    test_chiasmus_annotation()


