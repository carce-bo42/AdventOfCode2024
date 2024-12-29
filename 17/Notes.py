# Its program is a list of 3-bit numbers (0-7) like 0,1,2,3
# Eight instructions, each identified by a 3-bit numbers, called instruction's opcode.
# Each instruction also reads the 3bit number after it as an input: its called its operand.

# 0,1,2,3
# instruction opcode 0, operand 1
# instrction opcode 2, operand 3
# Halt.

# Two types of operands: literal operand and combo operand.

# Each instruction specifies the type of its operand.
# The value of a literal operand is the operand itself.

# Combo operands 0 through 3 represent literal values 0 through 3.
# Combo operand 4 represents the value of register A.
# Combo operand 5 represents the value of register B.
# Combo operand 6 represents the value of register C.
# Combo operand 7 is reserved and will not appear in valid programs.

# opcodes:

# 0: adv -> division
## - Numerator is the value in the A register.
## - Denominator is found by raising 2**(combo operand), meaning if operand = (0,3) (2**0,2**3), but if operand == (4,6) => 2**A, 2**B, 2**C
## The result is truncated to an integer then written to the A register.

# 1: bxl -> bitwise B XOR (literal operand)
## - lhand B
## - rhand literal operand. (0,7) -> (0,7)
## Writes result to B register.

# 2 : bst -> calculates the value of its combo operand mod 8. (keeping only its lowest 3 bits)
## Writes result to B register.

# 3: jnz -> does NOTHING if A is 0.
## if A is not zero, it jumps by setting the instruction pointer to the value of its literal operand.
##

# 4: bxc -> XOR between B and C
## It IGNORES its operand
## Writes result to B.

# 5: out -> combo operand mod 8.
## Outputs the value.
## If a program outputs multiple values, they are separated by commas

# 6: bdv -> adv but with B.
## Divides A / combo operand, casts to int.
## Writes the result to B

# 7: cdv -> adv but with C
## Divides A / combo operand, casts to int.
## Writes the result to C


# Program:  2,4   1,1   7,5   0,3   1,4   4,4   5,5   3,0

# bst 4 --- rB = rA%8
# bxl 1 --- rB = rB ^ 1
# cdv 5 --- rC = rA >> rB
# adv 3 --- rA = rA >> 3
# bxl 4 --- rB = rB ^ rA
# bxc 4 --- rB = rB ^ rC
# out 5 --- print rB%8
# jnz 0 --- jump to 0 if rA != 0

# Lo que es seguro es que para cuando rA == 0.
# y rA se va dividiendo entre 8.
# tiene qe imprimir 16 numeros.
# Asi que como maximo A es 1*8**16 -1
# y como minimo A es 8**15
# 8**16 = 281474976710656
# 8**16 -1 = 281474976710655
# 8**15 = 35184372088832

# (0,100000) -> nada.
# (100001, 1000000) -> nada.
# (1000001, )

# Buscamos este output:
# 2,4,1,1,7,5,0,3,1,4,4,4,5,5,3,0

# Ojo
# rango 170000001000000 -> 1000000000

# Importante:
# Durante una iteracion del bucle, todos los valores derivan de
# forma directa de rA.
# rA solo depende de si misma, ya que se va dividiendo entre 8.
# rB se asigna a rA%8.
# rC se asigna a rA >> rB.
# Por lo que no es importante lo que valiesen rB y rC antes de
# empezar el bucle. No se acarrean valores anteriores.