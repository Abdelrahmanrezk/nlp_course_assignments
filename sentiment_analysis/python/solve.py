import math
from collections import defaultdict
class SolveSentimentProblem:
	"""docstring for ClassName"""
	def __init__(self):
		self.postive_words = defaultdict(lambda: 0) 
		self.negtive_words = defaultdict(lambda: 0) 
		self.V = set() # becuase we need total non repeated words so using set
		
	def compute_words(self, klass, words): 
		'''
			 a function compute negtive and positive words in all of documents that take
			klass is related to negtive or positive class
		'''
		if klass == "pos":
			for word in words:
				self.postive_words[word] +=1
				self.V.add(word)
		else:
			for word in words:
				self.negtive_words[word] +=1
				self.V.add(word)


	def compute_score(self, words):
		positive_score = 0.0
		negtive_score  = 0.0
		total_positive = math.log(sum(self.postive_words.values())+len(self.V))
		total_negtive  = math.log(sum(self.negtive_words.values())+len(self.V))

		for word in words:
			positive_score += math.log(self.postive_words[word]+1)
			positive_score -=total_positive
			negtive_score += math.log(self.negtive_words[word]+1)
			negtive_score -=total_negtive
		return positive_score, negtive_score