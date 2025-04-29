# Paso a paso para crear una página HTML con Chart.js y servirla con Python HTTP Server

## Requisitos previos
- Tener instalado Python 3.x
- Un editor de texto (como VS Code, Notepad++, etc.)
- Un navegador web

## Paso 1: Crear la estructura del proyecto
1. Crea una carpeta para tu proyecto, por ejemplo, `mi_proyecto_graficos`
2. Dentro de la carpeta, crea dos archivos:
   - `index.html`
   - `script.js`

## Paso 2: Crear la página HTML
1. Copia el contenido del archivo `index.html` proporcionado
2. Asegúrate de que incluya la referencia a Chart.js desde el CDN y el enlace al archivo `script.js`

## Paso 3: Crear el código JavaScript para el gráfico
1. Copia el contenido del archivo `script.js` proporcionado
2. Este código crea un gráfico de barras con datos de ejemplo

## Paso 4: Configurar el servidor HTTP con Python
1. Abre una terminal o línea de comandos
2. Navega a la carpeta de tu proyecto:
```bash
cd ruta/a/mi_proyecto_graficos
```
3. Inicia el servidor HTTP con Python:
```bash
python -m http.server 8000
```

## Paso 5: Visualizar la página
1. Abre un navegador web
2. Visita `http://localhost:8000`
3. Deberías ver una página con un gráfico de barras mostrando datos de ejemplo

## Notas adicionales
- El puerto 8000 es el predeterminado, pero puedes usar otro cambiando el número en el comando
- Para detener el servidor, presiona `Ctrl+C` en la terminal
- Puedes modificar los datos en `script.js` para mostrar diferentes valores o tipos de gráficos
- Chart.js ofrece otros tipos de gráficos (líneas, pastel, etc.) que puedes explorar en su documentación oficial
