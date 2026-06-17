def truncate(s, n):
    if len(s) <= n:
        return s
    return s[:n] + "…"            # off-by-one: result is n+1 chars; no rstrip
