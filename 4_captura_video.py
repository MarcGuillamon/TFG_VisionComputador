import cv2

# Intenta con diferentes índices si 0 no funciona (0, 1, 2, etc.)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica la conexión.")
    exit()

while True:
    # Captura frame por frame
    ret, frame = cap.read()

    # Si el frame no se captura correctamente, sal del bucle
    if not ret:
        print("No se pudo recibir el video. Saliendo...")
        break

    # Muestra el frame en una ventana
    cv2.imshow('Camara del iPad', frame)

    # Presiona 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la captura y cierra las ventanas
cap.release()
cv2.destroyAllWindows()