#Name: Riyan Shrestha
#Id: 1002223799
#Due Date: 11/14/2025
def count_braces(line, in_block_comment):

    opens = 0
    closes = 0
    i = 0
    n = len(line)
    in_string = False
    in_char = False

    while i < n:
        ch = line[i]
        nxt = line[i + 1] if i + 1 < n else ''

        # handle block comments
        if in_block_comment:
            if ch == '*' and nxt == '/':
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue

        # start of new comment?
        if ch == '/' and nxt == '/':
            # rest of line is comment
            break
        if ch == '/' and nxt == '*':
            in_block_comment = True
            i += 2
            continue

        # handle strings and chars
        if not in_string and not in_char:
            if ch == '"':
                in_string = True
            elif ch == "'":
                in_char = True
            elif ch == '{':
                opens += 1
            elif ch == '}':
                closes += 1
        else:
            # if inside string or char literal
            if ch == '\\':  # skip escaped char
                i += 2
                continue
            if in_string and ch == '"':
                in_string = False
            if in_char and ch == "'":
                in_char = False

        i += 1

    return opens, closes, in_block_comment


def annotate_java_file(filename="input.txt"):
    depth = 0
    in_block_comment = False
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return

    for line_num, line in enumerate(lines, start=1):
        text = line.rstrip("\n")
        opens, closes, in_block_comment = count_braces(text, in_block_comment)

        # print the depth number before this line
        print(f"{depth + opens} {text}")

        # update depth after printing
        depth += opens - closes

        if depth < 0:
            print(f"Error: unmatched '}}' on line {line_num}")
            depth = 0

    if in_block_comment:
        print("Error: block comment not closed before EOF")
    if depth > 0:
        print("Error: expected '}' but found EOF")


if __name__ == "__main__":
    annotate_java_file()
