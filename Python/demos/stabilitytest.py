from klampt import *
from klampt import forceClosure,comEquilibrium,supportPolygon
from klampt.contact import *

#these form a square + a downward facing point
fc_contacts = [ContactPoint([-1,-1,0],[0,0,1],0.5),
				ContactPoint([1,-1,0],[0,0,1],0.5),
				ContactPoint([1,1,0],[0,0,1],0.5),
				ContactPoint([-1,1,0],[0,0,1],0.5),
				ContactPoint([0,0,1],[0,0,-1],0.5)]

#these form a square
stable_contacts = [ContactPoint([-1,-1,0],[0,0,1],0.5),
				ContactPoint([1,-1,0],[0,0,1],0.5),
				ContactPoint([1,1,0],[0,0,1],0.5),
				ContactPoint([-1,1,0],[0,0,1],0.5)]

#these form two points pointing in strange directions
unstable_contacts = [ContactPoint([-1,-1,0],[0,1,0],0.5),
				ContactPoint([1,11,0],[1,0,0],0.5)]

print "Force closure (should be True)",forceClosure([c.tolist() for c in fc_contacts])
print "Force closure (should be False)",forceClosure([c.tolist() for c in stable_contacts])
print "Stable COM (should be list of forces)",comEquilibrium([c.tolist() for c in stable_contacts],[0,0,-1],(0,0,0))
print "Stable COM (should be list of forces)",comEquilibrium([c.tolist() for c in stable_contacts],[0,0,-1],(0,0,10))
print "Stable COM (should be None)",comEquilibrium([c.tolist() for c in stable_contacts],[0,0,-1],(2,0,10))
print "Any stable (should be True)",comEquilibrium([c.tolist() for c in stable_contacts],[0,0,-1],None)
print "Any stable (should be False)",comEquilibrium([c.tolist() for c in unstable_contacts],[0,0,-1],None)
print "Support polygon planes (should be a square)",supportPolygon([c.tolist() for c in stable_contacts])
print "Support polygon planes (should be entire plane)",supportPolygon([c.tolist() for c in fc_contacts])
print "Support polygon planes (should be invalid)",supportPolygon([c.tolist() for c in unstable_contacts])