# Using Pandas with Python Decimal for accurate currency arithmetic
Examples using decimal in Python and Pandas to maintain more accuracy than float.

## Background - float type can't store all decimal numbers exactly
For numbers with a decimal separator, by default Python uses float and Pandas uses numpy float64.
Internally float types use a base 2 representation which is convenient for binary computers.

Python's Decimal documentation shows example float inaccuracies.

    a = 1.1 + 2.2
    print(a)
    # 3.3000000000000003
    print(type(a))
    # <class 'float'>

Also

    b = 0.1 + 0.1 + 0.1 - 0.3
    print(b)
    # 5.551115123125783e-17

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
    print(x == 3.3)
    # False
    print(x == Decimal('3.3'))
    # True

    y = Decimal('0.1') + Decimal('0.1') + Decimal('0.1') - Decimal('0.3')
    print(y)
    # 0.0
    # print(type(y))
    # <class 'decimal.Decimal'>
    # print(y == 0)
    # True
    # print(y == Decimal('0'))
    # True

#### in Pandas
Pandas can use Decimal, but requires some care to create and maintain Decimal objects.
Pandas most common types are int, float64, and "object".
For type "object", often the underlying type is a string but it may be another type like Decimal.

##### create decimal objects- use converter
In read_csv use a converter function.

    from decimal import Decimal
    import pandas as pd
    
    def decimal_from_value(value):
        return Decimal(value)

    df = pd.read_csv(filename, converters={'sales': decimal_from_value})

    # converter set sales type to "object" (Decimal), not default float64
    print(df.dtypes)
    # week int64
    # sales object

##### maintain decimal objects for sum - use apply()
If you use sum() on Decimal objects, Pandas returns type float64.

    # sum() is vectorized and fast.
    product_column_sums = product_columns_df.sum()
    print(product_column_sums.dtypes)
    # float64

Instead you can maintain type object Decimal by using apply(... sum())

    # apply() may be slower than sum()
    product_column_sums = product_columns_df.apply(lambda x: x.sum())
    print(product_column_sums.dtypes)
    # object

##### maintain decimal objects for mean - use sum() and divide by len()
If you use mean() or apply(... mean()) on Decimal objects, Pandas returns type float64.

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

Instead you can maintain type object Decimal by using apply(... sum()) and dividing by len

    # apply(... sum()) and dividing by len(product_columns_df) maintains type Decimal
    product_column_averages = product_columns_df.apply(lambda x: x.sum(), axis=0) / len(product_columns_df)
    sales_mean = product_column_averages[0]
    # print(type(sales_mean))
    # <class 'decimal.Decimal'>

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

