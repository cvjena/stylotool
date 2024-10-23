import freestylo.TextObject as to
import freestylo.PolysyndetonAnnotation as pa
import freestylo.TextPreprocessor as tp
import numpy as np



def test_polysyndeton_annotation():
    text = to.TextObject(
            text = "Yesterday I wrote, and read, and then I slept, and then I woke up, and then I wrote again. This is a sentence. This is another sentence, and a short one at that.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="en")
    preprocessor.process_text(text)

    polysysndeton = pa.PolysyndetonAnnotation(
            text = text,
            min_length = 2,
            conj = ["and", "or", "but", "nor"])

    polysysndeton.find_candidates()


    candidate = polysysndeton.candidates[0]
    assert(len(polysysndeton.candidates) == 1)
    assert(len(candidate.ids) == 4)
    assert(candidate.word == "and")


    


    for candidate in polysysndeton.candidates:
        print(" ".join(text.tokens[candidate.ids[0][0]:candidate.ids[-1][-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")


if __name__ == "__main__":
    test_polysyndeton_annotation()


