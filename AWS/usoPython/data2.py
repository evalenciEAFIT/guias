import requests  # Biblioteca para realizar solicitudes HTTP a la API
import json  # Biblioteca para manejar datos en formato JSON
import pandas as pd  # Biblioteca para leer archivos Excel
from colorama import init, Fore, Style  # Biblioteca para salida de texto coloreada en la consola
import os  # Biblioteca para verificar la existencia de archivos

# Inicializa colorama para habilitar texto coloreado en la consola
init(autoreset=True)

# Define la URL base de la API (reemplazar con la URL real de la API)
API_URL = 'https://yg13sh47v3.execute-api.us-east-1.amazonaws.com'

class SimpleAPIClientCLI:
    def __init__(self):
        # Inicializa la variable para almacenar la ruta del archivo Excel
        self.excel_file = ""

    def display_menu(self):
        # Muestra un menú coloreado con opciones para operaciones de la API
        print(f"{Fore.CYAN}=== MENU API Cliente ===")
        print(f"{Fore.GREEN}1. Especificar Archivo Excel")  # Opción para cargar un archivo Excel
        print(f"{Fore.GREEN}2. Ingresar Usuario")  # Opción para crear un nuevo usuario
        print(f"{Fore.GREEN}3. Listar Usuarios")  # Opción para listar todos los usuarios
        print(f"{Fore.GREEN}4. Buscar Usuario por ID")  # Opción para obtener un usuario por ID
        print(f"{Fore.GREEN}5. Actualizar Usuario")  # Opción para actualizar un usuario
        print(f"{Fore.GREEN}6. Borrar Usuario")  # Opción para eliminar un usuario
        print(f"{Fore.RED}7. Terminar")  # Opción para salir del programa
        print(f"{Fore.CYAN}======================")

    def read_excel(self):
        # Lee el archivo Excel si está especificado y verifica su formato
        if not self.excel_file:
            print(f"{Fore.RED}Error: No se ha especificado un archivo Excel.")
            return None
        if not os.path.exists(self.excel_file):
            print(f"{Fore.RED}Error: El archivo {self.excel_file} no existe.")
            return None
        try:
            df = pd.read_excel(self.excel_file)
            # Verifica que el archivo tenga las columnas requeridas
            if not all(col in df.columns for col in ['id', 'nombre', 'correo']):
                print(f"{Fore.RED}Error: El archivo Excel debe tener las columnas: id, nombre, correo")
                return None
            return df
        except Exception as e:
            print(f"{Fore.RED}Error al leer el archivo Excel: {e}")
            return None

    def get_user_input(self):
        # Solicita al usuario que ingrese datos (ID, nombre, correo) para operaciones de creación/actualización
        id_usuario = input(f"{Fore.CYAN}Ingresa ID: {Style.RESET_ALL}").strip()
        nombre = input(f"{Fore.CYAN}Ingresa Nombre: {Style.RESET_ALL}").strip()
        correo = input(f"{Fore.CYAN}Ingresa Correo: {Style.RESET_ALL}").strip()
        # Valida que todos los campos estén completos
        if not id_usuario or not nombre or not correo:
            print(f"{Fore.RED}Error: Todos los campos son obligatorios.")
            return None
        return id_usuario, nombre, correo  # Devuelve una tupla con los datos del usuario

    def get_user_id(self):
        # Solicita al usuario que ingrese un ID para operaciones de búsqueda/eliminación
        id_usuario = input(f"{Fore.CYAN}Ingrese el ID: {Style.RESET_ALL}").strip()
        # Valida que el ID esté proporcionado
        if not id_usuario:
            print(f"{Fore.RED}Error: El ID es una información requerida.")
            return None
        return id_usuario  # Devuelve el ID del usuario

    def crear_usuario(self, id_usuario, nombre, correo):
        # Envía una solicitud POST para crear un nuevo usuario
        url = f'{API_URL}/usuarios'  # Endpoint de la API para crear usuarios
        headers = {'content-type': 'application/json'}  # Especifica el tipo de contenido JSON
        data = {'id': str(id_usuario), 'nombre': nombre, 'correo': correo}  # Datos del usuario en formato diccionario
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))  # Envía la solicitud POST
            response.raise_for_status()  # Lanza un error si la solicitud falla
            print(f"{Fore.GREEN}Usuario creado: {response.json()}")  # Muestra mensaje de éxito con la respuesta
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al crear usuario: {e}")  # Muestra mensaje de error

    def listar_usuarios(self):
        # Envía una solicitud GET para listar todos los usuarios
        url = f'{API_URL}/usuarios'  # Endpoint de la API para listar usuarios
        try:
            response = requests.get(url)  # Envía la solicitud GET
            response.raise_for_status()  # Lanza un error si la solicitud falla
            usuarios = response.json()  # Analiza la respuesta JSON
            print(f"{Fore.GREEN}Usuarios encontrados:")  # Muestra encabezado para la lista de usuarios
            for usuario in usuarios:
                # Muestra los detalles de cada usuario en amarillo
                print(f"{Fore.YELLOW}- ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al listar usuarios: {e}")  # Muestra mensaje de error

    def obtener_usuario(self, id_usuario):
        # Envía una solicitud GET para obtener un usuario por ID
        url = f'{API_URL}/usuarios/{id_usuario}'  # Endpoint de la API para obtener un usuario específico
        try:
            response = requests.get(url)  # Envía la solicitud GET
            response.raise_for_status()  # Lanza un error si la solicitud falla
            usuario = response.json()  # Analiza la respuesta JSON
            # Muestra los detalles del usuario encontrado
            print(f"{Fore.GREEN}Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al obtener usuario: {e}")  # Muestra mensaje de error

    def actualizar_usuario(self, id_usuario, nombre, correo):
        # Envía una solicitud PUT para actualizar un usuario existente
        url = f'{API_URL}/usuarios'  # Endpoint de la API para actualizar usuarios
        headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
        data = {'id': str(id_usuario), 'nombre': nombre, 'correo': correo}  # Datos actualizados del usuario
        try:
            response = requests.put(url, headers=headers, data=json.dumps(data))  # Envía la solicitud PUT
            response.raise_for_status()  # Lanza un error si la solicitud falla
            print(f"{Fore.GREEN}Usuario actualizado: {response.json()}")  # Muestra mensaje de éxito con la respuesta
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al actualizar usuario: {e}")  # Muestra mensaje de error

    def borrar_usuario(self, id_usuario):
        # Envía una solicitud DELETE para eliminar un usuario por ID
        url = f'{API_URL}/usuarios/{id_usuario}'  # Endpoint de la API para eliminar un usuario
        try:
            response = requests.delete(url)  # Envía la solicitud DELETE
            response.raise_for_status()  # Lanza un error si la solicitud falla
            print(f"{Fore.GREEN}Usuario borrado: {response.json()['mensaje']}")  # Muestra mensaje de éxito
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al borrar usuario: {e}")  # Muestra mensaje de error

    def run(self):
        # Bucle principal para ejecutar la interfaz CLI y manejar las interacciones del usuario
        while True:
            self.display_menu()  # Muestra el menú
            choice = input(f"{Fore.CYAN}Seleccione la opción (1-7): {Style.RESET_ALL}")  # Obtiene la opción del usuario
            if choice == '1':
                # Especifica la ruta del archivo Excel
                self.excel_file = input(f"{Fore.CYAN}Ingrese la ruta del archivo Excel: {Style.RESET_ALL}").strip()
                if self.excel_file:
                    print(f"{Fore.GREEN}Archivo Excel configurado: {self.excel_file}")
                else:
                    print(f"{Fore.YELLOW}No se especificó archivo Excel. Se usará ingreso manual.")
            elif choice == '2':
                # Crea nuevos usuarios usando Excel o ingreso manual
                df = self.read_excel() if self.excel_file else None
                if df is not None:
                    # Procesa cada fila del archivo Excel
                    for _, row in df.iterrows():
                        self.crear_usuario(row['id'], row['nombre'], row['correo'])
                else:
                    # Solicita datos manualmente si no hay archivo Excel válido
                    user_data = self.get_user_input()
                    if user_data:
                        self.crear_usuario(*user_data)
            elif choice == '3':
                # Lista todos los usuarios
                self.listar_usuarios()
            elif choice == '4':
                # Obtiene un usuario por ID
                id_usuario = self.get_user_id()
                if id_usuario:
                    self.obtener_usuario(id_usuario)
            elif choice == '5':
                # Actualiza usuarios usando Excel o ingreso manual
                df = self.read_excel() if self.excel_file else None
                if df is not None:
                    # Procesa cada fila del archivo Excel
                    for _, row in df.iterrows():
                        self.actualizar_usuario(row['id'], row['nombre'], row['correo'])
                else:
                    # Solicita datos manualmente si no hay archivo Excel válido
                    user_data = self.get_user_input()
                    if user_data:
                        self.actualizar_usuario(*user_data)
            elif choice == '6':
                # Elimina un usuario por ID
                id_usuario = self.get_user_id()
                if id_usuario:
                    self.borrar_usuario(id_usuario)
            elif choice == '7':
                # Sale del programa
                print(f"{Fore.GREEN}Exiting...")
                break
            else:
                # Maneja opciones de menú no válidas
                print(f"{Fore.RED}Opción inválida. Por favor seleccione 1-7.")

if __name__ == '__main__':
    # Crea una instancia del cliente CLI y ejecuta el programa
    client = SimpleAPIClientCLI()
    client.run()