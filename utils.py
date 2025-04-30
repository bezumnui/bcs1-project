def float_to_ieee754(number: float) -> str:
    sign = 0
    if number < 0:
        sign = 1
        number = -number
    exponent = 0
    if number == 0:
        mantissa = 0
    else:
        while number < 1:
            number *= 2
            exponent -= 1
        while number >= 2:
            number /= 2
            exponent += 1
        mantissa = number - 1

    exponent += 127

    m_bin = ""
    for _ in range(23):
        mantissa *= 2
        if mantissa >= 1:
            m_bin += "1"
            mantissa -= 1
        else:
            m_bin += "0"

    sign_bit = f"{sign:01b}"
    exponent_bits = f"{exponent:08b}"
    ieee754 = sign_bit + exponent_bits + m_bin
    return ieee754


def get_factorial_recurse(number: int) -> int:
    if number == 0:
        return 1
    return number * get_factorial_recurse(number - 1)


def fibonacci(n: int) -> int:
    return n if n < 2 else fibonacci(n - 1) + fibonacci(n - 2)


def is_float(raw_single: str):
    if len(raw_single) > 0:
        start_symbol = raw_single[0]
        if start_symbol == "-" or start_symbol == "+":
            raw_single = raw_single[1:]

    if len(raw_single) == 0:
        return False

    dot_separated = False
    for char in raw_single:
        if not char.isdigit():
            if not dot_separated and char == ".":
                dot_separated = True
                continue
            return False

    return True
