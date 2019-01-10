# Insert sort
# -----------
# Simple implementation. Due to memory constraints, the maximum array length is 10.

# Input data
N       DATA    010     # Maximum value is 10!
arr     DATA    -131    # The data array
        DATA    -182
        DATA    438
        DATA    60
        DATA    10
        DATA    181
        DATA    -47
        DATA    711
        DATA    181
        DATA    299

# Data load/store commands
storer  DATA    604
loader  DATA    104

# Numeric primitives
zero    DATA    000

# Counters etc
i       DATA    000
cntr    DATA    000
index   DATA    000

# Swapping variables
swaddr1 DATA    001
swaddr2 DATA    008
swval1  DATA    000
swval2  DATA    000

# Main
loop1   CLA     i
        ADD     000     # Value of one
        SUB     N
        TAC     cont
        JMP     coda
cont    ADD     N
        STO     i
        STO     cntr
loop2   JMP     swdown
        CLA     cntr
        SUB     000     # Value of one
        STO     cntr
        TAC     loop1
        JMP     loop2
coda    JMP     arrout
        HRS     00

# Load from array subroutine
# Loads an array element to the accumulator
#
# Args:
#   index: the index of the array element to load

aload   CLA     99
        STO     alexit

        CLA     loader
        ADD     index
        STO     doload
doload  CLA     00

alexit  JMP     00

# Store to array subroutine
# Stores the value in the accumulator in an array element
#
# Args:
#   index: the index of the array element to store into

astore  STO     001     # Bootloader address free to use
        CLA     99
        STO     asexit

        CLA     storer
        ADD     index
        STO     dostore
        CLA     001     # Bootloader address free to use
dostore STO     00

asexit  JMP     00


# Single swap down subroutine
# Checks two adjacent array elements and swaps them if the left element is larger than the right element
#
# Args:
#   cntr: the index of the right array element
swdown  CLA     99
        STO     sdexit

        # Store the left array address and element
        CLA     cntr
        SUB     000     # Value of one
        TAC     sdexit  # If left array index < 0
        STO     swaddr1
        STO     index
        JMP     aload
        STO     swval1

        # Store the right array address and element
        CLA     cntr
        STO     swaddr2
        STO     index
        JMP     aload
        STO     swval2

        # Compare element values
        SUB     swval1
        TAC     doswap  # If left larger, swap
        JMP     sdexit

        # Write new left element
doswap  CLA     swaddr1
        STO     index
        CLA     swval2
        JMP     astore

        # Write new right element
        CLA     swaddr2
        STO     index
        CLA     swval1
        JMP     astore

sdexit  JMP     00


# Output array subroutine
# Outputs all array elements
#
arrout  CLA     99
        STO     aoexit

        # Start from zero
        CLA     zero
        STO     i

        # Loop over elements
aoloop  CLA     i
        SUB     N
        TAC     aocont
        JMP     aoexit
aocont  ADD     N
        STO     index
        ADD     000
        STO     i
        JMP     aload
        STO     001     # Bootloader address free to use
        OUT     001     # Bootloader address free to use
        JMP     aoloop

aoexit  JMP     00