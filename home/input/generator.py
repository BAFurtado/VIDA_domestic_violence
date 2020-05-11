# Later replace by self.model.random
import random
import numpy as np
import pandas as pd

import home.input.geography as geo
import home.input.population as pop


""" Objective is to have data on population, age, gender and qualification.
    Geography class provides the list of IBGE's AREAS DE PONDERAÇÃO (APs) for a given metropolis input.
    Using that, population gets number of people by age and gender in each AP.
    Here, we unite all the data, given a metropolis.
    
    Population gives me 
    
    Possible metropolis include the following ACPs:
    
    # STATE    -       ACPs
    # ------------------------
    # "AM"     -      "MANAUS"
    # "PA"     -      "BELEM"
    # "AP"     -      "MACAPA"
    # "MA"     -      "SAO LUIS", "TERESINA"
    # "PI"     -      "TERESINA"
    # "CE"     -      "FORTALEZA", "CRAJUBAR" - CRAJUBAR refers to JUAZEIRO DO NORTE - CRATO - BARBALHA
    # "RN"     -      "NATAL"
    # "PB"     -      "JOAO PESSOA", "CAMPINA GRANDE"
    # "PE"     -      "RECIFE", "PETROLINA - JUAZEIRO"
    # "AL"     -      "MACEIO"
    # "SE"     -      "ARACAJU"
    # "BA"     -      "SALVADOR", "FEIRA DE SANTANA", "ILHEUS - ITABUNA", "PETROLINA - JUAZEIRO"
    # "MG"     -      "BELO HORIZONTE", "JUIZ DE FORA", "IPATINGA", "UBERLANDIA"
    # "ES"     -      "VITORIA"
    # "RJ"     -      "VOLTA REDONDA - BARRA MANSA", "RIO DE JANEIRO", "CAMPOS DOS GOYTACAZES"
    # "SP"     -      "SAO PAULO", "CAMPINAS", "SOROCABA", "SAO JOSE DO RIO PRETO", "SANTOS", "JUNDIAI",
    #                 "SAO JOSE DOS CAMPOS", "RIBEIRAO PRETO"
    # "PR"     -      "CURITIBA" "LONDRINA", "MARINGA"
    # "SC"     -      "JOINVILLE", "FLORIANOPOLIS"
    # "RS"     -      "PORTO ALEGRE", "NOVO HAMBURGO - SAO LEOPOLDO", "CAXIAS DO SUL", "PELOTAS - RIO GRANDE"
    # "MS"     -      "CAMPO GRANDE"
    # "MT"     -      "CUIABA"
    # "GO"     -      "GOIANIA", "BRASILIA"
    # "DF"     -      "BRASILIA"
"""


def quali_table(metro):
    """ Provide list of municipality codes for a metropolitan region and
    return a table with APs codes and percentage of qualification by years of study
    """
    params = dict()
    params['PROCESSING_ACPS'] = [metro]
    my_geo = geo.Geography(params)
    mun_codes = [str(value) for value in my_geo.mun_codes]
    # Load qualifications data 2000, combining municipal-level with AP-level
    quali_aps = pd.read_csv('quali_aps.csv', sep=';')
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


def sort_into_families():
    pass


if __name__ == '__main__':
    metro = 'BRASILIA'

    # Necessary parameters to generate data
    prms = dict()
    prms['PROCESSING_ACPS'] = [metro]
    prms['PERCENTAGE_ACTUAL_POP'] = .005
    prms['SIMPLIFY_POP_EVOLUTION'] = False
    prms['LIST_NEW_AGE_GROUPS'] = [6, 12, 17, 25, 35, 45, 65, 100]

    # Parameters for this model
    prms['MEMBERS_PER_FAMILY'] = 2.5
    prms['INITIAL_FAMILIES'] = 500

    my_geo = geo.Geography(prms)
    cod = [value for value in my_geo.mun_codes]
    p = pop.filter_pop(cod).copy()
    p.loc[:, 'PROP'] = p.num_people / p.num_people.sum()
    # Logo
    prms['PERCENTAGE_ACTUAL_POP'] = prms['INITIAL_FAMILIES'] * prms['MEMBERS_PER_FAMILY'] / p.num_people.sum()
    qt = quali_table(metro)
    ppl = generate_people(prms, p, 'PROP')
