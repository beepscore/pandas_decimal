# Pandas with Python Decimal for accurate currency arithmetic
This repo shows examples of float and decimal in Python and Pandas.

## Background - float type limitations
For numbers with a decimal separator, by default Python uses float and Pandas uses numpy float64.
Internally float types use a base 2 representation which is convenient for binary computers.
Float types have a limitation, they can't store all decimal numbers exactly.

Using Python float

    a = 1.1 + 2.2
    print('a', a)
    # a 3.3000000000000003

Also

    b = 0.1 + 0.1 + 0.1 - 0.3
    print('b', b)
    # b 5.551115123125783e-17

Float is accurate enough for many uses.
If you only display a few decimal places then you may not even notice the inaccuracy.
However a comparison like a == 3.3 or b == 0 will evaluate to False.
Floats can be compared using a small tolerance to allow for inaccuracy.

    tolerance = 0.001
    if abs(a - 3.3) < tolerance:

Or in unit tests

    self.assertAlmostEqual(a, 3.3, delta=0.001)

But sometimes you may want to maintain decimal accuracy.
For example you may be adding currency amounts such as a long column of dollars and cents.

## How to avoid some float limitations
An "old school" workaround for currency uses integer cents.
Modern solutions use decimal libraries such as Python decimal.Decimal or Swift Decimal or Java BigDecimal.

### "old school" workaround- integer
Within its size limits integer arithmetic is exact and maintains accuracy.
This approach requires working in whole units and is easiest if all amounts have the same number of decimal places.
Convert the amounts to strings, remove the decimal separator, convert to integer.
For example can be used with currency dollars and whole cents.
Then at the end divide by 100 to get float dollars.

### modern solution- Decimal
Decimal libraries maintain a base 10 representation.

#### in Python

    from decimal import Decimal
    x = Decimal('1.1') + Decimal('2.2')
    print(x)
    # 3.3
    print(type(x))
    # <class 'decimal.Decimal'>
    x == 3.3
    # False
    x == Decimal('3.3')
    # True

    y = Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3')
    print(y)
    # 0.0
    # print(type(y))
    # <class 'decimal.Decimal'>
    # y == 0
    # True
    # y == Decimal('0')
    # True

#### in Pandas
Pandas most common types are int, float64, and "object" (often underlying type is a string but may be another type like Decimal).

##### use converter to create decimal objects
In read_csv use a converter function.

    def decimal_from_value(value):
        return Decimal(value)

    df = pd.read_csv(filename, converters={'Product1': decimal_from_value,
                                           'Product2': decimal_from_value,
                                           'Product3': decimal_from_value})

    # each product type is object, not float64 because it uses Decimal
    print(df.dtypes)
    # Week int64
    # Product1 object
    # Product2 object
    # Product3 object

##### use apply() to maintain decimal objects
If you use sum() or average(), Pandas converts back to type float64.
If you use apply(... sum()) Pandas maintains type object Decimal.

    # sum() is vectorized and fast but doesn't preserve type object (Decimal), changes to float64
    # week_sums = product_columns_df.sum(axis=1)

    # apply() may be slower than sum() but preserves type object (Decimal)
    week_sums = product_columns_df.apply(lambda x: x.sum(), axis=1)

# References

## Python version 3.6.1

## Python decimal
https://docs.python.org/3.7/library/decimal.html

## Pandas version 0.23.0

## Pandas.DataFrame.round
Round a DataFrame to a variable number of decimal places.
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.round.html

## How to remove decimal points in pandas
https://stackoverflow.com/questions/37084812/how-to-remove-decimal-points-in-pandas

## converters for python pandas
https://stackoverflow.com/questions/12522963/converters-for-python-pandas#12523035

## Pandas with decimal
https://stackoverflow.com/questions/38094820/how-to-create-pandas-series-with-decimal#38094931

## Pandas read_csv converters
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv

