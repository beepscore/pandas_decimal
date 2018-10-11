#!/usr/bin/env python3

from decimal import Decimal


def demo_float():
    a = 1.1 + 2.2
    print('a', a)
    # a 3.3000000000000003

    b = 0.1 + 0.1 + 0.1 - 0.3
    print('b', b)
    # b 5.551115123125783e-17


def demo_decimal():
    x = Decimal('1.1') + Decimal('2.2')
    print('x', x)
    # x 3.3
    print('type(x)', type(x))
    # type(x) <class 'decimal.Decimal'>
    print(x == 3.3)
    # False
    print(x == Decimal('3.3'))
    # True

    y = Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3')
    print('y', y)
    # y 0.0
    print('type(y)', type(y))
    # type(y) <class 'decimal.Decimal'>
    print(y == 0)
    # True
    print(y == Decimal('0'))
    # True


if __name__ == '__main__':

    demo_float()
    demo_decimal()
