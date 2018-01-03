import random
import hexu

class HexWorld:
    """
        Hexagonal Game of Life.
        
        Allow to create random world and evolve them according to a set of rules.
        
        The data structures used are:
          - tuple(q, r) : Axial Coordinates (refered simply as (q,r) later)
          - cells = set( (q,r), ... ) : current cells alive
          - neighbors = { key = (q,r) : value = (
                set( (q,r), ... ) = direct neighbors 
                set( (q,r), ... ) = second order neighbors
                ) }
          - colors = { key=(q,r) : value = (hue, saturation) }
          - potential_population = set( (q,r), ... ) : cells to consider at
            next cycle
    """
    def __init__(self, map_radius):
        self.map_radius = map_radius
        self.rules_environment = { 2, 3 }
        self.rules_fertility = { 2 }
        self.cells = set()
        self.colors = {}
        self.cycles = 0
        self.use_extended_neighbors = True
        self.extended_neighbors_factor = 3
        self.potential_population = set()
        
        # Dictionary indexed by cell coordinate and pointing to a tuple
        # of two sets (direct_neighbors, extended_neighbors)
        self.neighbors = {}
        
        # Compute every cell neighbors in advance (minus the periphery)
        for c in hexu.hexagonal_map_gen(map_radius):
            direct_neighbors = set()
            extended_neighbors = set()
            for n in hexu.cell_neighbors(c):
                if hexu.cells_distance((0,0), n) <= map_radius:
                    direct_neighbors.add(n)
            for n in hexu.cell_ring(c, 2):
                if hexu.cells_distance((0,0), n) <= map_radius:
                    extended_neighbors.add(n)
            self.neighbors[c] = (direct_neighbors, extended_neighbors)

        # Define a non linear color intensity
        #self.intensities = [i for i in range(80, 35, -5)]
        #self.intensities.insert(0, 100)
        
    def __len__(self):
        return len(self.neighbors)

    def set_rules(self, environement, fertility):
        self.rules_environment = environement
        self.rules_fertility = fertility
        
    def clear(self):
        self.cells.clear()
        self.potential_population.clear()
        self.cycles = 0
        
    def random(self, density, initial_radius):
        self.clear()
        if initial_radius < self.map_radius:
            potential_cells = [c for c in hexu.hexagonal_map_gen(initial_radius) ]
            self.cells = set( random.sample( potential_cells,
                                k = int( density * len(potential_cells) ) ) )
            for c in self.cells:
                self.colors[c] = random.choice( [(60,100), (180,100), (300,100)] )
                self.potential_population.update(self.neighbors[c][0] | self.neighbors[c][1])
        else:
            raise ValueError('initial_radius is larger than map_radius')
        
    def evolve(self):
        next_generation = set()
        next_candidates = set()
        next_colors = {}
        # for c in hexu.hexagonal_map_gen(self.map_radius-1):
        for c in self.potential_population:
            alive_neighbors = len( self.neighbors[c][0].intersection(self.cells) )
            if self.use_extended_neighbors:
                alive_neighbors += len( 
                    self.neighbors[c][0].intersection(self.cells) ) // self.extended_neighbors_factor
            if c in self.cells:
                if alive_neighbors in self.rules_environment:
                    next_generation.add(c)
                    intensity = self.colors[c][1]
                    if intensity == 100:
                        intensity = 70
                    elif intensity > 25:
                        intensity -= 5
                    next_colors[c] = (self.colors[c][0], intensity)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
            else:
                if alive_neighbors in self.rules_fertility:
                    next_generation.add(c)
                    hue = 0
                    count = 0
                    for n in self.neighbors[c][0]:
                        if n in self.cells:
                            hue += self.colors[n][0]
                            count += 1
                    hue = ( hue // count ) % 360
                    next_colors[c] = (hue, 100)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
        self.cells = next_generation
        self.colors = next_colors
        self.potential_population = next_candidates
        self.cycles += 1
