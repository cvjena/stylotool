from freestylo.TextObject import TextObject

"""
This class is used to find alliterations candidates in a text.
It uses the TextObject class to store the text and its annotations.
"""

class AlliterationAnnotation:
    def __init__(self, text : TextObject, max_skip = 2, min_length=3, skip_tokens=[".", ",", ":", ";", "!", "?", "…", "(", ")", "[", "]", "{", "}", "„", "“", "‚", "‘:", "‘", "’"]):
        """
        Constructor for the AlliterationAnnotation class.
        @param text: TextObject stores the text and its annotations
        """

        self.text = text
        self.candidates = []
        self.max_skip = max_skip
        self.min_length = min_length
        self.skip_tokens = skip_tokens


    def find_candidates(self):
        """
        This method finds alliteration candidates in the text.
        """
        tokens = self.text.tokens

        open_candidates = {}
        i = 0

        for i in range(len(tokens)):
            token = tokens[i]
            token_char = token[0].lower()
            # check if there is an  alliteration candidate with the current character
            if not token_char.isalpha():
                continue
            # if not, create a new one
            if token_char not in open_candidates:
                open_candidates[token_char] = [AlliterationCandidate([i], token_char), 0]
                continue
            # if yes, add the current token to the candidate
            candidate = open_candidates[token_char][0]
            candidate.ids.append(i)

            # close candidates
            keys_to_delete = []
            for key in open_candidates:
                candidate_pair = open_candidates[key]
                candidate = candidate_pair[0]
                if token_char in self.skip_tokens:
                    candidate_pair[1] += 1
                if i - candidate.ids[-1] >= self.max_skip+1+candidate_pair[1]:
                    if len(candidate.ids) > self.min_length:
                        self.candidates.append(candidate)
                    keys_to_delete.append(key)
            for key_del in keys_to_delete:
                    del open_candidates[key_del]
        # get the remaining ones
        for key in open_candidates:
            candidate = open_candidates[key][0]
            if len(candidate.ids) > self.min_length:
                self.candidates.append(candidate)



    def serialize(self) -> list:
        candidates = []
        for c in self.candidates:
            candidates.append({
                "ids": c.ids,
                "length": c.length,
                "char": c.char})
        return candidates


class AlliterationCandidate():
    def __init__(self, ids, char):
        self.ids = ids
        self.char = char

    @property
    def score(self):
        return len(self.ids)

    @property
    def length(self):
        return len(self.ids)
