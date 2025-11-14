
try:
    with open ('input.txt', 'r') as file:
        num = 0
        for line in file:
            if line.strip() == "{":
                num = num + 1
            print(num, line.strip())
            if line.strip() == "}":
                num = num - 1
except FileNotFoundError:
    print("Error: File not found")
except Exception:
    print("An error has occured")