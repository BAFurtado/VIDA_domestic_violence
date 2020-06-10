""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""


import pandas as pd


p_etnias = {'cor': ['branca', 'preta', 'amarela', 'parda', 'indigena'],
            'PROP': [47.52, 7.52, 1.1, 43.43, .43]}
etnias = pd.DataFrame.from_dict(p_etnias)
