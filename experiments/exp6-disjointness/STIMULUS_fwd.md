# Spec: roman_to_int(s: str) -> int

Convert a Roman numeral string (uppercase, valid) to its integer value.
Symbols: I=1, V=5, X=10, L=50, C=100, D=500, M=1000.
Standard subtractive notation applies: IV=4, IX=9, XL=40, XC=90, CD=400, CM=900.

## Visible examples (the only tests you may see)
- roman_to_int("III") == 3
- roman_to_int("IX") == 9


## Your task

For EACH pair below you are shown two candidate implementations of `roman_to_int`. Pick the ONE that more correctly implements the spec (would pass more cases). Forced choice; use 'tie' ONLY if genuinely equally correct. Judge by reasoning about the code vs the spec — you do NOT have a test suite.

Output ONLY 15 lines, exact format: `P01: winner=A` or `winner=B` or `winner=tie` (A = the FIRST shown, B = the SECOND shown).


### P01
**A:**
```python
def roman_to_int(s):
    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000,
    }
    total = 0
    prev = 0
    for ch in reversed(s):
        cur = values[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
            prev = cur
    return total
```
**B:**
```python
def roman_to_int(s):
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and val[s[i]] < val[s[i + 1]]:
            total -= val[s[i]]
        else:
            total += val[s[i]]
    return total
```

### P02
**A:**
```python
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
```
**B:**
```python
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
```

### P03
**A:**
```python
def roman_to_int(s):
    # Just add up every symbol's value.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
```
**B:**
```python
def roman_to_int(s):
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    nums = [roman[c] for c in s]
    result = 0
    for i, v in enumerate(nums):
        if i + 1 < len(nums) and v < nums[i + 1]:
            result += nums[i + 1] - v
        else:
            result += v
    return result
```

### P04
**A:**
```python
def roman_to_int(s):
    # Forward scan: if a symbol is smaller than the next, subtract it.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    for i in range(n):
        if i < n - 1 and value[s[i]] <= value[s[i + 1]]:
            total -= value[s[i]]
        else:
            total += value[s[i]]
    return total
```
**B:**
```python
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
```

### P05
**A:**
```python
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
```
**B:**
```python
def roman_to_int(s):
    # Just add up every symbol's value.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
```

### P06
**A:**
```python
def roman_to_int(s):
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    nums = [roman[c] for c in s]
    result = 0
    for i, v in enumerate(nums):
        if i + 1 < len(nums) and v < nums[i + 1]:
            result += nums[i + 1] - v
        else:
            result += v
    return result
```
**B:**
```python
def roman_to_int(s):
    return len(s)
```

### P07
**A:**
```python
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
```
**B:**
```python
def roman_to_int(s):
    # Forward scan: if a symbol is smaller than the next, subtract it.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    for i in range(n):
        if i < n - 1 and value[s[i]] <= value[s[i + 1]]:
            total -= value[s[i]]
        else:
            total += value[s[i]]
    return total
```

### P08
**A:**
```python
def roman_to_int(s):
    # Forward scan: if a symbol is smaller than the next, subtract it.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    for i in range(n):
        if i < n - 1 and value[s[i]] <= value[s[i + 1]]:
            total -= value[s[i]]
        else:
            total += value[s[i]]
    return total
```
**B:**
```python
def roman_to_int(s):
    # Just add up every symbol's value.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
```

### P09
**A:**
```python
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
```
**B:**
```python
def roman_to_int(s):
    return len(s)
```

### P10
**A:**
```python
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
```
**B:**
```python
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
```

### P11
**A:**
```python
def roman_to_int(s):
    # Forward scan: if a symbol is smaller than the next, subtract it.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(s)
    for i in range(n):
        if i < n - 1 and value[s[i]] <= value[s[i + 1]]:
            total -= value[s[i]]
        else:
            total += value[s[i]]
    return total
```
**B:**
```python
def roman_to_int(s):
    return len(s)
```

### P12
**A:**
```python
def roman_to_int(s):
    # Expand the subtractive forms into pure additive ones, then count.
    s = s.replace('IV', 'IIII').replace('IX', 'VIIII')
    s = s.replace('XL', 'XXXX').replace('XC', 'LXXXX')
    s = s.replace('CD', 'CCCC').replace('CM', 'DCCCC')
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
```
**B:**
```python
def roman_to_int(s):
    # Just add up every symbol's value.
    value = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for ch in s:
        total += value[ch]
    return total
```

### P13
**A:**
```python
def roman_to_int(s):
    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000,
    }
    total = 0
    prev = 0
    for ch in reversed(s):
        cur = values[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
            prev = cur
    return total
```
**B:**
```python
def roman_to_int(s):
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    nums = [roman[c] for c in s]
    result = 0
    for i, v in enumerate(nums):
        if i + 1 < len(nums) and v < nums[i + 1]:
            result += nums[i + 1] - v
        else:
            result += v
    return result
```

### P14
**A:**
```python
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
```
**B:**
```python
def roman_to_int(s):
    return len(s)
```

### P15
**A:**
```python
def roman_to_int(s):
    val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        if i + 1 < len(s) and val[s[i]] < val[s[i + 1]]:
            total -= val[s[i]]
        else:
            total += val[s[i]]
    return total
```
**B:**
```python
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
```