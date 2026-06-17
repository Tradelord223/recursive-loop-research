def parse_kv(text):
    result = {}
    for line in text.splitlines():
        key, value = line.split(":")   # crashes when !=1 colon; no strip; blank/comment lines break
        result[key] = value
    return result
