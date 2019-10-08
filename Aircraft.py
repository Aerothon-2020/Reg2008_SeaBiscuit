from __future__ import division # let 5/2 = 2.5 rather than 2
from scalar.units import M, FT, IN, ARCDEG, RAD, LBF, SEC, KG, SLUG
from scalar.units import AsUnit
from Aerothon.ACAircraft import ACTailAircraft
from Aerothon.ACWingWeight import ACSolidWing, ACRibWing
from Aerothon.DefaultMaterialsLibrary import Monokote, PinkFoam, Basswood, Steel, Balsa, CarbonBar
from Fuselage import Fuselage
from Propulsion import Propulsion
from BiWing import BoxWing
import pylab as pyl
import cmath as math
from Aerothon.ACTLenAircraft import ACTLenAircraft

#
# Create the Aircraft from the ACTLenAircraft class, which limits the sum of the L,W,and H
#
Aircraft = ACTLenAircraft()
Aircraft.name = 'Aircraft2008'

#
# The total allowable lengths summing height + width + length of the aircraft
#
Aircraft.TotalLengths = 174*IN

# 
# Assign the already generated parts
#
Aircraft.SetFuselage(Fuselage)
Aircraft.SetPropulsion(Propulsion)
Aircraft.SetWing(BoxWing)

#
# Position the wing on the bottom of the fuselage
#
Aircraft.WingFuseFrac = -0.30

#
# Aircraft Properties
#
Aircraft.TotalWeight = 31*LBF

Aircraft.TippingAngle     = 10*ARCDEG
Aircraft.RotationAngle    = 10*ARCDEG
Aircraft.Alpha_Groundroll = 0*ARCDEG
    
Aircraft.CMSlopeAt   = (10 * ARCDEG, 11 * ARCDEG)
Aircraft.CLSlopeAt   = (6  * ARCDEG, 7  * ARCDEG) 
Aircraft.CLHTSlopeAt = (8  * ARCDEG, 9  * ARCDEG) 
Aircraft.DWSlopeAt   = (7  * ARCDEG, 8  * ARCDEG)

Aircraft.Alpha_Zero_CM  = 5 * ARCDEG
Aircraft.StaticMargin   = 0.1

#
# Maximum velocity for plotting purposes
#
Aircraft.VmaxPlt = 70*FT/SEC

#
# Estimate for the time the aircraft rotates on the ground during takeoff
#
Aircraft.RotationTime = 0.1 * SEC

###############################################################################
#
# Tail surfaces
#
###############################################################################

#==============================================================================
# Horizontal tail
#
HTail = Aircraft.HTail
#HTail.Airfoil  = 'NACA0012'
#HTail.Airfoil  = 'clarky'
HTail.Airfoil  = 'e423m'
HTail.AR       = 4
HTail.TR       = 0.6
#HTail.S        = 200 * IN**2
HTail.L        = 100 * IN
HTail.VC       = 0.45
HTail.FullWing = True
HTail.DWF      = 2.0 #Main wing Down wash factor (Between 1.0 and 2.0)
HTail.Inverted = True

#
# Elevator properties
#
HTail.Elevator.Fc = 0.3
HTail.Elevator.Fb = 1.0
HTail.Elevator.Ft = 0.0

HTail.Elevator.Servo.Fc  = 0.3
HTail.Elevator.Servo.Fbc = 0.1

#Set the sweep about the elevator hinge
HTail.SweepFc  = 1.0 - HTail.Elevator.Fc

#
# Structural properties
# Spar taken as 1/8 inch width and thickness of the max thickness at the root
#
Basswood = Basswood.copy()
BWRibMat = Balsa.copy()
BWRibMat.Thickness = 3/32 * IN

#HTail.SetWeightCalc(ACRibWing)
#HTail.WingWeight.RibMat                    = BWRibMat
#HTail.WingWeight.RibSpace                  = 3 * IN
HTail.SetWeightCalc(ACSolidWing)
HTail.WingWeight.WingMat                    = PinkFoam.copy()
HTail.WingWeight.WingMat.ForceDensity      *= 0.4

HTail.WingWeight.AddSpar("HMainSpar",0.25*IN,0.5*IN)
HTail.WingWeight.HMainSpar.SparMat = CarbonBar.copy()
HTail.WingWeight.SkinMat                    = Monokote.copy()


#==============================================================================
# Vertical tail
#
VTail = Aircraft.VTail
VTail.Airfoil = 'NACA0012'
VTail.VC      = 0.040
VTail.AR      = 1.95
VTail.TR      = 0.7
VTail.Axis    = (0, 1)
VTail.L       = 100.0 * IN
#VTail.S       = 100 * IN**2
#VTail.b       = 10 * IN

#
# Rudder properties
#
VTail.Rudder.Fc = 0.4
VTail.Rudder.Servo.Fc  = 0.3
VTail.Rudder.Servo.Fbc = 0.1

#Set the sweep about the rudder hinge
VTail.SweepFc = 1.0 - VTail.Rudder.Fc

#
# Structural properties
# Spar taken as 1/8 inch width and thickness of the max thickness at the root
#
#VTail.SetWeightCalc(ACRibWing)
#VTail.WingWeight.RibMat                    = BWRibMat
#VTail.WingWeight.RibSpace                  = 3 * IN
VTail.SetWeightCalc(ACSolidWing)
VTail.WingWeight.WingMat                    = PinkFoam.copy()
VTail.WingWeight.WingMat.ForceDensity      *= 0.4

VTail.WingWeight.AddSpar("VMainSpar",0.25*IN,0.125*IN)
VTail.WingWeight.VMainSpar.SparMat          = CarbonBar.copy()
VTail.WingWeight.SkinMat                    = Monokote.copy()


###############################################################################
#
# Landing Gear
#
###############################################################################
Steel = Steel.copy()
MainGear = Aircraft.MainGear
MainGear.Theta        = 30*ARCDEG
MainGear.GearHeight   = 8   * IN
MainGear.StrutW       = 0.2 * IN
MainGear.StrutH       = 0.1 * IN
MainGear.WheelDiam    = 2.5 * IN
MainGear.X[1]         = 2.5 * IN
MainGear.Strut.Weight = math.pi*(0.125/2*IN)**2*12*IN*Steel.ForceDensity #1/8 inch diameter steel, l=12in
MainGear.Wheel.Weight = 0.1*LBF

NoseGear = Aircraft.NoseGear
NoseGear.StrutW    = 0.1 * IN
NoseGear.StrutH    = 0.1 * IN
NoseGear.WheelDiam = 2.5 * IN
NoseGear.Strut.Weight = math.pi*(0.125/2*IN)**2*8*IN*Steel.ForceDensity #1/8 inch diameter steel, l=8in
NoseGear.Wheel.Weight = 0.1*LBF


#alphas = Aircraft.Wing.AlphaRange()
##CM = Aircraft.CM(alphas, del_e = 0*ARCDEG, Xcg = 0.5*IN, i = 0*ARCDEG)
#CL = HTail.CL(alphas)

#pyl.figure(8)
#pyl.plot(alphas/(ARCDEG), CL)

#HTail.Draw2DAirfoilPolars(fig=1)
#HTail.Draw3DWingPolars(fig=2)
#pyl.show()

if __name__ == '__main__':
    
    TCG = Aircraft.CG()
    ACG = Aircraft.Fuselage.AircraftCG()
    dCG = TCG - ACG
        
    print 'Aircraft Xnp   :', AsUnit( Aircraft.Xnp(), 'in' )
    print 'Aircraft Xcg   :', AsUnit( Aircraft.Xcg(), 'in' )
    print 'Aircraft CM    :', Aircraft.CM(15*ARCDEG, del_e = 10*ARCDEG)
    print 'Aircraft dCM_da:', AsUnit( Aircraft.dCM_da(), '1/rad' )
    print
    print 'Wing Area      :', AsUnit( Aircraft.Wing.S, 'in**2' )
    print 'Wing MAC       :', AsUnit( Aircraft.Wing.MAC(), 'in' )
    print 'Wing dCl_da    :', AsUnit( Aircraft.Wing.dCL_da(), '1/rad' )
    print 'Wing Xac       :', AsUnit( Aircraft.Wing.Xac(), 'in' )
    print
    print 'Horiz Area     :', AsUnit( Aircraft.HTail.S, 'in**2' )
    print 'Horiz Length   :', AsUnit( Aircraft.HTail.L, 'in' )
    print 'Horiz iht      :', AsUnit( Aircraft.HTail.i, 'deg' )
    print 'Horiz dCl_da   :', AsUnit( Aircraft.HTail.dCL_da(), '1/rad' )
    print 'Horiz Design CL:', Aircraft.GetHT_Design_CL()
    print
    print 'Wing  Weight   :', AsUnit( Aircraft.Wing.Weight, 'lbf' )
    print 'Horiz Weight   :', AsUnit( Aircraft.HTail.Weight, 'lbf' )
    print 'Vert  Weight   :', AsUnit( Aircraft.VTail.Weight, 'lbf' )
    print
    print 'Vert Area      :', AsUnit( Aircraft.VTail.S, 'in**2' )
    print 'Vert Span      :', AsUnit( Aircraft.VTail.b, 'in' )
    print
    print 'True CG        :', TCG[0]
    print 'Desired CG     :', ACG[0]
    print 'delta CG       :', dCG[0]
    print 'Empty   Weight :', AsUnit( Aircraft.EmptyWeight, 'lbf' )
    print 'Payload Weight :', AsUnit( Aircraft.PayloadWeight(), 'lbf' )
    print
    print 'Propulsion MOI :', AsUnit( Aircraft.Propulsion.MOI(), 'slug*ft**2' )
    print 'Wing       MOI :', AsUnit( Aircraft.Wing.MOI(), 'slug*ft**2' )
    print 'HTail      MOI :', AsUnit( Aircraft.HTail.MOI(), 'slug*ft**2' )
    print 'VTail      MOI :', AsUnit( Aircraft.VTail.MOI(), 'slug*ft**2' )
    print 'Aircraft   MOI :', AsUnit( Aircraft.MOI(), 'slug*ft**2' )
    print
    print 'Aircraft Groundroll :', AsUnit( Aircraft.Groundroll(), 'ft' )
    print
    print 'HTail Length   : ', Aircraft.HTail.L
    print 'VTail Length   : ', Aircraft.VTail.L
    print
    print 'Aircraft   V_LO :', AsUnit( Aircraft.GetV_LO(), 'ft/s' )
    print 'Wing       V_LO :', AsUnit( Aircraft.Wing.GetV_LO(), 'ft/s' )
    print 'Ground Roll Distance: ',  Aircraft.Groundroll()
    print

    H = max(Aircraft.Wing.Upper(0*IN), Aircraft.VTail.Tip()[2])
    W = Aircraft.Wing.b
    L = Aircraft.HTail.MaxTE()
    print
    print 'Wing Height    : ', Aircraft.Wing.Upper(0*IN)
    print 'Vertical Tail H: ', Aircraft.VTail.Tip()[2]
    print 'Width          : ', W
    print 'Length         : ', L
    print 'Sum of Lengths : ', AsUnit( W + L + H, 'in')


#    Aircraft.PlotTailLoad(fig=7)
#    Aircraft.PlotTrimmedPolars(fig=6)
##    Aircraft.PlotCMPolars(5, (-10*ARCDEG, -5*ARCDEG, 0*ARCDEG, +5*ARCDEG, +10 * ARCDEG), (+0.5 * IN, -0.5 * IN))
#    Aircraft.PlotPolarsSlopes(fig=4)
#    Aircraft.WriteAVLAircraft('AVLAircraft.avl')
#    Aircraft.PlotDragBuildup(fig=3)
    Aircraft.Draw()
    pyl.show()
    
