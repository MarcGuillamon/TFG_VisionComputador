import cv2

# Abrir la cámara (0 suele ser la cámara integrada del portátil)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ No se pudo abrir la cámara")
    exit()

while True:
    # Leer el fotograma de la cámara
    ret, frame = cap.read()

    if not ret:
        print("❌ Error al capturar el fotograma")
        break

    # Mostrar el fotograma en una ventana
    cv2.imshow("Cámara en Vivo", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
cap.release()
cv2.destroyAllWindows()
