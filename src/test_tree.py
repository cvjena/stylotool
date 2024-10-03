import spacy
from nltk import Tree

nlp = spacy.load('en_core_web_sm')

text = ("This is a word, and this is another word, finally this is the last word or is this one the final word? This is the next sentence.")
doc = nlp(text)

#def to_nltk_tree(node):
#    if node.n_lefts + node.n_rights > 0:
#        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
#    else:
#        return node.orth_


#[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]



def get_phrases(doc):
    conj = ["and", "or", "but", "nor", "so", "yet"]
    phrases = []

    current_start = 0
    current_end = -1
    for i, token in enumerate(doc):
        if token.text in conj or token.dep_ == "punct":
            if i-current_start > 2:
                phrases.append([current_start, i])
                current_start = i+1
    phrases.append([current_start, len(doc)])
    return phrases

def get_candidates(doc, phrases):
    candidates = []
    current_candidate = []
    current_word = ""
    for phrase in phrases:
        word = doc[phrase[1]-1].text
        print(phrase, word)
        if word != current_word:
            print(word, current_word)
            if len(current_candidate) > 1:
                candidates.append(current_candidate)
            current_candidate = [phrase]
            current_word = word
        elif word == current_word:
            current_candidate.append(phrase)
    return candidates

phrases = get_phrases(doc)

for phrase in phrases:
    print(doc[phrase[0]:phrase[1]])

candidates = get_candidates(doc, phrases)

for candidate in candidates:
    print(candidate)



