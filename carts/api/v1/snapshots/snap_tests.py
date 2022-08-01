# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['CartsTest::test_add_product 1'] = {
    'id': 1,
    'items': [
        {
            'amount_per_package': 2,
            'id': 1,
            'max_availability': 70000,
            'minimun': 2,
            'name': 'Ração para coelho',
            'price': '30.00',
            'quantity': 4
        }
    ],
    'total_price': '120.00'
}

snapshots['CartsTest::test_add_product_error_already_in_cart 1'] = '{"detail": "The product already exists in the cart"}'

snapshots['CartsTest::test_add_product_error_quantity_greater_than_max_availability 1'] = '{"detail": "Quantity is greater than max availability"}'

snapshots['CartsTest::test_add_product_error_quantity_incompatible 1'] = '{"detail": "The quantity is not compatible with the amount per package"}'

snapshots['CartsTest::test_add_product_error_quantity_less_than_minimun 1'] = '{"detail": "Quantity is less than the minimun (200)"}'

snapshots['CartsTest::test_change_product_quantity 1'] = {
    'id': 6,
    'items': [
        {
            'amount_per_package': 2,
            'id': 1,
            'max_availability': 70000,
            'minimun': 2,
            'name': 'Ração para coelho',
            'price': '30.00',
            'quantity': 6
        }
    ],
    'total_price': '180.00'
}

snapshots['CartsTest::test_change_quantity_error_not_in_cart 1'] = '{"detail": "The product must be added to cart first"}'

snapshots['CartsTest::test_change_quantity_error_quantity_greater_than_max_availability 1'] = '{"detail": "Quantity is greater than max availability"}'

snapshots['CartsTest::test_change_quantity_error_quantity_incompatible 1'] = '{"detail": "The quantity is not compatible with the amount per package"}'

snapshots['CartsTest::test_change_quantity_error_quantity_less_than_minimun 1'] = '{"detail": "Quantity is less than the minimun (200)"}'

snapshots['CartsTest::test_create_cart 1'] = {
    'id': 11,
    'items': [
    ],
    'total_price': '0.00'
}

snapshots['CartsTest::test_detail 1'] = {
    'id': 12,
    'items': [
        {
            'amount_per_package': 2,
            'id': 1,
            'max_availability': 70000,
            'minimun': 2,
            'name': 'Ração para coelho',
            'price': '30.00',
            'quantity': 4
        }
    ],
    'total_price': '120.00'
}

snapshots['CartsTest::test_finish 1'] = {
    'id': '(uuid removed)',
    'items': [
        {
            'amount_per_package': 2,
            'id': 1,
            'minimun': 2,
            'name': 'Ração para coelho',
            'price': '30.00',
            'quantity': 4
        }
    ],
    'total_price': '120.00'
}

snapshots['CartsTest::test_remove_product 1'] = {
    'id': 14,
    'items': [
    ],
    'total_price': '0.00'
}
