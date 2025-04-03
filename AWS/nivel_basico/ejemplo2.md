# Guía Fácil: Crea tu Microservicio Bancario en AWS desde Cero

¡Hola! Esta guía te enseña a hacer un mini programa en AWS para guardar y ver transacciones bancarias (como depósitos o retiros) usando solo un navegador. No necesitas saber mucho, solo sigue los pasos con calma. ¡Vamos a hacerlo juntos!

---

## Cosas que necesitas antes de empezar
- **Cuenta en AWS**: Haz una gratis en [aws.amazon.com](https://aws.amazon.com).
- **Herramientas**: Un navegador (como Chrome) y un editor de texto simple (como el Bloc de Notas).
- **Opcional**: Postman (bájalo en [postman.com](https://www.postman.com)) si quieres probar más fácil.

---

## Paso 1: Haz un lugar para guardar datos (DynamoDB)

### ¿Qué es esto?
Vamos a crear una "caja" en AWS llamada **DynamoDB** donde guardaremos las transacciones, como un cuaderno digital.

### ¿Cómo lo hago?
1. **Entra a AWS**:
   - Ve a [console.aws.amazon.com](https://console.aws.amazon.com) y pon tu usuario y contraseña.
2. **Busca DynamoDB**:
   - Arriba, en la barra de búsqueda, escribe "DynamoDB" y haz clic en él.
3. **Crea tu caja**:
   - Haz clic en **Crear tabla**.
   - **Nombre**: Escribe `TransaccionesBancarias`.
   - **Clave de partición**: Escribe `cuenta` y elige "String" (es como el número de cuenta).
   - **Clave de ordenación**: Escribe `idTransaccion` y elige "String" (un número especial para cada transacción).
   - **Capacidad**: Marca "Capacidad bajo demanda" (es gratis para empezar).
   - Haz clic en **Crear tabla**.
4. **Espera un poquito**:
   - Verás "Activa" cuando esté lista.

### ¡Lo lograste!
- ¡Ya tienes tu caja lista! Aquí guardarás cosas como `{ "cuenta": "12345", "tipo": "deposito", "monto": 100 }`. Es el primer paso para tu programa.

---

## Paso 2: Crea el cerebro del programa (Lambda)

### ¿Qué es esto?
Vamos a hacer un programa en **AWS Lambda** que guarda transacciones y las busca cuando quieras.

### ¿Cómo lo hago?
1. **Ve a Lambda**:
   - En AWS, busca "Lambda" y entra.
2. **Crea tu programa**:
   - Haz clic en **Crear función**.
   - Elige **Crear desde cero**.
   - **Nombre**: Escribe `BancaMicroservicio`.
   - **Runtime**: Elige "Python 3.9" (o el más nuevo).
   - Haz clic en **Crear función**.
3. **Pega este código**:
   - En el editor (donde dice "Código fuente"), borra todo y copia esto:

```python
import json
import boto3
from uuid import uuid4
from datetime import datetime

# Conecta con la caja de datos
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TransaccionesBancarias')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        # Busca transacciones
        try:
            query_params = event.get('queryStringParameters', {}) or {}
            cuenta = query_params.get('cuenta')
            
            if not cuenta:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Falta el número de cuenta en la dirección'}),
                    'headers': {'Content-Type': 'application/json'}
                }
            
            response = table.query(
                KeyConditionExpression='cuenta = :cuenta',
                ExpressionAttributeValues={':cuenta': cuenta}
            )
            transacciones = response.get('Items', [])
            
            if transacciones:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'transacciones': transacciones}),
                    'headers': {'Content-Type': 'application/json'}
                }
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No hay transacciones para esa cuenta'}),
                'headers': {'Content-Type': 'application/json'}
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': f'Error al buscar: {str(e)}'}),
                'headers': {'Content-Type': 'application/json'}
            }
    
    elif http_method == 'POST':
        # Guarda una transacción
        try:
            body = json.loads(event['body'])
            cuenta = body.get('cuenta')
            tipo = body.get('tipo')  # "deposito" o "retiro"
            monto = float(body.get('monto'))
            
            if not all([cuenta, tipo, monto]) or tipo not in ['deposito', 'retiro'] or monto <= 0:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Algo está mal o falta información'}),
                    'headers': {'Content-Type': 'application/json'}
                }
            
            item = {
                'cuenta': cuenta,
                'idTransaccion': str(uuid4()),
                'tipo': tipo,
                'monto': monto,
                'fecha': datetime.utcnow().isoformat()
            }
            
            table.put_item(Item=item)
            
            return {
                'statusCode': 201,
                'body': json.dumps({
                    'message': 'Transacción guardada',
                    'idTransaccion': item['idTransaccion']
                }),
                'headers': {'Content-Type': 'application/json'}
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': f'Error al guardar: {str(e)}'}),
                'headers': {'Content-Type': 'application/json'}
            }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Método no funciona'}),
        'headers': {'Content-Type': 'application/json'}
    }
