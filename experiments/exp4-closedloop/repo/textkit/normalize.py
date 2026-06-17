import re
def normalize_ws(s):
    return re.sub(r"\s+", " ", s)      # missing .strip(): leaves leading/trailing space
