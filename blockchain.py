from hashlib import sha256 # se importa la libreria que ya viene por defecto con python
import json
import time

mensaje = {
    'nonce': 0,
    'data': "cuantas peras hay"
}
mensaje_str = json.dumps(mensaje, sort_keys=True)
hash = sha256(mensaje_str.encode()).hexdigest()

# while True:
#     mensaje['nonce'] += 1
#     mensaje_str = json.dumps(mensaje, sort_keys=True)
#     hash = sha256(mensaje_str.encode()).hexdigest() # se encripta el mensaje y se utiliza .hexadigest() para convertir el encriptado a hexagecimal.
#     if hash.startswith('0'):
#         print(hash)
#         print(mensaje)
#         break


while not hash.startswith('0000'):
    mensaje['nonce'] += 1
    mensaje_str = json.dumps(mensaje, sort_keys=True)
    hash = sha256(mensaje_str.encode()).hexdigest()

print(mensaje)
print(hash)