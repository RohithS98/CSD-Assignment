@256
D=A
@SP
M=D
@main
0;JMP

(mult)
@SP
A=M

M=0
A=A+1
M=0
A=A+1

D=A
@SP
M=D


@0
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

@1
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

(Loop)

@LCL
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
A=A-1
D=M-D
@GTt0
D;JGT
@SP
A=M-1
M=0
@GTe0
0;JMP
(GTt0)
@SP
A=M-1
M=-1
(GTe0)

@SP
AM=M-1
D=M
@END
D;JNE

@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
A=A-1
M=D+M

@SP
M=M-1
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

@LCL
D=M
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
A=A-1
M=D+M

@SP
M=M-1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
A=M
D=M
@R13
A=M
M=D

@LOOP
0;JMP

(END)

@LCL
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@5
A=D-A
D=M
@R13
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D

D=A+1
@SP
M=D

@LCL
AM=M-1
D=M
@THAT
M=D
@LCL
AM=M-1
D=M
@THIS
M=D
@LCL
AM=M-1
D=M
@ARG
M=D
@LCL
A=M-1
D=M
@LCL
M=D
@R13
A=M
0;JMP

(main)
@SP
A=M


D=A
@SP
M=D


@3
D=A
@SP
A=M
M=D
@SP
M=M+1

@8
D=A
@SP
A=M
M=D
@SP
M=M+1

@5
D=A
@SP
A=M
M=D
@SP
M=M+1

@SP
D=M
@R13
M=D
@RET1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@R13
D=M
@2
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@mult
0;JMP
(RET1)

@SP
AM=M-1
D=M
A=A-1
M=D+M

@LCL
D=M
@5
A=D-A
D=M
@R13
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D

D=A+1
@SP
M=D

@LCL
AM=M-1
D=M
@THAT
M=D
@LCL
AM=M-1
D=M
@THIS
M=D
@LCL
AM=M-1
D=M
@ARG
M=D
@LCL
A=M-1
D=M
@LCL
M=D
@R13
A=M
0;JMP

(ENDOFCODE)
@ENDOFCODE
0;JMP