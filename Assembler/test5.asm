//Stack pointer is R0
//R1 holds initial n value
//When function is called top of stack is n, second element is return address
//When the function returns, top of stack is the value of fib(n)

@100
D=A
@R0
M=D

@START
0;JMP

(FIB)
	@R0
	M=M-1
	A=M
	D=M
	@n
	M=D
	
	@R0
	M=M-1
	A=M
	D=M
	@ret
	M=D
	
	@n
	D=M
	@ZERO_ONE
	D;JEQ
	@ZERO_ONE
	D=D-1;JEQ
	
	//Recursion
	
	@ret
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@n
	M=M-1
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@RET1
	D=A
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@n
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@FIB
	0;JMP
	(RET1)
	
	@R0
	M=M-1
	A=M
	D=M
	@temp
	M=D
	
	@R0
	M=M-1
	A=M
	M=M-1
	D=M
	@n
	M=D
	@R0
	M=M+1
	
	@temp
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@RET2
	D=A
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@n
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@FIB
	0;JMP
	(RET2)
	
	@R0
	M=M-1
	A=M
	D=M
	
	@R0
	M=M-1
	A=M
	D=M+D
	@temp
	M=D
	
	@R0
	M=M-1
	
	@R0
	M=M-1
	A=M
	D=M
	@ret
	M=D
	
	@temp
	D=M
	@R0
	A=M
	M=D
	@R0
	M=M+1
	
	@END_FN
	0;JMP
	
	//Recursion End
	
	(ZERO_ONE)
	@R0
	A=M
	M=1
	@R0
	M=M+1
	
	(END_FN)
	@ret
	A=M
	0;JMP
	

(START)
@FUNCTION_RETURN
D=A
@R0
A=M
M=D
@R0
M=M+1

@R1
D=M
@R0
A=M
M=D
@R0
M=M+1

@FIB
0;JMP
(FUNCTION_RETURN)

@R0
M=M-1
A=M
D=M
@R2
M=D

(END)
@END
0;JMP
