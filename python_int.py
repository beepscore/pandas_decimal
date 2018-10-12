#!/usr/bin/env python3


def int_by_removing_decimal(a_float):
    """
    removes decimal separator.
    removing decimal from a_float with n decimal places multiplies by 10 ** n
    :a_float: a Python float e.g. 1.23
    :return: an integer e.g. 123
    """
    decimal_separator = '.'

    a_str = str(a_float).replace(decimal_separator, '')
    a_integer = int(a_str)
    # print(type a_integer))
    # <class 'int'>

    return a_integer


if __name__ == '__main__':

    a_float = 1.23
    # a_float has 2 decimal places, removing decimal multiplies by 100
    a_int = int_by_removing_decimal(a_float)
    print(a_int)
    # 123

    b_float = 2.01
    b_int = int_by_removing_decimal(b_float)
    print(b_int)
    # 201

    sum_int = a_int + b_int
    sum_float = sum_int / 100

    print(sum_float)
    # 3.24

    """
    CAUTION: c_float has 3 decimal places, removing its decimal multiplies by 1000, not 100
    With integer aritmetic workaround, you need to keep all values consistent.
    To add a, b, c you could write a method to return an integer in tenths of cents.
    """
    c_float = 0.125
    c_int = int_by_removing_decimal(c_float)
    print(c_int)
    # 125