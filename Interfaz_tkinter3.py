import tkinter as tk
import time

class RubikGUI:
    def __init__(self, solved_sides):
        self.solved_sides = solved_sides  # Referencia al diccionario compartido
        
        self.colores = ['white', 'orange', 'green', 'red', 'blue', 'yellow']
        self.estado_cubo = {
            'U': [[None]*3 for _ in range(3)],
            'L': [[None]*3 for _ in range(3)],
            'F': [[None]*3 for _ in range(3)],
            'R': [[None]*3 for _ in range(3)],
            'B': [[None]*3 for _ in range(3)],
            'D': [[None]*3 for _ in range(3)]
        }
        self.root = tk.Tk()
        self.root.title("Cubo de Rubik")
        self.root.geometry("500x400")
        self.canvas = tk.Canvas(self.root, width=500, height=400)
        self.canvas.pack()
        
        # Mapeo de caras a posiciones y colores iniciales (solo centro)
        self.cara_info = {
            'U': (150, 50, 'white'),
            'L': (50, 150, 'orange'),
            'F': (150, 150, 'green'),
            'R': (250, 150, 'red'),
            'B': (350, 150, 'blue'),
            'D': (150, 250, 'yellow')
        }
        
        self.inicializar_interfaz()

        self.ultima_actualizacion = time.time()
        self.verificar_cambios_activo = True
        self.programar_verificacion()

    def programar_verificacion(self):
        if self.verificar_cambios_activo:
            self.root.after(100, self.verificar_cambios)  # Verificar cada 100ms

    def verificar_cambios(self):
        """Verifica cambios en la GUI y actualiza solved_sides"""
        for cara in self.estado_cubo:
            # Convertir matriz de colores a string (ej: "WWWWWWWWW")
            nuevo_estado = []
            for i in range(3):
                for j in range(3):
                    color = self.estado_cubo[cara][i][j]
                    nuevo_estado.append(self.color_nombre_a_letra(color) if color else '?')
            
            nuevo_estado_str = ''.join(nuevo_estado)
        
        # Actualizar solo si hubo cambios    
        if self.solved_sides.get(cara, '') != nuevo_estado:
            self.solved_sides[cara] = nuevo_estado

    def detener_verificacion(self):
        self.verificar_cambios_activo = False
    
    def reset_cara(self, cara_key):
        """Resetea una cara a solo el centro visible"""
        x_offset, y_offset, color_centro = self.cara_info[cara_key]
        
        # Destruir todos los widgets de esta cara
        for widget in self.canvas.winfo_children():
            if isinstance(widget, tk.Frame):
                x_pos = widget.winfo_x()
                y_pos = widget.winfo_y()
                if (x_offset <= x_pos < x_offset + 96 and 
                    y_offset <= y_pos < y_offset + 96):
                    widget.destroy()
        
        # Recrear solo el centro
        self.estado_cubo[cara_key] = [[None]*3 for _ in range(3)]
        cell = tk.Frame(
            master=self.canvas,
            width=30,
            height=30,
            bg=color_centro,
            borderwidth=1,
            relief="solid"
        )
        cell.place(x=x_offset + 32, y=y_offset + 32)  # Posición del centro
        self.estado_cubo[cara_key][1][1] = color_centro
        cell.bind("<Button-1>", lambda e, c=cara_key, x=1, y=1: self.rotar_color(e, c, x, y))

    def rotar_color(self, event, cara, i, j):
        color_actual = event.widget.cget("bg")
        indice_actual = self.colores.index(color_actual)
        nuevo_color = self.colores[(indice_actual + 1) % len(self.colores)]
        event.widget.config(bg=nuevo_color)
        self.estado_cubo[cara][i][j] = nuevo_color

        # Actualizar solved_sides inmediatamente
        self.actualizar_solved_sides(cara)

        # Actualizar solved_sides compartido si es una cara completa
        if all(all(row) for row in self.estado_cubo[cara]):
            color_letras = []
            for row in self.estado_cubo[cara]:
                for color in row:
                    color_letras.append(self.color_letra_a_nombre(color))
            self.solved_sides[cara] = ''.join(color_letras)

    def actualizar_solved_sides(self, cara_key):
        """Actualiza solved_sides con los cambios de la GUI"""
        try:
            # Convertir matriz de colores a string (ej: "WWWWWWWWW")
            color_letras = []
            for i in range(3):
                for j in range(3):
                    color = self.estado_cubo[cara_key][i][j]
                    color_letras.append(self.color_nombre_a_letra(color) if color else '?')
            self.solved_sides[cara_key] = ''.join(color_letras)
        except Exception as e:
            print(f"Error actualizando solved_sides: {e}")
    
    def crear_cara(self, x_offset, y_offset, color_inicial, cara_key):
        # Solo creamos el centro inicialmente
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:  # Solo el centro
                    cell = tk.Frame(
                        master=self.canvas,
                        width=30,
                        height=30,
                        bg=color_inicial,
                        borderwidth=1,
                        relief="solid"
                    )
                    cell.grid(row=i, column=j)
                    cell.place(x=x_offset + j*32, y=y_offset + i*32)
                    self.estado_cubo[cara_key][i][j] = color_inicial
                    cell.bind("<Button-1>", lambda e, c=cara_key, x=i, y=j: self.rotar_color(e, c, x, y))
                else:
                    # Celda vacía inicialmente
                    self.estado_cubo[cara_key][i][j] = None
    
    def actualizar_cara(self, cara_key, colors):
        """Actualiza una cara completa con los colores detectados"""
        x_offset, y_offset, _ = self.cara_info[cara_key]
        
        # Limpiar cara existente
        for widget in self.canvas.winfo_children():
            if isinstance(widget, tk.Frame):
                # Verificar si el widget pertenece a esta cara
                x_pos = widget.winfo_x()
                y_pos = widget.winfo_y()
                if (x_offset <= x_pos < x_offset + 96 and 
                    y_offset <= y_pos < y_offset + 96):
                    widget.destroy()
        
        # Crear nueva cara completa
        for i in range(3):
            for j in range(3):
                color = self.color_letra_a_nombre(colors[i*3 + j])
                cell = tk.Frame(
                    master=self.canvas,
                    width=30,
                    height=30,
                    bg=color,
                    borderwidth=1,
                    relief="solid"
                )
                #cell.grid(row=i, column=j)
                cell.place(x=x_offset + j*32, y=y_offset + i*32)
                self.estado_cubo[cara_key][i][j] = color
                cell.bind("<Button-1>", lambda e, c=cara_key, x=i, y=j: self.rotar_color(e, c, x, y))
    
    def color_letra_a_nombre(self, nombre_color):
        """Convierte W, R, etc. a nombres de color"""
        mapeo = {
            'W': 'white',
            'O': 'orange',
            'G': 'green',
            'R': 'red',
            'B': 'blue',
            'Y': 'yellow'
        }
        return mapeo.get(nombre_color, '?')  # Gris para desconocido
    
    def color_nombre_a_letra(self, nombre_color):
        """Convierte nombres de color a letras (W, R, etc.)"""
        mapeo = {
            'white': 'W',
            'orange': 'O',
            'green': 'G',
            'red': 'R',
            'blue': 'B',
            'yellow': 'Y'
        }
        return mapeo.get(nombre_color, '?')
    
    def inicializar_interfaz(self):
        """Inicializa la interfaz con solo los centros visibles"""
        for cara_key, (x, y, color) in self.cara_info.items():
            self.crear_cara(x, y, color, cara_key)
    
    def run(self):
        self.root.mainloop()

    def actualizar_cara_segura(self, cara_key, colors):
        """Método seguro para actualizar desde otros hilos"""
        def actualizar():
            self.actualizar_cara(cara_key, colors)
        self.root.after(0, actualizar)  # Programar la actualización en el hilo principal

    
def mostrar_interfaz():
    gui = RubikGUI()
    gui.run()
    return gui