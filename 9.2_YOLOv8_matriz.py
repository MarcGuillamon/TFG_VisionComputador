from ultralytics import YOLO
import numpy as np
import cv2

# Cargar modelo
model = YOLO('best.pt')
cap = cv2.VideoCapture(0)

# Configuración de color (de tu script 7.1_Detec_color.py)
area_size = 3  
half_size = area_size // 2

def get_dominant_color(frame, x, y):
    """Obtiene el color promedio en un área 3x3 alrededor de (x,y) en formato BGR"""
    roi = frame[y-half_size:y+half_size+1, x-half_size:x+half_size+1]
    if roi.size == 0:
        return None
    return np.mean(roi, axis=(0, 1)).astype(int)

def classify_color(bgr_color):
    """Clasifica el color BGR a letra"""
    if bgr_color is None:
        return "?"
    
    # Convertir BGR a HSV
    hsv = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv
    
    # Clasificación (adaptada de tu código)
    if s < 50:
        return "W" if v > 135 else "N"  # Blanco o Negro
    else:
        if h < 5 or h > 175: return "R"  # Rojo
        elif 5 <= h < 22: return "O"     # Naranja
        elif 22 <= h < 40: return "A"    # Amarillo
        elif 40 <= h < 78: return "G"    # Verde
        elif 78 <= h < 131: return "B"   # Azul
        else: return "?"

while True:
    ret, frame = cap.read()
    if not ret: break

    results = model(frame)
    masks = results[0].masks
    boxes = results[0].boxes if results[0].boxes else []

    if masks:
        for mask, box in zip(masks, boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            h, w = y2-y1, x2-x1
            
            # Dividir en 3x3 facelets
            for i in range(3):
                for j in range(3):
                    # Centro del facelet (i,j)
                    center_x = x1 + (j * w//3) + (w//6)
                    center_y = y1 + (i * h//3) + (h//6)
                    
                    # Obtener y clasificar color
                    color_bgr = get_dominant_color(frame, center_x, center_y)
                    color_letter = classify_color(color_bgr)
                    
                    # Dibujar cuadrado + letra
                    cv2.rectangle(frame, 
                                (x1 + j*w//3, y1 + i*h//3),
                                (x1 + (j+1)*w//3, y1 + (i+1)*h//3),
                                (0,255,0), 1)
                    
                    cv2.putText(frame, color_letter,
                              (center_x-5, center_y+5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                              (255,255,255), 2)

    cv2.imshow('Rubik Color Detection', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()