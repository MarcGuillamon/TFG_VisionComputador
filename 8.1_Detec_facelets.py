import cv2
import numpy as np

cap = cv2.VideoCapture(1)  # Ajusta el índice de la cámara

def classify_color(h, s, v):
    """Clasifica el color basado en HSV (igual que antes)"""
    if s < 50:
        if v > 150: return "Blanco"
        elif v < 50: return "Negro"
        else: return "Gris"
    else:
        if h < 5 or h > 175: return "Rojo"
        elif 5 <= h < 22: return "Naranja"
        elif 22 <= h < 33: return "Amarillo"
        elif 33 <= h < 78: return "Verde"
        elif 78 <= h < 131: return "Azul"
        elif 131 <= h < 145: return "Morado"
        elif 145 <= h < 160: return "Rosa"
        elif 160 <= h < 175: return "Rojo (tono rosado)"
    return "Indeterminado"

def detect_facelets(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_ranges = {
        "Rojo": ([0, 100, 100], [10, 255, 255], [160, 100, 100], [180, 255, 255]),
        "Verde": ([33, 100, 100], [78, 255, 255]),
        "Azul": ([78, 100, 100], [131, 255, 255]),
        "Amarillo": ([22, 100, 100], [33, 255, 255]),
        "Naranja": ([5, 100, 100], [22, 255, 255]),
        "Blanco": ([0, 0, 150], [180, 50, 255]),
    }
    
    for color_name, ranges in color_ranges.items():
        if color_name == "Rojo":
            mask = cv2.inRange(hsv, np.array(ranges[0]), np.array(ranges[1])) + \
                   cv2.inRange(hsv, np.array(ranges[2]), np.array(ranges[3]))
        else:
            mask = cv2.inRange(hsv, np.array(ranges[0]), np.array(ranges[1]))
        
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Área mínima para considerar una cara completa
                x, y, w, h = cv2.boundingRect(cnt)
                
                # Dividir la cara en 3x3 regiones (9 facelets)
                rows, cols = 3, 3
                facelet_w, facelet_h = w // cols, h // rows
                
                for i in range(rows):
                    for j in range(cols):
                        # Centro de cada facelet
                        center_x = x + (j * facelet_w) + (facelet_w // 2)
                        center_y = y + (i * facelet_h) + (facelet_h // 2)
                        
                        # Obtener color en el centro
                        roi = frame[center_y-2:center_y+2, center_x-2:center_x+2]
                        if roi.size == 0:
                            continue
                        avg_bgr = np.mean(roi, axis=(0, 1)).astype(int)
                        hsv_roi = cv2.cvtColor(np.array([[avg_bgr]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
                        color_name_detected = classify_color(*hsv_roi)
                        
                        # Dibujar círculo y texto
                        cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), 2)
                        cv2.putText(frame, color_name_detected, (center_x-20, center_y-15),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                # Si no es una cara completa, tratar como facelet individual
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                roi = frame[int(y)-2:int(y)+2, int(x)-2:int(x)+2]
                if roi.size == 0:
                    continue
                avg_bgr = np.mean(roi, axis=(0, 1)).astype(int)
                hsv_roi = cv2.cvtColor(np.array([[avg_bgr]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
                color_name_detected = classify_color(*hsv_roi)
                cv2.circle(frame, center, int(radius), (0, 255, 0), 2)
                cv2.putText(frame, color_name_detected, (center[0]-20, center[1]-15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = detect_facelets(frame)
    cv2.imshow("Deteccion de 'Facelets'", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()