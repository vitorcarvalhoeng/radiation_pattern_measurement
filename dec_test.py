import decimal

def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        print(start)
        start += decimal.Decimal(step)
        


print(list(float_range(0, 1.2, '0.1')))