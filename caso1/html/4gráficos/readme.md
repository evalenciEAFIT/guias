# Paso a paso para crear una página HTML con Chart.js mostrando cuatro tipos de gráficos

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
2. Incluye la referencia a Chart.js desde el CDN, cuatro lienzos (`canvas`) para los gráficos y estilos CSS para organizar los gráficos en una cuadrícula
3. Asegúrate de enlazar el archivo `script.js`

## Paso 3: Crear el código JavaScript para los gráficos
1. Copia el contenido del archivo `script.js` proporcionado
2. El código genera cuatro gráficos:
   - Gráfico de barras
   - Gráfico de líneas
   - Gráfico de pastel
   - Gráfico de área polar
3. Todos los gráficos usan los mismos datos de ejemplo para comparación

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
3. Deberías ver una página con cuatro gráficos diferentes mostrando los mismos datos de ejemplo

## Notas adicionales
- El puerto 8000 es el predeterminado; cámbialo si es necesario en el comando
- Para detener el servidor, presiona `Ctrl+C` en la terminal
- Modifica los datos en `script.js` (arreglo `datos` o `labels`) para personalizar los gráficos
- Explora la documentación de Chart.js para más tipos de gráficos o configuraciones avanzadas
