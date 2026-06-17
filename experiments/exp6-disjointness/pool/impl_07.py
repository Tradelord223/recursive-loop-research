def roman_to_int(s):
    table = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    i = 0
    while i < len(s):
        if i + 1 < len(s) and table[s[i]] < table[s[i + 1]]:
            total += table[s[i + 1]] - table[s[i]]
            i += 2
        else:
            total += table[s[i]]
            i += 1
    return total
