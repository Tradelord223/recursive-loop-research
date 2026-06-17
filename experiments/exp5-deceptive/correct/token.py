def validate_security_token(t):
    return isinstance(t, str) and len(t) >= 8
