# Later replace by self.model.random
from collections import defaultdict

import numpy as np
import pandas as pd
import random
import violence.input.geography as geo
import violence.input.population as population

""" 
    Objective is to have data on population, age, gender and qualification.
    Geography class provides the list of IBGE's AREAS DE PONDERAÇÃO (APs) for a given metropolis input.
    Using that, population gets number of people by age and gender in each AP.
    Here, we unite all the data, given a metropolis.
    
    Population gives me 
    
    Possible metropolis include the following ACPs:
"""

metropolis = ["MANAUS", "BELEM", "MACAPA", "SAO LUIS", "TERESINA", "FORTALEZA", "CRAJUBAR", "NATAL", "JOAO PESSOA",
              "CAMPINA GRANDE", "RECIFE", "MACEIO", "ARACAJU", "SALVADOR", "FEIRA DE SANTANA",
              "ILHEUS - ITABUNA", "PETROLINA - JUAZEIRO", "BELO HORIZONTE", "JUIZ DE FORA", "IPATINGA", "UBERLANDIA",
              "VITORIA", "VOLTA REDONDA - BARRA MANSA", "RIO DE JANEIRO", "CAMPOS DOS GOYTACAZES", "SAO PAULO",
              "CAMPINAS", "SOROCABA", "SAO JOSE DO RIO PRETO", "SANTOS", "JUNDIAI", "SAO JOSE DOS CAMPOS",
              "RIBEIRAO PRETO", "CURITIBA", "LONDRINA", "MARINGA", "JOINVILLE", "FLORIANOPOLIS", "PORTO ALEGRE",
              "NOVO HAMBURGO - SAO LEOPOLDO", "CAXIAS DO SUL", "PELOTAS - RIO GRANDE", "CAMPO GRANDE", "CUIABA",
              "GOIANIA", "BRASILIA"]


def quali_table(params):
    """ Provide list of municipality codes for a metropolitan region and
    return a table with APs codes and percentage of qualification by years of study
    """
    my_geo = geo.Geography(params)
    mun_codes = [str(value) for value in my_geo.mun_codes]
    # Load qualifications data 2000, combining municipal-level with AP-level
    quali_aps = pd.read_csv(f"violence/input/{params['DATA_YEAR']}/quali_aps.csv", sep=';')
    quali_aps.AREAP = quali_aps.AREAP.astype(str)
    selected_quali = quali_aps[quali_aps.AREAP.str[:7].isin(mun_codes)]
    return selected_quali


def generate_people(params, df, col):
    num_people = int(params['INITIAL_FAMILIES'] * params['MEMBERS_PER_FAMILY'])
    indexes = np.random.choice(df.index, num_people, p=df[col])
    people = df[df.index.isin(indexes)]
    people = people[['AREAP', 'gender', 'age']]
    people.loc[people['gender'] == 1, 'gender'] = 'female'
    people.loc[people['gender'] == 2, 'gender'] = 'male'
    return people


def adjust_instruction_2010(study):
    template = {1: random.randint(1, 8),
                2: random.randint(9, 11),
                3: random.randint(12, 15),
                4: random.randint(16, 17),
                5: random.randint(1, 17)}
    return template[study]


def add_qualification(people, qualification, _2010=False):
    # TODO: reconfigure for new years of study division
    # Restricting schooling to possible attainable years of study, given age of person
    for i in people.index:
        age = people.loc[i, 'age']
        if age <= 6:
            people.loc[i, 'years_study'] = 0
            continue
        while True:
            study = np.random.choice(qualification.loc[qualification['AREAP'] == str(people.loc[i, 'AREAP']), 'qual'],
                                     p=qualification.loc[qualification['AREAP'] == str(people.loc[i, 'AREAP']),
                                                         'perc_qual_AP'])
            if _2010:
                study = adjust_instruction_2010(study)
            if study <= max(0, age - 6):
                people.loc[i, 'years_study'] = study
                break
    return people


def add_etnias(people, etnias):
    to_add = np.random.choice(list(etnias['cor']), len(people), p=list(etnias['PROP']/100))
    people.loc[:, 'cor'] = to_add
    return people


def filter_pop(data, codes):
    return data[data.mun.isin(codes)]


def sort_into_families(people):
    # Creating categories
    people.loc[(people.gender == 'male') & (people.age > 18), 'category'] = 'male_adult'
    people.loc[(people.gender == 'female') & (people.age > 18), 'category'] = 'female_adult'
    people.loc[people.age <= 18, 'category'] = 'child'
    people = people.sort_values(by=['AREAP', 'category'], ascending=False)

    # Sorting into families by APs, ensuring one potential aggressor by family
    lst_aps = people.AREAP.unique()
    families = defaultdict(list)
    for ap in lst_aps:
        temp_ppl = people[people.AREAP == ap].copy()
        males = list(temp_ppl[temp_ppl.category == 'male_adult'].index)
        females = list(temp_ppl[temp_ppl.category == 'female_adult'].index)
        children = list(temp_ppl[temp_ppl.category == 'child'].index)
        if len(males) > 0:
            for alpha in males:
                families[alpha].append(alpha)
            while len(females) > 0:
                alpha = np.random.choice(males)
                families[alpha].append(females.pop())
            while len(children) > 0:
                alpha = np.random.choice(males)
                families[alpha].append(children.pop())
        elif len(females) > 0:
            for femme in females:
                families[femme].append(femme)
            while len(children) > 0:
                femme = np.random.choice(females)
                families[femme].append(children.pop())
    return list(families.values())


def main(params):
    """ Needs basic config parameters, especially metropolitan area of choice, average  number of people per family
        and approximate number of families in the sample.

        The process samples actual data for GENDER, AGE, SCHOOLING IN YEARS from Census 2000 and color
        (from 2012 generic source)

        Returns DataFrame and indexes of grouped families by APs (weighting areas from IBGE)
        """

    # Parameters to run Geography that do not change
    params['PERCENTAGE_ACTUAL_POP'] = .005
    params['SIMPLIFY_POP_EVOLUTION'] = False
    params['LIST_NEW_AGE_GROUPS'] = [6, 12, 17, 25, 35, 45, 65, 100]

    my_geo = geo.Geography(params)
    cod = [value for value in my_geo.mun_codes]
    pop = pd.read_csv(f"violence/input/{params['DATA_YEAR']}/num_people_age_gender_AP.csv", sep=';')
    people = filter_pop(pop, cod).copy()
    people.loc[:, 'PROP'] = people.num_people / people.num_people.sum()
    qt = quali_table(params)
    people = generate_people(params, people, 'PROP')
    people = add_qualification(people, qt, True if params['DATA_YEAR'] == 2010 else False)
    people = add_etnias(people, population.etnias)
    # families = None
    families = sort_into_families(people)
    return people, families


if __name__ == '__main__':
    metro = 'BRASILIA'
    # Necessary parameters to generate data
    prms = dict()
    prms['PROCESSING_ACPS'] = [metro]
    # Parameters for this model
    prms['MEMBERS_PER_FAMILY'] = 2.5
    prms['INITIAL_FAMILIES'] = 500
    ppl, fams = main(prms)
