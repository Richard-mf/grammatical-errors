# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 20:18:30 2016

@author: Fianna
"""
from __future__ import division
from Util import tag_dict, candidate_selection
from collections import defaultdict
from organizing_sents_for_classification import conll_data, train2014, test2014
from pattern.vector import NB, SLP
from features import FeatExtract
from random import shuffle
#from perceptron import AoD_classifier

class Word_error_classifier:
    def __init__(self, error_tag):
        self.error_tag = error_tag
        
        self.training = self.return_information(training=True)
        self.testing = self.return_information(training=False)
        self.train_feat = self.get_labeled_feats(self.training)
        self.test_feat = self.get_labeled_feats(self.testing)
        
    def Naive_Bayes(self):
        return Classifier('NB',iterations=None, train = self.train_feat, test = self.test_feat)
    
    def Perceptron(self, iterations=None):
        return Classifier('SLP', iterations, self.train_feat, self.test_feat)
        
    def return_information(self, training=True):
        if training ==True:
            path = train2014
        else:
            path = test2014
        Conll = conll_data(path)
        return self.get_labeled_words(Conll.error_tagged_words(self.error_tag), training)
        
    def get_labeled_feats(self, data):
        #return [(FeatExtract(w, ArtOrDet=(self.error_tag=='ArtOrDet')).binary_features(), t) for (w,t) in data]
        return [(FeatExtract(w, ArtOrDet=False).binary_features(), t) for (w,t) in data]        
        
    def get_labeled_words(self, data_set, training=True):
        data = []
        for error in data_set:
            data+=self.sent_labeled_words(error, training)
        return data
    
    def sent_labeled_words(self, error, training=True):
        assert all([w.sentence for w in error])
        word = error[0]
        sent = word.sentence
        tagged = sent.words
        has_error = "Has %s error"%self.error_tag
        no_error = "correct"
        good = [(w, no_error) for w in tagged if w not in error]
        bad = [(w, has_error) for w in error]
        if training ==True:
            shuffle(good)
            good = good[:len(bad)]
        labeled_words = good + bad
        return labeled_words
    
class Classifier:
    def __init__(self, name, iterations = None, train= [], test= []):
        self.name = name
        self.iterations = iterations
        self.train_data = train
        self.test_data = test
        self.myclassifier = self.set_classifier()
        self.accuracy, self.precision, self.recall, self.f1 = self.myclassifier.test(self.test_data)
    
    def set_classifier(self):
        if self.name=='SLP':
            return SLP(train = self.train_data, iterations = self.iterations)
        elif self.name =='NB':
            return NB(train = self.train_data)
        else:
            print "Unknown classifier name"
            
    def classify(self, doc):
        return self.myclassifier.classify(doc)
        
    def results(self):
        print "Accuracy: "+str(self.accuracy)
        print "Precision: "+str(self.precision)
        print "Recall: "+str(self.recall)
        print "F-1 Score: "+str(self.f1)

#################################################################
        
nounNum = Word_error_classifier('Nn')
vForm = Word_error_classifier('Vform')
vT = Word_error_classifier('Vt')
prep = Word_error_classifier('Prep')
art = Word_error_classifier('ArtOrDet')