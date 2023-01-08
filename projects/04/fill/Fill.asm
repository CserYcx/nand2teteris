// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @SCREEN
    D=A
    @addr
    M=D         //addr = 16384
    @i
    M=0         //i=0
    @j
    M=0         //j=0
(END)
    @24576
    D=M         // keyboard's value
    @LOOP1
    D;JGT       // keyborad is pressed, jump to loop
    @END
    D;JEQ
(LOOP1)
    @j
    M=0
    @i          //17
    D=M
    @8096
    D=D-A
    M=D
    @32
    D=A
    @i
    M=M+D       //i = i+32
    @8096
    D=M
    @END
    D;JGE       // if i >=8092, end the loop
    @LOOP2
    D;JLT
(LOOP2)
    @j          //18
    D=M
    @32
    D=D-A
    @LOOP1
    D;JGE       //if j>=32, back to the LOOP1
    @addr
    A=M
    M=-1        // addr[index] = -1
    D=0
    @j
    M=M+1       //j = j+1
    @j
    D=D+M
    @32
    D=A
    @addr       // 16
    M=M+1       //index = index  + 1(you can look the j like the 1)
    @LOOP2
    0;JMP

    