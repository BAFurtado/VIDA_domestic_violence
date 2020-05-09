""" Gets a metropolitan region choice and returns a dictionary with male and female proportion of population
by age groups.
"""
import math

import numpy as np
import pandas as pd
import statsmodels.api as sm
import home.input.geography as geo


def simplify_pops(pops, params):
    """Simplify population"""
    # Inserting the 0 on the new list of ages
    list_new_age_groups = [0] + params['LIST_NEW_AGE_GROUPS']

    pops_ = {}
    for gender, pop in pops.items():
        # excluding the first column (region ID)
        pop_edit = pop.iloc[:, pop.columns != 'code']

        # Transform the columns ID in integer values (to make easy to select the intervals and sum the pop. by region)
        list_of_ages = [int(x) for x in [int(t) for t in list(pop_edit.columns)]]
        # create the first aggregated age class
        temp = pop_edit.iloc[:, [int(t) <= list_new_age_groups[1] for t in list_of_ages]].sum(axis=1)
        # add the first column with the region ID
        pop_fmt = pd.concat([pop.iloc[:, pop.columns == 'code'], temp], axis=1)
        # excluding the processed columns in the previous age aggregation
        pop_edit = pop_edit.iloc[:, [int(i) > list_new_age_groups[1] for i in list_of_ages]]
        for i in range(1, len(list_new_age_groups) - 1):
            # creating the full new renaming ages list
            list_of_ages = [int(x) for x in [int(t) for t in list(pop_edit.columns)]]
            # selecting the new aggregated age class based on superior limit from list_new_age_groups, SUM by ROW
            temp = pop_edit.iloc[:, [int(t) <= list_new_age_groups[i + 1] for t in list_of_ages]].sum(axis=1)
            # joining to the previous processed age class
            pop_fmt = pd.concat([pop_fmt, temp], axis=1)
            # excluding the processed columns in the previous age aggregation
            pop_edit = pop_edit.iloc[:, [int(age) > list_new_age_groups[i + 1] for age in list_of_ages]]
        # changing the columns names
        pop_fmt.columns = ['code'] + list_new_age_groups[1:len(list_new_age_groups)]
        pops_[gender] = pop_fmt

    return pops_


def format_pops(pops):
    """Rename the columns names to be compatible as the pop simplification modification"""
    for pop in pops.values():
        list_of_columns = ['code'] + [int(x) for x in list(pop.columns)[1: len(list(pop.columns))]]
        pop.columns = list_of_columns
    return pops


def pop_age_data(pop, code, age, percent_pop):
    """Select and return the proportion value of population
    for a given municipality, gender and age"""
    n_pop = pop[pop['code'] == str(code)][age].iloc[0] * percent_pop
    rounded = int(round(n_pop))

    # for small `percent_pop`, sometimes we get 0
    # when it's better to have at least 1 agent
    if rounded == 0 and math.ceil(n_pop) == 1:
        return 1

    return rounded


def load_pops(mun_codes, params):
    """Load populations for specified municipal codes."""
    pops = {}
    for name, gender in [('men', 'male'), ('women', 'female')]:
        pop = pd.read_csv('pop_{}.csv'.format(name), sep=';', header=0, decimal=',')
        pop = pop[pop['cod_mun'].isin(mun_codes)]

        # rename from cod_mun b/c we may also have
        # AP codes, not just municipal codes
        pop.rename(columns={'cod_mun': 'code'}, inplace=True)
        pops[gender] = pop

    ap_pops = pd.read_csv('num_people_age_gender_AP.csv', sep=';', header=0)
    for code, group in ap_pops.groupby('AREAP'):
        if not int(str(code)[:7]) in mun_codes:
            continue
        for gender, gender_code in [('male', 1), ('female', 2)]:
            df = pops[gender]
            sub_group = group[group.gender == gender_code][['age', 'num_people']].to_records()
            row = [0 for _ in range(101)]
            for idx, age, count in sub_group:
                row[age] = count
            row = [code] + row
            df.loc[df.shape[0]] = row

    for pop in pops.values():
        pop['code'] = pop['code'].astype(np.int64).astype(str)

    total_pop = sum(round(pop.iloc[:, pop.columns != 'code'].sum(axis=1).sum(0) * params['PERCENTAGE_ACTUAL_POP']) for pop in pops.values())
    if params['SIMPLIFY_POP_EVOLUTION']:
        pops = simplify_pops(pops, params)
    else:
        pops = format_pops(pops)

    return pops, total_pop


if __name__ == '__main__':
    p = dict()
    metro = 'BRASILIA'
    p['PROCESSING_ACPS'] = [metro]
    p['PERCENTAGE_ACTUAL_POP'] = .005
    p['SIMPLIFY_POP_EVOLUTION'] = False
    p['LIST_NEW_AGE_GROUPS'] = [6, 12, 17, 25, 35, 45, 65, 100]
    my_geo = geo.Geography(p)
    codes = [str(value) for value in my_geo.mun_codes]
    ps, tps = load_pops(codes, p)

