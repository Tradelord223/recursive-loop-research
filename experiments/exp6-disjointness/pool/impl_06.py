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
