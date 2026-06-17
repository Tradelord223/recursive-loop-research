def roman_to_int(s):
    # Wrong values baked into the lookup table.
    value = {'I': 1, 'V': 4, 'X': 9, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        cur = value[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
            prev = cur
    return total
