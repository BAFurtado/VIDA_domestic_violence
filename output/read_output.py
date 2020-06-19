import pandas as pd

""" Reading output for text content
"""

model_scale = 1000


# Standard run for 200 times
def many_runs_output():
    o = pd.read_csv('output_200_10.csv', sep=';')
    o = o[(o.index + 1) % 11 == 0]
    runs = len(o)

    o.loc[:, 'Denounce per female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
    print(f"1. For {runs} runs, denounces per {model_scale} female is {o['Denounce per female'].mean()}")


def percentage(data, flag='Got attacked', flag2='dissuasion'):
    perc = (data.loc[True, flag] - data.loc[False, flag]) / data.loc[True, flag] * 100
    print(f"Percentual {flag} with {flag2} {perc:.2f}%")


def true_false_output(flag='dissuassion'):
    print(flag.title())
    o = pd.read_csv(f"output_200_8_dict_keys(['{flag}']).csv", sep=';')
    o.loc[:, 'Denounce per female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
    o = o.groupby(flag).agg('mean')[['Got attacked', 'Denounce per female']]
    print(o)
    percentage(o, 'Got attacked', flag)
    percentage(o, 'Denounce per female', flag)


def main():
    many_runs_output()
    true_false_output('dissuasion')
    true_false_output('quarantine')


if __name__ == '__main__':
    main()
