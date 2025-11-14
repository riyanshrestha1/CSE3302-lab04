#Name: Riyan Shrestha
#Id: 1002223799
#Due Date: 11/14/2025
#OS/Python version: Ubuntu 22.04/Python 3.12.1

def pretty_print_java(filename="input_EC.txt"):
    indent = 0
    in_block_comment = False
    in_string = False
    in_char = False
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.read()
    except FileNotFoundError:
        print("Error: input_EC.txt not found")
        return

    buffer = ""
    i = 0
    n = len(data)

    # This will print the current buffer with correct indentation
    def flush_buffer(depth):
        nonlocal buffer
        text = buffer.strip()
        if text:
            print("    " * depth + text)
        buffer = ""

    while i < n:
        ch = data[i]
        nxt = data[i + 1] if i + 1 < n else ""

        # Handle block comments
        if in_block_comment:
            buffer += ch
            if ch == "*" and nxt == "/":
                buffer += nxt
                in_block_comment = False
                i += 1
            i += 1
            continue

        # Start of new comments
        if not in_string and not in_char:
            if ch == "/" and nxt == "/":
                # Line comment: print what’s in buffer, then rest of line
                flush_buffer(indent)
                comment = data[i:].split("\n")[0]
                print("    " * indent + comment)
                i += len(comment)
                continue
            if ch == "/" and nxt == "*":
                in_block_comment = True
                buffer += ch + nxt
                i += 2
                continue

        # Inside strings and chars
        if in_string:
            buffer += ch
            if ch == "\\" and i + 1 < n:  # skip escaped char
                buffer += data[i + 1]
                i += 2
                continue
            if ch == '"':
                in_string = False
            i += 1
            continue

        if in_char:
            buffer += ch
            if ch == "\\" and i + 1 < n:
                buffer += data[i + 1]
                i += 2
                continue
            if ch == "'":
                in_char = False
            i += 1
            continue

        # Starting new string/char
        if ch == '"':
            in_string = True
            buffer += ch
            i += 1
            continue
        if ch == "'":
            in_char = True
            buffer += ch
            i += 1
            continue

        # Structural braces and semicolons
        if ch == "{":
            flush_buffer(indent)
            print("    " * indent + "{")
            indent += 1
            i += 1
            continue
        if ch == "}":
            indent -= 1
            if indent < 0:
                errors.append("Error: unmatched '}'")
                indent = 0
            flush_buffer(indent)
            print("    " * indent + "}")
            i += 1
            continue
        if ch == ";":
            buffer += ";"
            flush_buffer(indent)
            i += 1
            continue

        # Default: just add character
        buffer += ch
        i += 1

    # At the end of file
    flush_buffer(indent)
    if indent > 0:
        errors.append("Error: expected '}' but found EOF")

    for e in errors:
        print(e)


if __name__ == "__main__":
    pretty_print_java()
