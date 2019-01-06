CARDIAC
=======

Implementation of the CARDboard Illustrative Aid to Computation (see 
https://en.wikipedia.org/wiki/CARDboard_Illustrative_Aid_to_Computation).

This implementation leans heavily on the work of Kevin Veroneau (see 
http://www.pythondiary.com/blog/Oct.15,2014/building-cpu-simulator-python.html) 
and the information found on https://www.cs.drexel.edu/~bls96/museum/cardiac.html.

The assembler provided is quite basic, but operational. Assembly code is expected to use
a 4-column format, with any number of whitespace used as seperator. The columns are as follows:

- Label for the memory location (optional), allowing it to be identified by name, rather than by address.
- Instruction name or DATA
- Operand (either numeric value or a label)
- Comment (optional)

Sample code
-----------

- count1.asm: simple upcounter, adapted from https://www.cs.drexel.edu/~bls96/museum/cardiac.html
- count2.asm: my own upcounter implementation

