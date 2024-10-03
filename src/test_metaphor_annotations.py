import TextObject as to
import MetaphorAnnotation as ma
import TextPreprocessor as tp
import numpy as np



def test_metaphor_annotation():
    text = to.TextObject(
            textfile = "../datasets/tests/metaphortest.txt",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)


    metaphor = ma.MetaphorAnnotation(
            text=text)
    metaphor.find_candidates()
    metaphor.load_model("../models/metaphor_de.pkl")
    metaphor.score_candidates()

    scores = [c.score for c in metaphor.candidates]
    indices = np.argsort(scores)[::-1]

    best_candidate = metaphor.candidates[indices[0]]
    #best_tokens = " ".join(text.tokens[best_candidate.A:best_candidate.A_+1])
    #assert(best_tokens == "Wörter gibt es häufig , doch selten gibt es Beispiele")

    #assert(scores[indices[0]] > 0)
    #assert(scores[indices[1]] < 0)

    


    for candidate in metaphor.candidates:
        print(" ".join(text.tokens[candidate.A:candidate.A_+1]))
        print(" ".join(text.pos[candidate.A:candidate.A_+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")

    text.serialize("../datasets/tests/test_metaphor_annotation.json")



if __name__ == "__main__":
    test_chiasmus_annotation()


