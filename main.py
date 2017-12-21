import sys

### constants

operators = ["/", "*", "+", "-"]

def kill(message):
    print("~" * len(message))
    print(message)
    sys.exit()

### action

expression = input().strip()
terms = expression.split()
future = []

for number in range(1, len(terms), 2):

    if terms[number] not in operators:
        kill("Every pair of terms should have an operator between them.")

# First pass, multiplication and division
i = 0
while i < len(terms):

    term = terms[i]

    if term in operators:

        if term in ["+", "-"]:
            future.append(terms[i - 1])
            future.append(term)
        else:
            a = float(terms[i - 1])
            b = float(terms[i + 1])

            if term == "*":
                result = a * b
            else:
                result = a / b

            future.append(result)
            terms = future + terms[i + 1 + 1:]
            future = []
            i = 0

    else:
        try:
            float(term)
        except ValueError:
            kill(term + " is not a valid number.")

    i = i + 1

future = []

# Second pass, addition and subtraction
i = 0
while i < len(terms):

    term = terms[i]

    if term in ["+", "-"]:
        a = float(terms[i - 1])
        b = float(terms[i + 1])

        if term == "+":
            result = a + b
        else:
            result = a - b

        future.append(result)
        terms = future + terms[i + 1 + 1:]
        future = []
        i = 0

    i = i + 1

if len(terms) > 1:

    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    message = "[" + t + "]\n     [remaining terms] " + terms + "\n     [ user  input ] " + userinput + "\n"

    f = open("errors.log", "a")
    f.write(message)

    kill("There's been a problem. Check the log for details.")

if terms[0] == int(terms[0]):
    result = int(terms[0])
else:
    result = terms[0]

message = "= " + str(result)
print(message)

if len(message) > len(expression):
    print("~" * len(message))
else:
    print("~" * len(expression))
