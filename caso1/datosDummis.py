# Importamos las bibliotecas necesarias
import requests
import random
import json
import time
import logging
import uuid
from datetime import datetime
from decimal import Decimal

# Configuramos el registro de errores en un archivo
logging.basicConfig(
    filename='errores.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL base del API Gateway
API_BASE_URL = "https://w5iesrsclb.execute-api.us-east-1.amazonaws.com/transacciones"
# Lista de cuentas ficticias para los datos de demostración
CUENTAS = ["CUENTA123", "CUENTA456", "CUENTA789", "CUENTA101"]

# Lista de tipos de transacciones posibles
TIPOS_TRANSACCION = ["DEPOSITO", "RETIRO"]

# Lista de descripciones posibles
DESCRIPCIONES = [
    "Depósito inicial",
    "Retiro en cajero",
    "Transferencia recibida",
    "Pago de servicios",
    "Depósito por nómina"
]

def validar_transaccion(transaccion):
    """
    Valida que la transacción tenga los campos requeridos y valores válidos.
    Args:
        transaccion (dict): Diccionario con los datos de la transacción.
    Returns:
        bool: True si es válida, False si no lo es.
    """
    try:
        # Verificamos que todos los campos necesarios estén presentes
        if not all(key in transaccion for key in ['idCuenta', 'monto', 'tipo', 'descripcion']):
            logging.error(f"Transacción inválida: faltan campos - {transaccion}")
            return False
        
        # Validamos idCuenta
        if transaccion['idCuenta'] not in CUENTAS:
            logging.error(f"Transacción inválida: idCuenta no válido - {transaccion['idCuenta']}")
            return False
        
        # Validamos monto (positivo y numérico)
        if not isinstance(transaccion['monto'], (int, float)) or transaccion['monto'] <= 0:
            logging.error(f"Transacción inválida: monto no válido - {transaccion['monto']}")
            return False
        
        # Validamos tipo
        if transaccion['tipo'] not in TIPOS_TRANSACCION:
            logging.error(f"Transacción inválida: tipo no válido - {transaccion['tipo']}")
            return False
        
        # Validamos descripcion (no vacía)
        if not transaccion['descripcion']:
            logging.error(f"Transacción inválida: descripción vacía - {transaccion}")
            return False
            
        return True
    except Exception as e:
        logging.error(f"Error al validar transacción: {str(e)} - {transaccion}")
        return False

def generar_transaccion():
    """
    Genera una transacción de demostración con datos aleatorios.
    Retorna un diccionario con los campos requeridos por el endpoint.
    """
    return {
        'idTransaccion': str(uuid.uuid4()),
        "idCuenta": random.choice(CUENTAS),  # Selecciona una cuenta aleatoria
        "monto": random.randint(1000, 10000000), #round(random.uniform(10, 1000), 2),  # Monto entre 10 y 1000
        "tipo": random.choice(TIPOS_TRANSACCION),  # Tipo de transacción aleatorio
        "descripcion": random.choice(DESCRIPCIONES)  # Descripción aleatoria
    }

def enviar_transaccion(transaccion, intentos_max=3, pausa_entre_intentos=1):
    """
    Envía una transacción al endpoint POST /transacciones con reintentos.
    Args:
        transaccion (dict): Diccionario con los datos de la transacción.
        intentos_max (int): Número máximo de intentos.
        pausa_entre_intentos (float): Segundos entre intentos.
    Returns:
        dict: Respuesta del servidor o None si falla.
    """
    for intento in range(intentos_max):
        try:
            # Enviamos la solicitud POST
            response = requests.post(
                API_BASE_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps(transaccion),
                timeout=10  # Tiempo máximo de espera
            )
            
            # Verificamos el código de estado
            if response.status_code == 201:
                return response.json()
            else:
                # Registramos el error con detalles
                logging.error(
                    f"Intento {intento+1} fallido: Código {response.status_code} - {response.text}"
                )
                if response.status_code in [400, 403, 404]:  # Errores no recuperables
                    return None
                # Continuamos con el siguiente intento para errores recuperables
                if intento < intentos_max - 1:
                    time.sleep(pausa_entre_intentos)
                
        except requests.exceptions.RequestException as e:
            # Registramos errores de conexión
            logging.error(f"Intento {intento+1} fallido: Error de conexión - {str(e)}")
            if intento < intentos_max - 1:
                time.sleep(pausa_entre_intentos)
    
    return None

def insertar_datos(n):
    """
    Inserta n transacciones de demostración usando el endpoint POST /transacciones.
    Args:
        n (int): Número de transacciones a insertar.
    """
    print(f"Iniciando inserción de {n} transacciones de demostración...")
    
    for i in range(n):
        # Generamos una transacción
        transaccion = generar_transaccion()
        #print(transaccion)
        
        # Validamos la transacción
        if not validar_transaccion(transaccion):
            print(f"Transacción {i+1} inválida, omitida. Ver errores.log.")
            continue
        
        # Enviamos la transacción con reintentos
        respuesta = enviar_transaccion(transaccion)
        
        if respuesta:
            print(f"Transacción {i+1} insertada: {respuesta['idTransaccion']}")
        else:
            print(f"Error en transacción {i+1}: No se pudo insertar. Ver errores.log.")
        
        # Pausa para evitar límites de tasa
        time.sleep(0.5)
            
    print("Inserción de datos completada.")

def main():
    """
    Función principal para ejecutar el script.
    Pregunta al usuario cuántas transacciones insertar y llama a insertar_datos.
    """
    try:
        # Solicitamos el número de transacciones
        n = int(input("¿Cuántas transacciones de demostración desea insertar? "))
        if n <= 0:
            print("Por favor, ingrese un número positivo.")
            return
        
        # Ejecutamos la inserción
        insertar_datos(n)
        
    except ValueError:
        print("Error: Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()