import pandas as pd

import home.input.geography as geo


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


if __name__ == '__main__':
    metropolitan_region_of_choice = 'BRASILIA'
    qt = quali_table(metropolitan_region_of_choice)

