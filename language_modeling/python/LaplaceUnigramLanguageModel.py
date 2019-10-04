import math, collections
from collections import defaultdict

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    # a defaultdict is used to assign an integer number for first time you do not see the token

    self.unigram_language_model = defaultdict(lambda: 0) 
    self.total_tokens = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  

    for sentence in corpus.corpus: # iterate over sentences in the corpus
      for datum_data in sentence.data: # iterate over datums in the sentence
        token = datum_data.word # get the word
        # for each time increase a token by one
        # every time you see a token increase number of total tokens
        self.unigram_language_model[token] = self.unigram_language_model[token]+1 
        self.total_tokens +=1
        # print("===========================================")
        # print(self.unigram_language_model[token])
        # print(self.unigram_language_model[token])
        # print(self.total_tokens[token])

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0
    for one_token in sentence:
        cnt = self.unigram_language_model[one_token]
        score +=math.log(cnt+1) # smothing add 1 because of zero token
        score -=math.log(self.total_tokens +len(self.unigram_language_model))
    return score
