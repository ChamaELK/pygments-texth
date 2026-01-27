import re
from pygments.lexer import Lexer
from pygments.token import Token
#from nlp  import tree#, colorize_tree
import nltk
from nltk.tokenize import TreebankWordTokenizer
from collections import defaultdict



def tree(text,backoff_tagger):
    index = defaultdict(list)
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



class SentenceLexer(Lexer):
    name = "Sentence"
    aliases = ["sent"]
    filenames = ["*.sentence"]

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

        brown_tagged_sents = nltk.corpus.brown.tagged_sents(categories='news')
        backoff_tagger = nltk.BigramTagger(brown_tagged_sents, backoff= nltk.DefaultTagger('NN'))
        for match in sentence_regex.finditer(text):
            sentence = match.group(0)
            i = sentence_index % 4 
            token = circular_tokens[i]
            np_index = 0
            if sentence: 
                nlptree = tree(sentence,backoff_tagger )
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
