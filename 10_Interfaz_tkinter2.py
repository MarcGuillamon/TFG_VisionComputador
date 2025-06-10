import tkinter as tk

# Definimos los colores para el cubo de Rubik
colores = ['white', 'orange', 'green', 'red', 'blue', 'yellow']

def rotar_color(event):
    # Obtener el color actual del cuadro que ha sido clickeado
    color_actual = event.widget.cget("bg")
    # Obtener el siguiente color en la lista de colores
    indice_actual = colores.index(color_actual)
    indice_siguiente = (indice_actual + 1) % len(colores)
    # Cambiar el color de fondo del cuadro al siguiente color
    event.widget.config(bg=colores[indice_siguiente])

def crear_cara(canvas, x_offset, y_offset, color):
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
            # Asociamos el evento de clic a la función rotar_color
            cell.bind("<Button-1>", rotar_color)

def main():
    root = tk.Tk()
    root.title("Cubo de Rubik")
    root.geometry("500x400")

    # Creamos un Canvas para contener todas las caras del cubo
    canvas = tk.Canvas(root, width=500, height=400)
    canvas.pack()

    # Definimos offsets para posicionar cada cara
    offsets = [(150, 50), (50, 150), (150, 150), (250, 150), (350, 150), (150, 250)]

    # Creamos las caras del cubo
    for (color, (x_offset, y_offset)) in zip(colores, offsets):
        crear_cara(canvas, x_offset, y_offset, color)

    root.mainloop()

if __name__ == "__main__":
    main()