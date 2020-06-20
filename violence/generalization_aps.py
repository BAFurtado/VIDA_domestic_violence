import os
if __name__ == '__main__':
    os.chdir('..')

import pandas as pd
from collections import defaultdict

from violence.agents import Person
from violence import model


def main(metro='BRASILIA', iterates=200, steps=10):
    """ Be careful. Number of runs = iterations * subdivisions ** num_parameters 
        120 * 8 ** 1
    """
    data = pd.DataFrame(columns=['index', 'attacked', 'denounce']).astype(int)
    # Run each metropolis a number of times
    for each in range(iterates):
        # For each model. Instantiate a model and move up to steps
        home = model.Home()
        for i in range(steps):
            home.step()
        attacked = defaultdict(int)
        denounced = defaultdict(int)
        # Gather the data from that run
        for a in home.schedule.agents:
            if isinstance(a, Person) and a.gender == 'female':
                attacked[a.address] += a.got_attacked
                denounced[a.address] += a.denounce
        df_attack = pd.DataFrame.from_dict(attacked, orient='index', columns=['attacked'])
        df_denounce = pd.DataFrame.from_dict(denounced, orient='index', columns=['denounce'])
        df = pd.merge(df_attack, df_denounce, right_index=True, left_index=True)
        df = df.reset_index()
        df.loc[:, 'run'] = each
        data = data.append(df)
    data = data.groupby('index').agg('mean')
    data = data.rename(columns={'index': 'AREAP'})
    data = data[['AREAP', 'attacked', 'denounce']]
    data.to_csv(f'output/output_{iterates}_{metro}', sep=';', index=False)
    return data


if __name__ == '__main__':
    d = main(metro='BRASILIA', iterates=5)
