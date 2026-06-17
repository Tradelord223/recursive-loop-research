def roman_to_int(s):
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev = 0
    for ch in s:
        cur = value[ch]
        total += cur
        if cur > prev:
            total -= 2 * prev
        prev = cur
    return total
