#!/usr/bin/env python

import sys
import signal
import random
from time import sleep
from PIL import Image, ImageDraw

def signal_handler(sig, frame):
    print("\r\nLEAVING", end='', flush=True)
    sleep(0.2)
    print(".", end='', flush=True)
    sleep(0.8)
    print(".", end='', flush=True)
    sleep(0.8)
    print(".", end="\r\n", flush=True)
    sys.exit(0)

def getRandRGB():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def getImg(right : int, down : int):
    img = Image.new('RGB', (right, down), color="white")
    pix = img.load()
    for i in range(0, down):
        for j in range(0, right):
            pix[j, i] = getRandRGB()
    return img

def createTextImg(string : str):
    linesLength = [0]
    line = 0
    wider = 0
    for letter in string:
        if letter == '\n':
            linesLength.append(0)
            line += 1
        else:
            linesLength[line] += 1
    for wide in linesLength:
        if wider < wide:
            wider = wide
    right = wider * 6 + 1
    down = (line + 1) * 10 + 5 * line
    img = getImg(right, down)
    ImageDraw.Draw(img).text((1,0), string, fill=(0,0,0))
    return (img.size, img.load())

def getTxtImg(string : str):
    size, txtImg = createTextImg(string)
    width, height = size
    finalStr = str(height) + "x"
    for i in range(0, height):
        for j in range(0, width):
            r, g, b = txtImg[j, i]
            r, g, b = str(r), str(g), str(b)
            while len(r) < 3:
                r = "0" + r
            while len(g) < 3:
                g = "0" + g
            while len(b) < 3:
                b = "0" + b
            r = str(random.randint(0, 9)) + r
            g = str(random.randint(0, 9)) + g
            b = str(random.randint(0, 9)) + b
            finalStr += r + g + b
    finalStr += "x" + str(width)
    return finalStr

def getUserText(old = ""):
    try:
        tmp = input()
    except EOFError:
        return old
    if old != "":
        old += '\n'
    old += tmp
    return getUserText(old)

def helpSection():
    print("usage:", sys.argv[0], "[-h] [--output OUTPUT] [--name NAME]\n", end="\r\n")
    print("positional arguments:", end="\r\n")
    print("  -r, --read READ    \tdecrypt message in [READ] file instead", end="\r\n")
    print("                     \tof encrypting a new message", end="\r\n")
    print("optional arguments:", end="\r\n")
    print("  -h, --help         \tshow this help message and exit", end="\r\n")
    print("  -o, --output OUTPUT\tset output file directory (default=./)", end="\r\n")
    print("  -n, --name NAME    \tset file name (default=newOne)", end="\r\n")

def writeInFile(string : str):
    output = "./"
    name = "newOne"
    length = len(sys.argv) - 1
    for i in range(1, length):
        if sys.argv[i - 1] == "-o" or sys.argv[i - 1] == "--output":
            output = sys.argv[i]
        if sys.argv[i - 1] == "-n" or sys.argv[i - 1] == "--name":
            name = sys.argv[i]
    f = open(output+name+".txt", "w")
    f.write(string)
    f.close()

def writeSection():
    length = len(sys.argv) - 1
    if length % 2 != 0:
        exit(84)
    print("Type the text: ", end='\r\n\t')
    text = getUserText()
    string = getTxtImg(text)
    writeInFile(string)

def getFileSize(string : str):
    count = 0
    while string[count] != 'x':
        count += 1
    count += 1
    height = int(string[:count - 1])
    string = string[count:]
    count = len(string) - 1
    while string[count] != 'x':
        count -= 1
    width = int(string[count + 1: len(string)])
    string = string[:count]
    return (width, height, string)

def getFirstRGB(string : str):
    r = string[1:4]
    g = string[5:8]
    b = string[9:12]
    test = (int(r), int(g), int(b))
    return test

def readSection():
    readname = ""
    output = "./"
    name = "decripted"
    for i in range(0, len(sys.argv)):
        if sys.argv[i - 1] == "-r" or sys.argv[i - 1] == "--read":
            readname = sys.argv[i]
        if sys.argv[i - 1] == "-o" or sys.argv[i - 1] == "--output":
            output = sys.argv[i]
        if sys.argv[i - 1] == "-n" or sys.argv[i - 1] == "--name":
            name = sys.argv[i]
    if readname == "":
        exit(84)
    f = open(readname, 'r')
    string = f.read()
    width, height, string = getFileSize(string)
    img = Image.new('RGB', (width, height), color='white')
    pix = img.load()
    for i in range(0, height):
        for j in range(0, width):
            pix[j, i] = getFirstRGB(string)
            string = string[12:]
    img.save(output + name + ".png")

def main():
    random.seed(None)
    if "--help" in sys.argv or "-h" in sys.argv:
        helpSection()
        exit(0)
    if not("-r" in sys.argv or "--read" in sys.argv):
        writeSection()
    else:
        readSection()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    main()