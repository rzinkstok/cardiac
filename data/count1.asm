n       DATA    009
cntr    DATA    000

        CLA	    00	    Initialize the counter
        STO	    cntr
loop	CLA	    n	    If n < 0, exit
        TAC	    exit
        OUT	    cntr	Output a card
        CLA	    cntr	Increment the card
        ADD	    00
        STO	    cntr
        CLA	    n	    Decrement n
        SUB	    00
        STO	    n
        JMP	    loop
exit	HRS	    00