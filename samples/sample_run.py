import os
import numpy as np
import matplotlib.pyplot as plt
import win32com.client as win32
import time

start_time = time.time()

aspen = win32.Dispatch('Apwn.Document')
aspen.InitFromArchive2(os.path.abspath('simulation/PBR.bkp'))
catalystWts = np.linspace(1, 2, 21)

x_buoh, x_buacet = [], []

for catalyst in catalystWts:
    aspen.Tree.FindNode("\Data\Blocks\PBR\Input\CATWT").Value = catalyst
    aspen.Engine.Run2()
    x_buoh.append(aspen.Tree.FindNode("\Data\Streams\OUTPUT\Output\MOLEFLOW\MIXED\BUTANOL").Value)
    x_buacet.append(aspen.Tree.FindNode("\Data\Streams\OUTPUT\Output\MOLEFLOW\MIXED\BUT-ACET").Value)

plt.plot(catalystWts, x_buacet, catalystWts, x_buoh)
plt.legend(['Butyl Acetate', 'Buthanol'])
plt.xlabel('Catalyst weight (kg)')
plt.ylabel('Mole flows')
plt.savefig('images/aspen-buac-test.png')
aspen.Close()
print("--- %s seconds ---" % (time.time() - start_time))
