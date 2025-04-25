Explicación de los Códigos de Cliente API
Este documento explica los cuatro archivos Python (data.py, data1B.py, data2.py, data2B.py) que implementan un cliente para interactuar con una API de gestión de usuarios. Cada archivo representa una iteración progresiva en funcionalidad, desde un script básico hasta una interfaz de línea de comandos (CLI) avanzada con soporte para archivos Excel y registro de resultados. A continuación, se detalla el propósito de cada archivo, su implementación, las mejoras introducidas y se incluye el código fuente completo de cada uno.
1. data.py: Script Básico de Interacción con la API
Propósito
data.py es un script inicial que proporciona funciones básicas para interactuar con una API RESTful que gestiona usuarios. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) a través de solicitudes HTTP.
Implementación

Librerías: Utiliza requests para solicitudes HTTP y json para manejar datos en formato JSON.
Funciones:
crear_usuario(id, nombre, correo): Envía una solicitud POST para crear un usuario.
listar_usuarios(): Envía una solicitud GET para listar todos los usuarios.
obtener_usuario(id_usuario): Envía una solicitud GET para obtener un usuario por ID.
actualizar_usuario(id_usuario, nombre, correo): Envía una solicitud PUT para actualizar un usuario.
borrar_usuario(id_usuario): Envía una solicitud DELETE para eliminar un usuario.


Pruebas: Incluye un bloque if __name__ == '__main__' con ejemplos comentados para probar las operaciones.
Manejo de Errores: Usa try-except con requests.exceptions.RequestException para capturar errores HTTP.

Características

Simple y funcional, diseñado para pruebas rápidas.
Salida básica en consola sin formato avanzado.
No ofrece una interfaz interactiva.

Código Fuente
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

2. data1B.py: Interfaz CLI Básica
Propósito
data1B.py introduce una interfaz de línea de comandos (CLI) interactiva, permitiendo a los usuarios seleccionar operaciones sin modificar el código.
Implementación

Librerías: Agrega colorama para salida coloreada, además de requests y json.
Clase SimpleAPIClientCLI:
display_menu(): Muestra un menú con opciones (1-6).
get_user_input(): Solicita ID, nombre y correo, validando entradas.
get_user_id(): Solicita solo el ID.
Métodos CRUD similares a data.py, con salida coloreada.
run(): Bucle principal para la CLI.


Mejoras:
Interfaz interactiva.
Salida coloreada para mejor legibilidad.
Validación de entrada.



Características

Amigable para usuarios no técnicos.
Mantiene simplicidad pero mejora la experiencia de usuario.
No soporta procesamiento masivo.

Código Fuente
import requests
import json
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# URL de la API (reemplaza con tu URL de invocación)
API_URL = 'https://yg13sh47v3.execute-api.us-east-1.amazonaws.com'

class SimpleAPIClientCLI:
    def display_menu(self):
        print(f"{Fore.CYAN}=== MENU API Cliente ===")
        print(f"{Fore.GREEN}1. Ingresar Usuario")
        print(f"{Fore.GREEN}2. Listar Usuario")
        print(f"{Fore.GREEN}3. Buscar Usuario por id")
        print(f"{Fore.GREEN}4. Actualizar Usuario")
        print(f"{Fore.GREEN}5. Borrar Usuario")
        print(f"{Fore.RED}6. Terminar")
        print(f"{Fore.CYAN}======================")

    def get_user_input(self):
        id_usuario = input(f"{Fore.CYAN}Ingresa ID: {Style.RESET_ALL}").strip()
        nombre = input(f"{Fore.CYAN}Ingresa Nombre: {Style.RESET_ALL}").strip()
        correo = input(f"{Fore.CYAN}Ingresa Correo: {Style.RESET_ALL}").strip()
        if not id_usuario or not nombre or not correo:
            print(f"{Fore.RED}Error: All fields are required.")
            return None
        return id_usuario, nombre, correo

    def get_user_id(self):
        id_usuario = input(f"{Fore.CYAN}Ingrese el ID: {Style.RESET_ALL}").strip()
        if not id_usuario:
            print(f"{Fore.RED}Error: ID es una informacion requerida.")
            return None
        return id_usuario

    def crear_usuario(self, id_usuario, nombre, correo):
        url = f'{API_URL}/usuarios'
        headers = {'content-type': 'application/json'}
        data = {'id': str(id_usuario), 'nombre': nombre, 'correo': correo}
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            print(f"{Fore.GREEN}Usuario creado: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al crear usuario: {e}")

    def listar_usuarios(self):
        url = f'{API_URL}/usuarios'
        try:
            response = requests.get(url)
            response.raise_for_status()
            usuarios = response.json()
            print(f"{Fore.GREEN}Usuarios encontrados:")
            for usuario in usuarios:
                print(f"{Fore.YELLOW}- ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al listar usuarios: {e}")

    def obtener_usuario(self, id_usuario):
        url = f'{API_URL}/usuarios/{id_usuario}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            usuario = response.json()
            print(f"{Fore.GREEN}Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al obtener usuario: {e}")

    def actualizar_usuario(self, id_usuario, nombre, correo):
        url = f'{API_URL}/usuarios'
        headers = {'Content-Type': 'application/json'}
        data = {'id': str(id_usuario), 'nombre': nombre, 'correo': correo}
        try:
            response = requests.put(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            print(f"{Fore.GREEN}Usuario actualizado: {response.json()}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al actualizar usuario: {e}")

    def borrar_usuario(self, id_usuario):
        url = f'{API_URL}/usuarios/{id_usuario}'
        try:
            response = requests.delete(url)
            response.raise_for_status()
            print(f"{Fore.GREEN}Usuario borrado: {response.json()['mensaje']}")
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}[X] Error al borrar usuario: {e}")

    def run(self):
        while True:
            self.display_menu()
            choice = input(f"{Fore.CYAN}Seleccione la opción (1-6): {Style.RESET_ALL}")
            if choice == '1':
                user_data = self.get_user_input()
                if user_data:
                    self.crear_usuario(*user_data)
            elif choice == '2':
                self.listar_usuarios()
            elif choice == '3':
                id_usuario = self.get_user_id()
                if id_usuario:
                    self.obtener_usuario(id_usuario)
            elif choice == '4':
                user_data = self.get_user_input()
                if user_data:
                    self.actualizar_usuario(*user_data)
            elif choice == '5':
                id_usuario = self.get_user_id()
                if id_usuario:
                    self.borrar_usuario(id_usuario)
            elif choice == '6':
                print(f"{Fore.GREEN}Exiting...")
                break
            else:
                print(f"{Fore.RED}Opcion invalida. Por favor seleccione 1-6.")

if __name__ == '__main__':
    client = SimpleAPIClientCLI()
    client.run()

3. data2.py: Soporte para Archivos Excel
Propósito
data2.py añade la capacidad de leer datos de un archivo Excel para operaciones masivas de creación y actualización.
Implementación

Librerías: Agrega pandas y os, además de requests, json, colorama.
Clase SimpleAPIClientCLI:
Atributos: excel_file para la ruta del archivo Excel.
Métodos:
read_excel(): Lee y valida el archivo Excel.
CRUD methods procesan datos de Excel o entrada manual.


run(): Maneja la opción para configurar excel_file.


Mejoras:
Soporte para operaciones masivas vía Excel.
Validación de archivos Excel.
Mantiene la CLI interactiva.



Características

Procesamiento de grandes volúmenes de datos.
Combina entrada manual y automatizada.
Sin registro de resultados más allá de la consola.

Código Fuente
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
        print   

(f"{Fore.GREEN}3. Listar Usuarios")  # Opción para listar todos los usuarios
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

4. data2B.py: Registro de Resultados en Excel
Propósito
data2B.py añade registro de resultados en un archivo Excel, mejorando la trazabilidad.
Implementación

Librerías: Igual que data2.py.
Clase SimpleAPIClientCLI:
Atributos: results (lista de resultados), output_file (nombre del archivo de salida).
Métodos:
save_results(): Guarda resultados en Excel.
CRUD methods registran resultados en results.


run(): Maneja la opción para guardar resultados.


Mejoras:
Registro detallado de operaciones.
Exportación a Excel.
Nombre de archivo de salida configurable.



Características

Solución completa con trazabilidad.
Ideal para entornos profesionales.
Combina todas las funcionalidades anteriores.

Código Fuente
import requests  # Biblioteca para realizar solicitudes HTTP a la API
import json  # Biblioteca para manejar datos en formato JSON
import pandas as pd  # Biblioteca para leer y escribir archivos Excel
from colorama import init, Fore, Style  # Biblioteca para salida de texto coloreada en la consola
import os  # Biblioteca para verificar la existencia de archivos

# Inicializa colorama para habilitar texto coloreado en la consola
init(autoreset=True)

# Define la URL base de la API (reemplazar con la URL real de la API)
API_URL = 'https://yg13sh47v3.execute-api.us-east-1.amazonaws.com'

class SimpleAPIClientCLI:
    def __init__(self):
        # Inicializa variables para la ruta del archivo Excel de entrada y los resultados
        self.excel_file = ""  # Ruta del archivo Excel de entrada
        self.results = []  # Lista para almacenar los resultados de las operaciones
        self.output_file = "api_results.xlsx"  # Nombre predeterminado del archivo Excel de salida

    def display_menu(self):
        # Muestra un menú coloreado con opciones para operaciones de la API
        print(f"{Fore.CYAN}=== MENU API Cliente ===")
        print(f"{Fore.GREEN}1. Especificar Archivo Excel de Entrada")  # Opción para cargar un archivo Excel de entrada
        print(f"{Fore.GREEN}2. Ingresar Usuario")  # Opción para crear un nuevo usuario
        print(f"{Fore.GREEN}3. Listar Usuarios")  # Opción para listar todos los usuarios
        print(f"{Fore.GREEN}4. Buscar Usuario por ID")  # Opción para obtener un usuario por ID
        print(f"{Fore.GREEN}5. Actualizar Usuario")  # Opción para actualizar un usuario
        print(f"{Fore.GREEN}6. Borrar Usuario")  # Opción para eliminar un usuario
        print(f"{Fore.GREEN}7. Guardar Resultados en Excel")  # Opción para guardar resultados en un archivo Excel
        print(f"{Fore.RED}8. Terminar")  # Opción para salir del programa
        print(f"{Fore.CYAN}======================")

    def read_excel(self):
        # Lee el archivo Excel de entrada si está especificado y verifica su formato
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

    def save_results(self):
        # Guarda los resultados de las operaciones en un archivo Excel
        try:
            output_path = self.output_file
            if not output_path.endswith('.xlsx'):
                output_path += '.xlsx'
            if self.results:
                df = pd.DataFrame(self.results)
                df.to_excel(output_path, index=False)
                print(f"{Fore.GREEN}Resultados guardados en {output_path}")
            else:
                print(f"{Fore.YELLOW}Advertencia: No hay resultados para guardar.")
        except Exception as e:
            print(f"{Fore.RED}Error al guardar el archivo Excel: {e}")

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
            result = response.json()
            # Almacena el resultado de la operación
            self.results.append({
                'id': id_usuario, 'nombre': nombre, 'correo': correo,
                'operation': 'create', 'status': 'success'
            })
            print(f"{Fore.GREEN}Usuario creado: {result}")  # Muestra mensaje de éxito con la respuesta
        except requests.exceptions.RequestException as e:
            # Almacena el error en los resultados
            self.results.append({
                'id': id_usuario, 'nombre': nombre, 'correo': correo,
                'operation': 'create', 'status': 'failed', 'error': str(e)
            })
            print(f"{Fore.RED}[X] Error al crear usuario: {e}")  # Muestra mensaje de error

    def listar_usuarios(self):
        # Envía una solicitud GET para listar todos los usuarios
        url = f'{API_URL}/usuarios'  # Endpoint de la API para listar usuarios
        try:
            response = requests.get(url)  # Envía la solicitud GET
            response.raise_for_status()  # Lanza un error si la solicitud falla
            usuarios = response.json()  # Analiza la respuesta JSON
            # Almacena el resultado de la operación
            self.results.append({
                'operation': 'list', 'status': 'success', 'data': usuarios
            })
            print(f"{Fore.GREEN}Usuarios encontrados:")  # Muestra encabezado para la lista de usuarios
            for usuario in usuarios:
                # Muestra los detalles de cada usuario en amarillo
                print(f"{Fore.YELLOW}- ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            # Almacena el error en los resultados
            self.results.append({
                'operation': 'list', 'status': 'failed', 'error': str(e)
            })
            print(f"{Fore.RED}[X] Error al listar usuarios: {e}")  # Muestra mensaje de error

    def obtener_usuario(self, id_usuario):
        # Envía una solicitud GET para obtener un usuario por ID
        url = f'{API_URL}/usuarios/{id_usuario}'  # Endpoint de la API para obtener un usuario específico
        try:
            response = requests.get(url)  # Envía la solicitud GET
            response.raise_for_status()  # Lanza un error si la solicitud falla
            usuario = response.json()  # Analiza la respuesta JSON
            # Almacena el resultado de la operación
            self.results.append({
                'id': id_usuario, 'operation': 'get', 'status': 'success',
                'nombre': usuario['nombre'], 'correo': usuario['correo']
            })
            # Muestra los detalles del usuario encontrado
            print(f"{Fore.GREEN}Usuario encontrado: ID: {usuario['id']}, Nombre: {usuario['nombre']}, Correo: {usuario['correo']}")
        except requests.exceptions.RequestException as e:
            # Almacena el error en los resultados
            self.results.append({
                'id': id_usuario, 'operation': 'get', 'status': 'failed', 'error': str(e)
            })
            print(f"{Fore.RED}[X] Error al obtener usuario: {e}")  # Muestra mensaje de error

    def actualizar_usuario(self, id_usuario, nombre, correo):
        # Envía una solicitud PUT para actualizar un usuario existente
        url = f'{API_URL}/usuarios'  # Endpoint de la API para actualizar usuarios
        headers = {'Content-Type': 'application/json'}  # Especifica el tipo de contenido JSON
        data = {'id': str(id_usuario), 'nombre': nombre, 'correo': correo}  # Datos actualizados del usuario
        try:
            response = requests.put(url, headers=headers, data=json.dumps(data))  # Envía la solicitud PUT
            response.raise_for_status()  # Lanza un error si la solicitud falla
            result = response.json()
            # Almacena el resultado de la operación
            self.results.append({
                'id': id_usuario, 'nombre': nombre, 'correo': correo,
                'operation': 'update', 'status': 'success'
            })
            print(f"{Fore.GREEN}Usuario actualizado: {result}")  # Muestra mensaje de éxito con la respuesta
        except requests.exceptions.RequestException as e:
            # Almacena el error en los resultados
            self.results.append({
                'id': id_usuario, 'nombre': nombre, 'correo': correo,
                'operation': 'update', 'status': 'failed', 'error': str(e)
            })
            print(f"{Fore.RED}[X] Error al actualizar usuario: {e}")  # Muestra mensaje de error

    def borrar_usuario(self, id_usuario):
        # Envía una solicitud DELETE para eliminar un usuario por ID
        url = f'{API_URL}/usuarios/{id_usuario}'  # Endpoint de la API para eliminar un usuario
        try:
            response = requests.delete(url)  # Envía la solicitud DELETE
            response.raise_for_status()  # Lanza un error si la solicitud falla
            result = response.json()['mensaje']
            # Almacena el resultado de la operación
            self.results.append({
                'id': id_usuario, 'operation': 'delete', 'status': 'success'
            })
            print(f"{Fore.GREEN}Usuario borrado: {result}")  # Muestra mensaje de éxito
        except requests.exceptions.RequestException as e:
            # Almacena el error en los resultados
            self.results.append({
                'id': id_usuario, 'operation': 'delete', 'status': 'failed', 'error': str(e)
            })
            print(f"{Fore.RED}[X] Error al borrar usuario: {e}")  # Muestra mensaje de error

    def run(self):
        # Bucle principal para ejecutar la interfaz CLI y manejar las interacciones del usuario
        while True:
            self.display_menu()  # Muestra el menú
            choice = input(f"{Fore.CYAN}Seleccione la opción (1-8): {Style.RESET_ALL}")  # Obtiene la opción del usuario
            if choice == '1':
                # Especifica la ruta del archivo Excel de entrada
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
                # Solicita el nombre del archivo Excel de salida y guarda los resultados
                self.output_file = input(f"{Fore.CYAN}Ingrese el nombre del archivo Excel de salida (default: api_results.xlsx): {Style.RESET_ALL}").strip() or "api_results.xlsx"
                self.save_results()
            elif choice == '8':
                # Sale del programa
                print(f"{Fore.GREEN}Exiting...")
                break
            else:
                # Maneja opciones de menú no válidas
                print(f"{Fore.RED}Opción inválida. Por favor seleccione 1-8.")

if __name__ == '__main__':
    # Crea una instancia del cliente CLI y ejecuta el programa
    client = SimpleAPIClientCLI()
    client.run()

Comparación de los Archivos



Característica
data.py
data1B.py
data2.py
data2B.py



Interfaz CLI
❌
✅
✅
✅


Salida coloreada
❌
✅
✅
✅


Soporte para Excel (entrada)
❌
❌
✅
✅


Registro de resultados en Excel
❌
❌
❌
✅


Validación de entrada
❌
✅
✅
✅


Operaciones masivas
❌
❌
✅
✅


Trazabilidad de operaciones
❌
❌
❌
✅


Cómo Usar los Códigos

Requisitos:

Instalar dependencias: pip install requests colorama pandas openpyxl.
Asegurarse de que la URL de la API (API_URL) sea correcta y la API esté operativa.


Ejecución:

data.py: Descomentar las pruebas en el bloque if __name__ == '__main__' y ejecutar python data.py.
data1B.py: Ejecutar python data1B.py y seguir el menú interactivo.
data2.py: Ejecutar python data2.py, opcionalmente especificar un archivo Excel con columnas id, nombre, correo.
data2B.py: Ejecutar python data2B.py, usar el menú para realizar operaciones y guardar resultados en un archivo Excel.


Formato del Archivo Excel (para data2.py y data2B.py):

Columnas requeridas: id (texto o número), nombre (texto), correo (texto).
Ejemplo:id,nombre,correo
1,Juan Pérez,juan@ejemplo.com
2,María López,maria@ejemplo.com




Archivo de Salida (data2B.py):

Contiene columnas como id, nombre, correo, operation, status, error (si aplica).
Ejemplo:id,nombre,correo,operation,status
1,Juan Pérez,juan@ejemplo.com,create,success
2,María López,maria@ejemplo.com,update,failed,404 Not Found





Conclusión
Los cuatro scripts representan una evolución en la interacción con una API de usuarios:

data.py es ideal para pruebas iniciales.
data1B.py mejora la usabilidad con una CLI.
data2.py añade soporte para operaciones masivas con Excel.
data2B.py ofrece trazabilidad completa con registro de resultados.

Cada versión es adecuada para diferentes necesidades, desde pruebas rápidas hasta aplicaciones robustas. Los códigos son modulares, bien documentados y manejan errores de manera efectiva, haciéndolos aptos para entornos de desarrollo y producción.
