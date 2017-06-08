"""Module with definition of ZDT problem interface"""
import buac_production.pbr_props as pbr_props
from nsga2.individual import Individual
from nsga2_problems import Problem
import random
import functools


class PBRCosts(Problem):
    def __init__(self, problem_definitions):
        self.problem_definitions = problem_definitions
        self.max_objectives = [None, None]
        self.min_objectives = [None, None]
        self.problem_type = None
        # VARIES
        self.n = 4

    def __dominates(self, individual2, individual1):
        worse_than_other = individual1.objectives[0] <= individual2.objectives[0] and individual1.objectives[1] <= individual2.objectives[1]
        better_than_other = individual1.objectives[0] < individual2.objectives[0] or individual1.objectives[1] < individual2.objectives[1]
        constraints = individual1.violated_constraints != -1 and individual1.violated_constraints < individual2.violated_constraints

        # worse_than_other = self.zdt_definitions.f1(individual1) <= self.zdt_definitions.f1(individual2) and self.zdt_definitions.f2(individual1) <= self.zdt_definitions.f2(individual2)
        # better_than_other = self.zdt_definitions.f1(individual1) < self.zdt_definitions.f1(individual2) or self.zdt_definitions.f2(individual1) < self.zdt_definitions.f2(individual2)
        return (worse_than_other and better_than_other) or constraints

    def generateIndividual(self):
        individual = Individual()
        individual.features = []

        # HERE WE HANDLE THE SEARCH SPACE
        # for i in range(self.n):
        #     individual.features.append(random.random())

        react_temp = random.uniform(pbr_props.temperature_lower_bound, pbr_props.temperature_upper_bound)
        react_pres = random.uniform(pbr_props.pressure_lower_bound, pbr_props.pressure_upper_bound)
        react_buoh = random.uniform(pbr_props.mole_flows_lower_bound, pbr_props.mole_flows_upper_bound)
        react_acac = random.uniform(pbr_props.mole_flows_lower_bound, pbr_props.mole_flows_upper_bound)

        individual.features.append(react_temp)
        individual.features.append(react_pres)
        individual.features.append(react_buoh)
        individual.features.append(react_acac)

        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        # self.calculate_objectives(individual)
        return individual

    def calculate_objectives(self, individual):
        # individual.objectives = []
        # individual.objectives.append(self.zdt_definitions.f1(individual))
        # individual.objectives.append(self.zdt_definitions.f2(individual))
        self.problem_definitions.evaluate(individual)

        for i in range(2):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
