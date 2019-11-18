import os
import re

currMem = 16
compCode = {'0':'101010', '1':'111111', '-1':"111010", 'D':'001100', 'A':'110000', 'M':'110000',
                        '!D':'001101', '!A':'110001', '!M':'110001', '-D':'001111', '-A':'110011', '-M':'110011',
                        'D+1':'011111', 'A+1':'110111', 'M+1':'110111', 'D-1':'001110', 'A-1':'110010',
                        'M-1':'110010', 'D+A':'000010', 'D+M':'000010', 'D-A':'000010', 'D-M':'000010',
                        'A-D':'000111', 'M-D':'000111', 'D&A':'000000', 'D&M':'000000', 'D|A':'010101',
                        'D|M':'010101'}
jumpCode = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
predefVar = {'R0':'0', 'R1':'1', 'R2':'2', 'R3':'3', 'R4':'4', 'R5':'5', 'R6':'6', 'R7':'7', 'R8':'8', 'R9':'9', 'R10':'10', 'R11':'11', 'R12':'12', 'R13':'13', 'R14':'14', 'R15':'15'}

def validASM_file(f):                             #Function to check the correct file extension 
    if f.split('.')[-1] != 'asm':
        return False
    return True

def clean(code):                                  #Function to remove all kinds of empty spaces, like new lines and spaces 
    newCode = []
    for i in range(len(code)):
        code[i] = code[i].strip('\n')
        code[i] = code[i].strip(' ')
        if code[i] and not (code[i][0] == '/' and code[i][1] == '/'):
            newCode.append(code[i])
    return newCode

def symbolPass(code):                             #First pass to fill the symbol table
    table = dict()
    line = 0
    label = re.compile(r"^\(\w*\)$")
    for i in code:
        if i in predefVar:
            table[i[:][:]] = i[1:] 
        elif label.match(i):
            table[i[1:][:-1]] = line
        else:
            line += 1
    return table

def get15Bin(num):
    return ('0'*15 + bin(int(num))[2:])[-15:]

def AInstr(line,sym):                             #Function to translate the A instruction
    global currMem
    hackIn = '0'
    tempLine = line[1:]
    if tempLine.isdigit():
        hackIn += get15Bin(tempLine)
    elif tempLine in sym:
        hackIn += get15Bin(sym[tempLine])
    else:
        sym[tempLine] = currMem
        currMem += 1
        hackIn += get15Bin(sym[tempLine])
    return hackIn

def checkDest(temp):
    temp=temp.strip(' ')
    if temp in ["A","M","D","AM","AD","MD","AMD"]:
        return temp
    elif temp == '':
        return 'null'
    else:
        return None

def checkComp(temp):
    temp=temp.strip(' ')
    if temp in ["0","1","-1","D","A","!D","!A","-D","-A","D+1","A+1","D-1","A-1","D-A","A-D","M","!M","-M","M+1",
                        "M-1","D-M","M-D"]:
        return temp
    elif temp in ["D+A","A+D"]:
        return "D+A"
    elif temp in ["D|A","A|D"]:
        return "D|A"
    elif temp in ["D&A","A&D"]:
        return "D&A"
    elif temp in ["D+M","M+D"]:
        return "D+M"
    elif temp in ["D&M","M&D"]:
        return "D&M"
    elif temp in ["D|M","M|D"]:
        return "D|M"
    else:
        return None

def checkJump(temp):
    if temp.strip(' ') in ['','JGT','JEQ','JGE','JLT','JNE','JLE','JMP']:
        return temp.strip(' ')
    return None

def destCode(dest):
    if dest == 'null':
        return '000'
    st = ''
    for i in 'ADM':
        if i in dest:
            st += '1'
        else:
            st += '0'
    return st
    

def getC(dest,comp,jump):
    hackIn = '111'
    if 'M' in comp:
        hackIn += '1'
    else:
        hackIn += '0'
    hackIn += compCode[comp]
    hackIn += destCode(dest)
    hackIn += jumpCode[jump]
    return hackIn
    

def CInstr(line):
    dest = 'null'
    comp = ''
    jump = 'null'
    line += '\n'

    i = 0
    p = 1
    temp = ''                                           #To keep parts of the C instruction for translation
    while i <len(line):
        
        if line[i] == '=':
            if p != 1 or temp == '':
                raise SyntaxError("Invalid =")
            else:
                dest = checkDest(temp)
                if not dest:
                    raise SyntaxError("Invalid Destination "+temp)
                p = 2
                temp = ''
                
        elif line[i] == ';':
            if p != 1 and p != 2 or temp == '':
                raise SyntaxError('Invalid ;')
            else:
                comp = checkComp(temp)
                if not comp:
                    raise SyntaxError('Invalid Operation')
                p = 3
                temp = ''
                
        elif line[i] == '\n':
            if p == 1 or p == 2:
                comp = checkComp(temp)
                if not comp:
                    raise SyntaxError('Invalid Operation')
            elif p == 3:
                jump = checkJump(temp)
                if not jump:
                    raise SyntaxError('Invalid Jump Code')
                temp = ''

        elif line[i] != ' ':
            temp += line[i]
        i += 1
    return getC(dest,comp,jump)
        

def translate(code,sym):
    global currMem
    hack = []
    label = re.compile(r"^\(\w*\)$")
    currMem = 16
    for i in code:
        if i[0] == '@':
            hack.append(AInstr(i,sym))
            print(hack[-1])
        elif label.match(i):
            pass
        else:
            hack.append(CInstr(i))
            print(hack[-1])
    return hack

def assemble(f):
    if not validASM_file(f):
        print("Invalid file extension")
        return
    f1 = open(f,'r')
    code = f1.readlines()
    f1.close()
    code = clean(code)
    #print(code)
    translationTable = symbolPass(code)
    #print(translationTable)
    hack = translate(code,translationTable)
    nm = '.'.join(f.split('.')[:-1] + ['hack'])
    f1 = open(nm,'w')
    f1.write('\n'.join(hack))
    f1.close()

fname = input("Enter File Name(.asm): ").strip()
assemble(fname)
