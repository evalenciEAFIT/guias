import argparse
import json
import requests
from tabulate import tabulate

#URL drl microservicio AWS
INSERT_URL= 'https://r3ieykdkxi.execute-api.us-east-1.amazonaws.com/prod/InsertItemFunction'
GET_URL = 'https://r3ieykdkxi.execute-api.us-east-1.amazonaws.com/prod/GetItemsFunction'


def insert_item (file_path): #insertar los datos en Dynamo
    pass

def get_items():  #consultar los datos de Dynamo
    pass


def main():
    parser = argparse.ArgumentParser(description='Este es un microservicio con AWS')
    parser.add_argument('--file', help='Ruta del arhivo de datos JSON')
    parser.add_argument('--get', action='store_true',help='Lista los datos registrados')

    args = parser.parse_args()

    if not args.file and not args.get:
        parser.print_help()
        return
    
    if args.file:
        insert_item(args.file)

    if args.get:
        get_items()


if __name__ == '__main__':
    main()
