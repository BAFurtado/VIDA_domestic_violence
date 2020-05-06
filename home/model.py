"""
A simple victim x aggressor encounter model
================================
Directly adapted from mesa example which is inspired by the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/GunsPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""
import numpy as np
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

try:
    from home.agents import Person, Family
    from home.schedule import RandomActivationByBreed
except ModuleNotFoundError:
    from agents import Person, Family
    from schedule import RandomActivationByBreed


class Home(Model):
    """
    A Home Violence Simulation Model
    """

    verbose = True  # Print-monitoring
    description = 'A model for simulating the victim aggressor interaction mediated by presence of home.'

    def __init__(self, height=40, width=40,
                 initial_families=400,
                 gender_stress=0.80,
                 is_working_pct=0.80,
                 chance_changing_working_status=0.05,
                 pct_change_wage=0.05):
        """
        Create a new Guns model with the given parameters.

        Args:
            initial_families: Number of families to start with
            initial_people: Number of people to start with

        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_families = initial_families

        self.gender_stress = gender_stress
        self.is_working_pct = is_working_pct
        self.chance_changing_working_status = chance_changing_working_status
        self.pct_change_wage = pct_change_wage

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        model_reporters = {
            "Person": lambda m: self.count_type_citizens(m, "person"),
            "Victim": lambda m: self.count_type_citizens(m, "victim"),
            "Aggressor": lambda m: self.count_type_citizens(m, "aggressor"),
            "Stress": lambda m: self.count_stress(m)}
        self.datacollector = DataCollector(model_reporters=model_reporters)

        # Create people:
        for i in range(self.initial_families):
            # 1. Create a family. Create a couple, add to the family
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # Create a family
            family = Family(self.next_id(), self, (x, y))
            # Add family to grid
            self.grid.place_agent(family, (x, y))
            self.schedule.add(family)
            # Add people to families
            to_marry = list()
            for gender in ['male', 'female']:
                adult = Person(self.next_id(), self, (x, y), gender=gender,
                               age=round(self.random.triangular(19, 80, 34)),
                               is_working=np.random.choice([True, False],
                                                           p=[self.is_working_pct, 1 - self.is_working_pct]),
                               reserve_wage=np.random.beta(2, 5))
                self.grid.place_agent(adult, (x, y))
                self.schedule.add(adult)
                family.add_agent(adult)
                to_marry.append(adult)
            # 2. Marry the couple
            to_marry[0].assign_spouse(to_marry[1])
            # 3. Create some children, Add to the family
            num_children = int(self.random.triangular(0, 5, 1.8))
            for ch in range(num_children):
                child = Person(self.next_id(), self, (x, y), gender=np.random.choice(['female', 'male'], p=[.6, .4]),
                               age=round(self.random.triangular(0, 18, 9)),
                               is_working=False,
                               wage=0)
                self.grid.place_agent(child, (x, y))
                self.schedule.add(child)
                family.add_agent(child)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Check if step will happen at individual levels or at family levels or BOTH
        if self.verbose:
            print([self.schedule.time, self.schedule.get_breed_count(Person)])

        # New condition to stop the model
        if self.schedule.get_breed_count(Person) == 0:
            self.running = False

    @staticmethod
    def count_type_citizens(model, condition):
        """
        Helper method to count agents by Type.
        """
        count = 0
        for agent in model.schedule.agents:
            if isinstance(agent, Person):
                if agent.category == condition:
                    count += 1
        return count

    @staticmethod
    def count_stress(model):
        count, size = 0, 0
        for agent in model.schedule.agents:
            if isinstance(agent, Family):
                count += agent.context_stress
                size += 1
        return count / size

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number of people: ', self.schedule.get_breed_count(Person))

        # Steps are not being set here, but on superclass. Changes should be made in the step function above!
        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number People: ', self.schedule.get_breed_count(Person))


if __name__ == '__main__':
    # Bernardo's debugging
    my_model = Home()
    my_model.run_model()
