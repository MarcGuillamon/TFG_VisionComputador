from ultralytics import YOLO
import logging

import numpy as np
import cv2
import time
from Kociembas2 import kociembas_algorithm

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

        print(f"\n=== CARA {face_name} ===")
        print(f"Fila 1: {colors[0]} {colors[1]} {colors[2]}")
        print(f"Fila 2: {colors[3]} {colors[4]} {colors[5]}")
        print(f"Fila 3: {colors[6]} {colors[7]} {colors[8]}")
        print(f"Cara {face_name} guardada: {solved_sides[face_name]}")
        
        # Si tenemos todas las caras, resolver el cubo
        if len(solved_sides) == 6:
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
                respuesta = input("\n¿Quieres enviar la secuencia a la ESP32? (SI/NO): ").strip().upper()
                
                if respuesta == "SI":
                    from ESP32_COMSerial import enviar_secuencia
                    enviar_secuencia(solution)
                    print("Secuencia enviada correctamente!")
                else:
                    print("Secuencia no enviada")
                    
            except Exception as e:
                print(f"\nError al resolver: {e}")

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