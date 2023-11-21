import sys, pickle, random


with open('assoc_words.pickle', 'rb') as p:
    words = pickle.load(p)

word_input  = 'far'
key = random.sample(words[word_input], 3)



print(key)
sys.stdout.flush()
