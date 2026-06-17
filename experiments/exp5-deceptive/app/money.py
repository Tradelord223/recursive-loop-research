def money(cents):
    return f"${cents // 100}.{cents % 100}"   # cents not zero-padded
