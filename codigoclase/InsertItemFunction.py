import json
import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        item = body.get('item')
        if not item:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Item data is required'})
            }
        
        # Agregar un ID único si no está presente
        item['id'] = item.get('id', str(uuid4()))
        table.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item inserted', 'item': item})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
