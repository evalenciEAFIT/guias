# Explicación del Código Python para Enviar Transacciones

Este script de Python está diseñado para generar y enviar datos de transacciones financieras ficticias a un API Gateway específico. A continuación, se detalla cada parte del código:

## 1. Importación de Bibliotecas

```python
import requests  # Para realizar solicitudes HTTP (enviar datos al API)
import random    # Para generar datos aleatorios (cuentas, montos, tipos, descripciones)
import json      # Para convertir los diccionarios de Python a formato JSON
import time      # Para introducir pausas (ej., entre reintentos o envíos)
import logging   # Para registrar errores en un archivo
import uuid      # Para generar identificadores únicos para cada transacción
from datetime import datetime # Aunque importada, no se usa explícitamente en el código final
from decimal import Decimal   # Aunque importada, no se usa explícitamente en el código final
```

Se importan las bibliotecas necesarias para diversas funcionalidades: comunicación web, aleatoriedad, manejo de datos JSON, control de tiempo, registro de eventos y generación de IDs únicos.

2. Configuración del Logging
```python
logging.basicConfig(
    filename='errores.log',      # Nombre del archivo donde se guardarán los errores
    level=logging.ERROR,         # Nivel de severidad (solo se registran errores o superiores)
    format='%(asctime)s - %(levelname)s - %(message)s' # Formato de cada línea de log
)
```
Se configura el sistema de registro (logging) para que cualquier error (level=logging.ERROR) que ocurra durante la ejecución se guarde en el archivo errores.log. El formato incluye la fecha/hora, el nivel del mensaje (ERROR) y el mensaje de error en sí.

3. Constantes de Configuración
```python
# URL base del API Gateway
API_BASE_URL = "[https://mexvlbd2a9.execute-api.us-east-1.amazonaws.com/transacciones](https://mexvlbd2a9.execute-api.us-east-1.amazonaws.com/transacciones)"

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
```
Se definen constantes para:

API_BASE_URL: La dirección web (endpoint) a la que se enviarán las transacciones.

CUENTAS: Una lista de identificadores de cuentas bancarias ficticias.

TIPOS_TRANSACCION: Los tipos válidos de transacción (depósito o retiro).

DESCRIPCIONES: Descripciones comunes para las transacciones.

4. Función validar_transaccion(transaccion)
```python
def validar_transaccion(transaccion):
    # ... (lógica de validación) ...
```
Esta función recibe un diccionario transaccion y verifica si cumple con ciertos criterios:

Campos requeridos: Comprueba que existan las claves idCuenta, monto, tipo, y descripcion.

idCuenta válido: Verifica que el idCuenta esté en la lista CUENTAS.

monto válido: Asegura que el monto sea un número (entero o flotante) y sea mayor que cero.

tipo válido: Confirma que el tipo esté en la lista TIPOS_TRANSACCION.

descripcion válida: Verifica que la descripcion no esté vacía.

Si alguna validación falla, registra un error detallado en errores.log y devuelve False. Si todo es correcto, devuelve True. Incluye un bloque try...except para capturar cualquier error inesperado durante la validación.

5. Función generar_transaccion()
```python
def generar_transaccion():
    return {
        'idTransaccion': str(uuid.uuid4()), # ID único universal
        "idCuenta": random.choice(CUENTAS),  # Elige una cuenta al azar
        "monto": round(random.uniform(10, 1000), 2), # Monto aleatorio entre 10.00 y 1000.00
        "tipo": random.choice(TIPOS_TRANSACCION),  # Elige un tipo al azar
        "descripcion": random.choice(DESCRIPCIONES) # Elige una descripción al azar
    }
```

Esta función crea un diccionario que representa una transacción con datos aleatorios:

Genera un idTransaccion único usando uuid.uuid4().

Selecciona aleatoriamente una idCuenta de la lista CUENTAS.

Genera un monto decimal aleatorio entre 10 y 1000, redondeado a 2 decimales.

Selecciona aleatoriamente un tipo de la lista TIPOS_TRANSACCION.

Selecciona aleatoriamente una descripcion de la lista DESCRIPCIONES.

Devuelve el diccionario con la transacción generada.

6. Función enviar_transaccion(transaccion, intentos_max=3, pausa_entre_intentos=1)
```python
def enviar_transaccion(transaccion, intentos_max=3, pausa_entre_intentos=1):
    # ... (lógica de envío con reintentos) ...
```
Esta función intenta enviar la transaccion (previamente validada y generada) al API_BASE_URL usando una solicitud HTTP POST.

Reintentos: Intenta enviar la transacción hasta intentos_max veces (por defecto 3) si ocurren ciertos errores.

Pausa: Espera pausa_entre_intentos segundos (por defecto 1) entre intentos fallidos.

Envío: Usa requests.post para enviar los datos en formato JSON. Establece un timeout de 10 segundos.

Manejo de Respuesta:

Si el servidor responde con el código de estado 201 (Creado), significa que la transacción fue aceptada, y la función devuelve la respuesta del servidor (en formato JSON).

Si responde con 400, 403, o 404, son errores del cliente o no encontrados que probablemente no se solucionarán reintentando, así que registra el error y devuelve None.

Para otros códigos de error (ej. errores del servidor 5xx), registra el error y reintenta si quedan intentos.

Manejo de Excepciones: Captura errores de conexión (requests.exceptions.RequestException), los registra y reintenta.

Si todos los intentos fallan, devuelve None.

7. Función insertar_datos(n)
```python
def insertar_datos(n):
    # ... (lógica de inserción en bucle) ...
```
Esta función orquesta el proceso de generar e insertar n transacciones.

Inicia un bucle que se repite n veces.

En cada iteración:

Llama a generar_transaccion() para crear una nueva transacción.

Llama a validar_transaccion() para verificarla. Si no es válida, imprime un mensaje, registra el error (hecho dentro de validar_transaccion) y pasa a la siguiente iteración (continue).

Si es válida, llama a enviar_transaccion() para enviarla al API.

Imprime un mensaje indicando si la transacción se insertó correctamente (mostrando su ID) o si hubo un error.

Hace una pausa de 0.5 segundos (time.sleep(0.5)) para no sobrecargar el API (evitar "rate limiting").

Al final, imprime un mensaje indicando que la inserción ha terminado.

8. Función main()
```python
def main():
    try:
        n = int(input("¿Cuántas transacciones de demostración desea insertar? "))
        if n <= 0:
            print("Por favor, ingrese un número positivo.")
            return
        insertar_datos(n)
    except ValueError:
        print("Error: Por favor, ingrese un número válido.")
```
Es la función principal que se ejecuta cuando corre el script.

Pide al usuario que ingrese cuántas transacciones desea generar e insertar.

Convierte la entrada a un número entero (int).

Verifica si el número es positivo. Si no, muestra un mensaje y termina.

Si el número es válido, llama a insertar_datos(n) para iniciar el proceso.

Usa un try...except ValueError para manejar el caso en que el usuario ingrese algo que no sea un número válido.

9. Bloque de Ejecución Principal
10. 
```python
if __name__ == "__main__":
    main()
```
Esta es una construcción estándar en Python. Asegura que la función main() solo se ejecute cuando el script es corrido directamente (no cuando es importado como un módulo por otro script).

```python
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
API_BASE_URL = "https://mexvlbd2a9.execute-api.us-east-1.amazonaws.com/transacciones"

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
        "monto": round(random.uniform(10, 1000), 2),  # Monto entre 10 y 1000
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
```
