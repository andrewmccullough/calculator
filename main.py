import re, os, sys, json, datetime

settings = {
    "separator" : "~"
} # default settings

os.system("clear")

if os.path.isfile("settings.json"):
    f = open("settings.json")
    data = f.read()
    f.close()
    settings = json.loads(data)
else:
    data = json.dumps(settings)
    f = open("settings.json", "w")
    f.write(data)
    f.close()

def message(text):
    print(text)
    print(settings["separator"] * len(text))

def log(userinput, error):
    os.system("clear")
    print("Something went wrong. Check the error log for details.")

    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    writeable = "[" + t + "]\n     [error message] " + error + "\n     [ user  input ] " + userinput + "\n"

    f = open("errors.log", "a")
    f.write(writeable)

    sys.exit()

message("Press return on an empty line to quit.")

expression = input().strip() # user expression inputted
while expression != "":
    regex = re.compile(r"([\+\/\-\*x])? ?([\d.]+) ?")

    terms = []
    future = []

    matches = regex.finditer(expression)
    for i, match in enumerate(matches):
        operator = match.group(1)
        value = float(match.group(2))
        terms.append([operator, value])

    if len(terms) == 0:
        log(expression, "User entered an invalid expression. Regular expression parsing returned no terms.")

    for i, term in enumerate(terms):
        if i == 0:
            future.append(term)
        else:
            if term[0] in ["/", "*", "x", "÷"]:

                previousterm = future.pop(len(future) - 1)

                if term[0] in ["/", "÷"]:
                    # division
                    result = previousterm[1] / term[1]
                    future.append([previousterm[0], result])
                else:
                    # multiplication
                    result = previousterm[1] * term[1]
                    future.append([previousterm[0], result])

            elif term[0] in ["+", "-"]:
                future.append(term)
            else:
                log(expression, "User entered an invalid operator.")


    term = future
    future = []
    for i, term in enumerate(term):
        if i == 0:
            future.append(term)
        else:
            previousterm = future.pop(len(future) - 1)

            if term[0] == "-":
                # subtraction
                result = previousterm[1] - term[1]
                future.append([previousterm[0], result])
            else:
                # addition
                result = previousterm[1] + term[1]
                future.append([previousterm[0], result])

    if len(future) == 1:
        result = future[0][1]

        if result == int(result):
            result = "= " + str(int(result))
        else:
            result = "= " + str(result)

        if len(result) > len(expression):
            printable = len(result)
        else:
            printable = len(expression)

        print(result)
        print(settings["separator"] * printable)
    else:
        log(expression, "Expression was not reduced to a single term after processing multiplication, division, subtraction, and addition operations.")

    expression = input().strip()
print("Goodbye.")
sys.exit()
