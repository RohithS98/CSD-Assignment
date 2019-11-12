import os
import re

loc = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}

def validVM(f):
    if f.split('.')[-1] != 'vm':
        return False
    return True

def clean(code):
    newCode = []
    for i in range(len(code)):
        code[i] = code[i].strip('\n')
        code[i] = code[i].strip(' ')
        if code[i] and not (code[i][0] == '/' and code[i][1] == '/'):
            newCode.append(code[i])
    return newCode

def emitSPAdj(adj):
    return ['@SP','M=M-1' if adj < 0 else 'M=M+1']

def getAddr(instr):
    if instr[1] != 'temp':
        return ['@'+loc[instr[1]],'D=M','@'+instr[2],'D=D+A']
    return ['@'+str(int(instr[2])+5),'D=A']

def emitMemInst(instr):
    code = []
    if instr[0] == 'pop':
        code.extend(emitSPAdj(-1))
    if instr[1] in ['local','argument','this','that','temp']:
        code.extend(getAddr(instr))
        if instr[0] == 'pop':
            code.extend(['@R13','M=D','@SP','A=M','D=M','@R13','A=M','M=D'])
        else:
            code.extend(['A=D','D=M','@SP','A=M','M=D'])
            code.extend(emitSPAdj(1))
        return code
    elif instr[1] == 'constant':
        code.append('@'+instr[2]+'\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1')
        return code
    elif instr[1] == 'pointer':
        target = 'THIS' if instr[2] == '0' else 'THAT'
        if instr[0] == 'pop':
            code.extend(['@SP\nA=M\nD=M\n@'+target,"A=M\nM=D"])
        else:
            code.extend(['@'+target,"A=M\nD=M",'@SP\nA=M\nM=D'])
            code.extend(emitSPAdj(1))
        return code

def emitBinInst(instr):
    code = ['@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n']

def convert(code):
    newCode = []
    for i in code:
        instr = i.split(' ')
        if instr[0] == 'push' or instr[0] == 'pop':
            newCode.extend(emitMemInst(instr))
        elif instr[0] in ['add','sub','eq','get','lt','and','or']:
            newCode.extend(emitBinInst(instr))
        elif instr[0] in ['neg','not']:
            
    return newCode
        

def translate(f):
    if not validVM(f):
        print("Invalid file extension")
        return
    f1 = open(f,'r')
    code = f1.readlines()
    f1.close()
    code = clean(code)

    asm = convert(code)
    
    nm = '.'.join(f.split('.')[:-1] + ['asm'])
    f1 = open(nm,'w')
    f1.write('\n'.join(asm))
    f1.close()

fname = input("Enter File Name(.vm): ").strip()
translate(fname)
