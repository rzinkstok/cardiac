# Insert sort
# -----------

# Numeric primitives
zero    DATA    000
one     DATA    001

# Array
N       DATA    010
arr     DATA    010
        DATA    009
        DATA    008
        DATA    007
        DATA    006
        DATA    005
        DATA    004
        DATA    003
        DATA    002
        DATA    001
storer  DATA    606
loader  DATA    106

# Counters etc
cntr    DATA    000
index   DATA    000
acc     DATA    000

# Swapping variables
swap1   DATA    001
swap2   DATA    008
swtmp1  DATA    000
swtmp2  DATA    000

# Program
        JMP     arrout
        HRS     00

# Load from array subroutine
aload   CLA     99
        STO     alexit
        CLA     loader
        ADD     index
        STO     doload
doload  CLA     00
alexit  JMP     00

# Store to array subroutine
astore  STO     acc
        CLA     99
        STO     asexit
        CLA     storer
        ADD     index
        STO     dostore
        CLA     acc
dostore STO     00
asexit  JMP     00

# Swap locations subroutine
swap    CLA     99
        STO     swexit

        CLA     swap1
        STO     index
        JMP     aload
        STO     swtmp1
        OUT     swap1

        CLA     swap2
        STO     index
        JMP     aload
        STO     swtmp2
        OUT     swap2

        CLA     swap1
        STO     index
        CLA     swtmp2
        JMP     astore
        OUT     swap1

        CLA     swap2
        STO     index
        CLA     swtmp1
        JMP     astore
        OUT     swap2
swexit  JMP     00

# Output array subroutine
arrout  CLA     99
        STO     aoexit
        CLA     N
        SUB     one
        STO     cntr
        CLA     cntr
aoloop  TAC     aoexit
        SUB     one
        STO     cntr
        JMP     aload
        STO     acc
        OUT     acc
        CLA     index
        ADD     one
        STO     index
        CLA     cntr
        TAC     aoexit
        JMP     aoloop
aoexit  JMP     00