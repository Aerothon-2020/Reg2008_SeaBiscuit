from Aerothon.ACControls import ACControls
from Aircraft import Aircraft
from scalar.units import IN, LBF, SLUG, FT, ARCDEG, SEC
from scalar.units import AsUnit
import pylab as pyl
import numpy as npy

#
# Set-up AVL Controls Run
#
Controls = ACControls(Aircraft)
Controls.RunDir = 'AVLControls/'
Controls.AddRun('Stab', 'AVLAircraft.avl', WriteAVLInput = True)
Controls.Stab.DumpStability('AVLDeriv.txt')
Controls.Stab.Exit()

Controls.ExecuteAVL()

Controls.ReadAVLFiles()

Controls.Ixx = 0.314*SLUG*FT**2
Controls.Iyy = 0.414*SLUG*FT**2
Controls.Izz = 0.570*SLUG*FT**2

Controls.Weight = 7.4*LBF

Deriv = Controls.Deriv[0]

Deriv.StabilityTable(fig=1)

print "\n Aircraft MOI: ",Aircraft.MOI()
print 'Steady state roll rate: ', AsUnit( Deriv.RollDueToAileron(20 * ARCDEG, 'Aileron'), 'deg/s' )

Aircraft.Draw(2)
pyl.show()