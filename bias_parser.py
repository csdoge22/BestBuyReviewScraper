from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import numpy as np     

def determineRating(line: str) -> float:
    """
    Sometimes there are people that intentionally leave a bad rating disguised as a five-star rating.\n\n
    So this function gives an estimate of what the user actually meant to rate using natural language processing and keywords.
    """
    # print("Splitting the sentence into separate words")
    # we will take every word as a separate token
    sentence = word_tokenize(line)
    
    # common words found in five star reviews (my approach: do the same thing with one star reviews)
    five_star_basis = ['excellent','love','best','worth','recommend','awesome', 'worth', 'thanks', 'amazing', 'simple', 'perfect', 'price', 'everything', 'ever', 'must', 'ipod', 'before', 'found', 'store', 'never', 'recommend', 'done', 'take', 'always', 'touch']
    
    # we will use nltk's wordnet to find synonyms for each word in both bases.
    five_star_synonyms: list[str] = []
    
    # because the list of synonyms are 3D lists, three nested loops would have to be done \n
    # to add each term tot he list of synonyms
    try:
        for base in five_star_basis:
            synonymMatrix = wordnet.synonyms(base)
            for synonymList in synonymMatrix:
                for synonym in synonymList:
                    five_star_synonyms.append(synonym)
    except:
        print("No good parsing words")
    one_star_basis = ['not','horrible','worst', "didn't", 'bad', 'waste', 'money', 'crashes', 'tried', 'useless', 'nothing', 'paid', 'open', 'deleted', 'downloaded', 'says', 'stupid', 'anything', 'actually', 'account', 'bought', 'apple', 'already']
    one_star_synonyms: list[str] = []
    try:
        for base in one_star_basis:
            synonymMatrix = wordnet.synonyms(base)
            # I do not want the synonyms list to be a 2D list as that will require repeated O(n^2) access
            for synonymList in synonymMatrix:
                for synonym in synonymList:
                    one_star_synonyms.append(synonym)
    except:
        print("No good parsing synonyms")
    # I will make a dictionary that stores the number of words corresponding to a five star review VS one star review (any words with a neutral connotation will not count)
    numTerms = 0
    deviation: dict[int,int] = dict()
    for word in sentence:
        if word in one_star_synonyms or word in one_star_basis:
            if(1 not in deviation):
                deviation[1] = 1
            else:
                deviation.update({1:deviation[1]+1})
            numTerms += 1
        if word in five_star_synonyms or word in five_star_basis:
            if(5 not in deviation):
                deviation[5] = 1
            else:
                deviation.update({5:deviation[5]+1})
            numTerms += 1
        # notice that I only increase the number of terms thar are part of the synonyms of the one word basis
    
    # add up all the terms
    avg = 0
    if 1 in deviation:
        avg += deviation[1]
    if 5 in deviation:
        # deviation[5] needs to be multiplied by 5 because we are summing up all 5 star reviews
        avg += deviation[5]*5
    
    if(numTerms==0):
        return 1.0
    avg /= numTerms
    return avg

# test case: actual review
# print(determineRating("Excellent laptop, Beautiful design, truly adds a professional design to a real powerhouse laptop. With some minor tweaks I've passed 13 hours of battery and no noticable performance loss. Worth the price for what you get, design matters more than I thought"))