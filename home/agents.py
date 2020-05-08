from mesa.agent import Agent


class Person(Agent):
    """
    A person who lives within a family, incurs in chance of suffering violence.

    """

    def __init__(self, unique_id, model, pos, gender='male', age=25, color='negra',
                 years_study=6, has_gun=False, is_working=False,
                 wage=0, reserve_wage=.5, under_influence=False,
                 category='person', denounce=False, condemnation=False,
                 knowledge_protection=False, knowledge_condemnation=False):
        super().__init__(unique_id, model)
        self.pos = pos
        self.gender = gender
        # Higher incidence of atack by 15-29. Victims 20-50
        self.age = age
        # H: Ethnicity influences victimization, likelihood increases 30%
        self.color = color
        # H: Education less than 6, likelihood increases 60%
        self.years_study = years_study
        self.has_gun = has_gun
        self.is_working = is_working
        self.reserve_wage = reserve_wage
        self.under_influence = under_influence
        self.wage = wage
        # Include: escolaridade (autor e vitima), posse de arma, dependencia quimica,
        # Dissuassão:
        self.spouse = None
        self.got_attacked = 0
        self.assaulted = 0
        self.hours_home = .34 if self.is_working else .67
        self.family = None
        # Correlate wage and numbers of family: likelihood that people by room is relevant
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
        # Check and execute
        if self.age > 18:
            self.trigger_violence()
        else:
            pass

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
        self.step_change()
        # Update num_members_family
        self.num_members_family = len(self.family.members)

        # Update stress based on gender, wage level, hours at home, family size and history of violence
        # Check new table of influences
        # Wage influences neighborhood_influence and house_size
        tmp = self.model.gender_stress if self.gender == 'male' else 1 - self.model.gender_stress
        tmp *= (1 - self.wage)
        tmp *= self.hours_home
        tmp **= 1/self.num_members_family
        tmp **= 1/(1 + self.assaulted)
        self.stress = tmp

    def trigger_violence(self):
        """
        Uses self stress and family context to incur in probability of becoming violent
        """
        self.update_stress()

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
        for agents in self.members.values():
            stress += agents.stress
        self.context_stress = stress / len(self.members)


if __name__ == '__main__':
    # Bernardo's debugging model
    from home_violence.home.model import Home
    m1 = Home()
    bob = m1.schedule.agents[0]
    maria = m1.schedule.agents[1]
    f1 = Family(m1.next_id(), m1, (1, 1))
    f1.add_agent(bob)
    f1.add_agent(maria)
    bob.assign_spouse(maria)
    bob.update_stress()
    bob.trigger_violence()
    bob.stress = 1
    bob.trigger_violence()
