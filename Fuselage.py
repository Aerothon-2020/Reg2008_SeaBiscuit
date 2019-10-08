from __future__ import division # let 5/2 = 2.5 rather than 2
from scalar.units import IN, LBF, SLUG, FT
from scalar.units import AsUnit
from Aerothon.ACBase import g
from Aerothon.ACMaterial import ACMaterial
from Aerothon.ACFuselage import ACFuselage
from Aerothon.DefaultMaterialsLibrary import Steel, AircraftPly, Basswood, Monokote

#
# Materials Set-up
#
Steel    = Steel.copy()
ACPly    = AircraftPly.copy()
Basswood = Basswood.copy()
Monokote = Monokote.copy() 

# Bulkhead plywood
# 1/8 inch thick with 75% material cut out
cutout = 0.75
ACPlyBH = ACMaterial()
ACPlyBH.Thickness = 0.125*IN
ACPlyBH.ForceDensity = ACPly.ForceDensity*(1-cutout)

# Section plywood (truss structure + monokote)
# 1/8 inch thick with 80% material cut out
cutout = 0.8
ACPlySkin = ACMaterial()
ACPlySkin.AreaDensity = ACPly.ForceDensity*(1-cutout)*0.125*IN/g + Monokote.AreaDensity

# Stringer material from basswood (w=0.25 in , t=0.25 in)
w = 0.25*IN ; t = 0.25*IN
BassStringer = ACMaterial()
BassStringer.LinearForceDensity = Basswood.ForceDensity * w * t


Fuselage = ACFuselage()
#
# Create the sections of the fuselage
#
Fuselage.AddSection('Nose'     , 6*IN,  1)
Fuselage.AddSection('PyldBay'  , 11*IN, 1)
Fuselage.AddSection('TailTaper')

#
# Size the engine fire wall
#
Fuselage.Nose.FrontBulk.Width  = 2.7*IN
Fuselage.Nose.FrontBulk.Height = 2.7*IN
Fuselage.Nose.FrontBulk.Material = ACPlyBH
Fuselage.Nose.Align             = -1
Fuselage.Nose.SkinMat = ACPlySkin

#
# Size the payload bay
#
Fuselage.PyldBay.FrontBulk.Width  = 6*IN
Fuselage.PyldBay.FrontBulk.Height = 6*IN
Fuselage.PyldBay.BackBulk.Width   = 6*IN
Fuselage.PyldBay.BackBulk.Height  = 6*IN
Fuselage.PyldBay.FrontBulk.Material = ACPlyBH
Fuselage.PyldBay.BackBulk.Material  = ACPlyBH
Fuselage.PyldBay.SkinMat = ACPlySkin
Fuselage.PyldBay.StringerMat = BassStringer

#
# Change the alignement of the tail taper section
#
Fuselage.TailTaper.BackBulk.Width  = 2.0*IN
Fuselage.TailTaper.BackBulk.Height = 2.0*IN
Fuselage.TailTaper.BackBulk.X      = [40*IN,0*IN,0*IN]  #Just for viewing, will actually be placed by the HT in the Aircraft file
Fuselage.TailTaper.Align       = -1
Fuselage.TailTaper.SkinMat     = ACPlySkin
Fuselage.TailTaper.StringerMat = BassStringer

#
# Add some components to the nose section
#
Fuselage.Nose.AddComponent    (     "Battery"   , 0.114*LBF, (0.25*IN,1.5*IN,1*IN)    , "Right"  , (0.2 , 0.5, 0.5) )
Fuselage.Nose.AddComponent    (     "FuelTank"  , 0.1*LBF , (2.5*IN,2*IN,1.25*IN)    , "Back"   , (0.75, 0.5, 0.7) )
Fuselage.Nose.AddComponent    ("NoseWheelServo" , 0.04*LBF , (.5*IN,1*IN,1*IN)        , "Bottom" , (0.6 , 0.2, 0.0) )
Fuselage.Nose.AddComponent    ("Receiver"       , 0.02*LBF , (.5*IN,1*IN,1*IN)        , "Left" , (0.6 , 0.2, 0.5) )

#
# Define which section contains the CG of the aircraft
#
Fuselage.XcgSection = Fuselage.PyldBay
Fuselage.XcgSecFrac = 0.5

#
# Determine which bulkhead should be set by the horizontal tail
#
Fuselage.TailBulk = Fuselage.TailTaper.BackBulk

if __name__ == '__main__':
    import pylab as pyl
    
    print 'Nose      Weight :', Fuselage.Nose.Weight
    print 'PyldBay   Weight :', Fuselage.PyldBay.Weight
    print 'TailTaper Weight :', Fuselage.TailTaper.Weight
    
    print 'Fuselage Weight    :', Fuselage.Weight
    print 'Fuselage MOI       :', AsUnit( Fuselage.MOI(), 'slug*ft**2' )
    print 'Fuselage CG        :', AsUnit( Fuselage.CG(), 'in' )
    print 'Fuselage Desired CG:', AsUnit( Fuselage.AircraftCG(), 'in' )
    
    
    Fuselage.Draw()
    pyl.show()