import tkinter as tk

# Definimos los colores para el cubo de Rubik
colores = ['white', 'red', 'blue', 'orange', 'green', 'yellow']

# Matriz para almacenar los colores actuales de cada casilla
estado_cubo = {
    'top': [[None]*3 for _ in range(3)],
    'left': [[None]*3 for _ in range(3)],
    'front': [[None]*3 for _ in range(3)],
    'right': [[None]*3 for _ in range(3)],
    'back': [[None]*3 for _ in range(3)],
    'bottom': [[None]*3 for _ in range(3)]
}

# Función para rotar el color
def rotar_color(event, cara, i, j):
    # Obtener el color actual del cuadro que ha sido clickeado
    color_actual = event.widget.cget("bg")
    # Obtener el siguiente color en la lista de colores
    indice_actual = colores.index(color_actual)
    indice_siguiente = (indice_actual + 1) % len(colores)
    nuevo_color = colores[indice_siguiente]
    # Cambiar el color de fondo del cuadro al siguiente color
    event.widget.config(bg=nuevo_color)
    # Actualizar la matriz de estado
    estado_cubo[cara][i][j] = nuevo_color
    print(estado_cubo)  # Para comprobar el estado actual de toda la matriz

def crear_cara(canvas, x_offset, y_offset, color, cara_key):
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
            # Inicializar la matriz de estado
            estado_cubo[cara_key][i][j] = color
            # Asociamos el evento de clic a la función rotar_color con parámetros adicionales
            cell.bind("<Button-1>", lambda event, cara=cara_key, x=i, y=j: rotar_color(event, cara, x, y))

def main():
    root = tk.Tk()
    root.title("Cubo de Rubik")
    root.geometry("500x400")

    # Creamos un Canvas para contener todas las caras del cubo
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

    root.mainloop()

if __name__ == "__main__":
    main()