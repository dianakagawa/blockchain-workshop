from time import time
import json
from hashlib import sha256
from flask import Flask, jsonify, request

class Bloque:
    def __init__(self, index, transacciones, timestamp, hash_anterior, nonce=0):
        self.index = index
        self.transacciones = transacciones
        self.timestamp = timestamp
        self.hash_anterior = hash_anterior
        self.nonce = nonce

class Blockchain:
    def __init__(self):
        self.cadena = []
        self.transacciones_pendientes = []
        self.crear_bloque_genesis()
    
    def crear_bloque_genesis(self):
        genesis = Bloque(0, ['Genesis'], time(), '0'*64)
        genesis.hash = self.criptar(genesis)
        self.cadena.append(genesis)

    @staticmethod
    def criptar(bloque):
        bloque_str = json.dumps(bloque.__dict__, sort_keys=True)
        return sha256(bloque_str.encode()).hexdigest()

    def agregar_transacciones(self, transaccion):
        self.transacciones_pendientes.append(transaccion)
    
    dificultad = 4

    def proof_of_work(self, bloque):
        bloque.nonce = 0

        hasheado = self.criptar(bloque)
        while not hasheado.startswith('0'*self.dificultad):
            bloque.nonce += 1
            hasheado = self.criptar(bloque)
        return hasheado

    @property
    def ultimo_bloque(self):
        return self.cadena[-1]

    def agregar_bloque(self, bloque, prueba):
        bloque.hash = prueba
        self.cadena.append(bloque)
        return True

    def cerrar_bloque(self):
        if not self.transacciones_pendientes:
            return False

        ultimo_bloque = self.ultimo_bloque
        nuevo_bloque = Bloque(ultimo_bloque.index + 1, self.transacciones_pendientes, time(), ultimo_bloque.hash)
        prueba = self.proof_of_work(nuevo_bloque)

        self.agregar_bloque(nuevo_bloque, prueba)
        self.transacciones_pendientes = []

        return nuevo_bloque

app = Flask(__name__)

cadena = Blockchain()

@app.route('/transaccion/new', methods=['POST'])
def nueva_transaccion():
    transaccion = request.get_json()
    cadena.agregar_transacciones(transaccion['transaccion'])
    response = {'mensaje': 'La transaccion se ha agregado'}
    return jsonify(response), 201

@app.route('/cerrar', methods=['GET'])
def cerrar():
    bloque = cadena.cerrar_bloque()
    response = {
        'mensaje': 'Se ha creado el bloque',
        'index': bloque.index,
        'transacciones': bloque.transacciones,
        'timestamp': bloque.timestamp,
    }
    return jsonify(response), 200

@app.route('/cadena', methods=['GET'])
def cadena_completa():
    chain = []
    for i in cadena.cadena:
        chain.append(i.__dict__)
    response = {
        'cadena': chain,
        'largo': len(chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port= 6000)

# deploy en postman