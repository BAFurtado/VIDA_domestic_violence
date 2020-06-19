import pandas as pd

""" Reading output for text content
"""

# Standard run for 200 times
o = pd.read_csv('output_200_10.csv', sep=';')
o = o[(o.index + 1) % 11 == 0]
runs = len(o)
model_scale = 1000
o.loc[:, 'denounce_per_female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
print(f'1. For {runs} runs, denounces per {model_scale} female is {o.denounce_per_female.mean()}')

print('2. Dissuasion')
o = pd.read_csv("output_200_8_dict_keys(['dissuasion']).csv", sep=';')
o.loc[:, 'denounce_per_female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
o = o.groupby('dissuasion').agg('mean')[['Got attacked', 'denounce_per_female']]
print(o)
perc = (o.loc[True, 'Got attacked'] - o.loc[False, 'Got attacked']) / o.loc[True, 'Got attacked'] * 100
print(f"Percentual attacks with dissuasion {perc:.2f}%")

print('3. Quarantine')
o = pd.read_csv("output_200_8_dict_keys(['quarantine']).csv", sep=';')
o.loc[:, 'denounce_per_female'] = o.loc[:, 'Denounce'] / o.loc[:, 'Females'] * model_scale
o = o.groupby('quarantine').agg('mean')[['Got attacked', 'denounce_per_female']]
print(o)
perc = (o.loc[True, 'Got attacked'] - o.loc[False, 'Got attacked']) / o.loc[True, 'Got attacked'] * 100
print(f"Percentual attacks with quarantine {perc:.2f}%")
