import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FormularioData')

def lambda_handler(event, context):
    #Determinar si es GET o POST
    http_method = event['httpMethod']

    if http_method == 'GET':
        #determinar los parametros de la consulta  queryStringParemeters
        params = event.get('queryStringParameters', {})
        nombre = params.get('nombre')
        fecha = params.get('fecha')
        
    elif http_method == 'POST':
        #datos se reciben en el body en formato json o formulario 
        body = event.get('body', '{}')
        if event.get('isBase64Encoded', False):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        params = dict(x.split('=') for x in body.split('&')) if '&' in body else json.loads(body)
        nombre = params.get('nombre')
        fecha = params.get('fecha')

    #Validar los datos
    if not nombre or not fecha:
        return {
            'statusCode': 400,
            'body': json.dumps('Faltan datos')
        }

    #guardar datos
    table.put_item(
        Item={
            'nombre': nombre,
            'fecha': fecha, 
            'timestamp': datetime.now().isoformat()
        }
    )   

    # Devolver una respuesta
    return {
        'statusCode': 200,
        'body': json.dumps(f'Datos guardados correctamente: {nombre}, {fecha}')
    }
