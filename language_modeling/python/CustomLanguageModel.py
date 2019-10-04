from collections import defaultdict
import math
class CustomLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.trigram_language_model = defaultdict(lambda: 0) 
    self.unigram_language_model = defaultdict(lambda: 0) 
    self.bigram_language_model = defaultdict(lambda:0)
    self.total = 0
    self.total_two_tokens = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
        tokens =sentence.data
        for indx in range(len(tokens)):
            self.total +=1
            second_previous = tokens[indx-2].word
            previous_toekn = tokens[indx-1].word
            current_token = tokens[indx].word
            self.unigram_language_model[previous_toekn] +=1
            self.bigram_language_model [previous_toekn +" "+current_token] +=1
            self.trigram_language_model[second_previous+" "+ previous_toekn +" "+current_token]
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0
    for indx in range(1,len(sentence)):
        current_token = sentence[indx]
        previous_token = sentence[indx-1]
        cnt_bigram = self.bigram_language_model[previous_token + " "+ current_token]
        if cnt_bigram:
            score += math.log(cnt_bigram) - math.log(self.unigram_language_model[previous_token])
        else:
            cnt_ungram = self.unigram_language_model[current_token]
            # instead of adding smotthing one add a small delta number
            score += math.log(.4)+math.log(cnt_ungram+.3) - math.log(self.total)
    return score