import buac_production.pbr_engine as pbr_engine
import buac_production.pbr_props as pbr_props
from nsga2_problems.problem_definitions import ProblemDefinitions


class PBRDefinitions(ProblemDefinitions):
    eval_counter = 0

    def __init__(self):
        self.n = 4

    def f1(self, individual):
        return individual.features[0]

    def f2(self, individual):
        return individual.features[0]

    def evaluate(self, individual):
        individual.objectives = []

        simulation_obj = pbr_engine.run(individual.features[0], individual.features[1], individual.features[2], individual.features[3])
        simulation_obj.calculate_costs()
        simulation_obj.constraints_violations()

        individual.objectives.append(simulation_obj.capital_costs)
        individual.objectives.append(simulation_obj.losses_costs)
        individual.violated_constraints = simulation_obj.constraints_count
        PBRDefinitions.eval_counter += 1

        if pbr_props.show_info and PBRDefinitions.eval_counter % 5 == 0:
            print 'evaluation counter ', PBRDefinitions.eval_counter
