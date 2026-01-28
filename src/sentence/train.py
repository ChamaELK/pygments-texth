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
cess_sents = nltk.corpus.cess_esp.tagged_sents()
uni_tag = nltk.tag.UnigramTagger(cess_sents, backoff = nltk.tag.DefaultTagger("NC"))
bi_tag = nltk.tag.BigramTagger(cess_sents, backoff=uni_tag)
joblib.dump(bi_tag, "./model/es_sent_tagger.pkl")

