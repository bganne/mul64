#!/usr/bin/python
import numpy as np

def hi(v):
    return (v >> np.uint64(32))

def lo(v):
    return (v & np.uint64(0xffffffff))

def mul64x64_128(a, b):
    ahi = hi(a)
    alo = lo(a)
    bhi = hi(b)
    blo = lo(b)

    rhi = ahi * bhi
    rmid1 = ahi * blo
    rmid2 = bhi * alo
    rlo = alo * blo

    rmidlo = lo(rmid1) + lo(rmid2)
    rmidhi = hi(rmid1) + hi(rmid2)

    rlohi = hi(rlo) + lo(rmidlo)
    rlolo = lo(rlo)

    rhi = rhi + rmidhi + hi(rmidlo) + hi(rlohi)
    rlo = (lo(rlohi) << np.uint64(32)) + rlolo

    return (rhi, rlo)

if __name__ == '__main__':
    import unittest
    import random

    class TestMul(unittest.TestCase):

        MAX_UINT64=(1<<64)-1
        
        def setup(self): pass

        def __check(self, a, b):
            a64, b64 = np.uint64(a), np.uint64(b)
            rhi, rlo = mul64x64_128(a64, b64)
            self.assertEqual(int(a)*int(b), (int(rhi) << 64) + int(rlo))

        def test_short(self):
            self.__check(self.MAX_UINT64, self.MAX_UINT64)
            self.__check(0, 1)
            self.__check(1, 1)

        def test_long(self):
            for _ in xrange(1000000):
                self.__check(random.randint(0, self.MAX_UINT64), random.randint(0, self.MAX_UINT64))

    unittest.main()
