# Guía Fácil: Crea tu Microservicio Bancario en AWS desde Cero

## ¡Hola!
Esta guía te enseña a hacer un mini programa en AWS para guardar y ver transacciones bancarias (como depósitos o retiros) usando solo un navegador. No necesitas saber mucho, solo sigue los pasos con calma. ¡Vamos a hacerlo juntos!

## Cosas que necesitas antes de empezar
- **Cuenta en AWS**: Haz una gratis en [aws.amazon.com](https://aws.amazon.com/).
- **Herramientas**: Un navegador (como Chrome) y un editor de texto simple (como el Bloc de Notas).
- **Opcional**: [Postman](https://www.postman.com/) si quieres probar más fácil.

---

## Paso 1: Haz un lugar para guardar datos (DynamoDB)
### ¿Qué es esto?
Vamos a crear una "caja" en AWS llamada **DynamoDB** donde guardaremos las transacciones, como un cuaderno digital.

### ¿Cómo lo hago?
1. **Entra a AWS**:
   - Ve a [console.aws.amazon.com](https://console.aws.amazon.com/) y pon tu usuario y contraseña.
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
Ya tienes tu caja lista. Aquí guardarás cosas como:
```json
{
  "cuenta": "12345",
  "tipo": "deposito",
  "monto": 100
}
```

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
3. **Pega este código** en el editor:
```python
import json
import boto3
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TransaccionesBancarias')

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        query_params = event.get('queryStringParameters', {}) or {}
        cuenta = query_params.get('cuenta')
        
        if not cuenta:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Falta el número de cuenta'})}
        
        response = table.query(
            KeyConditionExpression='cuenta = :cuenta',
            ExpressionAttributeValues={':cuenta': cuenta}
        )
        
        return {'statusCode': 200, 'body': json.dumps({'transacciones': response.get('Items', [])})}
    
    elif http_method == 'POST':
        body = json.loads(event['body'])
        cuenta = body.get('cuenta')
        tipo = body.get('tipo')
        monto = float(body.get('monto'))
        
        item = {
            'cuenta': cuenta,
            'idTransaccion': str(uuid4()),
            'tipo': tipo,
            'monto': monto,
            'fecha': datetime.utcnow().isoformat()
        }
        
        table.put_item(Item=item)
        return {'statusCode': 201, 'body': json.dumps({'message': 'Transacción guardada'})}
    
    return {'statusCode': 400, 'body': json.dumps({'message': 'Método no funciona'})}
```
4. **Guarda el código**:
   - Haz clic en **Deploy**.

### ¡Lo lograste!
Tu programa ya sabe qué hacer. Puede guardar y buscar transacciones.

---

## Paso 3: Dale permisos al programa (IAM)
1. **Ve a IAM**:
   - Busca "IAM" en AWS y entra.
2. **Crea un permiso**:
   - Haz clic en **Roles > Crear rol**.
   - Elige **AWS Service > Lambda**.
   - Marca `AWSLambdaBasicExecutionRole` y `AmazonDynamoDBFullAccess`.
   - **Nombre**: `LambdaBancaRole`.
   - Haz clic en **Crear rol**.
3. **Conéctalo a Lambda**:
   - Vuelve a Lambda > `BancaMicroservicio`.
   - En **Configuración > Permisos**, cambia el rol por `LambdaBancaRole`.

---

## Paso 4: Haz una dirección web (API Gateway)
1. **Ve a API Gateway**:
   - Busca "API Gateway" y entra.
2. **Crea tu dirección**:
   - Haz clic en **Crear API > API REST > Nueva API**.
   - **Nombre**: `BancaAPI`.
   - Crea un recurso `/transacciones`.
3. **Conéctalo a Lambda**:
   - Crea los métodos `GET` y `POST`.
   - Habilita **CORS**.
   - Despliega la API y copia la URL.

---

## Paso 5: Usa tu programa desde el navegador
Guarda este código como `index.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Guardar Transacción</title>
</head>
<body>
    <h1>Guarda una Transacción</h1>
    <form id="miFormulario">
        <input type="text" id="cuenta" required placeholder="Cuenta">
        <select id="tipo"><option value="deposito">Depósito</option><option value="retiro">Retiro</option></select>
        <input type="number" id="monto" step="0.01" required placeholder="Monto">
        <button type="submit">Guardar</button>
    </form>
</body>
</html>
```
### ¡Listo! Ahora puedes probar tu microservicio.

