import pandas as pd
from output.read_output import model_scale


def results():
    path = r"output_200_BRASILIA_TFTF_dict_keys(['quarantine', 'dissuasion']).csv"
    o = pd.read_csv(path, sep=';')
    o.loc[:, 'Attacks per female'] = o.loc[:, 'Got attacked'] / o.loc[:, 'Females'] * model_scale
    o.loc[:, 'Denounce per female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
    o = o.groupby(['dissuasion', 'quarantine']).agg('mean')[['Attacks per female', 'Denounce per female']]
    print(o)


if __name__ == '__main__':
    results()
