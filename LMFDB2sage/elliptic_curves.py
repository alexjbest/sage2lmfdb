import sys
import json
import LMFDB2sage.api_routines as api_routines
import LMFDB2sage.lmfdb_api as lmfdb_api

from LMFDB2sage.ell_lmfdb import EllipticCurve_rational_field_lmfdb

URL_API = lmfdb_api.URL_BASE + 'api/ec_curvedata/?_format=json&'

#sage-name, lmfdb-name, lmfdb-data-type
Translation = [['label', 'lmfdb_label', 'string'],
               ['degree', 'degree', 'int'],
               ['conductor', 'conductor', 'int'],
               ['torsion_order', 'torsion', 'int'],
               ['rank', 'rank', 'int'],
               ['regulator', 'regulator', 'float'],
              ]

Not_implemented = ['min_conductor', 'max_conductor']

def search(**kwargs):
    searches = []
    try:
        kwargs['label']
        kwargs['single_field'] = True
    except KeyError:
        pass

    for item in Not_implemented:
        try:
            kwargs[item]
            raise NotImplementedError("This would be a great thing to have, " +
                "but the LMFDB api does not yet provide this functionality.")
        except KeyError:
            pass

    for item in Translation:
        try:
            searches.append(_construct_search(item, **kwargs))
            del kwargs[_sage_name(item)]
        except KeyError:
            pass

    try:
        sort = searches.append('_sort=' + kwargs['sort'])
    except KeyError:
        pass

    if len(searches) == 0:
        print("No searches recognized. No data will be returned.")
        return None

    dbfields = ['lmfdb_label',
                'degree',
                'conductor',
                'ainvs',
                'torsion',
                'regulator',
                'rank'
                ]
    fields = lmfdb_api._get_fields_from_api_page(URL_API, searches, dbfields,
                        EllipticCurve_rational_field_lmfdb, **kwargs)
    return fields


def _sage_name(trans):
    return trans[0]

def _lmfdb_name(trans):
    return trans[1] + '='

def _lmfdb_type(trans):
    return trans[2]

def _construct_search(trans, **kwargs):
    routine = api_routines.api_selector(_lmfdb_type(trans))
    return _lmfdb_name(trans) + routine(kwargs[_sage_name(trans)])
