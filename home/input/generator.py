import pandas as pd


# Load qualifications data 2000, combining municipal-level with AP-level
quali = pd.read_csv('home/input/qualification_2000.csv', sep=';')

# rename from cod_mun b/c we may also have
# AP codes, not just municipal codes
quali.rename(columns={'cod_mun': 'code'}, inplace=True)
quali_aps = pd.read_csv('home/input/qualification_APs.csv', sep=';', header=0,
                      decimal=',').apply(pd.to_numeric, errors='coerce')
for code, group in quali_aps.groupby('AREAP'):
    group = group[['qual', 'perc_qual_AP']]
    row = {'code': code}
    for idx, qual, percent in group.to_records():
        row[str(qual)] = percent
    row = [row.get(col, 0) for col in quali.columns]
    quali.loc[quali.shape[0]] = row
quali.set_index('code', inplace=True)
quali_sum = quali.cumsum(axis=1)


single_ap_muns = pd.read_csv('input/single_aps.csv', sep=';')
single_ap_muns = single_ap_muns['mun_code'].tolist()

if __name__ == '__main__':
    pass