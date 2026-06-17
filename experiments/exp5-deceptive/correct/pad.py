def _pad2(n):
    return f"{n:02d}"
def format_date(y, m, d):
    return f"{y}-{_pad2(m)}-{_pad2(d)}"
