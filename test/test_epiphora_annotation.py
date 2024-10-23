import freestylo.TextObject as to
import freestylo.EpiphoraAnnotation as ea
import freestylo.TextPreprocessor as tp
import numpy as np



def test_epiphora_annotation():
    text = to.TextObject(
            text = "Yesterday I thought of the paper, then I wrote the paper, now I am publishing the paper. I also write another sentence, that consists of mulitple phrases, they all have different endings.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="en")
    preprocessor.process_text(text)

    epiphora = ea.EpiphoraAnnotation(
            text = text,
            min_length = 2,
            conj = ["and", "or", "but", "nor"])

    epiphora.find_candidates()


    candidate = epiphora.candidates[0]

    assert(len(epiphora.candidates) == 1)
    assert(len(candidate.ids) == 3)

    for candidate in epiphora.candidates:
        print(" ".join(text.tokens[candidate.ids[0][0]:candidate.ids[-1][-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")


if __name__ == "__main__":
    test_epiphora_annotation()


