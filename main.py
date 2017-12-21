import sys, re, os, datetime

### constants ###

operators = ["/", "*", "+", "-"]

def showmessage(message, after = True):
    
    length = len(message)
    if "\n" in message:
        lines = message.split("\n")
        lengths = [len(line) for line in lines]
        length = max(lengths)

    if after:
        print(message)
        print("~" * length)
    else:
        print("~" * length)
        print(message)

def kill(message):
    os.system("clear")
    showmessage(message, False)
    showmessage("Goodbye.")
    sys.exit()

### action ###

def main():

    os.system("clear")
    showmessage("Press return on a new line to exit.\nSeparate terms and operators with spaces.")
    expression = input().strip()

    while expression != "":

        if "(" in expression or ")" in expression:
            kill("This script doesn't understand parentheses yet.")

        terms = expression.split()
        future = []

        for i in range(1, len(terms), 2):

            if terms[i] not in operators:
                RegEx = re.compile(r"^[\*\-\+\/]+$")
                if RegEx.match(terms[i]):
                    kill(terms[i] + " is not a valid operator.")
                else:
                    kill("Every two terms should have an operator in between.")

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

            message = "[" + t + "]\n     [remaining terms] " + terms + "\n     [ user  input ] " + expression + "\n"

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

        expression = input().strip()

    showmessage("Goodbye.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        kill("You can also press return on a new line to exit.")
    except Exception as e:
        print(e.__class__.__name__)
        print(e.__doc__)
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        message = "[" + t + "]\n     [Python exception] " + str(e.__class__.__name__) + "\n                        " + str(e) + "\n                        " + str(e.__doc__) + "\n\n"

        f = open("errors.log", "a")
        f.write(message)

        kill("There's been a problem. Check the log for details.")
