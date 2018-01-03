import random
import hexu

class HexWorld:

    def __init__(self, map_radius):
        self.map_radius = map_radius
        self.rules_environment = { 2, 3 }
        self.rules_fertility = { 2 }
        self.cells = set()
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
                self.potential_population.update(self.neighbors[c][0] | self.neighbors[c][1])
        else:
            raise ValueError('initial_radius is larger than map_radius')
        
    def evolve(self):
        next_generation = set()
        next_candidates = set()
        # for c in hexu.hexagonal_map_gen(self.map_radius-1):
        for c in self.potential_population:
            alive_neighbors = len( self.neighbors[c][0].intersection(self.cells) )
            if self.use_extended_neighbors:
                alive_neighbors += len( 
                    self.neighbors[c][0].intersection(self.cells) ) // self.extended_neighbors_factor
            if c in self.cells:
                if alive_neighbors in self.rules_environment:
                    next_generation.add(c)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
            else:
                if alive_neighbors in self.rules_fertility:
                    next_generation.add(c)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
        self.cells = next_generation
        self.potential_population = next_candidates
        self.cycles += 1
