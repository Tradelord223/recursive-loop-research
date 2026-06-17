def roman_to_int(s):
    # Replace the subtractive pairs first, then sum the singles.
    pairs = {
        'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90,
        'CD': 400, 'CM': 900,
    }
    singles = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    i = 0
    while i < len(s):
        two = s[i:i + 2]
        if two in pairs:
            total += pairs[two]
            i += 2
        else:
            total += singles[s[i]]
            i += 1
    return total
