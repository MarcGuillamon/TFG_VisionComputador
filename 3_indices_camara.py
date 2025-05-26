import cv2

# Prueba con índices desde 0 hasta 10
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Índice {i}: Cámara conectada correctamente.")
        ret, frame = cap.read()
        if ret:
            print(f"Índice {i}: Video recibido correctamente.")
            cv2.imshow(f'Cámara {i}', frame)
            cv2.waitKey(1000)  # Muestra la imagen durante 1 segundo
            cv2.destroyAllWindows()
        else:
            print(f"Índice {i}: No se pudo recibir video.")
        cap.release()
    else:
        print(f"Índice {i}: No se pudo abrir la cámara.")