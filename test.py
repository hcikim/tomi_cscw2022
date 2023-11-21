import sys
import pickle, random
from random import randrange

sampleSentences = [
    "When was the last time you walked for more than an hour?", 
    "What was the best gift you ever received and why?",
    "If you had to move from California where would you go,and what would you miss the most about California?",
    "How did you celebrate last Halloween?",
    "Do you read a newspaper often and which do you prefer? Why? ",
    "What is a good number of people to have in a student household and why? ",
    "If you could invent a new flavor of ice cream, what would it be?",
    "What is the best restaurant you've been to in the last month that your partner hasn't been to?",
    "Describe the last pet you owned.", 
    "What is your favorite holiday? Why? "
]

print(sampleSentences[randrange(len(sampleSentences))])
sys.stdout.flush()

