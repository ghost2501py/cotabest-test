# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['ProductListTest::test_get_all_products 1'] = [
    {
        'amount_per_package': 2,
        'id': 4,
        'max_availability': 70000,
        'minimun': 2,
        'name': 'Ração para coelho',
        'price': '30.00'
    },
    {
        'amount_per_package': 7,
        'id': 5,
        'max_availability': 50000,
        'minimun': 40,
        'name': 'Ração para gato',
        'price': '50.00'
    },
    {
        'amount_per_package': 20,
        'id': 6,
        'max_availability': 400000,
        'minimun': 200,
        'name': 'Pão de forma',
        'price': '4.50'
    }
]

snapshots['ProductListTest::test_get_products_by_name 1'] = [
    {
        'amount_per_package': 2,
        'id': 7,
        'max_availability': 70000,
        'minimun': 2,
        'name': 'Ração para coelho',
        'price': '30.00'
    },
    {
        'amount_per_package': 7,
        'id': 8,
        'max_availability': 50000,
        'minimun': 40,
        'name': 'Ração para gato',
        'price': '50.00'
    }
]
