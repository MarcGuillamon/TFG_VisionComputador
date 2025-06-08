from ultralytics import YOLO
import logging

import numpy as np
import cv2
import time
from Kociembas2 import kociembas_algorithm

from Interfaz_tkinter3 import RubikGUI
import threading
import tkinter as tk

# Inicializar la GUI en un hilo separado
gui = None
solved_sides = {}  # Diccionario vacío al inicio
last_gui_check = time.time()    # Para verificar el tiempo GUI

if gui is not None: # Asegurarse de cerrar la GUI correctamente
    gui.root.quit()

def iniciar_interfaz():
    try:
        global gui
        gui = RubikGUI(solved_sides)  # Pasamos la referencia al diccionario
        gui.run()
    except Exception as e:
        print(f"Error al iniciar GUI: {e}")
        raise

# Iniciar la GUI en un hilo separado al principio del programa
threading.Thread(target=iniciar_interfaz, daemon=True).start()

# Esperar un momento para que la GUI se inicialice
time.sleep(0.5)

# Configuración inicial
model = YOLO('best.pt')
model.verbose = False  # Esto reduce algunos mensajes
logging.getLogger('ultralytics').setLevel(logging.WARNING)  # Silencia logs DEBUG e INFO

# Cargar la imagen
cap = cv2.VideoCapture(0)
color_history = []
stable_time_threshold = 2  # segundos
current_side = None
solved_sides = {}  # Almacenará las 6 caras (U, R, F, D, L, B)

# Funciones de detección de color (de 7.1_Detec_color.py)
area_size = 3  
half_size = area_size // 2

def get_dominant_color(frame, x, y):
    roi = frame[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
    if roi.size == 0:
        return None
    return np.mean(roi, axis=(0, 1)).astype(int)

def classify_color(bgr_color):
    if bgr_color is None:
        return "?"
    
    hsv = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv
    
    if s < 60:
        return "W" if v > 120 else "K"  # W: Blanco, K: Negro
    else:
        if h < 5 or h > 175: return "R"
        elif 5 <= h < 22: return "O"
        elif 22 <= h < 40: return "Y"
        elif 40 <= h < 78: return "G"
        elif 78 <= h < 131: return "B"
        else: return "?"

def convert_colors_to_kociemba_format(color_string):
    """
    Convierte los colores detectados (W,R,G,B,O,Y) al formato de posiciones (U,R,F,D,L,B)
    según el estándar de Kociemba:
    W -> U (Blanco/White -> Up)
    Y -> D (Amarillo/Yellow -> Down)
    R -> R (Rojo/Red -> Right)
    G -> F (Verde/Green -> Front)
    B -> B (Azul/Blue -> Back)
    O -> L (Naranja/Orange -> Left)
    """
    conversion_map = {
        'W': 'U',
        'Y': 'D',
        'R': 'R',
        'G': 'F',
        'B': 'B',
        'O': 'L'
    }
    return ''.join([conversion_map.get(c, '?') for c in color_string])

def save_side_colors(colors, position):
    """Guarda los colores detectados para una cara específica"""
    face_name = get_face_name(position)
    if face_name and len(colors) == 9:
        solved_sides[face_name] = "".join(colors)

        # Actualizar la interfaz gráfica
        if gui is not None:
            gui.actualizar_cara_segura(face_name, colors)
            # Sincronizar el estado interno de la GUI
            gui.estado_cubo[face_name] = [
                [gui.color_letra_a_nombre(colors[0]), gui.color_letra_a_nombre(colors[1]), gui.color_letra_a_nombre(colors[2])],
                [gui.color_letra_a_nombre(colors[3]), gui.color_letra_a_nombre(colors[4]), gui.color_letra_a_nombre(colors[5])],
                [gui.color_letra_a_nombre(colors[6]), gui.color_letra_a_nombre(colors[7]), gui.color_letra_a_nombre(colors[8])]]

        print(f"\n=== CARA {face_name} ===")
        print(f"Fila 1: {colors[0]} {colors[1]} {colors[2]}")
        print(f"Fila 2: {colors[3]} {colors[4]} {colors[5]}")
        print(f"Fila 3: {colors[6]} {colors[7]} {colors[8]}")
        print(f"Cara {face_name} guardada: {solved_sides[face_name]}")
        
        # Si tenemos todas las caras, verificar antes de resolver
        if len(solved_sides) == 6:
            print("\n¡Todas las caras registradas!")
            if gui is not None:
                gui.root.focus_force()  # Asegurar que la ventana tiene foco

            while True:
                if gui is not None:
                    gui.verificar_cambios()
                    
                #Preguntamos si queremos la solución del algoritmo de kociemba
                respuesta = get_input_con_actualizacion("\n¿Deseas obtener la solución ahora? (SI/NO/VER): ")
            
                if respuesta == "VER":
                    # Mostrar todas las caras registradas
                    print("\nCaras registradas:")
                    for cara, colores in solved_sides.items():
                        print(f"{cara}: {colores}")

                    # Preguntar si alguna cara necesita corrección
                    corregir = get_input_con_actualizacion("\n¿Quieres corregir alguna cara? (Nombre de la cara o pulsa 'ok' para continuar): ")
                    if corregir in solved_sides:
                        del solved_sides[corregir]  # Eliminar la cara para volver a registrarla
                        
                        # Actualizar GUI para mostrar solo el centro de la cara eliminada
                        if gui is not None:
                            gui.reset_cara(corregir)
                        print(f"\nCara {corregir} eliminada. Por favor, vuelve a registrar esta cara.")
                        return  # Salir de la función para permitir nuevo registro
                    
                elif respuesta == "SI":
                    try:
                        # Convertimos cada cara al formato Kociemba antes de enviar
                        U = convert_colors_to_kociemba_format(solved_sides['U'])
                        R = convert_colors_to_kociemba_format(solved_sides['R'])
                        F = convert_colors_to_kociemba_format(solved_sides['F'])
                        D = convert_colors_to_kociemba_format(solved_sides['D'])
                        L = convert_colors_to_kociemba_format(solved_sides['L'])
                        B = convert_colors_to_kociemba_format(solved_sides['B'])
                
                        solution = kociembas_algorithm(U, R, F, D, L, B)
                        print("\nSOLUCIÓN DEL CUBO:")
                        print(solution)
                
                        # Preguntar si enviar a ESP32
                        respuesta = get_input_con_actualizacion("\n¿Quieres enviar la secuencia a la ESP32? (SI/NO): ")
                        
                        if respuesta == "SI":
                            from ESP32_COMSerial import enviar_secuencia
                            enviar_secuencia(solution)
                            print("Secuencia enviada correctamente!")
                        break
                            
                    except Exception as e:
                        print(f"\nError al resolver: {e}")
                        print("Revisa los colores detectados e intenta nuevamente.")
                        # Mostrar colores actuales para facilitar diagnóstico
                        print("\nEstado actual del cubo:")
                        for cara, colores in solved_sides.items():
                            print(f"{cara}: {colores}")

                elif respuesta == "NO":
                    # Eliminar la última cara registrada para permitir corrección
                    ultima_cara = list(solved_sides.keys())[-1]
                    del solved_sides[ultima_cara]
                    print(f"\nCara {ultima_cara} eliminada. Por favor, vuelve a registrar esta cara o 'actualizar' la que quieras")

                    # Actualizar GUI para mostrar solo el centro
                    if gui is not None:
                        gui.reset_cara(ultima_cara)
                    return
                
                else:
                    print("Opción no válida. Por favor ingresa SI, NO o VER")

def get_input_con_actualizacion(prompt):
    """Versión de input que permite actualizar la GUI mientras espera"""
    if gui is None:
        return input(prompt).strip().upper()
    
    # Usamos una variable compartida y eventos
    from threading import Event
    respuesta = []
    evento_respuesta = Event()

    def mostrar_dialogo():
        try:
            dialogo = tk.Toplevel(gui.root)
            dialogo.title("Input")
            dialogo.transient(gui.root)
            
            tk.Label(dialogo, text=prompt).pack(padx=10, pady=5)
            entry = tk.Entry(dialogo)
            entry.pack(padx=10, pady=5)
            
            def on_ok():
                # VERIFICACIÓN ANTES DE CERRAR (NUEVO)
                if gui is not None:
                    for cara in ['U', 'R', 'F', 'D', 'L', 'B']:
                        if cara in solved_sides:
                            nuevo_estado = []
                            for i in range(3):
                                for j in range(3):
                                    color = gui.estado_cubo[cara][i][j]
                                    nuevo_estado.append(gui.color_nombre_a_letra(color) if color else '?')
                            solved_sides[cara] = ''.join(nuevo_estado)

                respuesta.append(entry.get().upper())
                dialogo.destroy()
                evento_respuesta.set()
                
            tk.Button(dialogo, text="OK", command=on_ok).pack(pady=5)
            
            dialogo.protocol("WM_DELETE_WINDOW", on_ok)
            entry.focus_set()
            
            # Centrar el diálogo
            dialogo.update_idletasks()
            width = dialogo.winfo_width()
            height = dialogo.winfo_height()
            x = (gui.root.winfo_screenwidth() // 2) - (width // 2)
            y = (gui.root.winfo_screenheight() // 2) - (height // 2)
            dialogo.geometry(f'+{x}+{y}')
            
        except Exception as e:
            print(f"Error en diálogo: {e}")
            respuesta.append("")
            evento_respuesta.set()
    
    # Ejecutar el diálogo en el hilo principal de Tkinter
    gui.root.after(0, mostrar_dialogo)
    
    # Esperar la respuesta mientras mantenemos la GUI activa
    while not evento_respuesta.is_set():
        if gui is not None:
            gui.root.update()
            time.sleep(0.05)
    
    return respuesta[0] if respuesta else ""

def get_face_name(center_color):
    """Asigna la cara basada en el color central según estándar WCA"""
    color_to_face = {
        'W': 'U',  # Blanco: Arriba (Up)
        'Y': 'D',  # Amarillo: Abajo (Down)
        'R': 'R',  # Rojo: Derecha (Right)
        'O': 'L',  # Naranja: Izquierda (Left)
        'G': 'F',  # Verde: Frontal (Front)
        'B': 'B'   # Azul: Trasera (Back)
    }
    return color_to_face.get(center_color, None)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    results = model(frame)
    masks = results[0].masks
    boxes = results[0].boxes if results[0].boxes else []

    current_colors = []
    if masks:
        for mask, box in zip(masks, boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            h, w = y2-y1, x2-x1
            
            # Procesar cada facelet
            facelet_colors = []
            for i in range(3):
                for j in [2, 1, 0]:
                    center_x = x1 + (j * w//3) + (w//6)
                    center_y = y1 + (i * h//3) + (h//6)
                    
                    color_bgr = get_dominant_color(frame, center_x, center_y)
                    color_letter = classify_color(color_bgr)
                    facelet_colors.append(color_letter)
                    
                    # Dibujar
                    cv2.rectangle(frame, (x1 + j*w//3, y1 + i*h//3),
                                (x1 + (j+1)*w//3, y1 + (i+1)*h//3),
                                (0,255,0), 1)
                    cv2.putText(frame, color_letter,
                                (center_x-5, center_y+5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255,255,255), 2)
            
            # Guardar colores del facelet central (posición 5)
            if len(facelet_colors) >= 5:
                current_colors = facelet_colors
                current_center_color = facelet_colors[4]  # Posición 5 (0-indexed)

    # Verificar cambios en la GUI cada cierto tiempo
    if time.time() - last_gui_check > 0.5:  # Verificar cada 0.5 segundos
        if gui is not None:
            # Sincronizar cualquier cambio manual en la GUI
            for cara in ['U', 'R', 'F', 'D', 'L', 'B']:
                if cara in solved_sides:
                    # Reconstruir el string desde la GUI
                    nuevo_estado = []
                    for i in range(3):
                        for j in range(3):
                            color = gui.estado_cubo[cara][i][j]
                            nuevo_estado.append(gui.color_nombre_a_letra(color) if color else '?')
                    solved_sides[cara] = ''.join(nuevo_estado)
        last_gui_check = time.time()

    # Verificar estabilidad de colores
    if current_colors:
        color_history.append((time.time(), current_colors))
        # Eliminar registros antiguos
        color_history = [(t, c) for t, c in color_history 
                        if time.time() - t <= stable_time_threshold]
        
        # Verificar si los colores son estables
        if len(color_history) > 10:  # Mínimo 10 frames consistentes
            all_same = all(
                np.array_equal(c, current_colors) 
                for _, c in color_history[-10:]
            )
            if all_same:
                save_side_colors(current_colors, current_center_color)
                color_history = []  # Resetear para la próxima cara

    cv2.imshow('Rubik Solver', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()