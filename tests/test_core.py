import numpy as np
import unittest

from py_ebay import is_nan


class TestCore(unittest.TestCase):

    def test_is_nan(self):
        assert(is_nan(np.NAN))
        assert(not is_nan(1))
        assert(not is_nan('1'))
        assert(not is_nan('NAN'))
