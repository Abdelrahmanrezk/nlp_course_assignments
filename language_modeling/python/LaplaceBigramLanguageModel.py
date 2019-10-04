from collections import defaultdict
import math
class LaplaceBigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.bigram_language_model = defaultdict(lambda:0)
    self.total_previous_word= 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
        for indx, bi_token in enumerate(sentence.data):
            previous_word = sentence.data[indx-1].word
            current_word = sentence.data[indx].word
            self.total_previous_word +=1
            bi_gram_pharse = previous_word + " " + current_word 
            self.bigram_language_model[bi_gram_pharse] +=1;

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0
    for indx, bi_token in enumerate(sentence):
        bi_gram_pharse = sentence[indx-1] + " " + sentence[indx]
        cnt_bi_gram = self.bigram_language_model[bi_gram_pharse]
        score +=math.log(cnt_bi_gram+1)
        score -=math.log(self.total_previous_word + len(self.bigram_language_model))
    return score