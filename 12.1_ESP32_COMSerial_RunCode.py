import serial
import time

PORT = 'COM10'
BAUDRATE = 115200
#CADENA = "D2 L' D' L2 U R2 F B L B D' B2 R2 U' R2 U' F2 R2 U' L2"
#CADENA_DE_CONJUNTOS = "D2 U2 L2 R2 B2 F2 D2 U2 L2 R2 B2 F2"
CADENA = "U D D' U2 U2 D2 F B U R' D2 B B2 F' R' L2 L R' L L L"

ser = serial.Serial(PORT, BAUDRATE, timeout=1)
try:
    # Simular el input automáticamente
    print(f"Enviando secuencia: {CADENA}")
    
    # Envía la cadena completa + terminador
    ser.write((CADENA + '\n').encode('utf-8'))
    
    time.sleep(0.1)

    # Esperar confirmación de finalización
    while True:
        if ser.in_waiting:
            response = ser.readline().decode('utf-8').strip()
            print(f"Respuesta recibida: {response}")
            
            if response == "DONE":  # Cuando la ESP32 termine
                print("Secuencia completada!")
                break
        
        time.sleep(0.1)  # Pequeña pausa para no saturar

finally:
    ser.close()