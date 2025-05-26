import cv2
import numpy as np

# Intenta con diferentes índices si 0 no funciona (0, 1, 2, etc.)
# Índices para IOs --> '0'
# Índices para Android --> '2'
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    # Si el frame no se captura correctamente, sal del bucle
    if not ret:
        print("No se pudo recibir el video. Saliendo...")
        break

    # 1. Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2. Aplicar suavizado para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Detectar bordes usando Canny
    edges = cv2.Canny(blurred, 50, 150)

    # 4. Encontrar contornos en la imagen
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Variables para almacenar el mejor contorno
    best_contour = None
    best_score = 0

    # 5. Filtrar contornos para detectar el cubo
    for contour in contours:
        # Aproximar el contorno a una forma poligonal
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Si el contorno tiene 4 vértices, es probable que sea un cuadrado o rectángulo
        if len(approx) == 4:
            # Calcular el área del contorno
            area = cv2.contourArea(contour)

            # Calcular la relación de aspecto (ancho/alto)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Calcular la solidez (solidity)
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            solidity = float(area) / hull_area if hull_area > 0 else 0

            # Puntuar el contorno basado en área, relación de aspecto y solidez
            score = area * (1 - abs(aspect_ratio - 1)) * solidity

            # Si este contorno tiene una puntuación más alta que el mejor anterior, actualizar
            if score > best_score:
                best_contour = approx
                best_score = score

    # Si encontramos un contorno válido, dibujarlo
    if best_contour is not None:
        cv2.drawContours(frame, [best_contour], -1, (0, 255, 0), 3)
        x, y, w, h = cv2.boundingRect(best_contour)
        cv2.putText(frame, "Cubo detectado", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Mostrar el frame con los contornos detectados
    cv2.imshow('Deteccion del cubo de Rubik', frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()