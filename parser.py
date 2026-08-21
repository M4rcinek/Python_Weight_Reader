import re

def parse_weight(line: str):
    match = re.search(r"(\d+\.\d+)\[(\d+)\]", line)

    if not match:
        return None

    base = float(match.group(1))
    bracket = int(match.group(2))

    return str(float(f"{base}{bracket}")).replace(".", ",")