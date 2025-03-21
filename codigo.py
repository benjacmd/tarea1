import serial

ser = serial.Serial('COM10', 57600, timeout=1)  # Ajusta el puerto y la velocidad

while True:
    print(ser.readline().decode('ascii', errors='ignore').strip())