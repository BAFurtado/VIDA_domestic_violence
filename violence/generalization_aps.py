#import pickle
import pandas as pd
from collections import defaultdict
from agents import Person
import model

def merge_df(*dataFrames) -> pd.DataFrame:
    return pd.merge(*dataFrames, right_index=True, left_index=True)

def main(metro='BRASILIA', iterates=5, steps=10):
    """ Be careful. Number of runs = iterations * subdivisions ** num_parameters 
        120 * 8 ** 1
    """
    data = pd.DataFrame(columns=['index', 'attacked', 'denounce', 'females', 'Attacks per female',
                                 'Denounces per female']).astype(int)
    # Run each metropolis a number of times
    for each in range(iterates):
        # For each model. Instantiate a model and move up to steps
        home = model.Home(metro=metro)

        # Execute the number of steps
        list(map(lambda _: home.step(), range(steps)))
        # for _ in range(steps): home.step()

        attacked, denounced, females = defaultdict(int), defaultdict(int), defaultdict(int)
        # Gather the data from that run
        
        update_info = lambda agent, attacked, denounced, females: \
        (
        attacked[agent.address]    + agent.got_attacked,
        denounced[agent.address]   + agent.denounce,
        females[agent.address]     + 1
        )
        
        for agent in home.schedule.agents:
            if isinstance(agent, Person) and agent.gender == 'female':
                attacked[agent.address], denounced[agent.address], females[agent.address] = \
                                         update_info(agent, attacked, denounced, females)
                
            # attacked[a.address] += a.got_attacked
            # denounced[a.address] += a.denounce
            # females[a.address] += 1
        
        # Create columns DataFrames to merge
        df_attack   = pd.DataFrame.from_dict(attacked, orient='index', columns=['attacked'])
        df_denounce = pd.DataFrame.from_dict(denounced, orient='index', columns=['denounce'])
        df_females  = pd.DataFrame.from_dict(females, orient='index', columns=['females'])

        # Merge Dataframes
        df          = merge_df(df_attack, df_denounce, df_females) 
        # df = pd.merge(df_attack, df_denounce, right_index=True, left_index=True)
        # df = df.merge(df_females, right_index=True, left_index=True)

        df['Attacks per female']   = df.loc[:, 'attacked'] / df.loc[:, 'females'] * home.model_scale
        df['Denounces per female'] = df.loc[:, 'denounce'] / df.loc[:, 'females'] * home.model_scale

        df = df.reset_index()

        # Indexing fault issue
        if not df.empty: df.loc[:, 'run'] = each
        data = data._append(df)

    data = data.groupby('index').agg('mean')
    data = data.reset_index()

    data = data.rename(columns={'index': 'AREAP'})
    data = data[['AREAP', 'attacked', 'denounce', 'females', 'Attacks per female', 'Denounces per female']]
    data.to_csv(f'output/output_{iterates}_{metro}.csv', sep=';', index=False)
    return data

if __name__ == '__main__':
    out = dict()
    metropolis = ["CAMPO GRANDE"]
    for m in metropolis:
        out[m] = main(metro=m)
    # with open('output/results.json', 'wb') as h:
    #     pickle.dump(out, h)
