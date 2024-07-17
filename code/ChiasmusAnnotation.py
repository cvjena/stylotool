from TextObject import TextObject

"""
This class is used to find chiasmus candidates in a text.
It uses the TextObject class to store the text and its annotations.
"""
class ChiasmusAnnotation:
    """
    Constructor for the ChiasmusAnnotation class.
    @param text: TextObject stores the text and its annotations
    @param window_size: int size of the window to search for chiasmus candidates
    """
    def __init__(self, text : TextObject, window_size=30):
        self.text = text
        self.window_size = window_size
        self.candidates = []
        self.blacklist = []
        self.whitelist = []


    """
    This method finds chiasmus candidates in the text.
    It uses the window_size to search for candidates.
    """
    def find_candidates(self):
        pos = self.text.pos

        outer_matches = []
        for i in range(len(pos)):
            outer_matches = self._find_matches(i, i + self.window_size)

        for match in outer_matches:
            A, A_ = match
            start_inner = A + 1
            inner_matches = self._find_matches(start_inner, A_)
            for B, B_ in inner_matches:
                self.candidates.append(ChiasmusCandidate(A, B, B_, A_))
    
    """
    This method finds matches in the pos list of the text.
    It uses the start and end index to search for matches.
    @param start: int start index of the search
    @param end: int end index of the search
    @return list of matches
    """
    def _find_matches(self, start : int, end : int) -> list:
        pos = self.text.pos

        if end > len(pos):
            end = len(pos)

        if end < start+3:
            return []

        if not self._check_pos(pos[start]):
            return []
        matches = []
        for i in range(start, end):
            if pos[start] == pos[i]:
                matches.append((start, i))
        return matches

    """
    This method checks if a pos is in the whitelist or not in the blacklist.
    @param pos: str pos to check
    @return bool True if pos is in whitelist or not in blacklist, False otherwise
    """
    def _check_pos(self, pos):
        if len(self.whitelist) > 0 and pos not in self.whitelist:
            return False
        if len(self.blacklist) > 0 and pos in self.blacklist:
            return False
        return True

    """
    This method checks if the text has chiasmus candidates.
    @return bool True if there are candidates, False otherwise
    """
    def has_candidates(self):
        return len(self.candidates) > 0

    """
    This method scores the chiasmus candidates.
    """
    def score_candidates(self):
        for candidate in self.candidates:
            self.score_candidate(candidate)

    """
    This method ranks a chiasmus candidate.
    @param candidate: ChiasmusCandidate candidate to rank
    """
    def score_candidate(self, candidate):
        print("Not implemented yet")
        tokens = self.text.tokens
        lemmas = self.text.lemmas
        pos = self.text.pos
        dep = self.text.dep
        vectors = self.text.vectors

        context_start = candidate.A - 5
        context_end = candidate.A_ + 5

        tokens_main = [tokens[i] for i in range(candidate.A, candidate.A_+1)]
        lemmas_main = [lemmas[i] for i in range(candidate.A, candidate.A_+1)]
        pos_main = [pos[i] for i in range(candidate.A, candidate.A_+1)]
        dep_main = [dep[i] for i in range(candidate.A, candidate.A_+1)]
        vectors_main = [vectors[i] for i in range(candidate.A, candidate.A_+1)]

        candidate.score = 0
        pass


class ChiasmusCandidate:
    def __init__(self, A, B, B_, A_):
        self.ids = [A, B, B_, A_]
        self.A = A
        self.B = B
        self.B_ = B_
        self.A_ = A_
        self.score = None

    def __str__(self):
        return f"{self.A} {self.B} {self.B_} {self.A_}"

