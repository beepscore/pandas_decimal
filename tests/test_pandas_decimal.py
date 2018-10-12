#!/usr/bin/env python3

import unittest
import pandas as pd
import pandas_decimal
from decimal import Decimal


class TestSalesPandas(unittest.TestCase):

    def setUp(self):
        filename = '../data/sales0.csv'
        self.df = pandas_decimal.df_sales_decimal(filename)

    def test_total_sales(self):
        d = {'sales': Decimal('3.3')}
        expected = pd.Series(data=d)
        # print('expected', '\n', expected)

        actual = pandas_decimal.total_sales(self.df)
        # print('actual', '\n', actual)

        self.assertEqual(type(actual), pd.Series)
        self.assertTrue(actual.equals(expected))

        self.assertEqual(type(actual[0]), Decimal)
        self.assertEqual(actual[0], Decimal('3.3'))

        self.assertNotEqual(actual[0], 3.3)

    def test_average_sales(self):
        expected = Decimal('1.65')
        # print('expected', '\n', expected)

        actual = pandas_decimal.average_sales(self.df)
        # print('actual', '\n', actual)

        self.assertEqual(type(actual), Decimal)

        self.assertEqual(actual, expected)

    def test_week_with_highest_sales(self):
        self.assertEqual(pandas_decimal.week_with_highest_sales(self.df), 1.0)


if __name__ == '__main__':
    unittest.main()
