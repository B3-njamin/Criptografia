import sys

def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            ascii_base = ord('a') if caracter.islower() else ord('A')
            nuevo_caracter = chr((ord(caracter) - ascii_base + desplazamiento) % 26 + ascii_base)
            resultado += nuevo_caracter
        else:
            # Mantiene espacios y caracteres especiales sin cifrar
            resultado += caracter
    return resultado

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py \"texto\" desplazamiento")
        sys.exit(1)

    texto_original = sys.argv[1]
    desplazamiento = int(sys.argv[2])

    texto_cifrado = cifrado_cesar(texto_original, desplazamiento)
    print(texto_cifrado)
