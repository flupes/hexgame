import math
import pygame
import collections
import hexu
import hexworld

# Define the radius of a cell
hex_radius = 10

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
YELLOW = ( 255, 255, 0)

class HexMap(hexworld.HexWorld):
    
    def __init__(self, map_radius, hex_radius, screen_size):
        super(HexMap, self).__init__(map_radius)
        self.map_radius = map_radius
        self.hex_radius = hex_radius
        self.screen_size = screen_size
        self.screen_center = tuple(d // 2 for d in screen_size)
        self.grid_size = hexu.map_px_size(map_radius, hex_radius)
        self.grid_offset = ( 0.5 * ( screen_size[0] - self.grid_size[0] ),
                0.5 * ( screen_size[1] - self.grid_size[1] ) )
        
        self.coords_map = self._build_grid_coordinates_(self.screen_center)
        self.grid_overlay = self._draw_base_grid_(self.coords_map)        
        
    def _build_grid_coordinates_(self, offset):
        coords = {}
        for h in hexu.hexagonal_map_gen(self.map_radius):
            center = hexu.cell_center(h)
            corners = []
            for i in range(0, 6):
                a = math.radians(60*i+30)
                x = round( self.hex_radius * (center[0] + math.cos(a)) + offset[0] )
                y = round( self.hex_radius * (center[1] + math.sin(a)) + offset[1] )
                corners.append( (int(x), int(y)) )
            coords[h] = corners
        return coords

    def _draw_base_grid_(self, coords):
        grid = pygame.Surface(self.grid_size, depth=32)
        grid.fill(WHITE)
        grid.set_colorkey(WHITE)
        for cell, points in coords.items():
            # Corner points are pre-computed in screen build_grid_coordinates
            # for optimal speed when drawing individual cells
            # Since the grid overlay is only a subset of the screen, it is
            # necessary to remove this offset
            local_points = []
            for p in points:
                local_points.append( tuple((p[0]-self.grid_offset[0],
                                            p[1]-self.grid_offset[1]) ) )
            pygame.draw.lines(grid, BLUE, True, local_points)
        return grid

    def overlay_grid(self, screen):
        screen.blit(self.grid_overlay, self.grid_offset)


    def draw_cells(self, screen):
        for c in self.cells:
            points = self.coords_map[c]
            pygame.draw.polygon(screen, YELLOW, points)

# Initialize Pygame
pygame.init()

# Get highest resolution
modes = pygame.display.list_modes()
modes.sort()
screen_size = modes[-1]
#screen_size = (1440, 900)
#screen_size = (1200, 800)

map_radius = hexu.max_map_radius(hex_radius, screen_size[1]-8)

hmap = HexMap(map_radius, hex_radius, screen_size)
                
# Create the drawing surface
screen = pygame.display.set_mode(screen_size, 
            pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
# screen = pygame.display.set_mode(screen_size, 
#             pygame.DOUBLEBUF|pygame.HWSURFACE)

# Clock to manage framerate
clock = pygame.time.Clock()

# Loop until the user clicks the close button.
done = False
            
print('Map Radius = %d' % hmap.map_radius)
print('Number of Cells = %d' % len(hmap))

# Set new rules

# Converge to stability very quickly
#hmap.set_rules({2, 3}, {4, 5})
#hmap.set_rules({2, 3}, {3, 4})

# Stabilize to oscillators
#hmap.set_rules({3, 4, 5}, {3, 4})
#hmap.set_rules({3, 4, 5}, {3})

# Seeds the world
hmap.random(0.5, int(0.75*hmap.map_radius))

counter = 0
skip = 2
randradius = collections.deque([0.5, 0.75, 0.25])

active = False
one_cycle = False

font_size = int( screen_size[1] / 36 )
font = pygame.font.Font(None, font_size)

legend = []
legend.append( font.render("quit: ESC", 1, GREEN) )
legend.append( font.render("clear map: c", 1, GREEN) )
legend.append( font.render("random radius: a", 1, GREEN) )
legend.append( font.render("random: e / r / t", 1, GREEN) )
legend.append( font.render("speed: s / d / f", 1, GREEN) )
legend.append( font.render("run/pause: SPACEBAR", 1, GREEN) )
legend.append( font.render("step one cycle (next): n", 1, GREEN) )
legend.append( font.render("toggle use extended neighbors: x", 1, GREEN) )
legend.append( font.render("environment rule: {1,2,3,4,5,6}", 1, GREEN) )
legend.append( font.render("fertility rule: SHIFT+{1,2,3,4,5,6}", 1, GREEN) )

def toggle_rule(rule, key):
    if key in rule:
        rule.discard(key)
    else:
        rule.add(key)

# Main event loop
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            elif event.key == pygame.K_SPACE:
                active = not active
            elif event.key == pygame.K_n:
                if not active:
                    one_cycle = True
            elif event.key == pygame.K_s:
                skip = 5
            elif event.key == pygame.K_d:
                skip = 2
            elif event.key == pygame.K_f:
                skip = 1
            elif event.key == pygame.K_c:
                hmap.clear()
            elif event.key == pygame.K_a:
                randradius.rotate()
            elif event.key == pygame.K_e:
                hmap.random(0.2, int(randradius[0]*hmap.map_radius))
            elif event.key == pygame.K_r:
                hmap.random(0.5, int(randradius[0]*hmap.map_radius))
            elif event.key == pygame.K_t:
                hmap.random(0.8, int(randradius[0]*hmap.map_radius))
            elif event.key == pygame.K_x:
                hmap.use_extended_neighbors = not hmap.use_extended_neighbors
            elif (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                if event.key == pygame.K_1:
                    toggle_rule(hmap.rules_fertility, 1)
                elif event.key == pygame.K_2:
                    toggle_rule(hmap.rules_fertility, 2)
                elif event.key == pygame.K_3:
                    toggle_rule(hmap.rules_fertility, 3)
                elif event.key == pygame.K_4 :
                    toggle_rule(hmap.rules_fertility, 4)
                elif event.key == pygame.K_5:
                    toggle_rule(hmap.rules_fertility, 5)
                elif event.key == pygame.K_6:
                    toggle_rule(hmap.rules_fertility, 6)
                elif event.key == pygame.K_7:
                    toggle_rule(hmap.rules_fertility, 7)
                elif event.key == pygame.K_8:
                    toggle_rule(hmap.rules_fertility, 8 )
                elif event.key == pygame.K_9:
                    toggle_rule(hmap.rules_fertility, 9 )                    
            elif event.key == pygame.K_1:
                toggle_rule(hmap.rules_environment, 1)
            elif event.key == pygame.K_2:
                toggle_rule(hmap.rules_environment, 2)
            elif event.key == pygame.K_3:
                toggle_rule(hmap.rules_environment, 3)
            elif event.key == pygame.K_4:
                toggle_rule(hmap.rules_environment, 4)
            elif event.key == pygame.K_5:
                toggle_rule(hmap.rules_environment, 5)
            elif event.key == pygame.K_6:
                toggle_rule(hmap.rules_environment, 6)
            elif event.key == pygame.K_7:
                toggle_rule(hmap.rules_environment, 7)
            elif event.key == pygame.K_8:
                toggle_rule(hmap.rules_environment, 8)
            elif event.key == pygame.K_9:
                toggle_rule(hmap.rules_environment, 9)

    # Clear the screen
    screen.fill(BLACK)
    
    # Draw living cells
    hmap.draw_cells(screen)
    
    # Apply the stored grid
    hmap.overlay_grid(screen)
    
    fps = clock.get_fps()
    text = font.render("fps: {0:0.1f}".format(fps), 1, GREEN)
    screen.blit(text, (screen_size[0]-160, 20))
    
    info = []
    info.append( font.render("map radius = {0:d}".format(hmap.map_radius), 1, GREEN) )
    info.append( font.render("number of cells = {0:d}".format(len(hmap)), 1, GREEN) )
    info.append( font.render("number of cycles = {0:d}".format(hmap.cycles), 1, GREEN) )
    info.append( font.render("use extended neighbors = {0}".format(hmap.use_extended_neighbors), 1, GREEN) )
    info.append( font.render("environment rule = {0:s}".format(str(hmap.rules_environment)), 1, GREEN) )
    info.append( font.render("fertility rule = {0:s}".format(str(hmap.rules_fertility)), 1, GREEN) )
    if not active:
        speed = 'paused'
    else:
        speed = "speed = {0:d}%".format( int( 1.0/skip*100.0 ) )
    info.append( font.render(speed, 1, GREEN) )
    
    y = 20
    for i in info:
        screen.blit(i, (20, y))
        y += font_size
        
    y = screen_size[1]-60
    for t in legend[::-1]:
        screen.blit(t, (20, y))
        y -= font_size

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    # Evolve
    if active:
        if (counter % skip) == 0:
            hmap.evolve()
        counter += 1
    else:
        if one_cycle:
            hmap.evolve()
            one_cycle = False
            
    # Limit to 60 frames per second
    clock.tick(10)

# Exit
pygame.quit()
print('Done.')
