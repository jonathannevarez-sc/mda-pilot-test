"""The package imports and the test command finds this file.

This is the setup test. Behaviour tests arrive one per acceptance line with
the story that needs them.
"""

import unittest

import dispatch


class PackageTest(unittest.TestCase):
    def test_package_imports(self) -> None:
        self.assertEqual(dispatch.__all__, [])


if __name__ == "__main__":
    unittest.main()
