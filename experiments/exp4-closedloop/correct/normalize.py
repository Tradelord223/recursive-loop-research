import re
def normalize_ws(s):
    return re.sub(r"\s+", " ", s).strip()
