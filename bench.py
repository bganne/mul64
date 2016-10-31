#!/usr/bin/python
import timeit
setup = '''
import numpy as np
from mul64 import mul64x64to128__, mul64x64to128

a64 = np.random.randint(0, (1<<64)-1, 2000000, dtype=np.uint64)
b64 = np.random.randint(0, (1<<64)-1, len(a64), dtype=np.uint64)
ai, bi = a64.astype('object'), b64.astype('object')

assert(np.array_equal(ai * bi, mul64x64to128(a64, b64)))
print '''

print timeit.timeit('mul64x64to128__(a64,b64)', setup=setup+'"u64:",', number=30)
print timeit.timeit('ai*bi', setup=setup+'"obj:",', number=30)
