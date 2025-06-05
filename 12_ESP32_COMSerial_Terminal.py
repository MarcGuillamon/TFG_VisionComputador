import serial

# Configuración
PORT = 'COM10'  # Cambia al puerto correcto (COMx en Windows, /dev/ttyUSB0 en Linux/Mac)
BAUDRATE = 115200
# CADENA = "U D D' U2 U2 D2 F B U R' D2 B B2 F' R' L2 L R' L L L"

# CODIGO PARA USAR MEDIANTE LOS INPUTS DE LA TERMINAL:
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

try:
    while True:
        cmd = input("Introduce la secuencia (o 'q' para salir): ").strip()
        if cmd.lower() == 'q':
            break
        
        # Envía la cadena completa + terminador
        ser.write((cmd + '\n').encode('utf-8')) 
        print(f"Enviado: {cmd}")

finally:
    ser.close()