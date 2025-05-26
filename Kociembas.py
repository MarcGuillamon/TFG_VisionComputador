# Kociemba es un algoritmo para resolver el cubo de Rubik en Python
import kociemba

#So, for example, a definition of a solved cube would be --> UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB

# Define la secuencia desordenada del cubo de Rubik usando la notación estándar (FRUBLD)
#scrambled_cube = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
#scrambled_cube = 'DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD'
scrambled_cube = 'DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL'

# Utiliza el algoritmo de Kociemba para resolver la secuencia
if scrambled_cube == 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
    print("El cubo ya está resuelto!")
else:
    solution = kociemba.solve(scrambled_cube)
    print("Solucion:", solution)