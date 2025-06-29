import cv2
from ultralytics import YOLO
import logging

# Cargar el modelo YOLOv8 (reemplaza con la ruta a tu modelo)
model = YOLO('yolov8n_NEW.pt')  # o la ruta a tu modelo descargado
model.verbose = False  # Esto reduce algunos mensajes
logging.getLogger('ultralytics').setLevel(logging.WARNING)  # Silencia logs DEBUG e INFO

# Configurar la cámara
cap = cv2.VideoCapture(0)  # Cambia el índice si es necesario

if not cap.isOpened():
    print("Error: Cámara no detectada.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo recibir el frame. Saliendo...")
        break
    
    # Realizar la detección
    results = model(frame, stream=True, conf=0.7)  # Aquí es donde se aplica el filtro)
    
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