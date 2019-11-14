import os
import re

labelCount = 1
loc = {'local':'LCL', 'argument':'ARG', 'this':'THIS', 'that':'THAT'}
instruction = {'add':'M=D+M', 'sub':'M=D-M', 'and':'M=D&M', 'or':'M=D|M'}
cond = {'gt':'GT', 'eq':'EQ', 'lt':'LT'}
jumpCode = {'gt':'JGT', 'eq':'JEQ', 'lt':'JLT'}

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

def emitMemInst(instr,name):
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
    elif instr[1] == 'static':
        if instr[0] == 'pop':
            code.extend(['A=M\nD=M\n@'+name+'.'+instr[2]+'\nM=D'])
        else:
            code.extend(['@'+name+'.'+instr[2]+'\nD=M\n@SP\nA=M\nM=D'])
            code.extend(emitSPAdj(1))
        return code

def emitBinInst(instr):
    return ['@SP\nAM=M-1\nD=M\nA=A-1', instruction[instr[0]]]

def emitUnInst(instr):
    return ['@SP\nA=M-1', 'M=-M' if instr[0] == 'neg' else 'M=!M']

def emitComp(instr):
    global labelCount
    lab, jmp = cond[instr[0]], jumpCode[instr[0]]
    code = ['@SP\nAM=M-1\nD=M\nA=A-1\nD=M-D']
    code.append('@'+lab+'t'+str(labelCount)+'\nD;'+jmp+'\n@SP\nA=M-1\nM=0\n@'+lab+'e'+str(labelCount)+
                          '\n0;JMP\n('+lab+'t'+str(labelCount)+')\n@SP\nA=M-1\nM=-1\n('+lab+'e'+str(labelCount)+')')
    labelCount += 1
    return code

def emitGoto(instr):
    return ['@'+instr[1],'0;JMP']

def emitIfGo(instr):
    return ['@SP\nAM=M-1\nD=M\n@'+instr[1],'D;JNE']

def convert(code,name):
    newCode = []
    for i in code:
        instr = i.split(' ')
        if instr[0] == 'push' or instr[0] == 'pop':
            newCode.extend(emitMemInst(instr,name))
        elif instr[0] in ['add','sub','and','or']:
            newCode.extend(emitBinInst(instr))
        elif instr[0] in ['neg','not']:
            newCode.extend(emitUnInst(instr))
        elif instr[0] in ['eq','gt','lt']:
            newCode.extend(emitComp(instr))
        elif instr[0] == 'label':
            newCode.append('('+instr[1]+')')
        elif instr[0] == 'goto':
            newCode.extend(emitGoto(instr))
        elif instr[0] == 'if-goto':
            newCode.extend(emitIfGo(instr))
        newCode.append('')
    return newCode
        

def translate(f):
    global labelCount
    labelCount = 0
    if not validVM(f):
        print("Invalid file extension")
        return
    name = '.'.join(f.split('.')[:-1])
    f1 = open(f,'r')
    code = f1.readlines()
    f1.close()
    code = clean(code)

    asm = convert(code,name)
    
    nm = '.'.join(f.split('.')[:-1] + ['asm'])
    f1 = open(nm,'w')
    f1.write('\n'.join(asm))
    f1.close()

fname = input("Enter File Name(.vm): ").strip()
translate(fname)
