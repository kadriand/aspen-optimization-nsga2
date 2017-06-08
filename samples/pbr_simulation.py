import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import time

aspen = win32.Dispatch('Apwn.Document')
print("--- loading aspen .bkp file ---")
aspen.InitFromArchive2(os.path.abspath('simulation/PBR.bkp'))
print("--- .bkp file loaded---")


def run_simulation(temperature, filename):
    print("--- starting simulation ---")
    start_time = time.time()
    catalystWts = np.linspace(100, 200, 11)
    x_buoh, x_buacet = [], []

    # temperature = aspen.Tree.FindNode("\Data\Blocks\PBR\Input\REAC_TEMP").Value
    aspen.Tree.FindNode("\Data\Blocks\PBR\Input\REAC_TEMP").Value = temperature

    for catalyst in catalystWts:
        aspen.Tree.FindNode("\Data\Blocks\PBR\Input\CATWT").Value = catalyst
        aspen.Engine.Run2()
        x_buoh.append(aspen.Tree.FindNode("\Data\Streams\OUTPUT\Output\MOLEFLOW\MIXED\BUTANOL").Value)
        x_buacet.append(aspen.Tree.FindNode("\Data\Streams\OUTPUT\Output\MOLEFLOW\MIXED\BUT-ACET").Value)

    plt.plot(catalystWts, x_buacet, catalystWts, x_buoh)
    plt.title('PBR profile at %s' % temperature)
    plt.legend(['Butyl Acetate', 'Buthanol'])
    plt.xlabel('Catalyst weight (kg)')
    plt.ylabel('Mole flows, mol/h')
    plt.savefig('images/' + filename + '-buac-test.png')
    plt.clf()
    plt.close()
    print("--- %s seconds ---" % (time.time() - start_time))

    response = PbrSimulation(temperature)
    return response


class PbrSimulation:
    def __init__(self, temperature):
        self.temperature = temperature


def close_aspen():
    print("--- closing simulation ---")
    aspen.close()
