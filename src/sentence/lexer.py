import re
from pygments.lexer import Lexer
from pygments.token import Token
#from nlp  import tree#, colorize_tree
import nltk
from nltk.tokenize import TreebankWordTokenizer
from collections import defaultdict
import logging
import joblib 

logging.getLogger("nltk").setLevel(logging.ERROR)
import warnings
warnings.filterwarnings("ignore", message=".*parsing empty text.*")

# nlp_tagger.py
import pickle
from pathlib import Path

_BACKOFF_TAGGER = None  # cache the loaded tagger

def get_backoff_tagger(lang="en"):
    
    global _BACKOFF_TAGGER
    """
    if _BACKOFF_TAGGER is None:
        brown_sents = nltk.corpus.brown.tagged_sents(categories='news')
        backoff = nltk.tag.DefaultTagger('NN')
        _BACKOFF_TAGGER = nltk.tag.BigramTagger(brown_sents, backoff=backoff)
    """
    paths  = {}
    paths["en"] = "en_sent_tagger.pkl"
    paths["es"] = "es_sent_tagger.pkl"
    if _BACKOFF_TAGGER is None:
        tagger_path = Path(__file__).parent / "model" / paths[lang]
        #with open(tagger_path, "rb") as f:
        _BACKOFF_TAGGER = joblib.load(tagger_path)
    
    return _BACKOFF_TAGGER


def tree(text):
    if not text.strip():
        return None
    else:
        index = defaultdict(list)
        tokens = nltk.word_tokenize(text)
        tagger = nltk.RegexpTagger(
            [(r'^%$', 'PCT'),
            (r'\d+(?:\.\d+)?','NUMBER'),
            (r'^(?:[A-Z]\.)+[A-Z]\.?|[A-Z]{2,}$', 'ABR'),
            (r'^\$$', 'CURR')],
            backoff=get_backoff_tagger())
        
        tags = tagger.tag(tokens)
        print(tags)
        tags = [(w, t if t is not None else "NN") for w, t in tags]
        #print(tags)
        kv_grammar = [
            ("PERCENT", "<NUMBER><PCT>"),
            ("CURRENCY", "<NUMBER><CURR>"),
            ("NP", "<AT>?<JJ>*<NN>+")
        ]

        grammar = "\n".join([f"{label}: {{ {pattern} }}" for label, pattern in kv_grammar])
        
        chunker = nltk.RegexpParser(grammar)
        return chunker.parse(tags)


class SentenceLexer(Lexer):
    name = "Sentence"
    aliases = ["sent"]
    filenames = ["*.sentence"]
    def __init__(self, lang="en", **kwargs):
        super().__init__(**kwargs)
        self.lang = lang
        
    def get_tokens_unprocessed(self, text):
        sentence_regex = re.compile(r'[^;,.!?]+[;,.!?]?', re.MULTILINE)
        sentence_index = 0
        cursor = 0
        circular_tokens = [Token.Sentence.One, Token.Sentence.Two,
                        Token.Sentence.Three, Token.Sentence.Four]
        GRAMMAR_TOKENS = {
            "NP":  Token.Sentence.NP,        
            "PERCENT": Token.Sentence.Percent,   
            "CURRENCY": Token.Sentence.Currency,  
        }
        CIRCULAR_TOKENS_NP = [Token.Sentence.NP.One, Token.Sentence.NP.Two,
                        Token.Sentence.NP.Three, Token.Sentence.NP.Four]
        tokenizer = TreebankWordTokenizer()

        for match in sentence_regex.finditer(text):
            sentence = match.group(0)
            i = sentence_index % 4 
            token = circular_tokens[i]
            np_index = 0
            if sentence: 
                nlptree = tree(sentence )
                cursor = match.start()
                subcursor = cursor 

                if nlptree:
                    
                    label_index = defaultdict(list)
                    
                    for subtree in nlptree: 
                        if isinstance(subtree, nltk.Tree):
                            grammar_color_token = GRAMMAR_TOKENS.get(subtree.label(), token)
                            if subtree.label() == "NP":
                                grammar_color_token = CIRCULAR_TOKENS_NP[i]
                            for word, tag in subtree.leaves():
                                label_index[word] = grammar_color_token


                    last_end = 0
                    for start, end in tokenizer.span_tokenize(sentence):
                        text_part = sentence[last_end:end]
                        sentence_nlp_token = sentence[start:end]
                        sentence_pygments_token = label_index[sentence_nlp_token]
                        
                        
                        #print(text_part)
                        last_end = end
                        if sentence_pygments_token : 
                            yield cursor + start , sentence_pygments_token, text_part
                        else:
                            yield cursor + start, token, text_part
                    
                else: 
                    yield match.start(), token, sentence
                sentence_index += 1

"""
import lexer
l = lexer.SentenceLexer()
text_path = "/home/chama/src/syntax_highlighter/test/input.sentence"
raw = open(text_path).read()
tokens = l.get_tokens_unprocessed(raw)
"""
