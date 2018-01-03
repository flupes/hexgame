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
                self.colors[c] = random.choice( [(60,100), (60,100), (60,100), (60,100), (180,100), (300,100)] )
                self.potential_population.add(c)
                self.potential_population.update(self.neighbors[c][0] | self.neighbors[c][1])
        else:
            raise ValueError('initial_radius is larger than map_radius')
    
    def cluster(self, number, seed_radius, density):
        self.clear()
        radius_variation = seed_radius // 2
        max_radius = self.map_radius - seed_radius - radius_variation
        center_choices = [c for c in hexu.hexagonal_map_gen(max_radius)]
        if  radius_variation < seed_radius and seed_radius < max_radius:
            for i in range(0, number):
                color = random.choice([(60,100), (180, 100), (300,100)])                
                radius = seed_radius + random.randint(-radius_variation, radius_variation)
                center = random.choice(center_choices)
                potential_cells = [hexu.cells_add(center, c) 
                                    for c in hexu.hexagonal_map_gen(radius) ]
                selected_cells = set( random.sample( potential_cells,
                                    k = int( density * len(potential_cells) ) ) )
                self.cells.update(selected_cells)
                for c in selected_cells:
                    self.colors[c] = color
            for c in self.cells:
                self.potential_population.add(c)
                self.potential_population.update(self.neighbors[c][0] | self.neighbors[c][1])
        else:
            raise ValueError('invalid seed radius')
    


    def _update_color_(self, cell, colormap):
        intensity = self.colors[cell][1]
        if intensity == 100:
            intensity = 70
        elif intensity > 25:
            intensity -= 5
        colormap[cell] = (self.colors[cell][0], intensity)
        
    def _select_color_(self, cell, colormap):
        hue = 0
        count = 0
        for n in self.neighbors[cell][0]:
            # only use the two first parents
            if count == 2:
                break
            if n in self.cells:
                hue += self.colors[n][0]
                count += 1
        hue = ( hue // count ) % 360
        colormap[cell] = (hue, 100)

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
                    self._update_color_(c, next_colors)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
            else:
                if alive_neighbors in self.rules_fertility:
                    next_generation.add(c)
                    self._select_color_(c, next_colors)
                    next_candidates.add(c)
                    next_candidates.update(self.neighbors[c][0] | self.neighbors[c][1])
        self.cells = next_generation
        self.colors = next_colors
        self.potential_population = next_candidates
        self.cycles += 1
