# Guías Rápidas para Usar DynamoDB, Lambda, API Gateway y Otras Funciones de AWS

Estas guías rápidas te ayudarán a configurar y usar **Amazon DynamoDB**, **AWS Lambda**, **Amazon API Gateway**, y otras funciones comunes de AWS para crear microservicios, utilizando la **consola web de AWS en español** y el **nivel gratuito**. Están diseñadas para principiantes, basadas en tu experiencia con una API de usuarios (tabla **Usuarios**, función Lambda **AdminUsuarios**, y `index.html`). Cada guía incluye pasos esenciales, un ejemplo práctico, y consejos para evitar errores como **403 Forbidden** o `httpMethod`.

---

## Tabla de Contenidos

1. Guía Rápida: Usar Amazon DynamoDB
2. Guía Rápida: Usar AWS Lambda
3. Guía Rápida: Usar Amazon API Gateway
4. Guía Rápida: Otras Funciones Comunes de AWS
5. Consejos Generales

---

## Guía Rápida: Usar Amazon DynamoDB

**Propósito**: Crear y gestionar una tabla DynamoDB para almacenar datos (por ejemplo, usuarios).

**Pasos**:

1. **Accede a DynamoDB**:
   - Ve a aws.amazon.com/es, inicia sesión, busca **DynamoDB** &gt; **Tablas**.
2. **Crea una tabla**:
   - Clic en **Crear tabla**.
   - Nombre: `Usuarios`.
   - Clave de partición: `id` (tipo Cadena).
   - Configuración: **Capacidad bajo demanda** (gratis para bajas cargas).
   - Clic en **Crear tabla**.
3. **Inserta un dato manualmente** (opcional):
   - Selecciona **Usuarios** &gt; **Explorar elementos** &gt; **Crear elemento**.
   - Añade: `id: "1"`, `nombre: "Ana"`, `correo: "ana@ejemplo.com"`.
   - Clic en **Crear elemento**.
4. **Confirma el ARN**:
   - En **Detalles de la tabla**, copia el ARN (por ejemplo, `arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios`).

**Ejemplo práctico**:

- Tabla **Usuarios** para almacenar registros con `id`, `nombre`, y `correo`.
- Usa esta tabla con Lambda para insertar datos (ver Guía Lambda).

**Consejos**:

- Verifica que el nombre sea **Usuarios** (sensible a mayúsculas) para evitar errores como `Table does not exist`.
- Usa `us-east-1` para mantener consistencia con otros servicios.
- Revisa el ARN para permisos en Lambda (Guía Lambda, Paso 3).

**Conexión con tu experiencia**:

- Creaste una tabla similar el 31 de marzo y 3 de abril de 2025 para un microservicio bancario. Esta guía simplifica esos pasos.

---

## Guía Rápida: Usar AWS Lambda

**Propósito**: Crear una función Lambda para procesar datos y escribir en DynamoDB.

**Pasos**:

1. **Accede a Lambda**:
   - Busca **Lambda** &gt; **Funciones** &gt; **Crear función**.
2. **Configura la función**:
   - Selecciona **Crear desde cero**.
   - Nombre: `AdminUsuarios`.
   - Runtime: **Python 3.12**.
   - Clic en **Crear función**.
3. **Añade permisos**:
   - En **Configuración** &gt; **Permisos**, haz clic en el rol (por ejemplo, `AdminUsuarios-role-xxx`).
   - En **IAM**, añade esta política (ajusta `CUENTA_ID`):

     ```json
     {
         "Version": "2012-10-17",
         "Statement": [
             {
                 "Effect": "Allow",
                 "Action": ["dynamodb:PutItem"],
                 "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
             },
             {
                 "Effect": "Allow",
                 "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                 "Resource": "*"
             }
         ]
     }
     ```
   - Guarda la política.
4. **Añade código**:
   - En **Código**, pega:

     ```python
     import json
     import boto3
     import uuid
     
     dynamodb = boto3.resource('dynamodb')
     table = dynamodb.Table('Usuarios')
     
     def lambda_handler(event, context):
         if 'httpMethod' not in event:
             return {'statusCode': 400, 'body': json.dumps({'mensaje': 'Falta httpMethod'})}
         if event['httpMethod'] == 'POST':
             body = json.loads(event['body'])
             item = {
                 'id': str(uuid.uuid4()),
                 'nombre': body['nombre'],
                 'correo': body['correo']
             }
             table.put_item(Item=item)
             return {'statusCode': 200, 'body': json.dumps(item)}
         return {'statusCode': 400, 'body': json.dumps({'mensaje': 'Método no soportado'})}
     ```
   - Clic en **Deploy**.
5. **Prueba la función**:
   - En **Probar**, crea un evento:

     ```json
     {
         "httpMethod": "POST",
         "body": "{\"nombre\": \"Lucía\", \"correo\": \"lucia@ejemplo.com\"}"
     }
     ```
   - Clic en **Probar**. Deberías ver un `statusCode: 200`.

**Ejemplo práctico**:

- Inserta un usuario en la tabla **Usuarios** con un ID único, nombre, y correo.

**Consejos**:

- Verifica permisos para evitar **AccessDenied** (como tu error **403 Forbidden**).
- Usa CloudWatch (**Monitor** &gt; **Ver registros**) para depurar errores como `httpMethod` (enfrentado el 7 de abril).
- Asegúrate de que la tabla sea **Usuarios** (sensible a mayúsculas).

**Conexión con tu experiencia**:

- Similar a tus funciones Lambda para microservicios bancarios (31 de marzo y 7 de abril). Incluye validación de `httpMethod` para evitar errores previos.

---

## Guía Rápida: Usar Amazon API Gateway

**Propósito**: Exponer la función Lambda como una API RESTful accesible desde una página web.

**Pasos**:

1. **Accede a API Gateway**:
   - Busca **API Gateway** &gt; **Crear API** &gt; **REST API** &gt; **Construir**.
2. **Configura la API**:
   - Nombre: `APIUsuarios`.
   - Tipo: **Regional**.
   - Clic en **Crear API**.
3. **Crea recursos y métodos**:
   - Clic en **Acciones** &gt; **Crear recurso**.
   - Nombre: `usuarios`, Ruta: `/usuarios`.
   - Clic en **Crear recurso**.
   - Selecciona `/usuarios`, clic en **Acciones** &gt; **Crear método** &gt; **POST**.
   - Integración: **Lambda**, Región: `us-east-1`, Función: `AdminUsuarios`.
   - Clic en **Guardar**.
4. **Configura CORS**:
   - En `/usuarios`, selecciona **POST** &gt; **Configuración de CORS**.
   - Origen: `*`, Encabezados: `Content-Type`, Métodos: `POST,OPTIONS`.
   - Marca **Habilitar CORS** &gt; **Guardar**.
   - En **CORS** (menú principal), configura lo mismo y guarda.
5. **Despliega la API**:
   - Clic en **Acciones** &gt; **Desplegar API**.
   - Etapa: **$default** &gt; **Desplegar**.
   - Copia la **URL de invocación** (por ejemplo, `https://xxx.execute-api.us-east-1.amazonaws.com`).
6. **Prueba con Postman**:
   - Método: POST
   - URL: `[tu-URL]/usuarios`
   - Cuerpo (JSON):

     ```json
     {"nombre": "Lucía", "correo": "lucia@ejemplo.com"}
     ```
   - Envía. Deberías ver un nuevo usuario.

**Ejemplo práctico**:

- Crea un endpoint POST `/usuarios` para insertar usuarios desde `index.html`.

**Consejos**:

- Configura CORS para evitar errores como **403 Forbidden** (enfrentado el 22 de abril).
- Desactiva **API Key** o **IAM** en **Configuración** si no los usas (Paso 2 de la respuesta anterior).
- Redepliega tras cada cambio.

**Conexión con tu experiencia**:

- Basado en tu API de usuarios (3 y 8 de abril). Incluye CORS para resolver problemas con `index.html`.

---

## Guía Rápida: Otras Funciones Comunes de AWS

**Propósito**: Configurar servicios AWS adicionales útiles para microservicios (S3, SQS, SNS).

### Amazon S3 (Almacenamiento de archivos)

**Pasos**:

1. Busca **S3** &gt; **Crear bucket**.
2. Nombre: `usuarios-archivos-único` (debe ser globalmente único).
3. Región: `us-east-1`, Desmarca **Bloquear acceso público** para pruebas.
4. Clic en **Crear bucket**.
5. Sube un archivo:
   - Selecciona el bucket &gt; **Cargar** &gt; Sube un archivo (por ejemplo, `foto.jpg`).
6. Permisos para Lambda:
   - En **IAM**, añade a la política del rol de **AdminUsuarios**:

     ```json
     {
         "Effect": "Allow",
         "Action": ["s3:PutObject", "s3:GetObject"],
         "Resource": "arn:aws:s3:::usuarios-archivos-único/*"
     }
     ```
7. Prueba desde Lambda:
   - Añade al código Lambda:

     ```python
     s3 = boto3.client('s3')
     s3.upload_file('local_file.txt', 'usuarios-archivos-único', 'test.txt')
     ```
   - Despliega y prueba.

**Ejemplo**: Almacena fotos de usuarios en S3.

**Consejos**: Habilita acceso público solo para pruebas; usa políticas estrictas en producción.

### Amazon SQS (Colas de mensajes)

**Pasos**:

1. Busca **SQS** &gt; **Crear cola** &gt; **Estándar**.
2. Nombre: `ColaUsuarios`.
3. Clic en **Crear cola**.
4. Permisos para Lambda:
   - Añade al rol:

     ```json
     {
         "Effect": "Allow",
         "Action": ["sqs:SendMessage"],
         "Resource": "arn:aws:sqs:us-east-1:CUENTA_ID:ColaUsuarios"
     }
     ```
5. Envía un mensaje desde Lambda:
   - Añade:

     ```python
     sqs = boto3.client('sqs')
     sqs.send_message(QueueUrl='[URL-de-la-cola]', MessageBody=json.dumps({'id': '1', 'nombre': 'Ana'}))
     ```
   - Despliega y prueba.

**Ejemplo**: Encola notificaciones de nuevos usuarios.

**Consejos**: Copia la **URL de la cola** desde SQS para el código.

### Amazon SNS (Notificaciones)

**Pasos**:

1. Busca **SNS** &gt; **Crear tema**.
2. Nombre: `NotificacionesUsuarios`.
3. Clic en **Crear tema**.
4. Suscribe un correo:
   - En el tema, clic en **Crear suscripción** &gt; Protocolo: **Correo electrónico**, Endpoint: tu correo.
   - Confirma la suscripción desde el correo recibido.
5. Permisos para Lambda:
   - Añade al rol:

     ```json
     {
         "Effect": "Allow",
         "Action": ["sns:Publish"],
         "Resource": "arn:aws:sns:us-east-1:CUENTA_ID:NotificacionesUsuarios"
     }
     ```
6. Publica desde Lambda:
   - Añade:

     ```python
     sns = boto3.client('sns')
     sns.publish(TopicArn='[ARN-del-tema]', Message='Nuevo usuario: Ana')
     ```
   - Despliega y prueba.

**Ejemplo**: Envía correos cuando se crea un usuario.

**Consejos**: Usa el **ARN del tema** desde SNS.

**Conexión con tu experiencia**:

- Inspirado en tu interés en microservicios bancarios (26 de marzo) donde mencionaste SQS y SNS para notificaciones.

---

## Consejos Generales

- **Evita errores de permisos**: Siempre verifica los ARNs y añade permisos específicos (como `dynamodb:PutItem`, `s3:PutObject`).
- **Depura con CloudWatch**: Revisa logs en **Lambda** &gt; **Monitor** &gt; **Ver registros** para errores como **AccessDenied** o `httpMethod`.
- **Prueba con Postman**: Usa tu URL de API Gateway (por ejemplo, `https://18k7rgh8uj.execute-api.us-east-1.amazonaws.com/usuarios`) para probar POST:

  ```json
  {"nombre": "Lucía", "correo": "lucia@ejemplo.com"}
  ```
- **Usa servidor local**: Para `index.html`, ejecuta `python -m http.server 8000` y abre `http://localhost:8000` para evitar errores de CORS.
- **Mantén el nivel gratuito**: Usa **Capacidad bajo demanda** en DynamoDB y evita recursos intensivos.
- **Región consistente**: Usa `us-east-1` para todos los servicios.

**Conexión con tu experiencia**:

- Estas guías simplifican las configuraciones de tus microservicios y resuelven errores como **403 Forbidden** y CORS.
- Incluyen pruebas con Postman y Python local (`probar_api.py`, 11 de abril) para alinear con tus métodos de prueba.

---
