from basics.multiplication import mul


def pow(num, base):
    result = 1
    for i in range(base):
        result = mul(result, num)
    return result
