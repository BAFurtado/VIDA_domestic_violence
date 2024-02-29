import pytest
import os, sys
import numpy as np
import pandas as pd
sys.path.append('./violence/')
from violence.agents import Person
from violence.model  import Home
from violence.generalization_aps import merge_df

####### Test Suit #######

# Testing if assigned_spouse method is correctly returning an Person object
def test_assigned_spouse():
    model      = Home()
    main       = Person(np.random.randint(9), model,
                        (np.random.randint(9),np.random.randint(9)))
    assert isinstance(main.assign_spouse(main), Person)

# Testing auxiliary function to merge dataframes
def test_merge_df():
    num_rounds = np.random.randint(2, 8)
    sclar = {'test': [1, 2], 'test_0': [3, 4] }
    dataframes = [ pd.DataFrame.from_dict(sclar) for _ in range(num_rounds) ]
    new_data = merge_df(*dataframes)
    assert (new_data.shape[0] == num_rounds)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pytest.main()