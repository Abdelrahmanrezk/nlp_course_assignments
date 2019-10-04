from collections import defaultdict
import math
class StupidBackoffLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    '''
       stupid backoff algorithm is all about when you using trigram
        for example and probability of word given its two previous word
        is 0 you are go back to bigram else go to unigram
        but here i am using only bigram and backoff to unigram
    '''
    # TODO your code here
    self.unigram_language_model = defaultdict(lambda: 0) 
    self.bigram_language_model = defaultdict(lambda:0)
    self.total = 0
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
            previous_toekn = tokens[indx-1].word
            current_token = tokens[indx].word
            self.unigram_language_model[previous_toekn] +=1
            self.bigram_language_model [previous_toekn +" "+current_token] +=1
            


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    score = 0
    for indx in range(1,len(sentence)):
        current_token = sentence[indx]
        previous_token = sentence[indx-1]
        cnt_bigram = self.bigram_language_model[previous_token + " "+ current_token]
        if cnt_bigram:
            score += math.log(cnt_bigram) - math.log(self.unigram_language_model[previous_token])
        else:
            cnt_ungram = self.unigram_language_model[current_token]
            score += math.log(.4)+math.log(cnt_ungram+1) - math.log(self.total+len(self.unigram_language_model))
    # print(score)
    return score