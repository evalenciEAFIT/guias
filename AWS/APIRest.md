# Guía para Principiantes: Crear una API RESTful con CRUD Completo en AWS, Página Web y Pruebas Locales

¡Hola! Vamos a crear una API en AWS que te permita **guardar**, **ver**, **editar**, y **borrar** información de usuarios (como su nombre y correo). Es como un cuaderno digital donde puedes escribir, leer, cambiar o quitar notas. Usaremos:

- **DynamoDB**: El cuaderno donde guardamos los datos.
- **Lambda**: El lápiz que escribe, lee, edita o borra en el cuaderno.
- **API Gateway**: La puerta que conecta tu cuaderno con internet.

Haremos todo desde la **página web de AWS en español**, sin comandos complicados, y probaremos con **Postman**, una **página web** (HTML con JavaScript), y un **programa Python local**. Esta guía es para alguien que nunca ha usado AWS, usa el **nivel gratuito** para no gastar dinero, y explica **por qué** hacemos cada paso. También solucionaremos el error `{"mensaje": "Error: 'httpMethod'"}`, que ocurre cuando la solicitud no le dice a Lambda qué acción hacer (como "guardar" o "leer").

## ¿Qué necesitas?

- **Cuenta de AWS**: Crea una gratis en aws.amazon.com/es. El nivel gratuito incluye:
  - 1 millón de usos al mes para Lambda.
  - 1 millón de solicitudes al mes para API Gateway.
  - 25 unidades de almacenamiento para DynamoDB.
- **Postman**: Descárgalo en postman.com para probar la API.
- **Navegador web**: Usa Chrome o Firefox para la página web.
- **Python 3**: Instálalo desde python.org para el programa local.
- **Editor de texto**: Como VS Code o Notepad++ para editar HTML y Python.
- **Paciencia**: Vamos despacio, explicando todo.

## Paso 1: Configura la página de AWS

**Qué hacemos**:
1. Ve a aws.amazon.com/es e **inicia sesión** (o crea una cuenta).
2. En la esquina superior derecha, asegúrate de que diga **Español**. Si no, cámbialo.
3. En la misma esquina, selecciona la región **EE.UU. Este (N. Virginia)** (`us-east-1`).

**Por qué lo hacemos**:
- Iniciamos sesión para usar las herramientas de AWS, como un cuaderno, lápiz y puerta.
- Ponemos la página en español para que los botones y menús sean fáciles de entender.
- Elegimos `us-east-1` porque todos los servicios (DynamoDB, Lambda, API Gateway) deben estar en la misma región para conectarse correctamente. Si usas otra región, pueden fallar las conexiones, causando errores como el de `httpMethod`.

## Paso 2: Crea una tabla en DynamoDB

DynamoDB es donde guardaremos los datos de los usuarios, como una tabla con columnas para ID, nombre y correo.

**Qué hacemos**:
1. **Entra a DynamoDB**:
   - En la barra de búsqueda (arriba), escribe **DynamoDB** y haz clic en el resultado.
2. **Crea una tabla**:
   - Haz clic en **Crear tabla**.
   - En **Nombre de la tabla**, escribe **Usuarios** (con "U" mayúscula, exactamente así).
   - En **Clave de partición**, escribe **id** (en minúscula) y selecciona **Cadena**.
   - Deja todo lo demás como está (usa "Bajo demanda" para el nivel gratuito).
   - Haz clic en **Crear tabla**.
3. **Confirma**:
   - En unos segundos, verás la tabla **Usuarios** en la lista. Haz clic en ella y asegúrate de que la **Clave de partición** sea **id**.

**Por qué lo hacemos**:
- Entramos a DynamoDB porque es el lugar donde guardaremos los datos, como un cuaderno.
- Creamos una tabla llamada **Usuarios** para organizar la información de los usuarios.
- Usamos **id** como clave de partición porque cada usuario necesita un identificador único (como un número de carné) para encontrarlo rápido.
- Elegimos "Bajo demanda" para que AWS gestione el espacio sin costos adicionales en el nivel gratuito.
- Confirmamos el nombre y la clave porque si la tabla no existe o el nombre es diferente (por ejemplo, "usuarios" en minúscula), Lambda no podrá encontrarla, causando errores como "Internal Server Error".

## Paso 3: Crea una función Lambda

Lambda es el programa que hace el trabajo: guarda, lee, edita o borra datos en la tabla.

**Qué hacemos**:
1. **Entra a Lambda**:
   - En la barra de búsqueda, escribe **Lambda** y selecciona el servicio.
2. **Crea una función**:
   - Haz clic en **Crear función**.
   - Selecciona **Crear desde cero**.
   - En **Nombre de la función**, escribe **AdminUsuarios**.
   - En **Entorno de ejecución**, elige **Python 3.9**.
   - En **Rol de ejecución**, selecciona **Crear un rol nuevo con permisos básicos de Lambda**.
   - Haz clic en **Crear función**.
3. **Pega el código**:
   - En el editor, borra el contenido de `lambda_function.py` y pega este código con comentarios detallados:

```python
import json  # Para manejar datos en formato JSON (como los que envía Postman)
import boto3  # Para conectar con servicios de AWS como DynamoDB
from botocore.exceptions import ClientError  # Para capturar errores de DynamoDB

# Conectar con la tabla Usuarios en DynamoDB
dynamodb = boto3.resource('dynamodb')  # Crea una conexión a DynamoDB
tabla = dynamodb.Table('Usuarios')  # Apunta a la tabla llamada 'Usuarios'

def lambda_handler(event, context):
    """
    Función principal que recibe solicitudes de API Gateway y decide qué hacer.
    - event: Contiene información de la solicitud (método, ruta, datos).
    - context: Información sobre la ejecución de Lambda (no la usamos aquí).
    """
    try:
        # Verificar si httpMethod existe para evitar el error 'httpMethod'
        if 'httpMethod' not in event:
            return responder(400, {'mensaje': 'Falta httpMethod en la solicitud'})

        # Obtener el método (POST, GET, etc.) y la ruta (/usuarios, /usuarios/1)
        metodo = event['httpMethod']
        ruta = event.get('path', '')  # Obtiene la ruta, o '' si no existe
        # Convertir el cuerpo de la solicitud (JSON) a un diccionario Python
        datos = json.loads(event.get('body', '{}')) if event.get('body') else {}

        # Decidir qué hacer según el método y la ruta
        if metodo == 'GET' and ruta == '/usuarios':
            return listar_usuarios()  # Mostrar todos los usuarios
        elif metodo == 'GET' and ruta.startswith('/usuarios/'):
            id_usuario = ruta.split('/')[-1]  # Extraer el ID de la ruta
            return obtener_usuario(id_usuario)  # Mostrar un usuario
        elif metodo == 'POST' and ruta == '/usuarios':
            return crear_usuario(datos)  # Crear un usuario
        elif metodo == 'PUT' and ruta == '/usuarios':
            return actualizar_usuario(datos)  # Actualizar un usuario
        elif metodo == 'DELETE' and ruta.startswith('/usuarios/'):
            id_usuario = ruta.split('/')[-1]  # Extraer el ID
            return borrar_usuario(id_usuario)  # Borrar un usuario
        else:
            return responder(400, {'mensaje': 'Operación no válida'})

    except KeyError as e:
        # Si falta un campo en el evento (como 'httpMethod'), devolver error
        return responder(500, {'mensaje': f'Error: Falta el campo {str(e)}'})
    except Exception as e:
        # Capturar cualquier otro error inesperado
        return responder(500, {'mensaje': f'Error: {str(e)}'})

def listar_usuarios():
    """Obtiene todos los usuarios de la tabla Usuarios."""
    try:
        respuesta = tabla.scan()  # Lee todos los elementos de la tabla
        return responder(200, respuesta.get('Items', []))  # Devuelve la lista
    except ClientError as e:
        return responder(500, {'mensaje': f'Error en DynamoDB: {str(e)}'})

def obtener_usuario(id_usuario):
    """Obtiene un usuario por su ID."""
    try:
        respuesta = tabla.get_item(Key={'id': id_usuario})  # Busca por ID
        usuario = respuesta.get('Item')
        if not usuario:
            return responder(404, {'mensaje': 'Usuario no encontrado'})
        return responder(200, usuario)  # Devuelve el usuario encontrado
    except ClientError as e:
        return responder(500, {'mensaje': f'Error en DynamoDB: {str(e)}'})

def crear_usuario(datos):
    """Crea un nuevo usuario con los datos recibidos."""
    try:
        usuario = {
            'id': datos.get('id', str(int(tabla.scan()['Count']) + 1)),  # Genera ID automático
            'nombre': datos.get('nombre'),
            'correo': datos.get('correo')
        }
        if not usuario['nombre'] or not usuario['correo']:
            return responder(400, {'mensaje': 'Falta nombre o correo'})
        tabla.put_item(Item=usuario)  # Guarda el usuario en la tabla
        return responder(201, usuario)  # Devuelve el usuario creado
    except ClientError as e:
        return responder(500, {'mensaje': f'Error en DynamoDB: {str(e)}'})

def actualizar_usuario(datos):
    """Actualiza un usuario existente con nuevos datos."""
    try:
        id_usuario = datos.get('id')
        if not id_usuario:
            return responder(400, {'mensaje': 'Falta el ID'})
        if not datos.get('nombre') or not datos.get('correo'):
            return responder(400, {'mensaje': 'Falta nombre o correo'})
        respuesta = tabla.update_item(
            Key={'id': id_usuario},  # Identifica el usuario por ID
            UpdateExpression='SET nombre = :n, correo = :c',  # Actualiza campos
            ExpressionAttributeValues={
                ':n': datos.get('nombre'),
                ':c': datos.get('correo')
            },
            ReturnValues='ALL_NEW'  # Devuelve los datos actualizados
        )
        return responder(200, respuesta['Attributes'])
    except ClientError as e:
        return responder(500, {'mensaje': f'Error en DynamoDB: {str(e)}'})

def borrar_usuario(id_usuario):
    """Borra un usuario por su ID."""
    try:
        tabla.delete_item(Key={'id': id_usuario})  # Elimina el usuario
        return responder(200, {'mensaje': 'Usuario borrado'})
    except ClientError as e:
        return responder(500, {'mensaje': f'Error en DynamoDB: {str(e)}'})

def responder(codigo, cuerpo):
    """
    Crea una respuesta para API Gateway con un código de estado y cuerpo.
    - codigo: Código HTTP (200, 400, etc.).
    - cuerpo: Datos o mensaje de error en JSON.
    """
    return {
        'statusCode': codigo,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Permite acceso desde cualquier origen
        },
        'body': json.dumps(cuerpo)  # Convierte el cuerpo a JSON
    }
```

4. **Guarda el código**:
   - Haz clic en **Deploy** (o **Desplegar**).

**Por qué lo hacemos**:
- Entramos a Lambda porque es donde ponemos el programa que hace el trabajo de la API.
- Creamos una función llamada **AdminUsuarios** para que sea claro que administra datos de usuarios.
- Elegimos **Python 3.9** porque es un lenguaje fácil y compatible con AWS.
- Creamos un rol nuevo para que Lambda tenga permisos básicos iniciales (luego añadiremos más).
- Pegamos el código que:
  - Maneja **GET** (ver todos o un usuario), **POST** (crear), **PUT** (editar), y **DELETE** (borrar).
  - Verifica si `httpMethod` existe para evitar el error `{"mensaje": "Error: 'httpMethod'"}`, que pasa si API Gateway envía una solicitud mal formada.
  - Incluye **comentarios detallados** para explicar cada función y línea importante.
  - Conecta con la tabla **Usuarios** en DynamoDB y valida los datos (por ejemplo, que `nombre` y `correo` no estén vacíos).
- Guardamos con **Deploy** para que AWS use la versión actualizada del código. Sin esto, podría usar una versión vieja y fallar.

## Paso 4: Dale permisos a Lambda

Lambda necesita permisos para leer y escribir en la tabla **Usuarios**.

**Qué hacemos**:
1. **Encuentra el rol**:
   - En la página de **AdminUsuarios**, ve a **Configuración** > **Permisos**.
   - Haz clic en el nombre del rol (por ejemplo, `AdminUsuarios-role-xxx`).
2. **Añade permisos**:
   - En **IAM**, haz clic en **Agregar permisos** > **Crear política inline**.
   - Selecciona **JSON** y pega:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:*:table/Usuarios"
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

- Haz clic en **Siguiente**, nombra la política **PermisosDynamoDB**, y haz clic en **Crear política**.

3. **Confirma**:
   - Asegúrate de que la política esté en la lista del rol.

**Por qué lo hacemos**:
- Vamos a **Permisos** porque Lambda necesita autorización para tocar la tabla **Usuarios**, como un pase de entrada.
- Encontramos el rol porque es la "identidad" de Lambda, y le damos permisos específicos.
- Creamos una política que permite:
  - Leer (`GetItem`, `Scan`), escribir (`PutItem`), actualizar (`UpdateItem`), y borrar (`DeleteItem`) en la tabla **Usuarios**.
  - Guardar registros (`logs`) en CloudWatch para ver qué pasa si hay errores.
- Usamos el ARN (`arn:aws:dynamodb:us-east-1:*:table/Usuarios`) para apuntar exactamente a nuestra tabla en `us-east-1`.
- Confirmamos porque si los permisos están mal, Lambda no podrá acceder a DynamoDB, causando errores como "AccessDenied" o "Internal Server Error".

## Paso 5: Crea una API con API Gateway

API Gateway es la puerta que conecta tu API con Postman, la página web, o el programa Python.

**Qué hacemos**:
1. **Entra a API Gateway**:
   - Busca **API Gateway** en la consola.
2. **Crea una API**:
   - Haz clic en **Crear API** > **API HTTP** > **Construir**.
   - En **Nombre de la API**, escribe **APIUsuarios**.
   - Haz clic en **Siguiente**.
3. **Añade rutas**:
   - Crea estas rutas:
     - **GET /usuarios**
     - **GET /usuarios/{id}**
     - **POST /usuarios**
     - **PUT /usuarios**
     - **DELETE /usuarios/{id}**
   - Haz clic en **Siguiente**.
4. **Configura la etapa**:
   - Usa **$default**.
   - Haz clic en **Siguiente** > **Crear**.
5. **Conecta con Lambda**:
   - Para cada ruta:
     - Haz clic en la ruta.
     - En **Integración**, selecciona **Lambda**.
     - Elige **AdminUsuarios**.
     - En **CORS**, pon `*` en **Origen** y activa **Habilitar CORS**.
     - Haz clic en **Guardar**.
6. **Despliega la API**:
   - Ve a **Desplegar**, selecciona **$default**, y haz clic en **Desplegar**.
   - Copia la **URL de invocación** (por ejemplo, `https://xxx.execute-api.us-east-1.amazonaws.com`).

**Por qué lo hacemos**:
- Entramos a API Gateway porque hace que tu API sea accesible desde internet.
- Creamos una **API HTTP** porque es simple y barata (nivel gratuito).
- Nombramos la API **APIUsuarios** para que sea claro que maneja datos de usuarios.
- Añadimos rutas para cada acción:
  - **GET /usuarios**: Ver todos los usuarios.
  - **GET /usuarios/{id}**: Ver un usuario específico.
  - **POST /usuarios**: Crear un usuario.
  - **PUT /usuarios**: Editar un usuario.
  - **DELETE /usuarios/{id}**: Borrar un usuario.
- Usamos **$default** porque es la configuración automática para probar rápido.
- Conectamos cada ruta a **AdminUsuarios** porque Lambda hace el trabajo, y API Gateway solo pasa las solicitudes.
- Activamos **C  **CORS** con `*` para que Postman, la página web, o el programa Python puedan enviar solicitudes sin ser bloqueados.
- Desplegamos la API para que los cambios estén disponibles en internet.
- Copiamos la **URL de invocación** porque es la dirección que usarás para probar. Si la integración está mal, puede causar el error `httpMethod` porque Lambda no recibe la solicitud correcta.

## Paso 6: Prueba la API con Postman

**Qué hacemos**:
1. **Abre Postman**:
   - Instala Postman desde postman.com si no lo tienes.
   - Crea una **nueva solicitud** (clic en **New** > **HTTP Request**).
2. **Prueba POST (Crear)**:
   - **Método**: POST.
   - **URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/usuarios`.
   - **Encabezados**: Añade `Content-Type: application/json`.
   - **Cuerpo** (raw, JSON):

```json
{
    "nombre": "Lucía",
    "correo": "lucia@ejemplo.com"
}
```

- Clic en **Send**.
- Deberías ver:

```json
{
    "id": "1",
    "nombre": "Lucía",
    "correo": "lucia@ejemplo.com"
}
```

3. **Prueba GET (Leer todos)**:
   - **Método**: GET.
   - **URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/usuarios`.
   - Clic en **Send**.
   - Deberías ver: `[ {"id": "1", "nombre": "Lucía", "correo": "lucia@ejemplo.com"} ]`.

4. **Prueba GET (Leer uno)**:
   - **Método**: GET.
   - **URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/usuarios/1`.
   - Clic en **Send**.
   - Deberías ver: `{"id": "1", "nombre": "Lucía", "correo": "lucia@ejemplo.com"}`.

5. **Prueba PUT (Actualizar)**:
   - **Método**: PUT.
   - **URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/usuarios`.
   - **Encabezados**: `Content-Type: application/json`.
   - **Cuerpo** (raw, JSON):

```json
{
    "id": "1",
    "nombre": "Lucía Actualizada",
    "correo": "lucia2@ejemplo.com"
}
```

- Clic en **Send**.
- Deberías ver: `{"id": "1", "nombre": "Lucía Actualizada", "correo": "lucia2@ejemplo.com"}`.

6. **Prueba DELETE (Borrar)**:
   - **Método**: DELETE.
   - **URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/usuarios/1`.
   - Clic en **Send**.
   - Deberías ver: `{"mensaje": "Usuario borrado"}`.

**Por qué lo hacemos**:
- Usamos Postman porque es una herramienta fácil para enviar solicitudes a la API y ver si funciona.
- Configuramos cada solicitud con:
  - El **Método** correcto (POST, GET, etc.) porque cada ruta espera un tipo específico.
  - La **URL** exacta para llegar a la ruta correcta.
  - **Content-Type: application/json** para indicar que los datos son JSON.
  - Un **Cuerpo** válido para POST y PUT porque el código espera `nombre` y `correo` (y `id` para PUT).
- Probamos todas las operaciones para confirmar que el CRUD funciona.
- Si el JSON, URL o método están mal, puede causar errores como `httpMethod` o "Internal Server Error".

## Paso 7: Crea una página web para consumir la API

**Qué hacemos**:
1. **Crea un archivo HTML**:
   - Abre un editor de texto (como VS Code o Notepad++).
   - Crea un archivo llamado `index.html` y pega este código:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestión de Usuarios</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; }
        input { padding: 5px; width: 200px; }
        button { padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        #resultado { margin-top: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Gestión de Usuarios</h1>
    
    <!-- Formulario para crear usuario -->
    <div class="form-group">
        <h3>Crear Usuario</h3>
        <label>Nombre:</label>
        <input type="text" id="nombreCrear">
        <label>Correo:</label>
        <input type="email" id="correoCrear">
        <button onclick="crearUsuario()">Crear</button>
    </div>
    
    <!-- Formulario para actualizar usuario -->
    <div class="form-group">
        <h3>Actualizar Usuario</h3>
        <label>ID:</label>
        <input type="text" id="idActualizar">
        <label>Nombre:</label>
        <input type="text" id="nombreActualizar">
        <label>Correo:</label>
        <input type="email" id="correoActualizar">
        <button onclick="actualizarUsuario()">Actualizar</button>
    </div>
    
    <!-- Formulario para borrar usuario -->
    <div class="form-group">
        <h3>Borrar Usuario</h3>
        <label>ID:</label>
        <input type="text" id="idBorrar">
        <button onclick="borrarUsuario()">Borrar</button>
    </div>
    
    <!-- Botón para listar usuarios -->
    <div class="form-group">
        <h3>Ver Usuarios</h3>
        <button onclick="listarUsuarios()">Listar Todos</button>
    </div>
    
    <!-- Área para mostrar resultados -->
    <div id="resultado"></div>

    <script>
        // URL de la API (reemplaza con tu URL de invocación)
        const API_URL = 'https://xxx.execute-api.us-east-1.amazonaws.com';

        async function crearUsuario() {
            const nombre = document.getElementById('nombreCrear').value;
            const correo = document.getElementById('correoCrear').value;
            if (!nombre || !correo) {
                mostrarResultado('Por favor, completa todos los campos.', 'error');
                return;
            }
            try {
                const response = await fetch(`${API_URL}/usuarios`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nombre, correo })
                });
                const data = await response.json();
                mostrarResultado(`Usuario creado: ${JSON.stringify(data)}`, 'success');
            } catch (error) {
                mostrarResultado(`Error: ${error.message}`, 'error');
            }
        }

        async function actualizarUsuario() {
            const id = document.getElementById('idActualizar').value;
            const nombre = document.getElementById('nombreActualizar').value;
            const correo = document.getElementById('correoActualizar').value;
            if (!id || !nombre || !correo) {
                mostrarResultado('Por favor, completa todos los campos.', 'error');
                return;
            }
            try {
                const response = await fetch(`${API_URL}/usuarios`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id, nombre, correo })
                });
                const data = await response.json();
                mostrarResultado(`Usuario actualizado: ${JSON.stringify(data)}`, 'success');
            } catch (error) {
                mostrarResultado(`Error: ${error.message}`, 'error');
            }
        }

        async function borrarUsuario() {
            const id = document.getElementById('idBorrar').value;
            if (!id) {
                mostrarResultado('Por favor, ingresa el ID.', 'error');
                return;
            }
            try {
                const response = await fetch(`${API_URL}/usuarios/${id}`, {
                    method: 'DELETE'
                });
                const data = await response.json();
                mostrarResultado(`Usuario borrado: ${data.mensaje}`, 'success');
            } catch (error) {
                mostrarResultado(`Error: ${error.message}`, 'error');
            }
        }

        async function listarUsuarios() {
            try {
                const response = await fetch(`${API_URL}/usuarios`, {
                    method: 'GET'
                });
                const data = await response.json();
                let tabla = '<table><tr><th>ID</th><th>Nombre</th><th>Correo</th></tr>';
                data.forEach(usuario => {
                    tabla += `<tr><td>${usuario.id}</td><td>${usuario.nombre}</td><td>${usuario.correo}</td></tr>`;
                });
                tabla += '</table>';
                mostrarResultado(tabla, 'success');
            } catch (error) {
                mostrarResultado(`Error: ${error.message}`, 'error');
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

2. **Abre la página**:
   - Guarda `index.html` en tu computadora.
   - Haz doble clic para abrirlo en tu navegador (Chrome o Firefox).
   - Reemplaza `https://xxx.execute-api.us-east-1.amazonaws.com` en el código con tu **URL de invocación** del Paso 5.
3. **Prueba la página**:
   - Usa los formularios para crear, actualizar, borrar, y listar usuarios.
   - Los resultados aparecerán en la sección "Resultado" (una tabla para listar, o mensajes para otras acciones).

**Por qué lo hacemos**:
- Creamos una página web para que puedas usar la API desde un navegador, sin necesidad de Postman o un programa Python.
- Usamos HTML para crear formularios y JavaScript para enviar solicitudes a la API, porque es simple y no requiere un servidor web.
- Añadimos estilos CSS para que la página sea fácil de usar y bonita.
- Incluimos funciones JavaScript para:
  - **Crear**: Enviar un POST con nombre y correo.
  - **Actualizar**: Enviar un PUT con ID, nombre y correo.
  - **Borrar**: Enviar un DELETE con ID.
  - **Listar**: Enviar un GET y mostrar los usuarios en una tabla.
- Abrimos la página localmente (con doble clic) porque no necesita un servidor, lo que la hace ideal para pruebas rápidas.
- Probamos todas las funciones para confirmar que la API funciona desde la web. Si CORS no está configurado, la página no podrá conectarse, causando errores.

## Paso 8: Crea un programa Python para probar la API localmente

**Qué hacemos**:
1. **Crea un archivo Python**:
   - Abre un editor de texto (como VS Code).
   - Crea un archivo llamado `probar_api.py` y pega este código:

```python
import requests  # Para enviar solicitudes HTTP a la API
import json  # Para manejar datos JSON

# URL de la API (reemplaza con tu URL de invocación)
API_URL = 'https://xxx.execute-api.us-east-1.amazonaws.com'

def crear_usuario(nombre, correo):
    """Envía una solicitud POST para crear un usuario."""
    url = f'{API_URL}/usuarios'
    headers = {'Content-Type': 'application/json'}
    data = {'nombre': nombre, 'correo': correo}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Lanza error si la solicitud falla
        print('Usuario creado:', response.json())
    except requests.exceptions.RequestException as e:
        print(f'Error al crear usuario: {e}')

def listar_usuarios():
    """Envía una solicitud GET para listar todos los usuarios."""
    url = f'{API_URL}/usuarios'
    try:
        response = requests.get(url)
        response.raise_for_status()
        usuarios = response.json()
        print('Usuarios encontrados:')
        for usuario in usuarios:
            print(f"- ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
    except requests.exceptions.RequestException as e:
        print(f'Error al listar usuarios: {e}')

def obtener_usuario(id_usuario):
    """Envía una solicitud GET para obtener un usuario por ID."""
    url = f'{API_URL}/usuarios/{id_usuario}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        usuario = response.json()
        print(f'Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener usuario: {e}')

def actualizar_usuario(id_usuario, nombre, correo):
    """Envía una solicitud PUT para actualizar un usuario."""
    url = f'{API_URL}/usuarios'
    headers = {'Content-Type': 'application/json'}
    data = {'id': id_usuario, 'nombre': nombre, 'correo': correo}
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print('Usuario actualizado:', response.json())
    except requests.exceptions.RequestException as e:
        print(f'Error al actualizar usuario: {e}')

def borrar_usuario(id_usuario):
    """Envía una solicitud DELETE para borrar un usuario."""
    url = f'{API_URL}/usuarios/{id_usuario}'
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print('Usuario borrado:', response.json()['mensaje'])
    except requests.exceptions.RequestException as e:
        print(f'Error al borrar usuario: {e}')

# Pruebas de todas las operaciones
if __name__ == '__main__':
    print('Probando la API...')
    # Crear un usuario
    crear_usuario('María', 'maria@ejemplo.com')
    # Listar todos los usuarios
    listar_usuarios()
    # Obtener un usuario específico
    obtener_usuario('1')
    # Actualizar un usuario
    actualizar_usuario('1', 'María Actualizada', 'maria2@ejemplo.com')
    # Borrar un usuario
    borrar_usuario('1')
```

2. **Instala la librería requerida**:
   - Abre una terminal (en Windows usa CMD o PowerShell; en Mac/Linux usa Terminal).
   - Ejecuta: `pip install requests`
3. **Ejecuta el programa**:
   - Reemplaza `https://xxx.execute-api.us-east-1.amazonaws.com` en el código con tu **URL de invocación** del Paso 5.
   - Guarda el archivo.
   - En la terminal, ve al directorio donde está `probar_api.py` (usa `cd ruta/del/directorio`).
   - Ejecuta: `python probar_api.py`
   - Deberías ver mensajes como:
     - `Usuario creado: {'id': '1', 'nombre': 'María', 'correo': 'maria@ejemplo.com'}`
     - `Usuarios encontrados: ...`
     - Etc.

**Por qué lo hacemos**:
- Creamos un programa Python para probar la API desde tu computadora, sin necesitar Postman o un navegador.
- Usamos la librería `requests` porque facilita enviar solicitudes HTTP (POST, GET, etc.) a la API.
- Incluimos funciones para cada operación (crear, listar, obtener, actualizar, borrar) con manejo de errores para que sea fácil ver qué falla.
- Instalamos `requests` porque no viene con Python por defecto, pero es necesaria para hacer solicitudes.
- Ejecutamos el programa para probar todas las operaciones automáticamente y confirmar que la API funciona. Si la URL o el JSON son incorrectos, puede causar errores como `httpMethod`.

## Paso 9: Solucionar el error "Error: 'httpMethod'"

Si ves `{"mensaje": "Error: 'httpMethod'"}` en Postman, la página web, o el programa Python, significa que Lambda no recibió el campo `httpMethod`, probablemente porque API Gateway no está configurado correctamente.

**Qué hacemos**:
1. **Revisa la integración en API Gateway**:
   - En **API Gateway**, selecciona **APIUsuarios**.
   - Haz clic en **Rutas** y revisa cada ruta (por ejemplo, **POST /usuarios**).
   - Asegúrate de que:
     - **Integración** sea **Lambda**.
     - La función sea **AdminUsuarios**.
     - La región sea `us-east-1`.
   - Si está mal, haz clic en **Editar**, corrige, y guarda.
   - Redepliega: Ve a **Desplegar**, selecciona **$default**, y haz clic en **Desplegar**.
2. **Verifica los permisos de API Gateway para Lambda**:
   - En **Lambda**, selecciona **AdminUsuarios**.
   - Ve a **Configuración** > **Permisos**.
   - En **Política de recursos**, haz clic en **Agregar permisos**.
   - Configura:
     - **Servicio**: API Gateway.
     - **Acción**: `lambda:InvokeFunction`.
     - **Principal**: `apigateway.amazonaws.com`.
     - **Origen**: Copia el ARN de tu API (en API Gateway, bajo **Detalles** de **APIUsuarios**).
   - Clic en **Agregar**.
3. **Prueba la solicitud**:
   - En Postman, usa los ejemplos del Paso 6.
   - En la página web, usa los formularios del Paso 7.
   - En el programa Python, ejecuta `probar_api.py` (Paso 8).
   - Asegúrate de que la URL, método, y cuerpo sean correctos.
4. **Revisa los registros en CloudWatch**:
   - En **Lambda**, selecciona **AdminUsuarios**.
   - Ve a **Monitor** > **Ver registros en CloudWatch**.
   - Clic en un **flujo de logs** reciente.
   - Si ves `Falta httpMethod en la solicitud`, repite el Paso 9.1.
   - Otros errores:
     - **"Table 'Usuarios' does not exist"**: La tabla no se llama **Usuarios**. Revisa el nombre en DynamoDB y corrige el código.
     - **"AccessDenied"**: Los permisos de IAM están mal. Revisa el Paso 4.
     - **"KeyError: 'nombre'"**: El JSON falta `nombre`. Usa los ejemplos correctos.
5. **Prueba Lambda directamente**:
   - En **Lambda**, selecciona **AdminUsuarios** > **Probar**.
   - Crea un evento:
     - **Nombre**: `PruebaPOST`.
     - JSON:

```json
{
    "httpMethod": "POST",
    "path": "/usuarios",
    "body": "{\"nombre\": \"Lucía\", \"correo\": \"lucia@ejemplo.com\"}"
}
```

- Clic en **Probar**.
- Si funciona, el problema está en API Gateway. Si falla, anota el error.

**Por qué lo hacemos**:
- Revisamos la integración porque el error `httpMethod` ocurre si API Gateway no envía el método (POST, GET, etc.) a Lambda, lo que pasa si la ruta está mal configurada.
- Verificamos permisos porque API Gateway necesita autorización para "hablar" con Lambda. Sin esto, la solicitud no llega.
- Probamos en Postman, la página web, y el programa Python para confirmar que la solicitud es correcta. Un método o URL equivocados pueden causar el error.
- Miramos CloudWatch porque los registros muestran qué falla (por ejemplo, si `httpMethod` falta).
- Probamos Lambda directamente para aislar el problema. Si funciona, el código está bien, y el error está en la conexión con API Gateway.

## Paso 10: Revisa los datos

**Qué hacemos**:
1. **Ve a DynamoDB**:
   - Busca **DynamoDB** y selecciona **Usuarios**.
2. **Explora**:
   - Clic en **Explorar elementos**.
   - Confirma que los usuarios aparecen, se actualizan, o se borran según las pruebas.

**Por qué lo hacemos**:
- Vamos a DynamoDB para verificar que los datos se guardaron, cambiaron o borraron correctamente.
- Esto confirma que Lambda y DynamoDB están conectados, descartando errores como "Table does not exist".

## Paso 11: Limpia

**Qué hacemos**:
1. **Borra la tabla**:
   - En DynamoDB, selecciona **Usuarios** > **Eliminar tabla**.
2. **Borra la API**:
   - En API Gateway, selecciona **APIUsuarios** > **Eliminar**.
3. **Borra la función**:
   - In Lambda, select **AdminUsuarios** > **Eliminar**.
4. **Borra el rol**:
   - En IAM, elimina `AdminUsuarios-role-xxx`.
5. **Borra los registros**:
   - En CloudWatch, elimina `/aws/lambda/AdminUsuarios`.

**Por qué lo hacemos**:
- Borramos todo para no dejar servicios corriendo que puedan costar dinero, aunque estén en el nivel gratuito.
- Esto mantiene tu cuenta limpia y evita sorpresas en la facturación.

## ¡Lo lograste!

Ahora tienes una API con CRUD completo, una página web para usarla, y un programa Python para pruebas locales. Si ves `{"mensaje": "Error: 'httpMethod'"}`, usa el **Paso 9** para solucionarlo. Si aparece otro error, comparte:

- El **error exacto** (por ejemplo, `{"mensaje": "Error: 'httpMethod'"}`).
- El **JSON** enviado (en Postman, la página, o Python).
- Los **registros de CloudWatch** (Paso 9.4).
- La **URL** y **región** (debe ser `us-east-1`).

