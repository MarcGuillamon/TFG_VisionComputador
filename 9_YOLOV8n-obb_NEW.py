import cv2
from ultralytics import YOLO
import logging
import numpy as np

# Cargar el modelo YOLOv8-OBB
model = YOLO('yolov8n-obb_NEW.pt')
model.verbose = False
logging.getLogger('ultralytics').setLevel(logging.WARNING)

# Configurar la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cámara no detectada.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break
    
    # Realizar la detección con confianza mínima de 70%
    results = model(frame, stream=True, conf=0.7)
    
    # Dibujar los resultados OBB
    for r in results:
        boxes = r.obb  # Usamos obb en lugar de boxes para las cajas orientadas
        
        for box in boxes:
            # Obtener coordenadas del polígono rotado (OBB)
            poly = box.xyxyxyxy.reshape(-1, 2).cpu().numpy()
            poly = poly.astype(np.int32)
            
            # Obtener confianza y clase
            conf = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])
            
            # Solo mostrar si la confianza es >70% (aunque ya está filtrado)
            if conf > 0.7:
                # Dibujar el polígono rotado
                cv2.polylines(frame, [poly], isClosed=True, color=(0, 255, 0), thickness=2)
                
                # Dibujar un punto en el primer vértice para mostrar la orientación
                cv2.circle(frame, tuple(poly[0]), 3, (0, 0, 255), -1)
                
                # Etiqueta con la clase y confianza
                label = f"{model.names[cls]} {conf}"
                cv2.putText(frame, label, tuple(poly[0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Mostrar el frame con las detecciones
    cv2.imshow('YOLOv8-OBB Object Detection', frame)
    
    # Salir con 'q'
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()