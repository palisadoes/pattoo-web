#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
if EXEC_DIR.endswith(
        '/pattoo-web/tests/test_pattoo_web') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo-web/tests/test_pattoo_web" directory. Please fix.''')
    sys.exit(2)

from tests.libraries.configuration import UnittestConfig
from pattoo_web import uri


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_chart_link(self):
        """Testing method / function chart_link."""
        # Test
        result = uri.chart_link('0', '1', '2', '3', '4')
        self.assertEqual(
            result,
            '''<a href="/pattoo/web/chart/0?heading=2&target=1\
&secondsago=4">3</a>''')
        result = uri.chart_link('0', '1', '2')
        self.assertEqual(
            result,
            '''<a href="/pattoo/web/chart/0?heading=2&target=1\
&secondsago=86400">Chart Data</a>''')

    def test_integerize_arg(self):
        """Testing method / function integerize_arg."""
        # Test
        test_value = '30'
        result = uri.integerize_arg(test_value)
        self.assertEqual(result, int(test_value))

        # Fail for non numeric strings and booleans
        result = uri.integerize_arg('Test')
        self.assertEqual(result, None)
        result = uri.integerize_arg(None)
        self.assertEqual(result, None)
        result = uri.integerize_arg(False)
        self.assertEqual(result, None)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
