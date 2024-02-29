"""
A simple violence model, based on attacker and victim characteristics and stay-at-home time.

"""
import numpy as np
import pandas as pd

from mesa       import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from agents     import Person, Family
from schedule   import RandomActivationByBreed
from input      import generator
from input.generator import metropolis

class Home(Model):
    """
    A Home Violence Simulation Model
    """

    verbose = True  # Print-monitoring
    description = 'A model for simulating the victim aggressor interaction.'

    def __init__(self, height=40, width=40,
                 initial_families               =  1000,
                 metro                          = 'BRASILIA',
                 gender_stress                  = .8,
                 under_influence                = .1,
                 has_gun                        = .1,
                 is_working_pct                 = .8,
                 chance_changing_working_status = .05,
                 pct_change_wage                = .05,
                 model_scale                    = 1000,
                 quarantine                     = False,
                 dissuasion                     = True,
                 data_year                      = 2010
                 ):
        """
        A violence model of Brazilian metropolis

        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width

        self.initial_families = initial_families
        self.metro = metro

        self.gender_stress = gender_stress
        self.under_influence = under_influence
        self.has_gun = has_gun
        self.is_working_pct = is_working_pct
        self.chance_changing_working_status = chance_changing_working_status
        self.pct_change_wage = pct_change_wage
        self.model_scale = model_scale
        self.quarantine = quarantine
        self.dissuasion = dissuasion
        self.data_year = data_year
        self.neighborhood_stress = dict()

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        # Model reporters. How they work: lambda function passes model and other parameters.
        # Then another function may iterate over each 'agent in model.schedule.agents'
        # Then server is going to collect info using the keys in model_reporters dictionary
        model_reporters = {
            "Denounce": lambda m: self.count_type_citizens(m, 'denounce'),
            "Got attacked": lambda m: self.count_type_citizens(m, 'got_attacked'),
            "Females": lambda m: self.count_type_citizens(m, 'female'),
            "Stress": lambda m: self.count_stress(m)}
        self.datacollector = DataCollector(model_reporters=model_reporters)

        # Create people ---------------------------------------------------
        # Parameters to choose metropolitan region
        # More details available at input/population
        params = dict()
        params['PROCESSING_ACPS'] = [self.metro]
        params['MEMBERS_PER_FAMILY'] = 2.5
        params['INITIAL_FAMILIES'] = self.initial_families
        params['DATA_YEAR'] = self.data_year
        people, families = generator.main(params=params)
        # General random data for each individual
        n = sum([len(f) for f in families])
        working = np.random.choice([True, False], n, p=[self.is_working_pct, 1 - self.is_working_pct])
        influence = np.random.choice([True, False], n, p=[self.under_influence, 1 - self.under_influence])
        gun = np.random.choice([True, False], n, p=[self.has_gun, 1 - self.has_gun])
        i = 0
        for fam in families:
            # 1. Create a family.
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # Create a family
            family = Family(self.next_id(), self, (x, y))
            # Add family to grid
            self.grid.place_agent(family, (x, y))
            self.schedule.add(family)
            # Marriage procedures
            engaged = ['male_adult', 'female_adult']
            to_marry = list()
            # Add people to families
            for each in fam:
                person = people.loc[each]
                doe = Person(self.next_id(), self, (x, y),
                             # From IBGE's sampling
                             gender=person.gender,
                             age=person.age,
                             color=person.cor,
                             address=person.AREAP,
                             years_study=person.years_study,
                             reserve_wage=person.wage,
                             # End of sampling
                             is_working=working[i],
                             under_influence=influence[i],
                             has_gun=gun[i])
                # Marrying
                if len(engaged) > 0:
                    if person.category in engaged:
                        engaged.remove(person.category)
                        to_marry.append(doe)
                # Change position in the random list previously sampled
                i += 1
                self.grid.place_agent(doe, (x, y))
                self.schedule.add(doe)
                family.add_agent(doe)
            # 2. Marry the couple
            if len(to_marry) == 2:  
                to_marry[0].assign_spouse(to_marry[1])

            # 3. Update number of family members
            for member in family.members.values():
                member.num_members_family = len(family.members)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.update_neighborhood_stress()
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Check if step will happen at individual levels or at family levels or BOTH
        if self.verbose:
            print([self.schedule.time, self.schedule.get_breed_count(Person)])

        # New condition to stop the model
        if self.schedule.get_breed_count(Person) == 0:
            self.running = False

    def update_neighborhood_stress(self):
        # Start from scratch every step
        self.neighborhood_stress = dict()
        counter = dict()
        for agent in self.schedule.agents:
            if isinstance(agent, Family):
                self.neighborhood_stress[agent.address] = self.neighborhood_stress.get(agent.address, 0) + \
                                                          agent.context_stress
                counter[agent.address] = counter.get(agent.address, 0) + 1
        for key in self.neighborhood_stress.keys():
            self.neighborhood_stress[key] = self.neighborhood_stress[key] / counter[key]
            # print(f'This neighborhood {key} stress levels is at {self.neighborhood_stress[key]}')

    @staticmethod
    def count_type_citizens(model: Model, condition):
        """
        Helper method to count agents by Type.
        """
        func_set = {
            'denounce':     lambda agent: agent.denounce,
            'got_attacked': lambda agent: agent.got_attacked,
            'female':       lambda agent: 1 if agent.gender == 'female' and agent.age > 18 else 0
        } 
        return np.sum([ func_set[condition](agent) if isinstance(agent, Person) else 0 
                        for agent in model.schedule.agents ])

    @staticmethod
    def count_stress(model):
        """
        Return the mean of the context_stress
        """
        return np.mean([ agent.context_stress for agent in model.schedule.agents
                         if isinstance(agent, Family) ]) if model.schedule.agents.__len__() else 0

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number of people: ', self.schedule.get_breed_count(Person))

        # Steps are not being set here, but on superclass. Changes should be made in the step function above!
        for _ in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number People: ', self.schedule.get_breed_count(Person))


def generate_output():
    # Running for all metropolis
    output = pd.DataFrame(columns=['metropolis', 'stress'])
    for metro in metropolis:
        home = Home(metro=metro)
        for _ in range(10):
            home.step()
        model_df = home.datacollector.get_model_vars_dataframe()
        output.loc[output.shape[0]] = [metro, model_df.loc[9, 'Stress']]
    output.to_csv('input/output.csv', sep=';', index=False)


if __name__ == '__main__':
    # my debugging
    # generate_output()
    home = Home()
    for j in range(10):
        home.step()
    model_df = home.datacollector.get_model_vars_dataframe()

    # To generate a number of runs of a metro, before BatchRunner
    # otp = pd.DataFrame(columns=['metropolis', 'stress'])
    # metro = 'JOINVILLE'
    # for i in range(20):
    #     home = Home(metro=metro)
    #     for j in range(10):
    #         home.step()
    #     model_df = home.datacollector.get_model_vars_dataframe()
    #     otp.loc[otp.shape[0]] = [metro, model_df.loc[9, 'Stress']]
    # otp.to_csv('joinville.csv', sep=';', index=False)