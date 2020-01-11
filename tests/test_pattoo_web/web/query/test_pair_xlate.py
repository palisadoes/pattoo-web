#!/usr/bin/env python3
"""Test pattoo configuration."""

import os
import unittest
import sys
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))

if EXEC_DIR.endswith(
        '/pattoo-web/tests/test_pattoo_web/web/query') is True:
    # We need to prepend the path in case PattooShared has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''\
This script is not installed in the "pattoo-web/tests/test_pattoo_web\
/web/query" directory. Please fix.''')
    sys.exit(2)

from tests.libraries.configuration import UnittestConfig
from pattoo_web.web.query import pair_xlate
from pattoo_shared import data

_LANGUAGE = data.hashstring(str(random()))

# Create a common dataset for testing
PAIRS = {'data': {'allPairXlateGroup': {'edges': [
    {'node': {'id': 'UGFpclhsYXRlR3JvdXA6MQ==',
              'idxPairXlateGroup': '1',
              'pairXlatePairXlateGroup': {'edges': []}}},
    {'node': {'id': 'UGFpclhsYXRlR3JvdXA6Mg==',
              'idxPairXlateGroup': '2',
              'pairXlatePairXlateGroup': {'edges': [
                  {'node': {
                      'description': (
                          'Interface Broadcast Packets (HC inbound)'),
                      'key': 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.9',
                      'language': {'code': 'en'}}},
                  {'node': {
                      'description': (
                          'Interface Multicast Packets (HC inbound)'),
                      'key': 'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.8',
                      'language': {'code': 'en'}}}]}}},
    {'node': {'id': 'UGFpclhsYXRlR3JvdXA6NA==',
              'idxPairXlateGroup': '4',
              'pairXlatePairXlateGroup': {'edges': [
                  {'node': {
                      'description': 'Supply Air Temperature (F)',
                      'key': 'pattoo_agent_modbustcpd_input_register_30486',
                      'language': {'code': 'en'}}},
                  {'node': {
                      'description': 'Return Air Temperature (F)',
                      'key': 'pattoo_agent_modbustcpd_input_register_30488',
                      'language': {'code': 'en'}}}]}}}]}}}

PAIR = {'data': {'pairXlateGroup': {
    'id': 'UGFpclhsYXRlR3JvdXA6NQ==',
    'idxPairXlateGroup': '5',
    'pairXlatePairXlateGroup': {'edges': [
        {'node': {'description': 'Output KVA (Main Panel)',
                  'key': 'pattoo_agent_bacnetipd_analog_value_point_27',
                  'language': {'code': 'en'}}},
        {'node': {'description': 'Percentage Load (Main Panel)',
                  'key': 'pattoo_agent_bacnetipd_analog_value_point_34',
                  'language': {'code': 'en'}}}]}}}}

PAIR2 = {'data': {'pairXlateGroup': {
    'id': 'UGFpclhsYXRlR3JvdXA6NQ==',
    'idxPairXlateGroup': '5',
    'pairXlatePairXlateGroup': {'edges': [
        {'node': {'description': 'Output KVA (Main Panel)',
                  'key': 'pattoo_agent_bacnetipd_analog_value_point_19',
                  'language': {'code': 'en'}}},
        {'node': {'description': 'Percentage Load (Main Panel)',
                  'key': 'pattoo_agent_bacnetipd_analog_value_point_78',
                  'language': {'code': _LANGUAGE}}}]}}}}


class TestPairXlates(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_agents(self):
        """Testing method / function agents."""
        _ = pair_xlate.PairXlates(PAIRS)
        result = _.datapoints()

        # We should get two DataPoint objects
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertIsInstance(item, pair_xlate.PairXlate)


class TestPairXlate(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup test objects
    _ = pair_xlate.PairXlates(PAIRS)
    tester = _.datapoints()
    other_tester = pair_xlate.PairXlate(PAIR)
    other_tester2 = pair_xlate.PairXlate(PAIR2)

    def test___init__(self):
        """Testing method / function __init__."""
        pass

    def test_id(self):
        """Testing method / function id."""
        # Test
        ids = [
            'UGFpclhsYXRlR3JvdXA6MQ==',
            'UGFpclhsYXRlR3JvdXA6Mg==',
            'UGFpclhsYXRlR3JvdXA6NA==']
        for index, item in enumerate(self.tester):
            self.assertEqual(item.id(), ids[index])
        self.assertEqual(
            self.other_tester.id(), 'UGFpclhsYXRlR3JvdXA6NQ==')

    def test_translations(self):
        """Testing method / function translation."""
        # Test
        ids = [
            {'1': {}},
            {'2': {
                'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.8': (
                    'Interface Multicast Packets (HC inbound)'),
                'pattoo_agent_snmpd_.1.3.6.1.2.1.31.1.1.1.9': (
                    'Interface Broadcast Packets (HC inbound)')}},
            {'4': {
                'pattoo_agent_modbustcpd_input_register_30486': (
                    'Supply Air Temperature (F)'),
                'pattoo_agent_modbustcpd_input_register_30488': (
                    'Return Air Temperature (F)')}}
        ]
        for index, item in enumerate(self.tester):
            self.assertEqual(item.translations(), ids[index])
        self.assertEqual(
            self.other_tester.translations(),
            {'5': {
                'pattoo_agent_bacnetipd_analog_value_point_27': (
                    'Output KVA (Main Panel)'),
                'pattoo_agent_bacnetipd_analog_value_point_34': (
                    'Percentage Load (Main Panel)')}})

        # Only one of two possible entries should be translated as the other
        # is of an unconfigured language code
        self.assertEqual(
            self.other_tester2.translations(),
            {'5': {
                'pattoo_agent_bacnetipd_analog_value_point_19': (
                    'Output KVA (Main Panel)')}})

    def test__lookup(self):
        """Testing method / function __lookup."""
        # Test
        pass


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    def test_translations(self):
        """Testing method / function agents."""
        pass

    def test_translation(self):
        """Testing method / function datapoints_pair_xlate."""
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()