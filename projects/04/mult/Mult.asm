// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

    @i 
    M = 0      // i = 0
    @2
    M = 0      // sum = 0
(LOOP)
    @i
    D = M
    @1
    D = M-D    // whether i < R1
    @END
    D;JEQ
    @i
    M = M+1    //i = i++
    @0
    D = M      //R0's value
    @2
    M = M+D    // R2 = R0+ nth(R1) ......+R0
    @LOOP
    0;JMP      //Back to loop
(END)
    @END
    0;JMP      //Infinite loop