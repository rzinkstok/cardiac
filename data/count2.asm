start   DATA    4           Start counting at
stop    DATA    200         Stop counting at
incr    DATA    10          Increment
res     DATA    0           Output buffer

        CLA     start       Load start number
        SUB     stop        Subtract end

loop    ADD     stop        Add end
        STO     res         Store for output
        OUT     res
        ADD     incr        Add increment
        SUB     stop        Subtract end
        TAC     loop        Check if (current number - end) < 0

        HRS     0