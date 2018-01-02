import random
import hexu

class HexWorld:

    def __init__(self, map_radius):
        self.map_radius = map_radius
        self.rules_environment = { 3, 5 }
        self.rules_fertility = { 2 }
        self.cells = set()
        self.cycles = 0
        
        self.neighbors = {}
        # Compute every cell neighbors in advance (minus the periphery)
        for c in hexu.hexagonal_map_gen(map_radius):
            sn = set()
            for n in hexu.cell_neighbors(c):
                if hexu.cells_distance((0,0), n) <= map_radius:
                    sn.add(n)
            self.neighbors[c] = sn

    def __len__(self):
        return len(self.neighbors)
        
    def set_rules(self, environement, fertility):
        self.rules_environment = environement
        self.rules_fertility = fertility
        
    def clear(self):
        self.cells.clear()
        self.cycles = 0
        
    def random(self, density, initial_radius):
        self.clear()
        if initial_radius < self.map_radius:
            potential_cells = [c for c in hexu.hexagonal_map_gen(initial_radius) ]
            self.cells = set( random.sample( potential_cells,
                                k = int( density * len(potential_cells) ) ) )
        else:
            raise ValueError('initial_radius is larger than map_radius')
        
    def evolve(self):
        next_generation = set()
        for c in hexu.hexagonal_map_gen(self.map_radius-1):
            alive_neighbors = len( self.neighbors[c].intersection(self.cells) )
            if c in self.cells:
                if alive_neighbors in self.rules_environment:
                    next_generation.add(c)
            else:
                if alive_neighbors in self.rules_fertility:
                    next_generation.add(c)
        self.cells = next_generation
        self.cycles += 1
