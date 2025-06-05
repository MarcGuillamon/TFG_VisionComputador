#CADENA = "D2 L' D' L2 U R2 F B L B D' B2 R2 U' R2 U' F2 R2 U' L2"
CADENA = "U D D' U2 U2 D2 F B U R' D2 B B2 F' R' L2 L R' L L L"
print("Cadena original:", CADENA)

print("\nCaracteres secuenciales separados:")

# Definimos pares de movimientos opuestos
opuestos = [{'U', 'D'}, {'F', 'B'}, {'R', 'L'}]
i = 0
n = len(CADENA)

while i < n:
    if CADENA[i] == ' ':  # Saltamos espacios
        i += 1
        continue
        
    if CADENA[i] in ['U', 'D', 'F', 'B', 'R', 'L']:
        # Obtenemos el primer movimiento
        mov1 = CADENA[i]
        if i+1 < n and CADENA[i+1] in ["'", "2"]:
            mov1 += CADENA[i+1]
            i += 1
        
        # Verificamos si hay un movimiento opuesto después
        j = i + 1
        # Saltamos espacios
        while j < n and CADENA[j] == ' ':
            j += 1
            
        if j < n and CADENA[j] in ['U', 'D', 'F', 'B', 'R', 'L']:
            # Obtenemos el segundo movimiento
            mov2 = CADENA[j]
            if j+1 < n and CADENA[j+1] in ["'", "2"]:
                mov2 += CADENA[j+1]
                j += 1
            
            # Comprobamos si son opuestos
            for par in opuestos:
                if {mov1[0], mov2[0]} == par:
                    print(f"{mov1}{mov2}")  # Movimientos opuestos combinados
                    i = j + 1
                    break
            else:
                print(mov1)  # Movimiento individual
                i += 1
        else:
            print(mov1)  # Movimiento individual
            i += 1
    else:
        i += 1