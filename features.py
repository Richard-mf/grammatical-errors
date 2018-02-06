# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 18:09:24 2016

@author: Fianna
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 01 18:09:24 2016

@author: Fianna
"""
import pattern
from collections import defaultdict

tag_dict = {'Nn':['NN', 'NNS', 'NNP', 'NNPS'],
            'Vform':['MD', 'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG'],
            'Vt':['MD', 'VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG'],
            'Prep':'IN',
            'ArtOrDet': 'DT'}

def candidate_selection(sentence, error_type):
    return [w for w in sentence.words if w.type in tag_dict[error_type]]

class FeatExtract:
    def __init__(self, word, ArtOrDet=False):
        self.word = word
        self.features = self.get_features(self.word, ArtOrDet)
    
    def __add_padding(self,words):
        copy = [w for w in words]
        for i in range(4):
            copy.insert(0,"START")
            copy.append("END")
        return copy
    
    def binary_features(self):
        binary_feats = defaultdict(int)
        for (n,v) in self.features.items():
            if type(v)==str or type(v)==unicode:
                name = "__".join([n,v])
                binary_feats[name]=True
        return binary_feats
            
    
    
    def n_gram_POS_features(self, word):
        assert type(word)==pattern.text.tree.Word
        sent = word.sentence
        i = word.index+4
        sent_w = self.__add_padding([w.string for w in sent])
        sent_p = self.__add_padding([w.type for w in sent.words])
        assert sent_w[i]==word.string
        assert sent_p[i]==word.type
        feats = {'w': sent_w[i],
        'wB': sent_w[i-1],
        'w2B': sent_w[i-2],
        'w3B': sent_w[i-3],
        'wA': sent_w[i+1],
        'w2A': sent_w[i+2],
        'w3A': sent_w[i+3],
        'wB_w': sent_w[i-1]+' '+sent_w[i],
        'wB_wA': sent_w[i-1]+' '+sent_w[i+1],
        'w_wA': sent_w[i]+' '+sent_w[i+1],
        'w2B_wB': sent_w[i-2]+' '+sent_w[i-1],
        'wA_w2A': sent_w[i+1]+' '+sent_w[i+2],
        'w3B_w2B_wB': sent_w[i-3]+' '+sent_w[i-2]+' '+sent_w[i-1],
        'w2B_wB_w': sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i],
        'w2B_wB_wA': sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i+1],
        'wB_w_wA': sent_w[i-1]+' '+sent_w[i]+' '+sent_w[i+1],
        'w_wA_w2A': sent_w[i]+' '+sent_w[i+1]+' '+sent_w[i+2],
        'wB_wA_w2A': sent_w[i-1]+' '+sent_w[i+1]+' '+sent_w[i+2],
        'wA_w2A_w3A': sent_w[i+1]+' '+sent_w[i+2]+' '+sent_w[i+3],
        'w4B_w3B_w2B_wB': sent_w[i-4]+' '+sent_w[i-3]+' '+sent_w[i-2]+' '+sent_w[i-1],
        'w3B_w2B_wB_w': sent_w[i-3]+' '+sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i],
        'w3B_w2B_wB_wA': sent_w[i-3]+' '+sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i+1],
        'w2B_wB_wA_w2A': sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i+1]+' '+sent_w[i+2],
        'w2B_wB_w_wA': sent_w[i-2]+' '+sent_w[i-1]+' '+sent_w[i]+' '+sent_w[i+1],
        'wB_wA_w2A_w3A': sent_w[i-1]+' '+sent_w[i+1]+' '+sent_w[i+2]+' '+sent_w[i+3],
        'wB_w_wA_w2A': sent_w[i-1]+' '+sent_w[i]+' '+sent_w[i+1]+' '+sent_w[i+2],
        'w_wA_w2A_w3A': sent_w[i]+' '+sent_w[i+1]+' '+sent_w[i+2]+' '+sent_w[i+3],
        'wA_w2A_w3A_w4A': sent_w[i+1]+' '+sent_w[i+2]+' '+sent_w[i+3]+' '+sent_w[i+4],
        'p': sent_p[i],
        'pB': sent_p[i-1],
        'p2B': sent_p[i-2],
        'p3B': sent_p[i-3],
        'pA': sent_p[i+1],
        'p2A': sent_p[i+2],
        'p3A': sent_p[i+3],
        'pB_p': sent_p[i-1]+' '+sent_p[i],
        'pB_pA': sent_p[i-1]+' '+sent_p[i+1],
        'p_pA': sent_p[i]+' '+sent_p[i+1],
        'p2B_pB': sent_p[i-2]+' '+sent_p[i-1],
        'pA_p2A': sent_p[i+1]+' '+sent_p[i+2],
        'p3B_p2B_pB': sent_p[i-3]+' '+sent_p[i-2]+' '+sent_p[i-1],
        'p2B_pB_p': sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i],
        'p2B_pB_pA': sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i+1],
        'pB_p_pA': sent_p[i-1]+' '+sent_p[i]+' '+sent_p[i+1],
        'p_pA_p2A': sent_p[i]+' '+sent_p[i+1]+' '+sent_p[i+2],
        'pB_pA_p2A': sent_p[i-1]+' '+sent_p[i+1]+' '+sent_p[i+2],
        'pA_p2A_p3A': sent_p[i+1]+' '+sent_p[i+2]+' '+sent_p[i+3],
        'p4B_p3B_p2B_pB': sent_p[i-4]+' '+sent_p[i-3]+' '+sent_p[i-2]+' '+sent_p[i-1],
        'p3B_p2B_pB_p': sent_p[i-3]+' '+sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i],
        'p3B_p2B_pB_pA': sent_p[i-3]+' '+sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i+1],
        'p2B_pB_pA_p2A': sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i+1]+' '+sent_p[i+2],
        'p2B_pB_p_pA': sent_p[i-2]+' '+sent_p[i-1]+' '+sent_p[i]+' '+sent_p[i+1],
        'pB_pA_p2A_p3A': sent_p[i-1]+' '+sent_p[i+1]+' '+sent_p[i+2]+' '+sent_p[i+3],
        'pB_p_pA_p2A': sent_p[i-1]+' '+sent_p[i]+' '+sent_p[i+1]+' '+sent_p[i+2],
        'p_pA_p2A_p3A': sent_p[i]+' '+sent_p[i+1]+' '+sent_p[i+2]+' '+sent_p[i+3],
        'pA_p2A_p3A_p4A': sent_p[i+1]+' '+sent_p[i+2]+' '+sent_p[i+3]+' '+sent_p[i+4]}
        return feats
         
    def is_noun_compound(self, chunk):
        if chunk!=None:
            if len(chunk)>=2:
                if chunk.words[-2].type.startswith('NN'):
                    return chunk.words[-2].string
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def plur_or_sing(self, word):
        if word!=False:
            if pattern.en.singularize(word)!=pattern.en.pluralize(word):
                if pattern.en.singularize(word)==word:
                    return u"Singular"
                elif pattern.en.pluralize(word)==word:
                    return u"Plural"
            else:
                return u"Unclear"
        else:
            return False
        
    def window(self, chunk, n = 1, after = True):
        if chunk != None:
            assert n>0
            if after:
                if n>1:
                    curr_words = []
                    for i in range(n):
                        if chunk.stop+n<chunk.sentence.stop:
                            curr_words.append(chunk.sentence.words[chunk.stop+n].string)
                        else:
                            curr_words.append("OUT_OF_SENT")
                    return " ".join(curr_words)
                elif chunk.stop<chunk.sentence.stop:
                    return chunk.sentence.words[chunk.stop].string
                else:
                    return False
            else:
                before_chunk_start = chunk.start-1
                if n>1:
                    curr_words = []
                    for i in range(n):
                        if before_chunk_start-n>chunk.sentence.start:
                            curr_words.append(chunk.sentence.words[before_chunk_start-n].string)
                        else:
                            curr_words.append("OUT_OF_SENT")                        
                    return " ".join(curr_words)
                elif before_chunk_start>chunk.sentence.start:
                    return chunk.sentence.words[before_chunk_start].string
                else:
                    return False
        else:
            return False
        
    def is_Direct_Obj(self, chunk):
        if chunk!= None:
            if chunk.verb!= None:
                if chunk.verb.object == chunk:
                    return self.word.chunk.verb.head.string
                else:
                    return False
            else:
                return False
        else:
            return False
        
    def part_of_PNP(self, chunk):
        if chunk!=None:
            if chunk.sentence.words[chunk.start-1].chunk !=None:
                if chunk.sentence.words[chunk.start-1].chunk.type=='PP':
                    np = [w for w in chunk.words]
                    pp = [w for w in chunk.sentence.words[chunk.start-1].chunk.words]
                    PNP = [pnp for pnp in chunk.sentence.pnp if pnp.stop == chunk.stop]
                    if len(PNP)==1:
                        pnp = np+pp
                        if pnp == PNP:
                            prep=[w.string for w in pp]
                            if len(prep)==1:
                                prep = prep[0]
                            return prep
                        else:
                            return False
                    else:
                    		return False
                else:
                    return False
            else:
                return False
        else:
            return False
          
    def get_tagged(self, chunk, tag_start, tag=False):
        if chunk != None:
            if any([w.type.startswith(tag_start) for w in chunk.words]):
                if tag==True:
                    wanted = [w.type for w in chunk.words if w.type.startswith(tag_start)]
                    return ' '.join(wanted)
                else:
                    wanted = [w.string for w in chunk.words if w.type.startswith(tag_start)]
                    return ' '.join(wanted)
            else:
                return False
        else:
            return False
    
    def string_value(self, v1, v2):
        if all([v for v in [v1,v2]]):
            return " ".join([v1,v2])
        else:
            return False
    			
    def ArtOrDet(self, word):
        headWord = word.chunk.head.string if word.chunk!= None else False
        headPOS = word.chunk.head.type if word.chunk!=None else False
        NC = self.is_noun_compound(word.chunk)
        npWords = ' '.join([w.string for w in word.chunk.words]) if word.chunk!= None else False
        npTags = ' '.join([w.type for w in word.chunk.words]) if word.chunk!= None else False
        features = {'headWord': headWord, 
        'npWords': npWords, 
        'NC': self.is_noun_compound(word.chunk),
        'headNumber': self.plur_or_sing(headWord),
        'npTags_NC': self.string_value(npTags, NC),
        'verb': self.is_Direct_Obj(word.chunk),
        'prep': self.part_of_PNP(word.chunk),
        'source': word.string,
        'adj_headWord': self.string_value(self.get_tagged(word.chunk,'JJ'), headWord),
        'adjTag_headWord': self.string_value(self.get_tagged(word.chunk, 'JJ', tag=True), headWord),
        'adj_NC': self.string_value(self.get_tagged(word.chunk, 'JJ'), NC),
        'adjTag_NC': self.string_value(self.get_tagged(word.chunk, 'JJ', tag=True), NC),
        'npTags_headWord': self.string_value(npTags, headWord),
        'headWord_headPOS': self.string_value(headWord, headPOS),
        'headWord_wordAfterNP':self.string_value(headWord, self.window(word.chunk, 1, after=True)),
        'npWords_wordAfterNP': self.string_value(npWords, self.window(word.chunk, 1, after=True)),
        'headWord_2wordsAfterNP': self.string_value(headWord, self.window(word.chunk, 2, after=True)),
        'npWords_2wordsAfterNP': self.string_value(npWords, self.window(word.chunk, 2, after=True)),
        'headWord_3wordsAfterNP': self.string_value(headWord, self.window(word.chunk, 3, after=True)),
        'npWords_3wordsAfterNP': self.string_value(npWords, self.window(word.chunk, 3, after=True))}
        return features
    
    def get_features(self, word, ArtOrDet=False):
        features = {}
        features.update(self.n_gram_POS_features(word))
        if ArtOrDet==True:
            features.update(self.ArtOrDet(word))
        return features