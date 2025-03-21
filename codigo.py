import serial

# Configuración del puerto serial
ser = serial.Serial('COM10', 57600, timeout=1)  # Ajusta el puerto y la velocidad

while True:
    # Leer una línea de texto desde el puerto serial
    line = ser.readline().decode('ascii', errors='ignore').strip()
    
    # Verificar si se recibió una línea válida
    if line:
        print("\nTrama recibida (texto):", line)
        
        # Convertir el texto en una lista de bytes
        bytes_list = [int(byte, 16) for byte in line.split()]
        
        # Imprimir cada byte en formato hexadecimal y decimal
        print("Trama en hexadecimal y decimal:")
        for i, byte in enumerate(bytes_list):
            print(f"Byte {i}: Hex = {hex(byte)}, Dec = {byte}")