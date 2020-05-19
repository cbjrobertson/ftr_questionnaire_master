#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 21:00:27 2020

@author: cole
"""
import pandas as pd
import numpy as np
from collections import Counter

e24_qs = pd.read_csv("/Users/cole/Dropbox/ftr_research/chen_2/syntax_question_select/data/bothQ.csv")
qs = pd.read_excel("/Users/cole/Dropbox/ftr_research/ftr_questionnaire_master/questions.xlsx")
qs["e2_&_e4"] = np.where(qs.question_no.isin(e24_qs.questionNo.to_list()),"in","out")

e1 = pd.read_excel("../chen_1/working_data/long_syntax_e1_all.xlsx")


q_dic = {e1.question_no[x]:e1.intersection[x] for x in e1.index}

qs['e1_intersection'] = qs.question_no.apply(lambda x: q_dic[x])
qs.to_excel("/Users/cole/Dropbox/ftr_research/ftr_questionnaire/questions.xlsx",index=False)

#t = qs.drop_duplicates(subset="question_no")
#pd.crosstab(t.loc[t['e1_intersection'] == 'in',"miscode_cut"],t.loc[t['e1_intersection'] == 'in',"understand"])
