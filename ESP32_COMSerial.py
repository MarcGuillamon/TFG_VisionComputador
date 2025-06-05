import serial
import time

def enviar_secuencia(cadena):
    PORT = 'COM10'
    BAUDRATE = 115200
    
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"\nPreparando envío de secuencia: {cadena}")
        
        # Esperar a que la conexión se establezca
        time.sleep(2)
        
        # Enviar la cadena completa + terminador
        ser.write((cadena + '\n').encode('utf-8'))
        print("Secuencia enviada, esperando confirmación...")
        
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

    except Exception as e:
        print(f"Error en la comunicación serial: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()