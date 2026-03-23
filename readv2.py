import sys
from scapy.all import rdpcap, ICMP

def evaluar_probabilidad_texto(texto):
    # Diccionario rudimentario para identificar el mensaje en claro
    palabras_clave = [" Aleluya. ", " Ameeen"]
    score = sum(1 for palabra in palabras_clave if palabra in texto.lower())
    return score

def descifrar_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            ascii_base = ord('a') if caracter.islower() else ord('A')
            nuevo_caracter = chr((ord(caracter) - ascii_base - desplazamiento) % 26 + ascii_base)
            resultado += nuevo_caracter
        else:
            resultado += caracter
    return resultado

def extraer_mensaje(pcap_file):
    packets = rdpcap(pcap_file)
    mensaje_interceptado = ""

    for pkt in packets:
        # Filtramos solo los ICMP Echo Request (type 8)
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8:
            payload = bytes(pkt[ICMP].payload)
            # Verificamos que el payload sea suficientemente largo y extraemos el byte oculto
            if len(payload) >= 9:
                caracter_oculto = chr(payload[8])
                mensaje_interceptado += caracter_oculto

    return mensaje_interceptado

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: sudo python3 readv2.py archivo.pcapng")
        sys.exit(1)

    pcap_file = sys.argv[1]
    mensaje_interceptado = extraer_mensaje(pcap_file)
    
    mejor_puntaje = 0
    mejor_desplazamiento = 0

    # Determinar automáticamente el mejor desplazamiento
    for i in range(1, 26):
        texto_prueba = descifrar_cesar(mensaje_interceptado, i)
        puntaje_actual = evaluar_probabilidad_texto(texto_prueba)
        if puntaje_actual > mejor_puntaje:
            mejor_puntaje = puntaje_actual
            mejor_desplazamiento = i

    # Imprimir resultados
    for i in range(1, 26):
        texto_descifrado = descifrar_cesar(mensaje_interceptado, i)
        if i == mejor_desplazamiento:
            # Imprime en verde brillante usando códigos ANSI
            print(f"\033[92m{i}\t{texto_descifrado}\033[0m")
        else:
            print(f"{i}\t{texto_descifrado}")
