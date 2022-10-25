# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from kindtool.templates import Templates


class TestSimple(unittest.TestCase):

    def test_add_one(self):
        #self.assertEqual(add_one(5), 6)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
