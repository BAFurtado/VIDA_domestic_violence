""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""
# TODO: just read and process num_people_age_gender_AP.csv

import pandas as pd

import home.input.geography as geo


if __name__ == '__main__':
    p = dict()
    metro = 'BRASILIA'
    p['PROCESSING_ACPS'] = [metro]
    p['PERCENTAGE_ACTUAL_POP'] = .005
    p['SIMPLIFY_POP_EVOLUTION'] = False
    p['LIST_NEW_AGE_GROUPS'] = [6, 12, 17, 25, 35, 45, 65, 100]
    my_geo = geo.Geography(p)
    # codes = [str(value) for value in my_geo.mun_codes]
    # ps, tps = load_pops(codes, p)
    try:
        pop = pd.read_csv('home/input/num_people_age_gender_AP.csv', sep=';')
    except FileNotFoundError:
        pop = pd.read_csv('num_people_age_gender_AP.csv', sep=';')
    