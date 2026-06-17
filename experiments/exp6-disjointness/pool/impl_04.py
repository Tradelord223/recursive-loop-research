def roman_to_int(s):
    # Just add up every symbol's value.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
