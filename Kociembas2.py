import tkinter as tk
import kociemba

# Definimos los colores para el cubo de Rubik y su mapeo a notación Kociemba
colores = ['white', 'red', 'blue', 'orange', 'green', 'yellow']
color_map = {
    'white': 'U',
    'red': 'R',
    'blue': 'F',
    'orange': 'L',
    'green': 'B',
    'yellow': 'D'
}

# Matriz para almacenar los colores actuales de cada casilla
estado_cubo = {
    'top': [[None]*3 for _ in range(3)],
    'left': [[None]*3 for _ in range(3)],
    'front': [[None]*3 for _ in range(3)],
    'right': [[None]*3 for _ in range(3)],
    'back': [[None]*3 for _ in range(3)],
    'bottom': [[None]*3 for _ in range(3)]
}

def rotar_color(event, cara, i, j):
    """Función para rotar el color de una casilla al hacer clic"""
    color_actual = event.widget.cget("bg")
    indice_actual = colores.index(color_actual)
    indice_siguiente = (indice_actual + 1) % len(colores)
    nuevo_color = colores[indice_siguiente]
    event.widget.config(bg=nuevo_color)
    estado_cubo[cara][i][j] = nuevo_color

def crear_cara(canvas, x_offset, y_offset, color, cara_key):
    """Crea una cara del cubo en la interfaz gráfica"""
    for i in range(3):
        for j in range(3):
            cell = tk.Frame(
                master=canvas,
                width=30,
                height=30,
                bg=color,
                borderwidth=1,
                relief="solid"
            )
            cell.grid(row=i, column=j)
            cell.place(x=x_offset + j*32, y=y_offset + i*32)
            estado_cubo[cara_key][i][j] = color
            cell.bind("<Button-1>", lambda event, cara=cara_key, x=i, y=j: rotar_color(event, cara, x, y))

def generar_cadena_kociemba():
    """Convierte el estado actual del cubo a notación Kociemba"""
    # Mapeo de caras a posiciones en la cadena Kociemba
    orden_caras = ['top', 'right', 'front', 'bottom', 'left', 'back']
    cadena = ""
    
    for cara in orden_caras:
        for fila in estado_cubo[cara]:
            for color in fila:
                cadena += color_map[color]
    
    return cadena

def resolver_cubo():
    """Resuelve el cubo usando el algoritmo de Kociemba"""
    cadena = generar_cadena_kociemba()
    
    try:
        if cadena == 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
            resultado.set("El cubo ya está resuelto!")
        else:
            solucion = kociemba.solve(cadena)
            resultado.set(f"Solución: {solucion}")
    except Exception as e:
        resultado.set(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Cubo de Rubik con Solucionador Kociemba")
    root.geometry("500x450")

    canvas = tk.Canvas(root, width=500, height=400)
    canvas.pack()

    # Definimos offsets y etiquetamos cada cara
    cara_info = {
        'top': (150, 50),
        'left': (50, 150),
        'front': (150, 150),
        'right': (250, 150),
        'back': (350, 150),
        'bottom': (150, 250)
    }
    colores_iniciales = ['white', 'red', 'blue', 'orange', 'green', 'yellow']

    # Creamos las caras del cubo
    for cara_key, (x_offset, y_offset) in zip(cara_info, cara_info.values()):
        crear_cara(canvas, x_offset, y_offset, colores_iniciales.pop(0), cara_key)

    # Botón para resolver
    boton_resolver = tk.Button(root, text="Resolver Cubo", command=resolver_cubo)
    boton_resolver.pack(pady=5)

    # Etiqueta para mostrar resultados
    global resultado
    resultado = tk.StringVar()
    etiqueta_resultado = tk.Label(root, textvariable=resultado, wraplength=400)
    etiqueta_resultado.pack()

    root.mainloop()

if __name__ == "__main__":
    main()