import os
if __name__ == '__main__':
    os.chdir('..')

import numpy as np

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


def main(parameters, iterations=50):
    model_reporters = {
        "Person": lambda m: m.count_type_citizens(m, "person"),
        "Aggressor": lambda m: m.count_type_citizens(m, "aggressor"),
        "Stress": lambda m: m.count_stress(m)}
    batch_run = BatchRunner(model.Home, variable_parameters=parameters, max_steps=10, iterations=iterations,
                            model_reporters=model_reporters)
    batch_run.run_all()

    batch_df = batch_run.get_model_vars_dataframe()
    return batch_df


if __name__ == '__main__':
    """ Be careful. Number of runs = iterations * subdivisions ** num_parameters 
        120 * 8 ** 1
    """
    iterates = 120
    subdivisions = 8

    params = {'gender_stress': np.linspace(.1, .9, subdivisions)}
    params = {'under_influence': np.linspace(.01, .5, subdivisions)}
    params = {'has_gun': np.linspace(.1, .9, subdivisions)}
    params = {'is_working_pct': np.linspace(.1, .9, subdivisions)}
    params = {'chance_changing_working_status': np.linspace(.01, .5, subdivisions)}
    params = {'pct_change_wage': np.linspace(.01, .5, subdivisions)}
    params = {'metro': metropolis}
    df = main(params, iterations=iterates)
    df.loc[:, 'aggressor_pct'] = df['Aggressor'] / df['Person']
    df.to_csv(f'output_{iterates}_{subdivisions}_{params.keys()}.csv', sep=';', index=False)
