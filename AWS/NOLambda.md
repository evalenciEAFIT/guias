# Guía para Acceder a Amazon DynamoDB sin Usar AWS Lambda

Esta guía explica cómo interactuar con **Amazon DynamoDB** sin **AWS Lambda**, utilizando la **consola web de AWS en español** y el **nivel gratuito**. Está diseñada para principiantes y asume una tabla **Usuarios** (clave de partición: `id`, tipo Cadena) en `us-east-1`. Las opciones incluyen la consola de AWS, un programa Python local, Postman con API Gateway, AWS CLI, y el AWS SDK en una aplicación web. Cada método incluye pasos, un ejemplo práctico, y consejos para evitar errores como **403 Forbidden**.

---

## Tabla de Contenidos

1. [Opciones para Acceder a DynamoDB sin Lambda](#opciones-para-acceder-a-dynamodb-sin-lambda)
2. [Método 1: Usar la Consola de AWS](#método-1-usar-la-consola-de-aws)
3. [Método 2: Usar un Programa Python Local](#método-2-usar-un-programa-python-local)
4. [Método 3: Usar Postman con API Gateway](#método-3-usar-postman-con-api-gateway)
5. [Método 4: Usar el AWS CLI](#método-4-usar-el-aws-cli)
6. [Método 5: Usar el AWS SDK desde una Aplicación Web](#método-5-usar-el-aws-sdk-desde-una-aplicación-web)
7. [Consejos para Evitar Errores](#consejos-para-evitar-errores)
8. [Conclusión](#conclusión)

---

## Opciones para Acceder a DynamoDB sin Lambda

Puedes interactuar con DynamoDB directamente usando:

- **Consola de AWS**: Inserta, consulta, o modifica datos manualmente en la interfaz web.
- **Programa Python local**: Usa el AWS SDK (`boto3`) para acceder desde tu máquina.
- **Postman con API Gateway**: Usa una API RESTful (sin Lambda) para interactuar con DynamoDB.
- **AWS CLI**: Ejecuta comandos desde la terminal para operaciones en DynamoDB.
- **AWS SDK en una aplicación web**: Integra DynamoDB en una página web usando el AWS SDK para JavaScript.

**Por qué evitar Lambda**:
- Simplifica la arquitectura para acceso directo.
- Reduce latencia y costos en escenarios simples.
- Útil para pruebas, depuración, o aplicaciones locales.

---

## Método 1: Usar la Consola de AWS

**Descripción**: Inserta datos en la tabla **Usuarios** desde la consola web de AWS.

**Pasos**:

1. **Accede a DynamoDB**:
   - Ve a aws.amazon.com/es, inicia sesión, busca **DynamoDB** > **Tablas** > **Usuarios**.
2. **Inserta un dato**:
   - Clic en **Explorar elementos** > **Crear elemento**.
   - Añade:
     - `id`: `"1"` (Cadena).
     - `nombre`: `"Ana"`.
     - `correo`: `"ana@ejemplo.com"`.
   - Clic en **Crear elemento**.
3. **Verifica el dato**:
   - En **Explorar elementos**, busca el registro con `id: "1"`.

**Ejemplo práctico**:
- Inserta un usuario (`id: "1"`, `nombre: "Ana"`, `correo: "ana@ejemplo.com"`) y confírmalo en la consola.

**Ventajas**:
- No requiere programación ni configuración.
- Ideal para pruebas rápidas o datos iniciales.

**Limitaciones**:
- Manual, no apto para automatización.
- No integrable con aplicaciones web.

**Consejos**:
- Asegúrate de estar en `us-east-1`.
- Verifica que tu usuario IAM tenga permisos `dynamodb:PutItem`.

---

## Método 2: Usar un Programa Python Local

**Descripción**: Usa el AWS SDK (`boto3`) desde un script Python local para insertar datos en DynamoDB.

**Pasos**:

1. **Configura AWS CLI y credenciales**:
   - Instala AWS CLI: `pip install awscli`.
   - Configura credenciales:
     ```bash
     aws configure
     ```
     - Ingresa **Access Key ID**, **Secret Access Key**, región (`us-east-1`), y formato (`json`).
     - Obtén credenciales en **IAM** > **Usuarios** > [tu-usuario] > **Credenciales de seguridad** > **Crear clave de acceso**.
2. **Instala boto3**:
   - Ejecuta: `pip install boto3`.
3. **Crea un script Python**:
   - Crea un archivo `insertar_dynamodb.py`:

     ```python
     import boto3
     from botocore.exceptions import ClientError

     # Cliente de DynamoDB
     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
     table = dynamodb.Table('Usuarios')

     # Insertar un usuario
     try:
         response = table.put_item(
             Item={
                 'id': '2',
                 'nombre': 'Lucía',
                 'correo': 'lucia@ejemplo.com'
             }
         )
         print("Usuario insertado:", response)
     except ClientError as e:
         print("Error:", e.response['Error']['Message'])
     ```
4. **Ejecuta el script**:
   - Corre: `python insertar_dynamodb.py`.
   - Deberías ver: `Usuario insertado: {...}`.
5. **Verifica en la consola**:
   - En **DynamoDB** > **Usuarios** > **Explorar elementos**, busca `id: "2"`.

**Ejemplo práctico**:
- Inserta un usuario (`id: "2"`, `nombre: "Lucía"`, `correo: "lucia@ejemplo.com"`) desde tu máquina.

**Ventajas**:
- Automatizable y flexible.
- Ideal para scripts locales o pruebas.

**Limitaciones**:
- Requiere credenciales seguras.
- Necesita configuración inicial.

**Consejos**:
- Usa un perfil IAM con permisos `dynamodb:PutItem`:

  ```json
  {
      "Effect": "Allow",
      "Action": "dynamodb:PutItem",
      "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
  }
  ```
- Si ves **AccessDenied**, verifica credenciales o permisos.

---

## Método 3: Usar Postman con API Gateway

**Descripción**: Configura una API Gateway que interactúa directamente con DynamoDB (sin Lambda) y pruébala con Postman.

**Pasos**:

1. **Crea una API en API Gateway**:
   - Busca **API Gateway** > **Crear API** > **REST API** > **Construir**.
   - Nombre: `DynamoDBDirect`.
   - Clic en **Crear API**.
2. **Crea un recurso y método**:
   - Clic en **Acciones** > **Crear recurso**.
   - Nombre: `usuarios`, Ruta: `/usuarios`.
   - Selecciona `/usuarios` > **Acciones** > **Crear método** > **POST**.
   - Integración: **AWS Service**.
   - Servicio: **DynamoDB**.
   - Acción: **PutItem**.
   - Región: `us-east-1`.
   - Rol de ejecución: Crea un rol en **IAM** con:

     ```json
     {
         "Effect": "Allow",
         "Action": "dynamodb:PutItem",
         "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
     }
     ```
   - Clic en **Guardar**.
3. **Configura la solicitud de integración**:
   - En **Integración**, selecciona **Solicitud de integración** > **Plantilla de mapeo**.
   - Añade una plantilla para `application/json`:

     ```json
     {
         "TableName": "Usuarios",
         "Item": {
             "id": {"S": "$input.path('$.id')"},
             "nombre": {"S": "$input.path('$.nombre')"},
             "correo": {"S": "$input.path('$.correo')"}
         }
     }
     ```
   - Guarda.
4. **Configura CORS**:
   - En `/usuarios` > **POST** > **Configuración de CORS**:
     - Origen: `*`.
     - Encabezados: `Content-Type`.
     - Métodos: `POST,OPTIONS`.
     - Marca **Habilitar CORS** > **Guardar**.
   - En **CORS** (menú principal), configura lo mismo.
5. **Despliega la API**:
   - Clic en **Acciones** > **Desplegar API** > Etapa: **$default** > **Desplegar**.
   - Copia la **URL de invocación** (por ejemplo, `https://yyy.execute-api.us-east-1.amazonaws.com`).
6. **Prueba con Postman**:
   - Método: POST
   - URL: `[tu-URL]/usuarios`
   - Cuerpo (JSON):

     ```json
     {
         "id": "3",
         "nombre": "Carlos",
         "correo": "carlos@ejemplo.com"
     }
     ```
   - Envía. Deberías ver un `statusCode: 200`.
7. **Verifica en DynamoDB**:
   - En **Usuarios** > **Explorar elementos**, busca `id: "3"`.

**Ejemplo práctico**:
- Inserta un usuario (`id: "3"`, `nombre: "Carlos"`, `correo: "carlos@ejemplo.com"`) usando Postman.

**Ventajas**:
- Integra con aplicaciones web (por ejemplo, una página HTML).
- Ideal para pruebas con herramientas como Postman.

**Limitaciones**:
- Requiere configurar API Gateway.
- Menos flexible para operaciones complejas.

**Consejos**:
- Si ves **403 Forbidden**, verifica el rol de ejecución o CORS.
- Usa la URL en una aplicación web si necesitas integrarla.

---

## Método 4: Usar el AWS CLI

**Descripción**: Ejecuta comandos desde la terminal para insertar datos en DynamoDB.

**Pasos**:

1. **Instala y configura AWS CLI**:
   - Instala: `pip install awscli`.
   - Configura: `aws configure` (ingresa **Access Key ID**, **Secret Access Key**, `us-east-1`, `json`).
2. **Inserta un dato**:
   - Ejecuta:

     ```bash
     aws dynamodb put-item \
         --table-name Usuarios \
         --item '{"id": {"S": "4"}, "nombre": {"S": "Sofía"}, "correo": {"S": "sofia@ejemplo.com"}}' \
         --region us-east-1
     ```
   - Deberías ver una respuesta vacía (`{}`) si es exitoso.
3. **Verifica en DynamoDB**:
   - En **Usuarios** > **Explorar elementos**, busca `id: "4"`.

**Ejemplo práctico**:
- Inserta un usuario (`id: "4"`, `nombre: "Sofía"`, `correo: "sofia@ejemplo.com"`) desde la terminal.

**Ventajas**:
- Rápido para pruebas manuales.
- No requiere código complejo.

**Limitaciones**:
- Sintaxis JSON estricta.
- No integrable con aplicaciones web.

**Consejos**:
- Asegúrate de que tu usuario IAM tenga `dynamodb:PutItem`.
- Si ves **AccessDenied**, revisa las credenciales o permisos.

---

## Método 5: Usar el AWS SDK desde una Aplicación Web

**Descripción**: Integra DynamoDB en una página web usando el AWS SDK para JavaScript, sin Lambda.

**Pasos**:

1. **Configura credenciales seguras**:
   - Crea un usuario IAM con:

     ```json
     {
         "Effect": "Allow",
         "Action": "dynamodb:PutItem",
         "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
     }
     ```
   - Genera una **Access Key ID** y **Secret Access Key**.
   - **Advertencia**: Evita exponer credenciales en el código; usa **AWS Cognito** para producción.
2. **Crea una página web**:
   - Crea un archivo `index.html`:

     ```html
     <!DOCTYPE html>
     <html lang="es">
     <head>
         <meta charset="UTF-8">
         <title>Gestión de Usuarios</title>
         <script src="https://sdk.amazonaws.com/js/aws-sdk-2.1440.0.min.js"></script>
         <style>
             body { font-family: Arial, sans-serif; margin: 20px; }
             .form-group { margin-bottom: 15px; }
             label { display: block; }
             input { padding: 5px; width: 200px; }
             button { padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }
             button:hover { background-color: #0056b3; }
             #resultado { margin-top: 20px; }
         </style>
     </head>
     <body>
         <h1>Gestión de Usuarios</h1>
         <div class="form-group">
             <h3>Crear Usuario</h3>
             <label>Nombre:</label>
             <input type="text" id="nombreCrear">
             <label>Correo:</label>
             <input type="email" id="correoCrear">
             <button onclick="crearUsuario()">Crear</button>
         </div>
         <div id="resultado"></div>
         <script>
             // Configura AWS SDK
             AWS.config.update({
                 region: 'us-east-1',
                 credentials: new AWS.Credentials('TU_ACCESS_KEY', 'TU_SECRET_KEY')
             });
             const dynamodb = new AWS.DynamoDB.DocumentClient();
             async function crearUsuario() {
                 const nombre = document.getElementById('nombreCrear').value;
                 const correo = document.getElementById('correoCrear').value;
                 if (!nombre || !correo) {
                     mostrarResultado('Por favor, completa todos los campos.', 'error');
                     return;
                 }
                 const params = {
                     TableName: 'Usuarios',
                     Item: {
                         id: Date.now().toString(),
                         nombre: nombre,
                         correo: correo
                     }
                 };
                 try {
                     await dynamodb.put(params).promise();
                     mostrarResultado(`Usuario creado: ${nombre}`, 'success');
                 } catch (error) {
                     mostrarResultado(`Error: ${error.message}`, 'error');
                     console.error('Detalles:', error);
                 }
             }
             function mostrarResultado(mensaje, tipo) {
                 const resultado = document.getElementById('resultado');
                 resultado.innerHTML = mensaje;
                 resultado.style.color = tipo === 'error' ? 'red' : 'green';
             }
         </script>
     </body>
     </html>
     ```
3. **Prueba localmente**:
   - Ejecuta un servidor local: `python -m http.server 8000`.
   - Abre `http://localhost:8000`, completa el formulario, y haz clic en **Crear**.
4. **Verifica en DynamoDB**:
   - Busca el nuevo usuario en **Usuarios** > **Explorar elementos**.

**Ejemplo práctico**:
- Inserta un usuario desde la página web sin usar Lambda.

**Ventajas**:
- Integra directamente con una interfaz web.
- Evita la latencia de Lambda y API Gateway.

**Limitaciones**:
- Exponer credenciales en el cliente es inseguro para producción.
- Requiere conocimientos de JavaScript.

**Consejos**:
- Usa **AWS Cognito** para producción:
  - Crea un **User Pool** y **Identity Pool** en **Cognito**.
  - Actualiza el código:

    ```javascript
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: 'TU_IDENTITY_POOL_ID'
    });
    ```
- Si ves **AccessDenied**, verifica los permisos IAM.

---

## Consejos para Evitar Errores

1. **Permisos correctos**:
   - Asegúrate de que el usuario IAM o rol tenga `dynamodb:PutItem` para `arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios`.
   - Ejemplo:

     ```json
     {
         "Effect": "Allow",
         "Action": "dynamodb:PutItem",
         "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
     }
     ```
2. **Región consistente**:
   - Usa `us-east-1` en todos los métodos.
3. **Evita exponer credenciales**:
   - Usa Cognito para el Método 5.
   - Almacena credenciales en `.aws/credentials` para Python y CLI.
4. **Depura con Postman o consola**:
   - Prueba con Postman (Método 3) para confirmar API Gateway.
   - Usa la consola (Método 1) para verificar datos.
5. **Servidor local para web**:
   - Usa `python -m http.server 8000` en el Método 5 para evitar problemas de CORS.
6. **Revisa errores**:
   - **AccessDenied**: Verifica permisos IAM.
   - **403 Forbidden**: Revisa CORS (Método 3) o credenciales.
   - **Table does not exist**: Confirma el nombre **Usuarios** y región.

---

## Conclusión

Puedes acceder a **DynamoDB** sin Lambda usando la consola de AWS, un programa Python local, Postman con API Gateway, AWS CLI, o el AWS SDK en una aplicación web. Los métodos más prácticos son:

- **Python local (Método 2)**: Ideal para automatización y pruebas locales.
- **Postman con API Gateway (Método 3)**: Bueno para integrar con aplicaciones web.
- **AWS SDK en web (Método 5)**: Perfecto para acceso directo desde el navegador, pero usa Cognito en producción.

**Siguientes pasos**:
- Prueba el Método 2 o 3 para insertar un usuario y verifica en la consola.
- Implementa el Método 5 con Cognito para una aplicación web segura.
- Si encuentras errores, comparte:
  - El mensaje (por ejemplo, `AccessDenied`).
  - El método usado.
  - Los permisos IAM.
