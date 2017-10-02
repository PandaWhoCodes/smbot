import nltk
from nltk.stem.lancaster import LancasterStemmer
import json


class classification():
    """
    Clasifies the text into classes -> or intents
    """
    corpus_words = {}
    class_words = {}
    stemmer = LancasterStemmer()

    def __init__(self):
        training_data = []
        with open("nlu_functions/trainer.json", "r") as f:
            data = f.read()
        Traindata = json.loads(data)
        training_data.extend(Traindata)
        corpus_words = {}
        class_words = {}
        # Removing duplicated by turning the list into a set
        classes = list(set([a['class'] for a in training_data]))
        for c in classes:
            # prepare a list of words within each class
            class_words[c] = []
        # capture unique stemmed words in the training corpus
        corpus_words = {}
        class_words = {}
        # Removing duplicated by turning the list into a set
        classes = list(set([a['class'] for a in training_data]))
        for c in classes:
            # prepare a list of words within each class
            class_words[c] = []

        # loop through each sentence in our training data
        for data in training_data:
            # tokenize each sentence into words
            for word in nltk.word_tokenize(data['sentence']):
                # ignore a some things
                if word not in ["?", "'s"]:
                    # stem and lowercase each word
                    stemmed_word = self.stemmer.stem(word.lower())
                    # have we not seen this word already?
                    if stemmed_word not in corpus_words:
                        corpus_words[stemmed_word] = 1
                    else:
                        corpus_words[stemmed_word] += 1
                    # add the word to our words in class list
                    class_words[data['class']].extend([stemmed_word])
                    # Training done
        self.corpus_words = corpus_words
        self.class_words = class_words

    # we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality as in how common is the word)
    # also we have all words in each class
    # we can now calculate a score for a new sentence


    # now we can find the class with the highest score
    # calculate a score for a given class taking into account word commonality
    def calculate_class(self, sentence, class_name, show_details=True):
        score = 0
        # tokenize each word in our new sentence
        for word in nltk.word_tokenize(sentence):
            # check to see if the stem of the word is in any of our classes
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                # treat each word with relative weight
                score += (1 / self.corpus_words[self.stemmer.stem(word.lower())])
                if show_details:
                    print("   match: %s (%s)" % (
                        self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
        return score

    # now we can find the class with the highest score
    # for c in class_words.keys():
    #     print("Class: %s  Score: %s \n" % (c, calculate_class(sentence, c)))

    # return the class with highest score for sentence
    def classify(self, sentence):
        high_class = None
        high_score = 0
        sentence = sentence.lower()
        # loop through our classes
        for c in self.class_words.keys():
            # calculate score of sentence for each class
            score = self.calculate_class(sentence, c, show_details=False)
            # keep track of highest score
            if score > high_score:
                high_class = c
                high_score = score

        return (high_class, high_score)
