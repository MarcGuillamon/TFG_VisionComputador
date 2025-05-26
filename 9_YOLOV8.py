import cv2
from ultralytics import YOLO
import numpy as np

# Cargar el modelo YOLOv8 (reemplaza con la ruta a tu modelo)
model = YOLO('best.pt')  # o la ruta a tu modelo descargado

# Configurar la cámara
cap = cv2.VideoCapture(1)  # Cambia el índice si es necesario

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

# Obtener dimensiones
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x, center_y = width // 2, height // 2

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break
    
    # Realizar la detección
    results = model(frame, stream=True)
    
    # Dibujar los resultados
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Coordenadas del bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Dibujar el rectángulo
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Etiqueta con la clase y confianza
            conf = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])
            label = f"{model.names[cls]} {conf}"
            cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Mostrar el frame con las detecciones
    cv2.imshow('YOLOv8 Object Detection', frame)
    
    # Salir con 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()