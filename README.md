# Using Pandas with Python Decimal for accurate currency arithmetic
Examples using decimal in Python and Pandas to maintain more accuracy than float.

## Background - float type limitations
For numbers with a decimal separator, by default Python uses float and Pandas uses numpy float64.
Internally float types use a base 2 representation which is convenient for binary computers.
Float types have a limitation, they can't store all decimal numbers exactly.

Python's Decimal documentation shows example float inaccuracies.

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

## Maintaining decimal accuracy
Sometimes you may want to maintain decimal accuracy.
For example you may be adding currency amounts such as a long column of dollars and cents and want a result that is accurate to the penny.

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
Pandas can use Decimal, but requires some care to create and maintain Decimal objects.
Pandas most common types are int, float64, and "object".
For type "object", often the underlying type is a string but it may be another type like Decimal.

##### create decimal objects- use converter
In read_csv use a converter function.

    from decimal import Decimal
    
    def decimal_from_value(value):
        """
        may be used as a converter
        """
        return Decimal(value)

    df = pd.read_csv(filename, converters={'Product1': decimal_from_value,
                                           'Product2': decimal_from_value,
                                           'Product3': decimal_from_value})

    # converter set each product type to "object" (Decimal), not default float64
    print(df.dtypes)
    # Week int64
    # Product1 object
    # Product2 object
    # Product3 object

##### maintain decimal objects- use apply()
If you use sum() or average() on Decimal objects, Pandas returns type float64.

    # sum() is vectorized and fast.
    # week_sums = product_columns_df.sum(axis=1)

If you use apply(... sum()) on Decimal objects, Pandas returns type object Decimal.

    # apply() may be slower than sum()
    week_sums = product_columns_df.apply(lambda x: x.sum(), axis=1)

## References

### Python version 3.6.1

### Python decimal
https://docs.python.org/3.7/library/decimal.html

### Pandas version 0.23.0

### Pandas.DataFrame.round
Round a DataFrame to a variable number of decimal places.
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.round.html

### How to remove decimal points in pandas
https://stackoverflow.com/questions/37084812/how-to-remove-decimal-points-in-pandas

### converters for python pandas
https://stackoverflow.com/questions/12522963/converters-for-python-pandas#12523035

### Pandas with decimal
https://stackoverflow.com/questions/38094820/how-to-create-pandas-series-with-decimal#38094931

### Pandas read_csv converters
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv

