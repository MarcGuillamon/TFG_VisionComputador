import serial

# Configuración
PORT = 'COM10'  # Cambia al puerto correcto (COMx en Windows, /dev/ttyUSB0 en Linux/Mac)
BAUDRATE = 9600

# Conexión
ser = serial.Serial(PORT, BAUDRATE, timeout=1)

# Control LED
while True:
    cmd = input("1 (ON) / 0 (OFF) / q (Salir): ").strip()
    if cmd == 'q':
        break
    if cmd in ('1', '0'):
        ser.write(cmd.encode())  # Envía '1' o '0' a la ESP32

ser.close()