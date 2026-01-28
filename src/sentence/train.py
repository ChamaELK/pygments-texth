# train_tagger.py
import nltk
import joblib

brown = nltk.corpus.brown.tagged_sents(categories='news')

tagger = nltk.tag.BigramTagger(
    brown,
    backoff=nltk.tag.DefaultTagger('NN')
)
joblib.dump(tagger, "./model/en_sent_tagger.pkl") 

# Spanish 
nltk.download('cess_esp')
spanish_sents = nltk.corpus.cess_esp.tagged_sents()
es_tagger = nltk.tag.BigramTagger(spanish_sents, backoff=nltk.tag.DefaultTagger('NC'))  # NC = common noun default
joblib.dump(es_tagger, "./model/es_sent_tagger.pkl")

