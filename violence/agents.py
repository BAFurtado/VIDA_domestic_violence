from mesa.agent import Agent

HIGH = 10
MEDIUM = 5
LOW = 1


class Person(Agent):
    """
    A person who lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model, pos, gender='male', age=25, color='negra',
                 years_study=6, has_gun=False, is_working=False,
                 wage=0, reserve_wage=.5, under_influence=False, address=None,
                 category='person', denounce=False, condemnation=False,
                 knowledge_protection=False, knowledge_condemnation=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.gender = gender
        self.age = age
        self.color = color
        self.years_study = years_study
        self.has_gun = has_gun
        self.is_working = is_working
        self.reserve_wage = reserve_wage
        self.under_influence = under_influence
        self.wage = wage
        self.address = address
        # Set during the simulation
        self.spouse = None
        self.got_attacked = 0
        self.assaulted = 0
        self.hours_home = .34 if self.is_working else .67
        self.family = None
        self.num_members_family = 1
        self.stress = 0
        self.category = category
        # Measures of dissuasion
        self.denounce = denounce
        self.condemnation = condemnation
        self.knowledge_protection = knowledge_protection
        self.knowledge_condemnation = knowledge_condemnation

    def step(self):
        """
        A model step.
        """
        self.update_stress()

        # Check and execute: if male, if adult, if got a victim at violence
        if self.gender == 'male':
            if self.age > 18:
                if self.spouse is not None:
                    self.trigger_violence()

    def step_change(self):
        # How conditions that cause stress change?
        if self.model.random.random() < self.model.chance_changing_working_status:
            self.is_working = not self.is_working
            if not self.is_working:
                self.wage = 0
            else:
                self.reserve_wage *= self.model.random.uniform(-self.model.pct_change_wage, self.model.pct_change_wage)
                self.wage = self.reserve_wage
            self.hours_home = .34 if self.is_working else .67

    def assign_spouse(self, agent):
        self.spouse = agent
        agent.spouse = self

    def update_stress(self):
        # Although all adults stress is updated, only 'males' are aggressors
        # Before updating stress, check whether conditions have changed
        self.step_change()

        # Update stress based on gender, wage level, hours at home, family size and history of violence
        # Check new table of influences at README.md
        # Wage influences neighborhood_quality and house_size
        # Gender
        # We fixed gender stress for females in .2
        tmp = self.model.gender_stress if self.gender == 'male' else .2
        # Salary
        tmp += (1 - self.wage) * HIGH
        # Neighborhood quality
        tmp += -self.family.family_wage * MEDIUM
        # House size: higher the wage or smaller the wage per person, less contribution to stress
        tmp += 1 - (self.family.family_wage / self.num_members_family) * MEDIUM

        # Hypothesis 1: # Education Education less than 6, likelihood increases by 60%
        if self.years_study < 6:
            tmp += (1 - (self.years_study / 10)) * 1.6 * HIGH
        else:
            tmp += (1 - (self.years_study / 10)) * HIGH
        # Hypothesis 2: # Higher incidence of attack by male between 15-29 years old
        if 18 > self.age > 29:
            tmp *= HIGH
        # Hypothesis 3: Ethnicity influences victimization, likelihood increases 30% when spouse is black
        # This stress indicator will only update for married males
        if self.spouse is not None:
            if self.spouse.color == 'preta':
                tmp *= 1.3
            # Hypothesis 4: relevance of women participating in the labor market
            if not self.spouse.is_working:
                # Increases -- level HIGH -- when spouse is NOT working
                # TODO: Find working data by gender by metropolis
                tmp += 1 * HIGH

        # Home permanence
        if not self.model.quarantine:
            tmp += self.hours_home * MEDIUM
        else:
            tmp += 1 * MEDIUM
        # History of assault. This stress indicator updates only for those 'male' attackers who already have a history
        tmp += self.assaulted / 10 * HIGH
        # Access to weapon
        tmp += 1 * HIGH if self.has_gun else 0
        # Chemical dependence
        tmp += 1 * self.model.random.random() * HIGH if self.under_influence else 0
        # General effect adjustment
        tmp /= self.model.model_scale
        self.stress = tmp

    def trigger_violence(self):
        """
        Uses self stress and family context to incur in probability of becoming violent
        """
        # First time offender get registered in the system and changes class as an Aggressor and a Victim
        if self.assaulted == 0:
            if self.stress > self.random.random():
                self.category = 'aggressor'
                self.assaulted += 1
                self.spouse.category = 'victim'
                self.spouse.got_attacked += 1

        # Second-time offender, checks to see if it is a recidivist.
        elif self.stress > self.random.random():
            self.assaulted += 1
            self.spouse.got_attacked += 1

    def trigger_call_help(self):
        # TODO: implement dissuasion
        # TODO: check two scenarios
        pass


class Family(Agent):
    """
    A family that provides the environment and contain agents who might become victims or aggressors
    """

    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.context_stress = 0
        self.members = dict()
        self.family_wage = 0

    def add_agent(self, agent):
        self.members[agent.unique_id] = agent
        agent.family = self

    def step(self):
        """
        A model step.
        """
        # It will include family stress indicator update
        # Likelihood of triggering aggression
        # New values
        stress = 0
        self.family_wage = 0
        for agent in self.members.values():
            stress += agent.stress
            self.family_wage += agent.wage
        self.context_stress = stress / len(self.members)
