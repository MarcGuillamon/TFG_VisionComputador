import cv2
import numpy as np

# Índices para IOs --> '0'
# Índices para Android --> '1' y '2'
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

# Obtener dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x, center_y = width // 2, height // 2

# Tamaño del área para el promedio (3x3 píxeles)
area_size = 3  
half_size = area_size // 2

def get_dominant_color(frame, x, y, size=3):
    """Obtiene el color promedio en un área de 'size x size' píxeles alrededor de (x, y)"""
    roi = frame[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
    if roi.size == 0:  # Evitar error si el ROI está fuera de la imagen
        return None
    avg_color = np.mean(roi, axis=(0, 1)).astype(int)
    return avg_color

def classify_color(h, s, v):
    """Clasifica el color basado en valores HSV"""
    if s < 50:  # Bajos niveles de saturación (grises/blancos/negros)
        if v > 150:
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
        elif 131 <= h < 145:
            return "Morado"
        elif 145 <= h < 160:
            return "Rosa"
        elif 160 <= h < 175:
            return "Rojo (tono rosado)"
    return "Indeterminado"

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir el video. Saliendo...")
        break

    # 1. Obtener el color promedio del área central (3x3 píxeles)
    avg_bgr = get_dominant_color(frame, center_x, center_y, area_size)
    if avg_bgr is None:
        continue  # Si no se puede leer, saltar este frame

    b, g, r = avg_bgr

    # 2. Convertir a HSV para mejor clasificación
    hsv_color = cv2.cvtColor(np.array([[avg_bgr]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv_color

    # 3. Clasificar el color
    color_name = classify_color(h, s, v)

    # 4. Dibujar el punto de referencia (después de leer el color)
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Punto rojo
    cv2.circle(frame, (center_x, center_y), 6, (255, 255, 255), 1)  # Borde blanco

    # 5. Mostrar información en pantalla
    color_info = f"BGR: ({b},{g},{r}) | HSV: ({h},{s},{v})"
    cv2.putText(frame, color_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Color: {color_name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Deteccion de Color Mejorada', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()