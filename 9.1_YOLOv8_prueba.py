from ultralytics import YOLO
import numpy as np
import cv2

model = YOLO('best.pt')  # El modelo está en la misma carpeta
# Índices para IOs --> '0'
# Índices para Android --> '1' y '2'
cap = cv2.VideoCapture(0)  # Cámara predeterminada (cambia a 1 si es externa)

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame)  # Detecta y segmenta
    masks = results[0].masks  # Dibuja solo Máscaras automáticamente
    boxes = results[0].boxes  # Bounding boxes

    if masks is not None:
        for mask, box in zip(masks, boxes):
            # Obtener coordenadas del bounding box desde 'boxes' (no desde 'mask')
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Dividir en 3x3 (9 facelets)
            h, w = y2-y1, x2-x1
            for i in range(3):
                for j in range(3):
                    fx1 = x1 + j * w//3
                    fy1 = y1 + i * h//3
                    fx2 = fx1 + w//3
                    fy2 = fy1 + h//3

                    # Dibujar cuadrícula
                    cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0, 255, 0), 1)

    cv2.imshow('Rubik Facelets', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()