A       DATA    021
B       DATA    014
result  DATA    000

        CLA     B           Reduce B by 1
        SUB     000
        STO     B

loop    CLA     B           Load B
        TAC     output      If < 0, go to output
        SUB     000         Subtract 1 and save
        STO     B
        CLA     result      Load result, add A and store
        ADD     A
        STO     result
        JMP     loop

output  OUT     result
        HRS     000