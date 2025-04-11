import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ItemsTable')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = reponse.get('Items', [])
        return {
            'statusCode': 200,
            'body': json.dumps({'Items':items})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

