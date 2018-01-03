import sys
import timeit
import hexworld

def main():
    if len(sys.argv[1:]) < 2:
        print("Usage: test_evolve map_radus number_of_cycles")
        sys.exit(1)

    radius = int(sys.argv[1])
    loops = int(sys.argv[2])

    world = hexworld.HexWorld(radius)
    density = 0.75
    world.rules_environment = {2, 3}
    world.rules_fertility = {2}
    world.random(density, radius // 2)
    
    start = timeit.default_timer()
    for i in range(loops):
        world.evolve()
    stop = timeit.default_timer()
    
    print('Elapsed for %d cycles: %r' % (loops, (stop-start)))


if __name__ == "__main__":
    main()
