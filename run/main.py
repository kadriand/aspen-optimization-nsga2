import buac_production.pbr_engine as pbr_engine
import buac_production.pbr_props as pbr_props
from nsga2.metrics.problems.zdt import ZDT3Metrics
from nsga2.evolution import Evolution
from nsga2_problems.impl import PBRCosts
from nsga2_problems.impl.pbr_definitions import PBRDefinitions
from plotter import Plotter
import time

start_time = time.time()


def print_generation(population, generation_num):
    print("Generation: {}".format(generation_num+1))


collected_metrics = {}


def collect_metrics(population, generation_num):
    pareto_front = population.fronts[0]
    metrics = ZDT3Metrics()
    hv = metrics.HV(pareto_front)
    hvr = metrics.HVR(pareto_front)
    collected_metrics[generation_num] = hv, hvr


pbr_props.show_info = True

pbr_definitions = PBRDefinitions()
plotter = Plotter(pbr_definitions)
problem = PBRCosts(pbr_definitions)
evolution = Evolution(problem, 50, 50)
evolution.register_on_new_generation(plotter.plot_population_best_front)
evolution.register_on_new_generation(print_generation)
evolution.register_on_new_generation(collect_metrics)
pareto_front = evolution.evolve()
plotter.write_report(pareto_front)

pbr_engine.close_aspen()

# plotter.plot_x_y(collected_metrics.keys(), map(lambda (hv, hvr): hvr, collected_metrics.values()), 'generation', 'HVR', 'HVR metric for PBR problem', 'hvr-pbr_problem')
print("--- Whole run: %s seconds ---" % (time.time() - start_time))
