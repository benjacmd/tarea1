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
        
        # Punto 6: Interpretar los bytes según el formato
        if len(bytes_list) == 8:  # Verificar que la trama tenga 8 bytes
            start_end = bytes_list[0]  # Byte de inicio/fin (7E)
            device_type = bytes_list[1]  # Tipo de dispositivo (01 o 02)
            device_id = bytes_list[2]  # ID del dispositivo
            query = bytes_list[3]  # Query (11)
            data = bytes_list[4]  # Datos (temperatura o humedad)
            crc_high = bytes_list[5]  # Parte alta del checksum
            crc_low = bytes_list[6]  # Parte baja del checksum
            end_marker = bytes_list[7]  # Byte de fin (7E)
            
            # Verificar el byte de inicio/fin
            if start_end == 0x7E and end_marker == 0x7E:
                # Interpretar el tipo de dispositivo
                if device_type == 0x01:
                    device_type_str = "01-temperature"
                    data_str = f"temperature: {data} °C"
                elif device_type == 0x02:
                    device_type_str = "02-humidity"
                    data_str = f"relative humidity: {data} %"
                else:
                    device_type_str = "unknown"
                    data_str = "unknown data"
                
                # Mostrar la información en el formato requerido
                print(f"\nDevice type: {device_type_str}, id: {device_id}, {data_str}")
            else:
                print("Error: Byte de inicio/fin incorrecto")
        else:
            print("Error: Trama incompleta")