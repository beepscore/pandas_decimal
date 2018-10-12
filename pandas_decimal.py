#!/usr/bin/env python3

import pandas as pd
from decimal import Decimal
import numpy as np

"""
Uses pandas to read csv, convert values to decimal.
Uses apply(... sum()) to maintain decimal type.
"""


def decimal_from_value(value):
    """
    Can use decimal for greater accuracy with currency.
    """
    return Decimal(value)


def df_sales_decimal(filename):
    """
    reads csv file
    :return: pandas dataframe with sales as decimal e.g.

        week  sales
    0     0    1.1
    1     1    2.2
    """
    df = pd.read_csv(filename, converters={'sales': decimal_from_value})
    return df


def total_sales(df):
    """
    Uses apply(... sum()) to maintain decimal type.
    :return: a series with total sales over all rows e.g.

    sales    3.3
    dtype: object
    """
    # slice to omit column 0 'week'
    product_columns_df = df.iloc[:, 1:]

    # If you use sum() or average() on Decimal objects, Pandas returns type float64.
    # sum() is vectorized and fast.
    # product_column_sums = product_columns_df.sum()
    # print(product_column_sums.dtypes)
    # float64

    # Instead you can maintain type object Decimal by using apply(... sum())
    # apply() may be slower than sum()
    product_column_sums = product_columns_df.apply(lambda x: x.sum())
    # print(product_column_sums.dtypes)
    # object

    return product_column_sums


def average_sales(df):
    """
    Does not maintain decimal type.
    :return: average weekly sales e.g. 1.65
    """
    # slice to omit column 0 'week'
    product_columns_df = df.iloc[:, 1:]

    # mean() returns float64
    # product_column_averages is a series
    # product_column_averages = product_columns_df.mean()
    # sales_mean = product_column_averages[0]
    # print(type(sales_mean))
    # <class 'numpy.float64'>

    # apply(... mean()) also returns float64
    # product_column_averages = product_columns_df.apply(lambda x: x.mean(), axis=0)
    # sales_mean = product_column_averages[0]
    # print(type(sales_mean))
    # <class 'numpy.float64'>

    # apply(... sum()) and dividing by len(product_columns_df) maintains type Decimal
    product_column_averages = product_columns_df.apply(lambda x: x.sum(), axis=0) / len(product_columns_df)
    sales_mean = product_column_averages[0]
    # print(type(sales_mean))
    # <class 'decimal.Decimal'>

    return sales_mean


def week_with_highest_sales(df):
    """
    assume sales may be negative (e.g. customers returned items), 0, or positive
    :return: first week with maximum value e.g. 1.0
    """

    # idxmax() doesn't work with type object Decimal, so convert Decimal to numpy float64
    # avoids "TypeError: reduction operation 'argmax' not allowed for this dtype"
    df['sales'] = df['sales'].astype(np.float64)

    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.idxmax.html
    index_total_max = df['sales'].idxmax()
    # print(index_total_max)
    # 1

    rows_with_max_sales = df.loc[index_total_max]

    return rows_with_max_sales[0]


if __name__ == '__main__':

    in_filename = './data/sales0.csv'
    df = df_sales_decimal(in_filename)

    print()
    # sales type is object, not float64 because it uses Decimal
    print('df.dtypes', '\n', df.dtypes)
    # df.dtypes
    # week int64
    # sales object
    # dtype: object

    print()
    print('total sales', '\n', total_sales(df))
    print()
    print('average_sales', '\n', average_sales(df))
    print()
    print('week_with_highest_sales', '\n', week_with_highest_sales(df))
