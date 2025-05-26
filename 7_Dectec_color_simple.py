import cv2
import numpy as np

# Índices para IOs --> '0'
# Índices para Android --> '1'
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

# Obtener dimensiones del video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x, center_y = width // 2, height // 2

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir el video. Saliendo...")
        break

    # Primero: Obtener el color del píxel central (antes de dibujar nada)
    bgr_color = frame[center_y, center_x].copy()  # Usamos copy() para evitar referencias
    b, g, r = bgr_color

    # Convertir a HSV
    hsv_color = cv2.cvtColor(np.array([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv_color

    # Clasificar el color (misma lógica que antes)
    color_name = "Indeterminado"
    if s < 50:
        if v > 150:
            color_name = "Blanco"
        elif v < 50:
            color_name = "Negro"
        else:
            color_name = "Gris"
    else:  # Colores saturados
        if h < 5 or h > 175:
            color_name = "Rojo"
        elif 5 <= h < 22:
            color_name = "Naranja"
        elif 22 <= h < 33:
            color_name = "Amarillo"
        elif 33 <= h < 78:
            color_name = "Verde"
        elif 78 <= h < 131:
            color_name = "Azul"

    # Ahora sí dibujamos el punto de referencia (después de leer el color)
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)  # Punto rojo
    cv2.circle(frame, (center_x, center_y), 6, (255, 255, 255), 1)  # Borde blanco para mejor visibilidad

    # Mostrar información
    color_info = f"BGR: ({b},{g},{r}) | HSV: ({h},{s},{v})"
    cv2.putText(frame, color_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Color: {color_name}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow('Deteccion de Color', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()