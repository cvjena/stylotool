from TextObject import TextObject

"""
This class is used to find alliterations candidates in a text.
It uses the TextObject class to store the text and its annotations.
"""

class AlliterationAnnotation:
    def __init__(self, text : TextObject):
        """
        Constructor for the AlliterationAnnotation class.
        @param text: TextObject stores the text and its annotations
        """

        self.text = text
        self.instances = []


    def find_instances(self):
        """
        This method finds alliteration instances in the text.
        """
        tokens = self.text.tokens
        pos = self.text.pos
        current_char = ""
        current_begin = None
        current_end = None

        for i in range(len(tokens)):
            token_char = tokens[i][0].lower()
            if token_char == current_char:
                current_end = i
            else:
                if current_char != "" and current_end is not None and current_begin is not None:
                    if current_end - current_begin > 1:
                        self.instances.append(((current_begin, current_end), current_char))
                current_char = token_char
                current_begin = i
                current_end = i

        # sort instances by length
        self.instances.sort(key=lambda x: x[0][1] - x[0][0], reverse=True)

