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


def main(parameters, iterations=50, max_steps=None):
    model_reporters = {
        "Person": lambda m: m.count_type_citizens(m, "person"),
        "Aggressor": lambda m: m.count_type_citizens(m, "aggressor"),
        "Stress": lambda m: m.count_stress(m)}
    if not max_steps:
        batch_run = BatchRunner(model.Home, variable_parameters=parameters, max_steps=10, iterations=iterations,
                                model_reporters=model_reporters)
    else:
        batch_run = BatchRunner(model.Home, max_steps=max_steps, iterations=iterations, model_reporters=model_reporters)

    batch_run.run_all()

    batch_df = batch_run.get_model_vars_dataframe()
    return batch_df


if __name__ == '__main__':
    """ Be careful. Number of runs = iterations * subdivisions ** num_parameters 
        120 * 8 ** 1
    """
    iterates = 10
    subdivisions = 2

    params = {'gender_stress': np.linspace(.1, .9, subdivisions)}
    params = {'under_influence': np.linspace(.01, .5, subdivisions)}
    params = {'has_gun': np.linspace(.1, .9, subdivisions)}
    params = {'is_working_pct': np.linspace(.1, .9, subdivisions)}
    params = {'chance_changing_working_status': np.linspace(.01, .5, subdivisions)}
    params = {'quarantine': [False, True]}
    params = {'dissuasion': [False, True]}
    params = {'pct_change_wage': np.linspace(.01, .5, subdivisions)}
    params = {'metro': metropolis}
    # # Max steps
    for each in np.linspace(10, 200, 2):
        home = model.Home()
        for i in range(int(each)):
            home.step()

        model_df = home.datacollector.get_model_vars_dataframe()
        model_df.to_csv(f'output/output_{iterates}_{5}_{each}.csv', sep=';', index=False)
    #
    # print([self.schedule.time, self.schedule.get_breed_count(Person)])
    df = main(params, iterations=iterates)
    df.to_csv(f'output/output_{iterates}_{subdivisions}_{params.keys()}.csv', sep=';', index=False)
