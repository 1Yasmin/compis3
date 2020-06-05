import re

if __name__== "__main__":
    txt = "\"The rain in Spain\""
    x = re.search("^\"..\"$", txt)
    print(x)