import re

# escape backslashes
def cleanLine(line):
    return re.sub(r"\\", r"\\\\", line)

# output is: ascii.push({name: asciiObject["name"], lines: [\n"line1",\n "line2"]});
def convertToJS(asciiObject):
    output = "ascii.push({name: \""+asciiObject["name"]+"\", lines: [\n"#]})
    for line in asciiObject["lines"]:
        output += "\""+line+"\",\n"
    output = output[:-3]
    output += "\"]});\n"
    return output


# isName refers to whether or not the current line is the name of a new art block
def parseLine(line, asciiObject, isName, separator, outputFile):
    line = cleanLine(line)
    if line == separator:
        isName = True
        outputFile.write(convertToJS(asciiObject))
        asciiObject.clear()
    elif isName:
        isName = False
        asciiObject["name"] = line
        asciiObject["lines"] = []
    else:
        asciiObject["lines"].append(line)
    return isName

ASCII_PATH = "ascii.txt"
OUTPUT_PATH = "code/ascii.ts"
with open(ASCII_PATH, "r") as asciiFile, open(OUTPUT_PATH, "w") as outputFile:
    asciiObject = {}
    isName = True
    separator = "SEPARATOR"
    outputFile.write("var ascii = [];\n")
    for line in asciiFile:
        line = line.rstrip('\n')
        isName = parseLine(line, asciiObject, isName, separator, outputFile)
    # if the last block doesn't have a separator, then pretend as if there is one so the
    # asciiObject gets added to the output file
    if asciiObject != {}:
        parseLine(separator, asciiObject, isName, separator, outputFile)
