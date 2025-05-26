import cv2
import numpy as np

# Inicializar cámara
cap = cv2.VideoCapture(1)  # Ajusta el índice según tu cámara

if not cap.isOpened():
    print("Error: No se pudo abrir la cámara.")
    exit()

def classify_color(h, s, v):
    """Clasifica el color basado en valores HSV (igual que tu código)"""
    if s < 50:  # Bajos niveles de saturación
        if v > 150:
            return "Blanco"
        elif v < 50:
            return "Negro"
        else:
            return "Gris"
    else:  # Colores saturados
        if h < 5 or h > 175:
            return "Rojo"
        elif 5 <= h < 22:
            return "Naranja"
        elif 22 <= h < 33:
            return "Amarillo"
        elif 33 <= h < 78:
            return "Verde"
        elif 78 <= h < 131:
            return "Azul"
        elif 131 <= h < 145:
            return "Morado"
        elif 145 <= h < 160:
            return "Rosa"
        elif 160 <= h < 175:
            return "Rojo (tono rosado)"
    return "Indeterminado"

def detect_facelets(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Rangos HSV para cada color del cubo (ajústalos según tus necesidades)
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
            lower1, upper1, lower2, upper2 = ranges
            mask1 = cv2.inRange(hsv, np.array(lower1), np.array(upper1))
            mask2 = cv2.inRange(hsv, np.array(lower2), np.array(upper2))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower, upper = ranges
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        
        # Filtrar ruido
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Filtrar por tamaño
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                center = (int(x), int(y))
                
                # Obtener color promedio del facelet
                roi = frame[int(y)-5:int(y)+5, int(x)-5:int(x)+5]  # Pequeña región
                if roi.size == 0:
                    continue
                avg_bgr = np.mean(roi, axis=(0, 1)).astype(int)
                b, g, r = avg_bgr
                hsv_roi = cv2.cvtColor(np.array([[avg_bgr]], dtype=np.uint8), cv2.COLOR_BGR2HSV)[0][0]
                h, s, v = hsv_roi
                
                # Clasificar color y dibujar
                color_name_detected = classify_color(h, s, v)
                cv2.circle(frame, center, int(radius), (0, 255, 0), 2)  # Círculo verde
                cv2.putText(frame, color_name_detected, (center[0]-20, center[1]-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo capturar el frame.")
        break
    
    frame_with_facelets = detect_facelets(frame)
    cv2.imshow("Deteccion de 'Facelets'", frame_with_facelets)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()