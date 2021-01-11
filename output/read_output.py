import pandas as pd

""" Reading output for text content
"""

model_scale = 1000


# Standard run for 200 times
def many_runs_output(path='output_200_10.csv'):
    # Read raw data
    o = pd.read_csv(path, sep=';')
    # Restrict to step 10 output of the model
    o = o[(o.index + 1) % 11 == 0]
    runs = len(o)
    # Get numbers by 100,000 females
    o.loc[:, 'Attacks per female'] = o.loc[:, 'Got attacked'] / o.loc[:, 'Females'] * model_scale
    o.loc[:, 'Denounce per female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
    print(f"Dissuasion: {path.split('_')[-2]}, Quarantine: {path.split('_')[-1].split('.')[0]}")
    print(f"1. For {runs} runs, denounces per hundred {model_scale} female is {o['Denounce per female'].mean():.2f}")
    print(f"2. For {runs} runs attacks per hundred {model_scale} female is {o['Attacks per female'].mean():.2f}")


def percentage(data, flag='Attacks per female', flag2='dissuasion'):
    idx = 0 if flag == 'Attacks per female' else 1
    perc = (data.iloc[-1, idx] - data.iloc[0, idx]) / data.iloc[-1, idx] * 100
    print(f"Percentual {flag} with {flag2} {perc:.2f}%")


def results(flag='dissuasion'):
    print(flag.title())
    o = pd.read_csv(f"output_200_8_dict_keys(['{flag}']).csv", sep=';')
    o.loc[:, 'Attacks per female'] = o.loc[:, 'Got attacked'] / o.loc[:, 'Females'] * model_scale
    o.loc[:, 'Denounce per female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
    o = o.groupby(flag).agg('mean')[['Attacks per female', 'Denounce per female']]
    print(o)
    percentage(o, 'Attacks per female', flag)
    percentage(o, 'Denounce per female', flag)


def main():
    many_runs_output()
    for each in ['dissuasion', 'quarantine', 'gender_stress', 'has_gun', 'is_working_pct', 'pct_change_wage',
                 'under_influence', 'chance_changing_working_status']:
        results(each)


if __name__ == '__main__':
    main()
    # For Policy tests
    # for p in ['output_200_False_False.csv',
    #           'output_200_False_True.csv',
    #           'output_200_True_False.csv',
    #           'output_200_True_True.csv']:
    #     many_runs_output(p)
