from ultralytics import YOLO
import cv2

model = YOLO('best.pt')  # El modelo está en la misma carpeta
# Índices para IOs --> '0'
# Índices para Android --> '1' y '2'
cap = cv2.VideoCapture(0)  # Cámara predeterminada (cambia a 1 si es externa)

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame)  # Detecta y segmenta
    annotated_frame = results[0].plot()  # Dibuja BBoxes + Máscaras automáticamente

    cv2.imshow('YOLOv8 Seg', annotated_frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()