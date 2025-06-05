# Kociemba es un algoritmo para resolver el cubo de Rubik en Python
import kociemba

# So, for example, a definition of a solved cube would be --> UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
# U --> WHITE
# R --> RED
# F --> GREEN
# D --> YELLOW
# L --> ORANGE
# B --> BLUE

""" |************|
    |*U1**U2**U3*|
    |************|
    |*U4**U5**U6*|
    |************|
    |*U7**U8**U9*|
    |************|"""

# Define la secuencia desordenada del cubo de Rubik usando la notación estándar (FRUBLD)
scrambled_cube = 'UUUUUUUUUFFFRRRRRRLLLFFFFFFDDDDDDDDDBBBLLLLLLRRRBBBBBB'   # EJEMPLO SIMPLE PARA ROTAR SOLO UNA CARA
#scrambled_cube = 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'
#scrambled_cube = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'

# Utiliza el algoritmo de Kociemba para resolver la secuencia
if scrambled_cube == 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
    print("El cubo ya está resuelto!")
else:
    solution = kociemba.solve(scrambled_cube)
    print("Solucion:", solution)