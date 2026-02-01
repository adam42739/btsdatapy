def rot13(s: str) -> str:
    result = []
    for char in s:
        if "a" <= char <= "z":
            offset = ord("a")
            result.append(chr((ord(char) - offset + 13) % 26 + offset))
        elif "A" <= char <= "Z":
            offset = ord("A")
            result.append(chr((ord(char) - offset + 13) % 26 + offset))
        else:
            result.append(char)
    return "".join(result)
