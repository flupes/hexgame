'''
Routines to manage an hexagonal grid.

Most coordinates and transformation concepts are coming from the amazing
article by Amit Patel:
https://www.redblobgames.com/grids/hexagons/

The main coordinate system used is the "Axial Coordinate System", which
is simply defined by a tuple of two elements. This basic representation 
optimize efficiency (hash, etc.) and provide the maximum speed (namedtuple
is amazingly slow to allocate because of string transforms, list or numpy
arrays have also been tested by were much less efficient than the basic tuple).

'''

import math

SQRT3 = math.sqrt(3)

def cell_neighbors(cell):
    """ Returns direct neighbors of an hexagonal cell."""
    return { 
            (cell[0]+1, cell[1]),
            (cell[0]+1, cell[1]-1),
            (cell[0], cell[1]-1),
            (cell[0]-1, cell[1]),
            (cell[0]-1, cell[1]+1),
            (cell[0], cell[1]+1)
            }

def cell_cube_coord(c):
    """ Returns a tuple with the cube coordinates corresponding to the 
        given axial coordinates.
    """
    x = c[0]
    z = c[1]
    return (x, -x-z, z)

def cells_distance(c1, c2):
    """ Computes the distance between to cells (axial coordinates)."""
    ccc1 = cell_cube_coord(c1)
    ccc2 = cell_cube_coord(c2)
    return max(abs(ccc1[0] - ccc2[0]), abs(ccc1[1] - ccc2[1]), abs(ccc1[2] - ccc2[2]))

def cell_center(cell):
    """ Returns the center of a cell from its axial coordinates.
        This is the center for a unit cell, it needs to be multiplied by
        the actual cell size.
    """
    return [ SQRT3 * (cell[0] + cell[1]/2.0), 3.0/2.0 * cell[1] ]

def hexagonal_map_gen(map_radius):
    """ Generator of an hexagonal map.
        This generator returns the axial coordinates of each cell
        compusing an hexagonal map of the given radius.
    """
    for q in range(-map_radius, map_radius+1):
        r1 = max(-map_radius, -q - map_radius)
        r2 = min(map_radius, -q + map_radius)
        for r in range(r1, r2+1):
            yield (q, r)

def max_map_radius(hex_radius, height):
    """ Returns the  maximum map radius fitting in 'height' pixels
        with cells of radius 'hex_radius'.
    """
    return int( math.floor( (height - 2 * hex_radius) / (3 * hex_radius) ) )
    
def map_px_size(map_radius, hex_radius):
    """ Returns the size in pixels of an hexagonal map with a given radius
        and cell size.
    """
    return ( 2 * int( math.ceil( (2 * map_radius + 1) * SQRT3 * hex_radius / 2) ),
                                hex_radius * (2 + 3 * map_radius) )
