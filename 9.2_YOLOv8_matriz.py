import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break
    
    results = model(frame)
    masks = results[0].masks  # Máscaras de segmentación

    if masks is not None:
        for mask in masks:
            # Obtener coordenadas del bounding box
            x1, y1, x2, y2 = map(int, mask.xyxy[0].cpu().numpy())
            
            # Crear máscara binaria
            mask_data = mask.data[0].cpu().numpy()
            binary_mask = (mask_data > 0).astype(np.uint8) * 255
            
            # Encontrar contornos para obtener la máscara exacta
            contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours: continue
            
            # Crear máscara convexa para la cara
            hull = cv2.convexHull(np.vstack(contours))
            face_mask = np.zeros_like(binary_mask)
            cv2.drawContours(face_mask, [hull], -1, 255, -1)

            # Dividir la región en 3x3
            h, w = y2-y1, x2-x1
            for i in range(3):
                for j in range(3):
                    # Coordenadas del facelet
                    fx1 = x1 + j * w//3
                    fx2 = x1 + (j+1) * w//3
                    fy1 = y1 + i * h//3
                    fy2 = y1 + (i+1) * h//3
                    
                    # Máscara del facelet
                    facelet_mask = face_mask[fy1:fy2, fx1:fx2]
                    facelet_area = frame[fy1:fy2, fx1:fx2]
                    
                    # Obtener color dominante (HSV)
                    if np.any(facelet_mask):
                        hsv = cv2.cvtColor(facelet_area, cv2.COLOR_BGR2HSV)
                        masked_hsv = hsv[facelet_mask == 255]
                        if len(masked_hsv) > 0:
                            median_hue = np.median(masked_hsv[:,0])
                            color_name = classify_color(median_hue)  # Tu función de clasificación
                            
                            # Dibujar información
                            cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (0,255,0), 1)
                            cv2.putText(frame, color_name, (fx1, fy1+15), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
                            
def classify_color(hue):
    if 0 <= hue < 15 or 165 <= hue <= 180: return "Rojo"
    elif 35 <= hue < 85: return "Verde"
    elif 100 <= hue < 140: return "Azul"
    # Añade más rangos según necesites
    return "Desconocido"

    cv2.imshow('Rubik Detection', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
