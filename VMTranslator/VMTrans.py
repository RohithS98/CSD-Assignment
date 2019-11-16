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

def emitFunction(instr):
    code = ['('+instr[1]+')\n@SP\nA=M\n']
    code.append('M=0\nA=A+1\n'*int(instr[2]))
    code.append('D=A\n@SP\nM=D\n')
    return code

#Store current SP in R13; Store return addr, LCL, ARG, THIS, THAT in stack. Store SP - n in ARG
#Store SP in LCL
def emitCall(instr):
    global labelCount
    code = ['@SP\nD=M\n@R13\nM=D\n@RET'+str(labelCount), 'D=A\n@SP\nA=M\nM=D']
    code.extend(emitSPAdj(1))
    for i in ['LCL','ARG','THIS','THAT']:
        code.append('@'+i+'\nD=M\n@SP\nA=M\nM=D')
        code.extend(emitSPAdj(1))
    code.append('@R13\nD=M\n@'+instr[2])
    code.append('D=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@'+instr[1])
    code.append('0;JMP\n(RET'+str(labelCount)+')')
    labelCount += 1
    return code

def emitReturn(instr):
    code = ['@LCL\nD=M\n@5\nA=D-A\nD=M\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n']
    code.append('D=A+1\n@SP\nM=D\n')
    for i in ['THAT', 'THIS', 'ARG']:
        code.append('@LCL\nAM=M-1\nD=M\n@'+i+'\nM=D')
    code.append('@LCL\nA=M-1\nD=M\n@LCL\nM=D\n@R13\nA=M\n0;JMP')
    return code

def emitStart():
    return ['@256\nD=A\n@SP\nM=D\n@main\n0;JMP']

def emitEnd():
    return ['(ENDOFCODE)\n@ENDOFCODE\n0;JMP']

def convert(code,name):
    newCode = []
    newCode.extend(emitStart())
    newCode.append('')
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
        elif instr[0] == 'function':
            newCode.extend(emitFunction(instr))
        elif instr[0] == 'call':
            newCode.extend(emitCall(instr))
        elif instr[0] == 'return':
            newCode.extend(emitReturn(instr))
        newCode.append('')
    newCode.extend(emitEnd())
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
    print('\n'.join(asm))
    f1 = open(nm,'w')
    f1.write('\n'.join(asm))
    f1.close()

fname = input("Enter File Name(.vm): ").strip()
translate(fname)
