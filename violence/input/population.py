""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""

import os
import pandas as pd


p_etnias = {'cor': ['branca', 'preta', 'amarela', 'parda', 'indigena'],
            'PROP': [47.52, 7.52, 1.1, 43.43, .43]}
etnias2000 = pd.DataFrame.from_dict(p_etnias)
etnias2010 = pd.read_csv('violence/input/2010/etnia_ap.csv', sep=';')
