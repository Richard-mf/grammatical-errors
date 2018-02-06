# -*- coding: utf-8 -*-
"""
Created on Sun Apr 03 20:42:25 2016

@author: Fianna
"""


tag_dict = {'Nn':['NN', 'NNS', 'NNP', 'NNPS'],
            'Vform':['MD', 'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG'],
            'Vt':['MD', 'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG'],
            'Prep':'IN',
            'ArtOrDet': 'DT'}

def candidate_selection(sentence, error_type):
    return [w for w in sentence.words if w.type in tag_dict[error_type]]
