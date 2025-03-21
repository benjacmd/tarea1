import serial
import crcmod

class TramaProcessor:
    def __init__(self, port, baudrate):
        # Configuración del puerto serial
        self.ser = serial.Serial(port, baudrate, timeout=1)
        
        # Configuración del CRC-16/CCITT-False
        self.crc16 = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0xFFFF, xorOut=0x0000)
    
    def calculate_crc(self, data):
        """Calcula el CRC-16/CCITT-False de los datos proporcionados."""
        return self.crc16(data)
    
    def process_trama(self, line):
        """Procesa una trama recibida y verifica su integridad."""
        print("\nTrama recibida (texto):", line)
        
        # Convertir el texto en una lista de bytes
        bytes_list = [int(byte, 16) for byte in line.split()]
        
        # Imprimir cada byte en formato hexadecimal y decimal
        print("Trama en hexadecimal y decimal:")
        for i, byte in enumerate(bytes_list):
            print(f"Byte {i}: Hex = {hex(byte)}, Dec = {byte}")
        
        # Verificar que la trama tenga 8 bytes
        if len(bytes_list) == 8:
            start_end = bytes_list[0]  # Byte de inicio/fin (7E)
            device_type = bytes_list[1]  # Tipo de dispositivo (01 o 02)
            device_id = bytes_list[2]  # ID del dispositivo
            query = bytes_list[3]  # Query (11)
            data = bytes_list[4]  # Datos (temperatura o humedad)
            crc_received = (bytes_list[5] << 8) | bytes_list[6]  # Checksum recibido (combinar 2 bytes)
            end_marker = bytes_list[7]  # Byte de fin (7E)
            
            # Verificar el byte de inicio/fin
            if start_end == 0x7E and end_marker == 0x7E:
                # Calcular el CRC de los bytes relevantes (sin inicio y fin)
                crc_calculated = self.calculate_crc(bytes(bytes_list[1:5]))  # Bytes 1 a 4
                
                # Mostrar el checksum calculado y el recibido
                print(f"\nChecksum calculado: {hex(crc_calculated)}")
                print(f"Checksum recibido: {hex(crc_received)}")
                
                # Verificar el checksum
                if crc_calculated == crc_received:
                    crc_status = "ok"
                else:
                    crc_status = "error"
                
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
                print(f"\nDevice type: {device_type_str}, id: {device_id}, {data_str}, checksum: {crc_status}")
            else:
                print("Error: Byte de inicio/fin incorrecto")
        else:
            print("Error: Trama incompleta")
    
    def read_serial_data(self):
        """Lee datos del puerto serial y procesa las tramas recibidas."""
        while True:
            # Leer una línea de texto desde el puerto serial
            line = self.ser.readline().decode('ascii', errors='ignore').strip()
            
            # Verificar si se recibió una línea válida
            if line:
                self.process_trama(line)

# Uso de la clase
if __name__ == "__main__":
    # Crear una instancia de TramaProcessor
    processor = TramaProcessor('COM10', 57600)  # Ajusta el puerto y la velocidad
    
    # Iniciar la lectura de datos seriales
    processor.read_serial_data()