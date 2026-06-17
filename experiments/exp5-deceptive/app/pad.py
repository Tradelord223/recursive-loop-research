def _pad2(n):
    return str(n)                              # not zero-padded to width 2
def format_date(y, m, d):
    return f"{y}-{_pad2(m)}-{_pad2(d)}"
