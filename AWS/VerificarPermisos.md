# Guía para Verificar Permisos de AWS Lambda para Insertar Datos en DynamoDB

Esta guía te ayudará a verificar y configurar los permisos necesarios para que una función **AWS Lambda** pueda insertar datos en una tabla de **Amazon DynamoDB** usando la **consola web de AWS en español** y el **nivel gratuito**. Está diseñada para principiantes y se basa en un ejemplo práctico de una API de usuarios (tabla **Usuarios**, función Lambda **AdminUsuarios**). Sigue cada paso para asegurarte de que tu función Lambda tenga los permisos correctos y pueda realizar operaciones de escritura en DynamoDB.

---

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Paso 1: Entender los permisos necesarios](#paso-1-entender-los-permisos-necesarios)
3. [Paso 2: Identificar el rol de ejecución de Lambda](#paso-2-identificar-el-rol-de-ejecución-de-lambda)
4. [Paso 3: Verificar los permisos del rol](#paso-3-verificar-los-permisos-del-rol)
5. [Paso 4: Corregir permisos si es necesario](#paso-4-corregir-permisos-si-es-necesario)
6. [Paso 5: Probar la inserción de datos desde Lambda](#paso-5-probar-la-inserción-de-datos-desde-lambda)
7. [Paso 6: Depurar errores con CloudWatch](#paso-6-depurar-errores-con-cloudwatch)
8. [Paso 7: Verificar resultados en DynamoDB](#paso-7-verificar-resultados-en-dynamodb)
9. [Solución de problemas comunes](#solución-de-problemas-comunes)
10. [Conclusión](#conclusión)

---

## Introducción

Para que una función **AWS Lambda** inserte datos en una tabla de **Amazon DynamoDB**, necesita permisos específicos configurados en su **rol de ejecución** (un rol de IAM). Estos permisos permiten a Lambda realizar operaciones como `PutItem` (insertar un registro) en la tabla. Sin los permisos correctos, Lambda devolverá errores como **403 Forbidden**, **AccessDenied**, o **Internal Server Error**, lo que puede causar problemas en tu API (como el error **"Forbidden"** que enfrentaste).

Esta guía te llevará a través del proceso de verificar y configurar los permisos, probar la inserción de datos, y depurar errores. Usaremos la consola web de AWS en español, siguiendo tu configuración existente:

- **Tabla DynamoDB**: **Usuarios** (clave de partición: `id`, tipo Cadena).
- **Función Lambda**: **AdminUsuarios** (en Python, gestiona un CRUD de usuarios).
- **Región**: `us-east-1`.

**Logros al completar la guía**:
- Confirmarás que Lambda tiene permisos para insertar datos.
- Corregirás cualquier problema de permisos.
- Probarás la inserción con éxito desde Lambda, Postman, y tu página web (`index.html`).
- Aprenderás a usar CloudWatch para identificar errores de permisos.

---

## Paso 1: Entender los permisos necesarios

**Qué hacemos**:
Entendemos qué permisos necesita Lambda para insertar datos en DynamoDB.

**Detalles**:
- Lambda usa un **rol de ejecución** (un rol de IAM) para interactuar con otros servicios de AWS.
- Para insertar datos en la tabla **Usuarios**, el rol debe incluir:
  - Acción: `dynamodb:PutItem` (permite insertar un registro).
  - Recurso: El ARN de la tabla **Usuarios** (por ejemplo, `arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios`).
- También necesita permisos para **CloudWatch Logs** para registrar errores:
  - Acciones: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`.
  - Recurso: `*` (todos los logs).

**Ejemplo de política IAM**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
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

**Por qué lo hacemos**:
- Sin `dynamodb:PutItem`, Lambda no puede insertar datos, causando errores como **AccessDenied**.
- Los permisos de CloudWatch permiten ver errores en los logs, lo que es clave para depurar.
- Entender los permisos nos ayuda a verificar si el rol está bien configurado.

---

## Paso 2: Identificar el rol de ejecución de Lambda

**Qué hacemos**:
Encontramos el rol de IAM asignado a la función Lambda **AdminUsuarios**.

**Instrucciones**:
1. Ve a aws.amazon.com/es, inicia sesión, y busca **Lambda** en la barra de búsqueda.
2. Selecciona **Funciones** > **AdminUsuarios**.
3. Haz clic en la pestaña **Configuración** > **Permisos**.
4. En **Rol de ejecución**, verás un nombre como `AdminUsuarios-role-xxx`. Haz clic en el enlace para abrirlo en **IAM**.
5. Anota el **ARN del rol** (por ejemplo, `arn:aws:iam::CUENTA_ID:role/AdminUsuarios-role-xxx`).

**Por qué lo hacemos**:
- El rol de ejecución define los permisos de Lambda.
- Necesitamos el rol para verificar y modificar sus permisos.
- El ARN nos ayuda a identificar la tabla y región correctas.

**Nota**: Si no ves un rol, crea uno nuevo en el **Paso 4**.

---

## Paso 3: Verificar los permisos del rol

**Qué hacemos**:
Revisamos la política IAM del rol para confirmar que incluye los permisos necesarios.

**Instrucciones**:
1. En **IAM**, con el rol abierto (del Paso 2), haz clic en la pestaña **Permisos**.
2. Busca la política asociada (por ejemplo, `AdminUsuarios-policy-xxx`) y haz clic en su nombre.
3. En **Editor JSON**, verifica que la política incluya:
   - `dynamodb:PutItem` para la tabla **Usuarios** (ARN: `arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios`).
   - Permisos de CloudWatch (`logs:CreateLogGroup`, etc.).
4. Compara con el ejemplo del **Paso 1**.
5. Si la política incluye otras acciones (como `dynamodb:Scan`, `dynamodb:GetItem`) para el CRUD completo, está bien; solo asegúrate de que `dynamodb:PutItem` esté presente.

**Ejemplo de política completa para el CRUD**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
                "dynamodb:DeleteItem"
            ],
            "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
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

**Por qué lo hacemos**:
- Si falta `dynamodb:PutItem` o el ARN es incorrecto, Lambda no podrá insertar datos, causando errores como **403 Forbidden** o **AccessDenied**.
- Confirmar los permisos de CloudWatch asegura que podamos depurar errores.
- Revisar la política nos dice si necesitamos corregirla.

**Qué buscar**:
- Si falta `dynamodb:PutItem` o el ARN no coincide, ve al **Paso 4**.
- Si los permisos están correctos, salta al **Paso 5** para probar.

---

## Paso 4: Corregir permisos si es necesario

**Qué hacemos**:
Añadimos o corregimos los permisos en el rol de Lambda si la política está incompleta o incorrecta.

**Instrucciones**:
1. En **IAM**, con el rol abierto, haz clic en la política (por ejemplo, `AdminUsuarios-policy-xxx`) > **Editar política** > **JSON**.
2. Reemplaza el JSON con la política correcta (ajusta `CUENTA_ID` con tu ID de cuenta AWS):
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "dynamodb:PutItem",
                   "dynamodb:GetItem",
                   "dynamodb:Scan",
                   "dynamodb:UpdateItem",
                   "dynamodb:DeleteItem"
               ],
               "Resource": "arn:aws:dynamodb:us-east-1:CUENTA_ID:table/Usuarios"
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
3. Haz clic en **Revisar política** > **Guardar cambios**.
4. Si no hay una política existente:
   - En el rol, haz clic en **Agregar permisos** > **Crear política**.
   - Selecciona **JSON** y pega el código anterior.
   - Haz clic en **Siguiente**, asigna un nombre (por ejemplo, `AdminUsuariosDynamoDBPolicy`), y guarda.
   - Asocia la política al rol con **Agregar permisos** > **Asociar políticas**.

**Por qué lo hacemos**:
- Actualizamos la política para incluir `dynamodb:PutItem` y asegurarnos de que el ARN sea correcto.
- Añadimos permisos de CloudWatch para depuración.
- Una política correcta elimina errores como **AccessDenied**.

**Nota**: Encuentra tu `CUENTA_ID` en **Mi cuenta** (esquina superior derecha de la consola AWS) o en el ARN del rol.

---

## Paso 5: Probar la inserción de datos desde Lambda

**Qué hacemos**:
Ejecutamos una prueba en Lambda para confirmar que puede insertar datos en la tabla **Usuarios**.

**Instrucciones**:
1. En **Lambda**, selecciona **AdminUsuarios** > **Probar**.
2. Crea un evento de prueba:
   - **Nombre**: `PruebaInsertarUsuario`
   - **JSON**:
     ```json
     {
         "httpMethod": "POST",
         "path": "/usuarios",
         "body": "{\"nombre\": \"Lucía\", \"correo\": \"lucia@ejemplo.com\"}"
     }
     ```
3. Haz clic en **Probar**.
4. Revisa la respuesta:
   - **Éxito**: Verás algo como `{"statusCode": 200, "body": "{\"id\": \"123\", \"nombre\": \"Lucía\", \"correo\": \"lucia@ejemplo.com\"}"}`.
   - **Error**: Puede mostrar `AccessDenied`, `Table 'Usuarios' does not exist`, o `Internal Server Error`.

**Por qué lo hacemos**:
- Probar directamente en Lambda aísla el problema: si funciona, los permisos están correctos; si falla, hay un problema con los permisos o la configuración.
- El evento simula una solicitud POST de tu API, como la que envía `index.html`.
- La respuesta nos dice si el problema está en los permisos, el código, o la tabla.

**Qué hacer según el resultado**:
- **Éxito**: Ve al **Paso 7** para verificar en DynamoDB.
- **AccessDenied**: Revisa los permisos (repite el **Paso 4**).
- **Table does not exist**: Verifica la tabla (Paso 7).
- **Otro error**: Ve al **Paso 6** para depurar.

---

## Paso 6: Depurar errores con CloudWatch

**Qué hacemos**:
Usamos **CloudWatch** para identificar errores de permisos o configuración en Lambda.

**Instrucciones**:
1. En **Lambda**, selecciona **AdminUsuarios** > **Monitor** > **Ver registros en CloudWatch**.
2. Haz clic en el **flujo de logs** más reciente (ordenado por fecha).
3. Busca errores como:
   - `AccessDeniedException`: Falta el permiso `dynamodb:PutItem` o el ARN es incorrecto (repite el **Paso 4**).
   - `Table 'Usuarios' does not exist`: La tabla no existe o el nombre está mal (ve al **Paso 7**).
   - `Falta httpMethod`: Problema en el código Lambda o la integración con API Gateway (verifica el código del **Paso 5** de la guía previa).
4. Si no ves logs, confirma que el rol tiene permisos de CloudWatch (Paso 4).

**Por qué lo hacemos**:
- CloudWatch muestra los errores exactos que ocurren en Lambda, como problemas de permisos o configuración.
- Nos ayuda a confirmar si el problema es de permisos (`AccessDenied`) o algo más (tabla o código).
- Los logs son esenciales para depurar errores como los **403 Forbidden** que enfrentaste.

**Nota**: Si no hay logs, prueba ejecutar el evento del **Paso 5** otra vez para generar nuevos registros.

---

## Paso 7: Verificar resultados en DynamoDB

**Qué hacemos**:
Confirmamos que el dato insertado en el **Paso 5** aparece en la tabla **Usuarios**.

**Instrucciones**:
1. Ve a aws.amazon.com/es, busca **DynamoDB**, y selecciona **Tablas** > **Usuarios**.
2. Haz clic en **Explorar elementos**.
3. Busca un registro con:
   - `id`: Un valor generado (por ejemplo, un UUID).
   - `nombre`: `Lucía`.
   - `correo`: `lucia@ejemplo.com`.
4. Si no ves el registro:
   - Confirma que la tabla se llama **Usuarios** (con "U" mayúscula) y está en `us-east-1`.
   - Verifica el código Lambda (debe usar `put_item` para la tabla **Usuarios**).
   - Repite el **Paso 5** y revisa CloudWatch (Paso 6).

**Por qué lo hacemos**:
- Verificar en DynamoDB confirma que Lambda insertó el dato correctamente.
- Si el registro no aparece, el problema puede ser la tabla, el código, o los permisos.
- Esto asegura que la configuración completa (permisos, Lambda, DynamoDB) funciona.

---

## Solución de problemas comunes

1. **Error: AccessDeniedException en CloudWatch**:
   - Causa: Falta `dynamodb:PutItem` o el ARN es incorrecto.
   - Solución: Revisa y corrige la política (Paso 4). Asegúrate de que el ARN incluya el `CUENTA_ID` correcto y `table/Usuarios`.

2. **Error: Table 'Usuarios' does not exist**:
   - Causa: La tabla no existe, tiene un nombre diferente, o está en otra región.
   - Solución:
     - Confirma el nombre y región en **DynamoDB** > **Tablas**.
     - Si es necesario, crea la tabla (Paso 2 de la guía previa).
     - Actualiza el código Lambda para usar el nombre correcto.

3. **No se insertan datos, pero no hay errores**:
   - Causa: El código Lambda no ejecuta `put_item` correctamente.
   - Solución:
     - Revisa el código Lambda (Paso 3 de la guía previa).
     - Asegúrate de que usa `dynamodb.put_item` con la tabla **Usuarios**.

4. **Error 403 Forbidden en index.html o Postman**:
   - Causa: Problema de permisos, autenticación, o CORS en API Gateway.
   - Solución:
     - Verifica CORS (Paso 3 de la respuesta anterior).
     - Confirma que no se requiere API Key o IAM (Paso 2 de la respuesta anterior).
     - Prueba desde un servidor local (Paso 8 de la respuesta anterior).

5. **No hay logs en CloudWatch**:
   - Causa: Falta permisos de CloudWatch en el rol.
   - Solución: Añade permisos de `logs:*` (Paso 4).

---

## Conclusión

¡Felicidades! Has verificado y configurado los permisos para que tu función Lambda **AdminUsuarios** pueda insertar datos en la tabla **Usuarios** de DynamoDB. Ahora puedes:

- Insertar datos desde Lambda sin errores de permisos.
- Depurar problemas usando CloudWatch.
- Confirmar los resultados en DynamoDB.
- Usar tu API desde `index.html`, Postman, o tu programa Python (`probar_api.py`).

**Siguientes pasos**:
- Prueba la API desde tu página web (`index.html`) o Postman para confirmar que la inserción funciona en un contexto real.
- Si encuentras errores como **403 Forbidden**, revisa la configuración de API Gateway (CORS, autenticación) usando la respuesta anterior.
- Si necesitas permisos adicionales (por ejemplo, para `Scan` o `UpdateItem`), añádelos al rol siguiendo el **Paso 4**.

