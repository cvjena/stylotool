import TextObject as to
import PolysyndetonAnnotation as pa
import TextPreprocessor as tp
import numpy as np



def test_polysyndeton_annotation():
    text = to.TextObject(
            text = "Yesterday I wrote, and read, and then I slept, and then I woke up, and then I wrote again. This is a sentence. This is another sentence.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="en")
    preprocessor.process_text(text)

    polysysndeton = pa.PolysyndetonAnnotation(
            text = text,
            min_length = 2,
            conj = ["and", "or", "but", "nor"])

    polysysndeton.find_candidates()


    scores = [c.score for c in polysysndeton.candidates]
    indices = np.argsort(scores)[::-1]

    


    for candidate in polysysndeton.candidates:
        print(" ".join(text.tokens[candidate.ids[0][0]:candidate.ids[-1][-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")

    #text.serialize("../datasets/tests/test_metaphor_annotation.json")



if __name__ == "__main__":
    test_polysyndeton_annotation()


