'''
Cube Coordinates - Unused...
'''

import numpy

class CubeCoord:
    """Elegant class to maintain cube coordinates.
        Unfortunately, it is impossible to make such a class as 
        efficient than a basic tuple because new objects creation is slow.
    """
    def __init__(self, x, y, z):
        """Initialization from 3 cube coordinates."""
        self.cube = numpy.array([x, y, z], dtype=numpy.int_)

    def __repr__(self):
        return 'CubeCoord(x=%d, y=%d, z=%d)' % (self.cube[0], self.cube[1], self.cube[2])

    @classmethod
    def from_axial_coord(cls, q, r):
        """Create cube coordinates from an axial coordinate q and r."""
        if q.is_integer() and r.is_integer():
            x = q
            y = -q-r
            z = r
            return cls(x, y, z)
        else:
            raise TypeError('q and r need to be integers')

    @classmethod
    def from_axial_tuple(cls, acoord):
        """Create cube coordinates from an axial coordinate (tuple)."""
        return cls(acoord[0], -acoord[0]-acoord[1], acoord[1])

    def distance_from(self, other):
        """Returns distance from this cube coord to another."""
        return numpy.max( numpy.abs( self.cube - other.cube ) )
