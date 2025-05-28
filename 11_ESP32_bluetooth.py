import serial
import time

bt_port = "COM10"
bt = serial.Serial(bt_port, 115200, timeout=2)  # Timeout de 2 segundos

def send_moves(moves):
    # Limpia buffer antes de enviar
    bt.reset_input_buffer()

    bt.write((moves + "\n").encode('utf-8'))
    print(f"[Python] Enviado: {moves}")
    
    time.sleep(0.1)  # Pausa crítica para esperar respuesta
    
    response = bt.readline().decode().strip()
    if response.startswith("OK:"):
        print(f"[ESP32] Movimiento confirmado: {response[3:]}")
    else:
        print(f"[ESP32] Respuesta inesperada: {response}")

# Prueba con un comando más corto primero
send_moves("R U R' U'")  # Comando simple de prueba
#send_moves("D2")         # Segundo comando corto

bt.close()