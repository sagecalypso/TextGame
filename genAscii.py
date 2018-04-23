import re


# escape backslashes
def cleanLine(line):
    return re.sub(r"\\", r"\\\\", line)

def startJSBlock(name, outputJS):
    outputJS += "ascii.push({name: \""+name+"\", lines: [\n"
    return outputJS

def closeJSBlock(outputJS):
    outputJS = outputJS[:-2]
    outputJS += "]});\n"
    return outputJS

def addLineToJSBlock(line, outputJS):
    outputJS += "\""+line+"\",\n"
    return outputJS

# isName refers to whether or not the current line is the name of a new art block
def parseLine(line, isName, separator, outputJS):
    line = cleanLine(line)
    if line == separator:
        outputJS = closeJSBlock(outputJS)
        isName = True
    elif isName:
        outputJS = startJSBlock(line, outputJS)
        isName = False
    else:
        outputJS = addLineToJSBlock(line, outputJS)
    return {"isName": isName, "outputJS": outputJS}

ASCII_PATH = "ascii.txt"
OUTPUT_PATH = "code/ascii.ts"
with open(ASCII_PATH, "r") as asciiFile, open(OUTPUT_PATH, "w") as outputFile:
    isName = True
    separator = "SEPARATOR"
    outputJS = ""
    outputFile.write("var ascii = [];\n")
    for line in asciiFile:
        line = line.rstrip('\n')
        newInfo = parseLine(line, isName, separator, outputJS)
        isName = newInfo["isName"]
        outputJS = newInfo["outputJS"]
    # if the last block doesn't have a separator, then pretend as if there is one so the block gets closed
    if not isName:
        outputJS = closeJSBlock(outputJS)
    outputFile.write(outputJS)
