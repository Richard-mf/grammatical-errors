from __future__ import division
import nltk
import pattern
from pattern.vector import SLP, Document
from random import shuffle
from Util import candidate_selection
from collections import defaultdict
from features import FeatExtract
from organizing_sents_for_classification import conll_data, training_data, testing_data

class AoD_classifier:
    def __init__(self):
        self.error_tag = "ArtOrDet"
        self.training = self.return_information(training=True)
        self.testing = self.return_information(training=False)
        self.classifier = self.set_classifier()
        self.accuracy, self.precision, self.recall, self.f1 = self.test()
        
    def results(self):
        print "Accuracy: "+str(self.accuracy)
        print "Precision: "+str(self.precision)
        print "Recall: "+str(self.recall)
        print "F-1 Score: "+str(self.f1)
    
    def test(self):
        test_feats = self.get_labeled_feats(self.testing)
        return self.classifier.test(test_feats)
        
    def set_classifier(self):
        train_feats = self.get_labeled_feats(self.training)
        tron = SLP(train = train_feats, iterations = 4)
        return tron

    def return_information(self, training=True):
        if training ==True:
            path = training_data
        else:
            path = testing_data
        Conll = conll_data(path)
        return self.get_labeled_words(Conll.error_tagged_words(self.error_tag), training)

    def get_labeled_feats(self, data):
        labeled_binary = []
        for (word,tag) in data:
            feat = FeatExtract(word, ArtOrDet=(self.error_tag=='ArtOrDet')).binary_features()
            d = Document(feat, type=tag, stopwords=True)
            labeled_binary.append(d)
        return labeled_binary

    def get_labeled_words(self, data_set, training=True):
        data = []
        for error in data_set:
            data+=self.sent_labeled_words(error, training)
        return data        
    
    def sent_labeled_words(self, error, training=True):
        assert all([w.sentence for w in error])
        word = error[0]
        sent = word.sentence
        tagged = candidate_selection(sent, self.error_tag)
        has_error = "Has %s error"%self.error_tag
        no_error = "correct"
        good = [(w, no_error) for w in tagged if w not in error]
        bad = [(w, has_error) for w in error]
        if training ==True:
            shuffle(good)
            good = good[:len(bad)]
        labeled_words = good + bad
        return labeled_words

print "PERCEPTRON"        
art = AoD_classifier()
art.results()        
     
