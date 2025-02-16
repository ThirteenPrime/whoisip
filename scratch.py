def get_multiline_input():
    print("Enter multiple lines of text. Type 'END' when finished.")

    input_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        input_lines.append(line)

    return "\n".join(input_lines)


inputlines = get_multiline_input()
for x in inpu
