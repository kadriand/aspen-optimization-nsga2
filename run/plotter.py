# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import matplotlib.pyplot as pyplot


class Plotter:
    generation_interval = 1
    pbr_xlabel = 'Costos de capital'
    pbr_ylabel = 'Costos de reactivo no recuperado'

    def __init__(self, problem):
        self.directory = 'plots'
        self.problem = problem

    def plot_population_best_front(self, population, generation_number):
        if generation_number == 0 or generation_number % Plotter.generation_interval == Plotter.generation_interval-1:
            filename = "{}/generation{}.png".format(self.directory, str(generation_number + 1))
            self.__create_directory_if_not_exists()
            computed_pareto_front = population.fronts[0]
            self.__plot_front(computed_pareto_front, filename, generation_number + 1)

    def plot_x_y(self, x, y, x_label, y_label, title, filename):
        filename = "{}/{}.png".format(self.directory, filename)
        self.__create_directory_if_not_exists()
        figure = pyplot.figure()
        axes = figure.add_subplot(111)
        axes.plot(x, y, 'r')
        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)
        axes.set_title(title)
        pyplot.savefig(filename)
        pyplot.close(figure)

    def write_report(self, pareto_front):
        with open("nsga-ii_report.info", 'w') as f:
            print("NSGA-II REPORT", file=f)
            print("Features : [Temperature, pressure, Buthanol flow, Acetic acid flow]", file=f)
            print("Objective function : [Temperature, pressure, Buthanol flow, Acetic acid flow]", file=f)
            print("Pareto front size: ", len(pareto_front), file=f)
            for indiv in pareto_front:
                print("\nIndividual ", pareto_front.index(indiv), file=f)
                print("Features: ", indiv.features, file=f)
                print("Objectives ", indiv.objectives, file=f)
                print("Violated constraints: ", indiv.violated_constraints, file=f)

    def __create_directory_if_not_exists(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def __plot_front(self, front, filename, gen_number):
        figure = pyplot.figure()
        axes = figure.add_subplot(111)

        computed_f1 = map(lambda individual: individual.objectives[0], front)
        computed_f2 = map(lambda individual: individual.objectives[1], front)
        axes.plot(computed_f1, computed_f2, 'g.')

        axes.set_xlabel(Plotter.pbr_xlabel)
        axes.set_ylabel(Plotter.pbr_ylabel)
        axes.set_title('Frente de pareto calculado - Generación %s'.decode("utf8") % gen_number)
        pyplot.savefig(filename)
        pyplot.close(figure)
