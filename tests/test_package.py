"""The package imports and the test command finds this file."""

import unittest

import dispatch


class PackageTest(unittest.TestCase):
    def test_package_exports_the_drive_order_names(self) -> None:
        self.assertIn("DriveOrder", dispatch.__all__)
        self.assertIn("accept_revision", dispatch.__all__)
        self.assertIn("driver_projection", dispatch.__all__)


if __name__ == "__main__":
    unittest.main()
