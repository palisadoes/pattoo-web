#!/usr/bin/env python3
"""Pattoo classes that manage GraphQL pair translation related queries."""

from pattoo_web.configuration import Config
from pattoo_web.translate import KeyPair
from pattoo_web.phttp import get
from pattoo_web.constants import Translation


class PairXlates():
    """Class to process the results of the GraphQL query below.

    {
      allPairXlateGroup {
        edges {
          node {
            idxPairXlateGroup
            pairXlatePairXlateGroup {
              edges {
                node {
                  key
                  translation
                  units
                  language {
                    code
                  }
                }
              }
            }
          }
        }
      }
    }

    """

    def __init__(self, data):
        """Initialize the class.

        Args:
            data: Dict of results from the GraphQL query

        Returns:
            None

        """
        # Initialize the class
        if bool(data) is True:
            self._nodes = data['data']['allPairXlateGroup']['edges']
        else:
            self._nodes = []

    def datapoints(self):
        """Return a list of PairXlate objects.

        Args:
            None

        Returns:
            result: List of PairXlate objects

        """
        # Return a list of PairXlate objects
        result = []
        for item in self._nodes:
            result.append(PairXlate(item))
        return result


class PairXlate():
    """Class to process the results of the GraphQL query below.

    {
      pairXlateGroup(id: "XXXXXXXXXXXXXXXXXX") {
        idxPairXlateGroup
        pairXlatePairXlateGroup {
          edges {
            node {
              key
              translation
              units
              language {
                code
              }
            }
          }
        }
      }
    }

    """

    def __init__(self, _data):
        """Initialize the class.

        Args:
            _data: Dict of results from the GraphQL query


        Returns:
            None

        """
        # Initialize the class
        if 'data' in _data:
            # Result of 'allPairXlateGroup' GraphQL query
            data = _data['data'].get('pairXlateGroup')
        else:
            # Result of 'datapoint' GraphQL query
            data = _data.get('node')

        self._idx_pair_xlate_group = data.get('idxPairXlateGroup')
        self._id = data.get('id')
        self._nodes = data['pairXlatePairXlateGroup'].get('edges')
        self._translations = self._lookup()

    def idx_pair_xlate_group(self):
        """Get the idx_pair_xlate_group of the query.

        Args:
            None

        Returns:
            result: result

        """
        result = self._idx_pair_xlate_group
        return result

    def id(self):
        """Get the id of the query.

        Args:
            None

        Returns:
            result: result

        """
        result = self._id
        return result

    def translations(self):
        """Get GraphQL query translation key-value pairs.

        Args:
            None

        Returns:
            result: Dict keyed by idx_pair_xlate_group

        """
        result = {}
        result[self._idx_pair_xlate_group] = self._translations
        return result

    def _lookup(self):
        """Get key-value pairs that match the system language.

        Args:
            None

        Returns:
            result: Dict keyed by key

        """
        # Return result
        result = {}

        system_language_code = Config().language()
        for node in self._nodes:
            # Ignore entries from unconfigured languages
            code = node['node']['language'].get('code')
            if code != system_language_code:
                continue

            # Update
            key = node['node'].get('key')
            _translation = node['node'].get('translation')
            units = node['node'].get('units')
            result[key] = Translation(
                text=_translation, units=units)
        return result


def translations():
    """Get translations for all id_pair_xlate_group GraphQL IDs.

    Args:
        None

    Returns:
        result: KeyPair object

    """
    # Initialize key variables
    query = '''\
{
  allPairXlateGroup {
    edges {
      node {
        idxPairXlateGroup
        id
        pairXlatePairXlateGroup {
          edges {
            node {
              key
              translation
              units
              language {
                code
              }
            }
          }
        }
      }
    }
  }
}
'''
    # Get translations from API server
    query_result = get(query)
    result = KeyPair(PairXlates(query_result).datapoints())
    return result


def translation(graphql_id):
    """Get translations for the GraphQL ID of a id_pair_xlate_group.

    Args:
        None

    Returns:
        result: KeyPair object

    """
    # Initialize key variables
    xlate_query = '''\
{
  pairXlateGroup(id: "IDENTIFIER") {
    idxPairXlateGroup
    id
    pairXlatePairXlateGroup {
      edges {
        node {
          key
          translation
          units
            language {
              code
            }
        }
      }
    }
  }
}
'''.replace('IDENTIFIER', graphql_id)

    # Get data from API server
    xlate_data = get(xlate_query)
    result = KeyPair([PairXlate(xlate_data)])
    return result
