# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 15:13:55 2016

@author: Fianna
"""
import pattern.en
from Util import *

testing_data = "Data/testing_data.txt"
training_data = "Data/training_data.txt"


class conll_data:
    def __init__(self, path):
        self.__filepath = path

    def get_data(self):
        SentsAndEdits = []      
        for x in open(self.__filepath).read().split('\n'):
            x = x.split('|||')
            sent = x[0].lower()
            edits = [t.split('~') for t in x[1].split('\t')]
            edits = [[int(start), int(end), tag, suggestion] for [start, end, tag, suggestion] in edits]
            SentsAndEdits.append([sent, edits])
        return SentsAndEdits

    def error_tagged_words(self,tag):
        error_words = []
        tagged_sents = [[s,e] for [s,e] in self.get_data() if any([rule==tag for [start,end,rule,w] in e])]
        for [sent,edits] in tagged_sents:
            sent_error_words = []
            start_ends = [[start,end] for [start,end,rule,word] in edits if rule==tag]
            sentence = pattern.en.parsetree(sent, relations=True)[0]
            for [start,end] in start_ends:
                if start!=end:
                    for word in sentence.words[start:end]:
                        sent_error_words.append(word)
                else:
                    pass
            candidate = candidate_selection(sentence, tag)
            wanted = [word for word in sent_error_words if word in candidate]
            if len(wanted)!=0:
                error_words.append(wanted)
        return error_words
    
    def straight_tagged_words(self, tag):
        error_tagged = []
        for sent, edits in self.get_data():
            tag_edits = [[start,end] for [start,end,error_type,blah] in edits if error_type==tag]
            s = pattern.en.parsetree(sent, relations = True)[0]
            copy = [w for w in s.words]
            if len(tag_edits)>0:
                for start,end in tag_edits:
                    replacements = [(w, "Has Nn error") for w in s[start:end]]
                    assert copy[start:end] == s[start:end]
                    copy[start:end] = replacements
            for i in range(len(copy)):
                if type(copy[i])==pattern.text.tree.Word:
                    assert copy[i]==s[i]
                    replacement = (copy[i], "correct")
                    copy[i] = replacement
            error_tagged.append(copy)
        return error_tagged