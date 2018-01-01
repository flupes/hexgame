"""
profile with:
  
  python3 -m cProfile -s cumtime vector_elmts_sum.py 1000000 1000 1000000 > stats.txt &&  head -n 20 stats.txt
"""

import sys
import math
import random
import numpy

def initialize(vec_sz, i_sz):
    vec_32 = numpy.arange(vec_sz, dtype=numpy.int32)
    vec_8 = numpy.arange(vec_sz, dtype=numpy.int8)
    return vec_32, vec_8
    
def shuffle_indices(vec_sz, i_sz):
    return numpy.random.randint(0, vec_sz, i_sz)

# With python, a single method would compute both the sum for the
# int32 and int8 arrays, however, we would not get the results separate ;-)
def compute_sum_32(vector, indices):
    return numpy.sum( vector[indices] )

# Redefinition of the above method, just for profiling!
def compute_sum_8(vector, indices):
    return numpy.sum( vector[indices] )

def main():
    if len(sys.argv[1:]) < 3:
        print("Usage: vector_elmts_sum.py vector_size indices_size loops")
        sys.exit(1)
    
    length = int(sys.argv[1])
    isize = int(sys.argv[2])
    loops = int(sys.argv[3])
    
    vec_32, vec_8 = initialize(length, isize)
    sum_8 = 0
    sum_32 = 0

    for i in range(0,loops):
        indices = shuffle_indices(length, isize)
        sum8 = compute_sum_8(vec_8, indices)
        sum32 = compute_sum_32(vec_32, indices)
    
    if ( loops == 1 and length < 50 ):
        print(vec_8)
        print(vec_32)
        print(indices)
        
    print("sum8 = %r" % sum8)
    print("sum32 = %r" % sum32)
    
if __name__ == "__main__":
    main()
