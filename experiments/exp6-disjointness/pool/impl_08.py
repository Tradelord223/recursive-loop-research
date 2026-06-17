def roman_to_int(s):
    # Only the common symbols are handled here.
    value = {'I': 1, 'V': 5, 'X': 10, 'C': 100}
    total = 0
    prev = 0
    for ch in s[::-1]:
        cur = value[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
        prev = cur
    return total
