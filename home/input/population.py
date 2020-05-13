""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""
# TODO: just read and process num_people_age_gender_AP.csv

import pandas as pd


try:
    pop = pd.read_csv('home/input/num_people_age_gender_AP.csv', sep=';')
except FileNotFoundError:
    pop = pd.read_csv('num_people_age_gender_AP.csv', sep=';')

p_etnias = {'cor': ['branca', 'preta', 'amarela', 'parda', 'indigena'],
            'PROP': [47.52, 7.52, 1.1, 43.43, .43]}
etnias = pd.DataFrame.from_dict(p_etnias)


def filter_pop(codes):
    return pop[pop.mun.isin(codes)]
