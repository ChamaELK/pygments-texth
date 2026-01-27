import nltk 

"""
import nlp 
import nltk
text = "The discount is 10% for 4$ in US dollars in \"Gen Z\" "

brown_tagged_sents = nltk.corpus.brown.tagged_sents(categories='news')
tree = nlp.tree(text,brown_tagged_sents )
for node in tree: 
    print(node)
"""
def tree(text,backoff_tagger):
    tokens = nltk.word_tokenize(text)
    tagger = nltk.RegexpTagger(
        [(r'^%$', 'PCT'),
        (r'\d+(?:\.\d+)?','NUMBER'),
        (r'^(?:[A-Z]\.)+[A-Z]\.?|[A-Z]{2,}$', 'ABR'),
        (r'^\$$', 'CURR')],
        backoff=backoff_tagger)
    
    tags = tagger.tag(tokens)
    kv_grammar = [
        ("PERCENT", "<NUMBER><PCT>"),
        ("CURRENCY", "<NUMBER><CURR>"),
        ("NP", "<AT>?<JJ>*<NN>+")
    ]

    grammar = "\n".join([f"{label}: {{ {pattern} }}" for label, pattern in kv_grammar])
    chunker = nltk.RegexpParser(grammar)
    tree = chunker.parse(tags)
    return tree



# ANSI color codes
COLORS = {
    "NP": "\033[94m",        # Blue
    "PERCENT": "\033[92m",   # Green
    "CURRENCY": "\033[91m",  # Red
    "RESET": "\033[0m"
}

def colorize_tree(tree):
    """Prints a chunk tree with different colors for each chunk type."""
    for subtree in tree:
        if isinstance(subtree, nltk.Tree):
            color = COLORS.get(subtree.label(), COLORS["RESET"])
            # Join the leaves into a string
            leaves = " ".join(f"{word}/{tag}" for word, tag in subtree.leaves())
            print(f"{color}{subtree.label()}: {leaves}{COLORS['RESET']}")
        else:
            # Plain token (not chunked)
            word, tag = subtree
            print(f"{word}/{tag}", end=" ")
    print()

