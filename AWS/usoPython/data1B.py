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