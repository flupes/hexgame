/*
  profile with:

  gcc -Wall -pg -o vector_elmts_sum vector_elmts_sum.c
  ./vector_elmts_sum 1000000 1000 1000000
  gprof --brief vector_elmts_sum
 */

#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

uint8_t *vec_8;
uint32_t *vec_32;
size_t *indices;

void init(size_t vec_sz, size_t i_sz) {
  vec_8 = malloc(vec_sz * sizeof(uint8_t));
  assert(vec_8 != NULL);

  vec_32 = malloc(vec_sz * sizeof(uint32_t));
  assert(vec_32 != NULL);

  for (size_t i = 0; i < vec_sz; i++) {
    vec_8[i] = (uint8_t)i;
    vec_32[i] = (uint32_t)i;
  }

  indices = malloc(i_sz * sizeof(size_t));
  assert(indices != NULL);
}

void clean() {
  free(vec_32);
  free(vec_8);
  free(indices);
}

void shuffle_indices(size_t vec_sz, size_t i_sz) {
  for (size_t i = 0; i < i_sz; i++) {
    indices[i] = (size_t)(rand() * vec_sz / RAND_MAX);
  }
}

int compute_sum8(size_t i_sz) {
  int sum = 0;
  for (size_t i = 0; i < i_sz; i++) {
    sum += vec_8[indices[i]];
  }
  return sum;
}

int compute_sum32(size_t i_sz) {
  int sum = 0;
  for (size_t i = 0; i < i_sz; i++) {
    sum += vec_32[indices[i]];
  }
  return sum;
}

void print_debug(size_t vec_sz, size_t i_sz) {
  printf("vec_8 = [");
  for (size_t i = 0; i < vec_sz; i++) {
    printf("%d ", vec_8[i]);
  }
  printf("]\n");
  printf("vec_32 = [");
  for (size_t i = 0; i < vec_sz; i++) {
    printf("%d ", vec_32[i]);
  }
  printf("]\n");
  printf("indices = [");
  for (size_t i = 0; i < i_sz; i++) {
    printf("%ld ", indices[i]);
  }
  printf("]\n");
}

int main(int argc, char *argv[]) {
  if (argc < 4) {
    printf("Usage: vector_elmts_sum vector_size indices_sz loops\n");
    exit(1);
  }
  size_t length = atoi(argv[1]);
  size_t isize = atoi(argv[2]);
  int loops = atoi(argv[3]);

  init(length, isize);

  int sum8 = 0;
  int sum32 = 0;

  for (int i = 0; i < loops; i++) {
    shuffle_indices(length, isize);
    sum8 += compute_sum8(isize);
    sum32 += compute_sum32(isize);
  }

  if (length < 50 && loops == 1) {
    print_debug(length, isize);
  }

  printf("sum8 = %d\n", sum8);
  printf("sum32 = %d\n", sum32);

  clean();
}
