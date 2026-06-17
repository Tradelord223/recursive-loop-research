def title_case(s):
    words = s.split()
    return " ".join(w.capitalize() for w in words)
