import os
if __name__ == '__main__':
    os.chdir('/home/furtadobb/MyModels/home_violence/')

import numpy as np
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from violence import model
from violence.input.generator import metropolis

# With the BatchRunner
# ___________ parameters to change:
#     metro = metropolis
#     gender_stress = .8,
#     under_influence = .1,
#     has_gun = .5,
#     is_working_pct = .8,
#     chance_changing_working_status = .05,
#     pct_change_wage = .05,


def plot(data, group_col, plot_col):
    data = data.groupby(group_col).agg('median').reset_index()
    data.plot(x=group_col, y=plot_col)
    plt.show()


def main(parameters, iterations=50):
    model_reporters = {
        "Person": lambda m: m.count_type_citizens(m, "person"),
        "Aggressor": lambda m: m.count_type_citizens(m, "aggressor"),
        "Stress": lambda m: m.count_stress(m)}
    batch_run = BatchRunner(model.Home, parameters, max_steps=10, iterations=iterations,
                            model_reporters=model_reporters)
    batch_run.run_all()

    batch_df = batch_run.get_model_vars_dataframe()
    return batch_df


if __name__ == '__main__':
    subdivisions = 2
    # Remember to use BatchRunnerMP
    # Remember to save figures and database
    params = {'gender_stress': np.linspace(.1, .9, subdivisions),
              'under_influence': np.linspace(.01, .5, subdivisions),
              'has_gun': np.linspace(.1, .9, subdivisions),
              'is_working_pct': np.linspace(.1, .9, subdivisions),
              'chance_changing_working_status': np.linspace(.01, .5, subdivisions),
              'pct_change_wage': np.linspace(.01, .5, subdivisions)}
              #'metro': metropolis}
    df = main(params, iterations=2)
    df.loc[:, 'aggressor_pct'] = df['Aggressor'] / df['Person']
    for each in params.keys():
        plot(df, each, "Stress")
        plot(df, each, "aggressor_pct")
