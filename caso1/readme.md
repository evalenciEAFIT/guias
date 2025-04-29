# Guía Paso a Paso para Crear un Microservicio en AWS con CRUD en una Única Función Lambda (Python)

Esta guía detalla cómo crear un microservicio en AWS para gestionar transacciones bancarias con operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando exclusivamente la consola web de AWS. Usaremos DynamoDB para almacenar datos, una única función Lambda con Python para todas las operaciones CRUD, API Gateway para exponer endpoints HTTP, y IAM para permisos. El archivo `lambda_function.py` estará bien comentado y manejará todas las operaciones.

---

## Prerrequisitos

- Cuenta activa de AWS con permisos administrativos.
- Conocimientos básicos de Python y APIs REST.
- Acceso a un editor de texto (ej. Notepad++ o Visual Studio Code) para escribir el código de Lambda.
- Postman o un navegador para probar los endpoints.

---

## Arquitectura

- **Amazon DynamoDB**: Almacena las transacciones bancarias.
- **AWS Lambda**: Una única función (`transaccionesBancarias`) ejecuta todas las operaciones CRUD en Python 3.12, usando un solo archivo `lambda_function.py`.
- **Amazon API Gateway**: Expone los endpoints HTTP (GET, POST, PUT, DELETE).
- **AWS IAM**: Gestiona permisos para que Lambda acceda a DynamoDB.
- **Amazon CloudWatch**: Registra logs automáticamente.

---

## Paso 1: Crear la Tabla en DynamoDB

1. **Accede a la consola de AWS**:

   - Inicia sesión en https://aws.amazon.com/es/console/.
   - En la barra de búsqueda, escribe **DynamoDB** y selecciona el servicio.

2. **Crear una tabla**:

   - Haz clic en **Crear tabla**.
   - Nombre de la tabla: `TransaccionesBancarias`.
   - Clave de partición: `idTransaccion` (tipo: Cadena).
   - Clave de ordenación: `idCuenta` (tipo: Cadena).
   - Configuración: Selecciona **Capacidad bajo demanda** para escalabilidad automática.
   - Haz clic en **Crear tabla**.

3. **Estructura de datos**: Cada transacción tendrá:

   - `idTransaccion`: Identificador único (UUID, String).
   - `idCuenta`: ID de la cuenta bancaria (String, ej. "CUENTA123").
   - `monto`: Monto de la transacción (Number).
   - `tipo`: Tipo de transacción (String, ej. "DEPOSITO", "RETIRO").
   - `fechaHora`: Fecha y hora (String, ISO 8601).
   - `descripcion`: Detalle de la transacción (String).

---

## Paso 2: Crear la Función Lambda

Crearemos una única función Lambda llamada `transaccionesBancarias` que manejará todas las operaciones CRUD en un solo archivo `lambda_function.py`.

1. **Accede a Lambda**:

   - En la consola de AWS, busca **Lambda** y selecciona el servicio.

2. **Crear la función**:

   - Haz clic en **Crear función**.
   - Selecciona **Crear desde cero**.
   - Nombre de la función: `transaccionesBancarias`.
   - Runtime: **Python 3.12**.
   - Rol de ejecución: Selecciona **Crear un nuevo rol con permisos básicos de Lambda** (lo ajustaremos luego).
   - Haz clic en **Crear función**.

3. **Agregar el código**:

   - Ve a la pestaña **Código** y pega el siguiente código en el archivo `lambda_function.py`. El código está diseñado para manejar las operaciones CRUD basándose en el método HTTP y la ruta, con comentarios detallados.

   **transaccionesBancarias/lambda_function.py**:

   ```python
   # Importamos las bibliotecas necesarias
   import json
   import boto3
   import uuid
   from datetime import datetime
   from decimal import Decimal
   
   # Inicializamos el cliente de DynamoDB
   dynamodb = boto3.resource('dynamodb')
   table = dynamodb.Table('TransaccionesBancarias')
   
   def lambda_handler(event, context):
       """
       Función Lambda única para manejar todas las operaciones CRUD de transacciones bancarias.
       Determina la operación (Crear, Leer, Actualizar, Eliminar) según el método HTTP y la ruta.
       - POST /transacciones: Crea una nueva transacción.
       - GET /transacciones/{idTransaccion}/{idCuenta}: Obtiene una transacción específica.
       - PUT /transacciones/{idTransaccion}/{idCuenta}: Actualiza una transacción.
       - DELETE /transacciones/{idTransaccion}/{idCuenta}: Elimina una transacción.
       """
       try:
           # Extraemos el método HTTP y la ruta del evento
           http_method = event['httpMethod']
           path = event['path']
   
           # Operación CREAR: POST /transacciones
           if http_method == 'POST' and path == '/transacciones':
               # Parseamos el cuerpo del evento (JSON) para obtener los datos
               body = json.loads(event['body'])
               id_cuenta = body['idCuenta']  # ID de la cuenta bancaria
               monto = Decimal(str(body['monto']))  # Monto de la transacción
               tipo = body['tipo']  # Tipo de transacción (DEPOSITO, RETIRO)
               descripcion = body['descripcion']  # Descripción de la transacción
   
               # Creamos el item para DynamoDB con un ID único y la fecha actual
               item = {
                   'idTransaccion': str(uuid.uuid4()),  # Generamos un UUID único
                   'idCuenta': id_cuenta,
                   'monto': monto,
                   'tipo': tipo,
                   'fechaHora': datetime.utcnow().isoformat(),  # Fecha en formato ISO
                   'descripcion': descripcion
               }
   
               # Guardamos el item en la tabla
               table.put_item(Item=item)
   
               # Retornamos una respuesta exitosa
               return {
                   'statusCode': 201,
                   'body': json.dumps({
                       'mensaje': 'Transacción creada',
                       'idTransaccion': item['idTransaccion']
                   })
               }
   
           # Operación LEER: GET /transacciones/{idTransaccion}/{idCuenta}
           elif http_method == 'GET' and path.startswith('/transacciones/'):
               # Extraemos los parámetros de la ruta
               id_transaccion = event['pathParameters']['idTransaccion']
               id_cuenta = event['pathParameters']['idCuenta']
   
               # Buscamos el item en la tabla usando la clave primaria
               response = table.get_item(
                   Key={
                       'idTransaccion': id_transaccion,
                       'idCuenta': id_cuenta
                   }
               )
   
               # Verificamos si el item existe
               if 'Item' not in response:
                   return {
                       'statusCode': 404,
                       'body': json.dumps({'mensaje': 'Transacción no encontrada'})
                   }
   
               # Retornamos el item encontrado
               return {
                   'statusCode': 200,
                   'body': json.dumps(response['Item'])
               }
   
           # Operación ACTUALIZAR: PUT /transacciones/{idTransaccion}/{idCuenta}
           elif http_method == 'PUT' and path.startswith('/transacciones/'):
               # Extraemos los parámetros de la ruta y el cuerpo
               id_transaccion = event['pathParameters']['idTransaccion']
               id_cuenta = event['pathParameters']['idCuenta']
               body = json.loads(event['body'])
               monto = body['monto']
               descripcion = body['descripcion']
   
               # Actualizamos el item en la tabla
               response = table.update_item(
                   Key={
                       'idTransaccion': id_transaccion,
                       'idCuenta': id_cuenta
                   },
                   UpdateExpression='SET monto = :m, descripcion = :d',
                   ExpressionAttributeValues={
                       ':m': monto,
                       ':d': descripcion
                   },
                   ReturnValues='UPDATED_NEW'
               )
   
               # Retornamos una respuesta exitosa
               return {
                   'statusCode': 200,
                   'body': json.dumps({
                       'mensaje': 'Transacción actualizada',
                       'atributosActualizados': response['Attributes']
                   })
               }
   
           # Operación ELIMINAR: DELETE /transacciones/{idTransaccion}/{idCuenta}
           elif http_method == 'DELETE' and path.startswith('/transacciones/'):
               # Extraemos los parámetros de la ruta
               id_transaccion = event['pathParameters']['idTransaccion']
               id_cuenta = event['pathParameters']['idCuenta']
   
               # Eliminamos el item de la tabla
               table.delete_item(
                   Key={
                       'idTransaccion': id_transaccion,
                       'idCuenta': id_cuenta
                   }
               )
   
               # Retornamos una respuesta exitosa
               return {
                   'statusCode': 200,
                   'body': json.dumps({'mensaje': 'Transacción eliminada'})
               }
   
           # Si el método o la ruta no coinciden, retornamos un error
           else:
               return {
                   'statusCode': 400,
                   'body': json.dumps({'error': 'Método o ruta no soportados'})
               }
   
       except Exception as e:
           # En caso de error general, retornamos un código 500
           return {
               'statusCode': 500,
               'body': json.dumps({'error': str(e)})
           }
   ```

4. **Publicar los cambios**:

   - Haz clic en **Implementar** para guardar el código.
   - Nota: No necesitamos capas adicionales porque `boto3` y `uuid` están incluidos en el entorno de Python 3.12 de Lambda.

---

## Paso 3: Configurar Permisos IAM

La función Lambda necesita permisos para acceder a DynamoDB y escribir logs en CloudWatch.

1. **Accede a IAM**:

   - En la consola de AWS, busca **IAM** y selecciona el servicio.

2. **Encontrar el rol de Lambda**:

   - Ve a **Roles**.
   - Busca el rol creado automáticamente para la función Lambda (ej. `transaccionesBancarias-role-xxx`).
   - Selecciona el rol.

3. **Agregar permisos para DynamoDB**:

   - Haz clic en **Adjuntar políticas** &gt; **Crear política**.
   - Selecciona **JSON** y pega:

     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": [
                     "dynamodb:PutItem",
                     "dynamodb:GetItem",
                     "dynamodb:UpdateItem",
                     "dynamodb:DeleteItem"
                 ],
                 "Resource": "arn:aws:dynamodb:*:*:table/TransaccionesBancarias"
             },
             {
                 "Effect": "Allow",
                 "Action": [
                     "logs:CreateLogGroup",
                     "logs:CreateLogStream",
                     "logs:PutLogEvents"
                 ],
                 "Resource": "*"
             }
         ]
     }
     ```
   - Haz clic en **Siguiente**, nombra la política `LambdaDynamoDBPolicy`, y crea la política.
   - Vuelve al rol y adjunta la política `LambdaDynamoDBPolicy`.

---

## Paso 4: Configurar API Gateway

Crearemos una API HTTP para exponer los métodos GET, POST, PUT y DELETE, todos integrados con la única función Lambda.

1. **Accede a API Gateway**:

   - En la consola de AWS, busca **API Gateway** y selecciona el servicio.

2. **Crear una API HTTP**:

   - Haz clic en **Crear API** &gt; **API HTTP** &gt; **Construir**.
   - Nombre: `TransaccionesBancariasAPI`.
   - Haz clic en **Siguiente** y **Crear**.

3. **Configurar rutas**:

   - Ve a **Rutas** y crea las siguientes rutas:
     - **POST /transacciones**
     - **GET /transacciones/{idTransaccion}/{idCuenta}**
     - **PUT /transacciones/{idTransaccion}/{idCuenta}**
     - **DELETE /transacciones/{idTransaccion}/{idCuenta}**

4. **Integrar con Lambda**:

   - Para cada ruta:
     - Haz clic en la ruta (ej. POST /transacciones).
     - En **Integración**, selecciona **Lambda** como tipo de integración.
     - Selecciona la función `transaccionesBancarias`.
     - Haz clic en **Crear**.

5. **Mapear parámetros para GET, PUT y DELETE**:

   - Para las rutas GET, PUT y DELETE:
     - Ve a la integración de la ruta.
     - En **Mapeo de solicitud**, selecciona **Editar** y agrega:

       ```json
       {
           "pathParameters": {
               "idTransaccion": "$context.request.path.idTransaccion",
               "idCuenta": "$context.request.path.idCuenta"
           }
       }
       ```

6. **Habilitar CORS**:

   - Ve a **CORS** en la API.
   - Configura:
     - **Origen de acceso**: `*` (para pruebas; usa un dominio específico en producción).
     - **Métodos permitidos**: GET, POST, PUT, DELETE.
     - **Encabezados permitidos**: `*`.
   - Guarda los cambios.

7. **Desplegar la API**:

   - Ve a **Desplegar** &gt; **Crear escenario**.
   - Nombre del escenario: `prod`.
   - Haz clic en **Desplegar**.
   - Copia la URL base de la API (ej. `https://<api-id>.execute-api.<region>.amazonaws.com/prod`).

---

## Paso 5: Probar el Microservicio

1. **Usar Postman o un navegador**:

   - **Crear una transacción** (POST):

     ```http
     POST https://<api-id>.execute-api.<region>.amazonaws.com/prod/transacciones
     Content-Type: application/json
     
     {
         "idCuenta": "CUENTA123",
         "monto": 100,
         "tipo": "DEPOSITO",
         "descripcion": "Depósito inicial"
     }
     ```

     - Respuesta esperada: `{ "mensaje": "Transacción creada", "idTransaccion": "<uuid>" }`

   - **Obtener una transacción** (GET):

     ```http
     GET https://<api-id>.execute-api.<region>.amazonaws.com/prod/transacciones/<idTransaccion>/CUENTA123
     ```

     - Respuesta esperada: `{ "idTransaccion": "...", "idCuenta": "CUENTA123", ... }`

   - **Actualizar una transacción** (PUT):

     ```http
     PUT https://<api-id>.execute-api.<region>.amazonaws.com/prod/transacciones/<idTransaccion>/CUENTA123
     Content-Type: application/json
     
     {
         "monto": 150,
         "descripcion": "Depósito ajustado"
     }
     ```

     - Respuesta esperada: `{ "mensaje": "Transacción actualizada", "atributosActualizados": { ... } }`

   - **Eliminar una transacción** (DELETE):

     ```http
     DELETE https://<api-id>.execute-api.<region>.amazonaws.com/prod/transacciones/<idTransaccion>/CUENTA123
     ```

     - Respuesta esperada: `{ "mensaje": "Transacción eliminada" }`

2. **Verificar en DynamoDB**:

   - Ve a la consola de DynamoDB.
   - Selecciona la tabla `TransaccionesBancarias`.
   - Haz clic en **Explorar elementos** para confirmar que las transacciones se crearon, actualizaron o eliminaron correctamente.

---

## Paso 6: Monitoreo

1. **Revisar logs en CloudWatch**:

   - En la consola de AWS, busca **CloudWatch**.
   - Ve a **Logs** &gt; **Grupos de logs**.
   - Busca `/aws/lambda/transaccionesBancarias`.
   - Revisa los logs para confirmar operaciones o investigar errores.

2. **Métricas de API Gateway**:

   - En API Gateway, ve a **Métricas**.
   - Habilita métricas detalladas en el escenario `prod`.
   - Monitorea latencia y errores (4xx/5xx).

---

## Notas Finales

- Este microservicio usa una única función Lambda para todas las operaciones CRUD, lo que simplifica la arquitectura pero puede ser menos modular. Para producción, considera:
  - Separar las operaciones en funciones individuales para mejor escalabilidad.
  - Agregar autenticación (ej. Amazon Cognito).
  - Implementar validaciones (ej. verificar que `monto` sea positivo).
  - Usar un dominio personalizado en API Gateway.
- Los comentarios en el código explican cada operación para facilitar la comprensión y mantenimiento.
- Si encuentras errores, revisa los logs en CloudWatch o verifica los permisos en IAM.
