#!/usr/bin/python
import numpy as np

def mul64x64to128__(a, b):
    hi32, lo32 = np.uint64(32), np.uint64(0xffffffff)
    ahi = a >> hi32
    a &= lo32; alo = a
    bhi = b >> hi32
    b &= lo32; blo = b

    rhi = ahi * bhi
    ahi *= blo; rmid1 = ahi
    bhi *= alo; rmid2 = bhi
    alo *= blo; rlo = alo

    rmidhi = (rmid1 >> hi32) + (rmid2 >> hi32)
    rmid1 &= lo32; rmid2 &= lo32; rmid1 += rmid2; rmidlo = rmid1

    rlohi = (rlo >> hi32) + (rmidlo & lo32)
    rlo &= lo32; rlolo = rlo

    rmidlo >>= hi32; rhi += rmidhi + rmidlo + (rlohi >> hi32)
    rlohi &= lo32; rlolo += rlohi << hi32; rlo = rlolo

    return (rhi, rlo)

def to128(hi, lo):
    hi, lo = hi.astype('object'), lo.astype('object')
    return ((hi << 64) | lo)

def mul64x64to128(a, b):
    hi, lo = mul64x64to128__(a, b)
    return to128(hi, lo)


if __name__ == '__main__':
    import unittest
    import random

    class TestMul(unittest.TestCase):

        MAX_UINT64=(1<<64)-1
        
        def setup(self): pass

        def test_wrong(self):
            a64, b64 = np.uint64(1), np.uint64(self.MAX_UINT64)
            self.assertFalse(mul64x64to128(a64, b64) == 0)

        def __check(self, a, b):
            a64, b64 = np.uint64(a), np.uint64(b)
            self.assertEqual(int(a)*int(b), mul64x64to128(a64, b64))

        def test_int_limits(self):
            self.__check(self.MAX_UINT64, self.MAX_UINT64)
            self.__check(0, 1)
            self.__check(1, 1)

        def test_int_rand(self):
            for _ in xrange(10000):
                self.__check(random.randint(0, self.MAX_UINT64), random.randint(0, self.MAX_UINT64))

        def test_array_rand(self):
            a64 = np.random.randint(0, self.MAX_UINT64, 1000000, dtype=np.uint64)
            b64 = np.random.randint(0, self.MAX_UINT64, len(a64), dtype=np.uint64)
            ai, bi = a64.astype('object'), b64.astype('object')
            self.assertTrue(np.array_equal(ai * bi, mul64x64to128(a64, b64)))

    unittest.main()
