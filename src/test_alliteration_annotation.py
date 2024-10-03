import TextObject as to
import AlliterationAnnotation as aa
import TextPreprocessor as tp
import numpy as np



def test_alliteration_annotation():
    text = to.TextObject(
            text = "Toller Text, tierisch triftige Thesen! Aber manchmal auch keine Alliteration. So muss manchem, auch manchmal, manches missfallen.",
            language="de")
    preprocessor = tp.TextPreprocessor(language="de")
    preprocessor.process_text(text)

    alliteration = aa.AlliterationAnnotation(
            text = text,
            max_skip = 2,
            min_length = 3)

    alliteration.find_candidates()


    scores = [c.score for c in alliteration.candidates]
    indices = np.argsort(scores)[::-1]

    


    for candidate in alliteration.candidates:
        print(" ".join(text.tokens[candidate.ids[0]:candidate.ids[-1]+1]))
        print("ids", candidate.ids)
        print("score:", candidate.score)
        print("")
        print("")
        print("")

    #text.serialize("../datasets/tests/test_metaphor_annotation.json")



if __name__ == "__main__":
    test_alliteration_annotation()


