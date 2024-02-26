import pytest
import os, sys
import numpy as np
sys.path.append('./violence/')
from violence.agents import Person
from violence.model  import Home

####### Test Suit #######

# Testing if assigned_spouse method is correctly returning an Person object
def test_assigned_spouse():
    model      = Home()
    main       = Person(np.random.randint(9), model,
                        (np.random.randint(9),np.random.randint(9)))
    assert isinstance(main.assign_spouse(main), Person)

def test_count_type_citizens():
    pass

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pytest.main()