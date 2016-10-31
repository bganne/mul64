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

        def test_wrong(self):
            a, b = np.uint64(1), np.uint64(self.MAX_UINT64)
            self.assertFalse(mul64x64_128(a, b) == 0)

        def __check(self, a, b):
            a64, b64 = np.uint64(a), np.uint64(b)
            rhi, rlo = mul64x64_128(a64, b64)
            self.assertEqual(int(a)*int(b), (int(rhi) << 64) + int(rlo))

        def test_int_limits(self):
            self.__check(self.MAX_UINT64, self.MAX_UINT64)
            self.__check(0, 1)
            self.__check(1, 1)

        def test_int_rand(self):
            for _ in xrange(10000):
                self.__check(random.randint(0, self.MAX_UINT64), random.randint(0, self.MAX_UINT64))

        def test_array_rand(self):
            a = np.random.randint(0, self.MAX_UINT64, 1000000, dtype=np.uint64)
            b = np.random.randint(0, self.MAX_UINT64, len(a), dtype=np.uint64)
            hi, lo = mul64x64_128(a, b)
            ai, bi = a.astype('object'), b.astype('object')
            hi, lo = hi.astype('object'), lo.astype('object')
            self.assertTrue(np.array_equal(ai * bi, ((hi << 64) | lo)))

    unittest.main()
