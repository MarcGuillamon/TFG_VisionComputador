import cv2
import numpy as np
from collections import defaultdict
import time

# Configuración de la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

# Obtener dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x, center_y = width // 2, height // 2

# Tamaño de la matriz 3x3 y celdas
matrix_size = 200  # Tamaño total de la matriz en píxeles
cell_size = matrix_size // 3
half_cell = cell_size // 2

# Colores para los cuadrados
square_colors = {
    "Blanco": (255, 255, 255),
    "Amarillo": (0, 255, 255),
    "Verde": (0, 255, 0),
    "Azul": (255, 0, 0),
    "Rojo": (0, 0, 255),
    "Naranja": (0, 165, 255),
    "Negro": (0, 0, 0),
    "Gris": (128, 128, 128)
}

# Letras para representar colores
color_letters = {
    "Blanco": "W",
    "Amarillo": "Y",
    "Verde": "G",
    "Azul": "B",
    "Rojo": "R",
    "Naranja": "O"
}

# Variables para almacenar las caras del cubo
faces = {
    "W": None,  # Blanco
    "Y": None,  # Amarillo
    "G": None,  # Verde
    "B": None,  # Azul
    "R": None,  # Rojo
    "O": None   # Naranja
}

# Tiempo de estabilidad requerido (2 segundos)
STABILITY_TIME = 2.0
# Diccionario para rastrear tiempos de detección
detection_times = defaultdict(float)
# Diccionario para rastrear los últimos colores detectados
last_colors = {}

def get_dominant_color(frame, x, y, size=3):
    """Obtiene el color promedio en un área de 'size x size' píxeles alrededor de (x, y)"""
    half_size = size // 2
    roi = frame[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
    if roi.size == 0:  # Evitar error si el ROI está fuera de la imagen
        return None
    avg_color = np.mean(roi, axis=(0, 1)).astype(int)
    return avg_color

def classify_color(h, s, v):
    """Clasifica el color basado en valores HSV"""
    if s < 50:  # Bajos niveles de saturación (grises/blancos/negros)
        if v > 200:
            return "Blanco"
        elif v < 50:
            return "Negro"
        else:
            return "Gris"
    else:  # Colores saturados
        if h < 5 or h > 175:
            return "Rojo"
        elif 5 <= h < 22:
            return "Naranja"
        elif 22 <= h < 33:
            return "Amarillo"
        elif 33 <= h < 78:
            return "Verde"
        elif 78 <= h < 131:
            return "Azul"
    return "Indeterminado"

def draw_matrix(frame, center_x, center_y, cell_size):
    """Dibuja la matriz 3x3 y devuelve las coordenadas centrales de cada celda"""
    # Coordenadas iniciales (esquina superior izquierda de la matriz)
    start_x = center_x - (cell_size * 3) // 2
    start_y = center_y - (cell_size * 3) // 2
    
    # Dibujar la matriz 3x3
    for i in range(3):
        for j in range(3):
            # Coordenadas del cuadrado
            x1 = start_x + j * cell_size
            y1 = start_y + i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            # Dibujar el cuadrado
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            # Coordenada central de la celda (para detección de color)
            cell_center_x = x1 + cell_size // 2
            cell_center_y = y1 + cell_size // 2
            
            yield (i, j), (cell_center_x, cell_center_y), (x1, y1, x2, y2)

def save_face_if_stable(current_colors, current_time):
    """Guarda la cara si los colores son estables por 2 segundos"""
    # Verificar si todos los colores son iguales a los anteriores
    if last_colors and all(last_colors.get((i, j)) == current_colors.get((i, j)) 
                          for i, j in current_colors):
        # Verificar si ha pasado el tiempo suficiente
        if (current_time - detection_times.get("last_change", 0)) >= STABILITY_TIME:
            # Obtener el color central para identificar la cara
            center_color = current_colors.get((1, 1))
            if center_color in color_letters:
                face_code = color_letters[center_color]
                # Crear la matriz 3x3 para la cara
                face_matrix = [[None]*3 for _ in range(3)]
                for (i, j), color in current_colors.items():
                    face_matrix[i][j] = color_letters.get(color, "?")
                
                # Guardar la cara
                faces[face_code] = face_matrix
                print(f"\nCara {face_code} guardada:")
                for row in face_matrix:
                    print(" ".join(row))
                print("\nCaras guardadas hasta ahora:")
                for code, face in faces.items():
                    if face:
                        print(f"Cara {code}:")
                        for row in face:
                            print(" ".join(row))
                        print()
                
                # Reiniciar el temporizador para esta cara
                detection_times["last_change"] = current_time
                return True
    return False

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir el video. Saliendo...")
        break

    # Obtener el tiempo actual
    current_time = time.time()

    # Diccionario para los colores actuales
    current_colors = {}

    # Dibujar la matriz 3x3 y procesar cada celda
    for (i, j), (cell_x, cell_y), (x1, y1, x2, y2) in draw_matrix(frame, center_x, center_y, cell_size):
        # 1. Obtener el color promedio en la celda
        avg_bgr = get_dominant_color(frame, cell_x, cell_y, 5)
        if avg_bgr is None:
            continue

        b, g, r = avg_bgr

        # 2. Convertir a HSV para mejor clasificación
        hsv_color = cv2.cvtColor(np.array([[avg_bgr]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv_color

        # 3. Clasificar el color
        color_name = classify_color(h, s, v)
        current_colors[(i, j)] = color_name

        # 4. Mostrar la letra del color en la celda
        if color_name in color_letters:
            letter = color_letters[color_name]
            text_size = cv2.getTextSize(letter, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = x1 + (cell_size - text_size[0]) // 2
            text_y = y1 + (cell_size + text_size[1]) // 2
            cv2.putText(frame, letter, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Verificar si los colores han cambiado
    if current_colors != last_colors:
        detection_times["last_change"] = current_time
        last_colors = current_colors.copy()

    # Intentar guardar la cara si los colores son estables
    save_face_if_stable(current_colors, current_time)

    # Mostrar información en pantalla
    cv2.putText(frame, "Centra el cubo en la matriz 3x3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Mantener estable 2 segundos para guardar", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Mostrar estado de las caras guardadas
    status_text = "Caras guardadas: " + " ".join([f"{k}" for k, v in faces.items() if v])
    cv2.putText(frame, status_text, (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Deteccion de Cubo Rubik 3x3', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()