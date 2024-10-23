import numpy as np
import freestylo.TextObject as to
import freestylo.TextPreprocessor as tp
import freestylo.AlliterationAnnotation as aa


def test_alliteration_annotation():
    text = to.TextObject(
            text = "Toller Text, tierisch triftige Thesen! Aber manchmal auch keine Alliteration. So muss manchem, auch manchmal, manches durchaus mächtig missfallen.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)

    alliteration = aa.AlliterationAnnotation(
            text = text,
            max_skip = 2,
            min_length = 3)

    alliteration.find_candidates()


    assert(len(alliteration.candidates) == 2)
    assert(text.tokens[alliteration.candidates[0].ids[0]] == "Toller")
    assert(text.tokens[alliteration.candidates[1].ids[0]] == "muss")
    assert(len(alliteration.candidates[0].ids) == 5)
    assert(len(alliteration.candidates[1].ids) == 6)


    


    for candidate in alliteration.candidates:
        print(" ".join(text.tokens[candidate.ids[0]:candidate.ids[-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")




if __name__ == "__main__":
    test_alliteration_annotation()


