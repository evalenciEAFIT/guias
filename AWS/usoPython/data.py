import requests  # Para enviar solicitudes HTTP a la API
import json  # Para manejar datos JSON

# URL de la API (reemplaza con tu URL de invocación)
API_URL = 'https://yg13sh47v3.execute-api.us-east-1.amazonaws.com'

def crear_usuario(id, nombre, correo):
    """Envía una solicitud POST para crear un usuario."""
    url = f'{API_URL}/usuarios'
    headers = {'content-type': 'application/json'}
    data = {'id': id, 'nombre': nombre, 'correo': correo}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print (f"ver llamdo POST: {response}")

        response.raise_for_status()  # Lanza error si la solicitud falla
        print('-> Usuario creado:', response.json())
    except requests.exceptions.RequestException as e:
        print(f'[X]......Error al crear usuario: {e}')

def listar_usuarios():
    """Envía una solicitud GET para listar todos los usuarios."""
    url = f'{API_URL}/usuarios'
    try:
        response = requests.get(url)
        response.raise_for_status()
        usuarios = response.json()
        print('-> Usuarios encontrados:')
        for usuario in usuarios:
            print(f"- ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
    except requests.exceptions.RequestException as e:
        print(f'[X]......Error al listar usuarios: {e}')

def obtener_usuario(id_usuario):
    """Envía una solicitud GET para obtener un usuario por ID."""
    url = f'{API_URL}/usuarios/{id_usuario}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        usuario = response.json()
        print(f'-> Usuario encontrado: ID: {usuario["id"]}, Nombre: {usuario["nombre"]}, Correo: {usuario["correo"]}')
    except requests.exceptions.RequestException as e:
        print(f'[X]...... Error al obtener usuario: {e}')
    

def actualizar_usuario(id_usuario, nombre, correo):
    """Envía una solicitud PUT para actualizar un usuario."""
    url = f'{API_URL}/usuarios'
    headers = {'Content-Type': 'application/json'}
    data = {'id': id_usuario, 'nombre': nombre, 'correo': correo}
    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print('-> Usuario actualizado:', response.json())
    except requests.exceptions.RequestException as e:
        print(f'[X]...... Error al actualizar usuario: {e}')

def borrar_usuario(id_usuario):
    """Envía una solicitud DELETE para borrar un usuario."""
    url = f'{API_URL}/usuarios/{id_usuario}'
    try:
        response = requests.delete(url)
        response.raise_for_status()
        print('-> Usuario borrado:', response.json()['mensaje'])
    except requests.exceptions.RequestException as e:
        print(f'[X]...... Error al borrar usuario: {e}')

# Pruebas de todas las operaciones
if __name__ == '__main__':
    print('Probando la API...')
    # Crear un usuario
    #crear_usuario('10','Edi Maria', 'maria@ejemplo.com')
    #crear_usuario('11','Ana Nova', 'maria@ejemplo.com')
    #crear_usuario('12','Jose Jaime', 'maria@ejemplo.com')
    #crear_usuario('13','Gertrudis', 'maria@ejemplo.com')
    #crear_usuario('14','Edison', 'maria@ejemplo.com')

    # Listar todos los usuarios
    #listar_usuarios()

    # Obtener un usuario específico
    #obtener_usuario('11')

    # Actualizar un usuario
    actualizar_usuario('13', 'Edison Valencia', 'edi2@ejemplo.com')
    listar_usuarios()

    # Borrar un usuario
    borrar_usuario('14')
    listar_usuarios()