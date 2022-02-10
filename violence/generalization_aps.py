
import pickle

import pandas as pd
from collections import defaultdict

from agents import Person
import model


def main(metro='BRASILIA', iterates=500, steps=10):
    """ Be careful. Number of runs = iterations * subdivisions ** num_parameters 
        120 * 8 ** 1
    """
    data = pd.DataFrame(columns=['index', 'attacked', 'denounce', 'females', 'Attacks per female',
                                 'Denounces per female']).astype(int)
    # Run each metropolis a number of times
    for each in range(iterates):
        # For each model. Instantiate a model and move up to steps
        home = model.Home(metro=metro)
        for i in range(steps):
            home.step()
        attacked, denounced, females = defaultdict(int), defaultdict(int), defaultdict(int)
        # Gather the data from that run
        for a in home.schedule.agents:
            if isinstance(a, Person) and a.gender == 'female':
                attacked[a.address] += a.got_attacked
                denounced[a.address] += a.denounce
                females[a.address] += 1
        df_attack = pd.DataFrame.from_dict(attacked, orient='index', columns=['attacked'])
        df_denounce = pd.DataFrame.from_dict(denounced, orient='index', columns=['denounce'])
        df_females = pd.DataFrame.from_dict(females, orient='index', columns=['females'])
        df = pd.merge(df_attack, df_denounce, right_index=True, left_index=True)
        df = df.merge(df_females, right_index=True, left_index=True)
        df.loc[:, 'Attacks per female'] = df.loc[:, 'attacked'] / df.loc[:, 'females'] * home.model_scale
        df.loc[:, 'Denounces per female'] = df.loc[:, 'denounce'] / df.loc[:, 'females'] * home.model_scale
        df = df.reset_index()
        df.loc[:, 'run'] = each
        data = data.append(df)
    data = data.groupby('index').agg('mean')
    data = data.reset_index()
    data = data.rename(columns={'index': 'AREAP'})
    data = data[['AREAP', 'attacked', 'denounce', 'females', 'Attacks per female', 'Denounces per female']]
    data.to_csv(f'output/output_{iterates}_{metro}.csv', sep=';', index=False)
    return data


if __name__ == '__main__':
    out = dict()
    for metro in ['BRASILIA', 'PORTO ALEGRE', 'CURITIBA', 'BELO HORIZONTE', 'RECIFE', 'VITORIA', 'RIO DE JANEIRO']:
        out[metro] = main(metro=metro)
    with open('output/results.json', 'wb') as h:
        pickle.dump(out, h)
