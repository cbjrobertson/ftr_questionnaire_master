#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:21:54 2019

@author: cole
"""
import pandas as pd

def w2l(path):
    df_wide = pd.read_excel(path)
    #changing some column names so it will be unique
    qnos = [x for x in df_wide.columns if x.startswith('question_no')]
    temp_qnos = [x.replace('question_no','qnum') for x in qnos]
    df_wide[temp_qnos] = df_wide[qnos]
    df_wide = df_wide.drop(qnos,1)
    df_wide['qform'] = df_wide.question_form
    df_wide = df_wide.drop('question_form',1)

    #first transformation
    long_question = pd.wide_to_long(df_wide,
                                 stubnames=['uneek_certain','uneek_uncertain','uneek_neutral',
                                            'question_uncertain','question_neutral','question_certain','word'],
                                 i = 'qform',
                                 j='question',
                                 suffix='\\w+',
                                 sep='_')
    #get variables back
    long_question['qform'] = [x[0] for x in long_question.index]
    long_question['language'] = [x[1] for x in long_question.index]
    long_question.index = range(long_question.shape[0])
    #second transformation
    long = pd.wide_to_long(long_question,
                             stubnames=['question','uneek','qnum','certainty'],
                             i = ['qform','language'],
                             j='probability',
                             suffix='\\w+',
                             sep='_')
    #get variables back
    long['question_form'] = [x[0] for x in long.index]
    long['language'] = [x[1] for x in long.index]
    long['probability'] = [x[2] for x in long.index]
    #change names back
    long['question_no'] = long.qnum
    long = long.drop('qnum',1)
    #reset index
    long.index = range(long.shape[0])
    
    #add english translation
    eng = {long.question_no[idx]:long.question[idx] for idx in long[long.language == 'english'].index}
    long['question_eng'] = long.question_no.apply(lambda x: eng[x])
    return long

if __name__ == '__main__':
    long = w2l(path='../ftr_questions/questionnaire_master.xlsx')
    long.to_excel('../ftr_questions/questionnaire_long.xlsx',index=False)
    
