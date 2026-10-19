# Guía de uso

La aplicación permite dibujar regiones poligonales sobre un vídeo, animar su posición mediante fotogramas clave, controlar cuándo son visibles y exportar vídeos con las regiones resaltadas, ocultas, aisladas o separadas en archivos individuales.

## Requisitos e inicio

- Python
- OpenCV (`opencv-python`)
- NumPy
- El vídeo de entrada `Video Práctica.mp4`

Instala las dependencias si todavía no están disponibles:

```bash
pip install opencv-python numpy
```

Coloca `Video Práctica.mp4` en la carpeta donde esté el código a ejecutar y ejecuta la aplicación desde esa carpeta:

```bash
python main.py
```

El vídeo y los archivos generados se buscan o guardan en la carpeta de trabajo actual. Las figuras y sus fotogramas clave solo se conservan durante la ejecución; no se guardan para la siguiente sesión.

## Controles

| Tecla o acción | Función |
| --- | --- |
| `D` | Avanza un fotograma. |
| `F` | Avanza aproximadamente un segundo. |
| `S` | Retrocede un fotograma. |
| `A` | Retrocede aproximadamente un segundo. |
| `Ctrl+Z` | Quita el último punto del polígono que se está dibujando. |
| `Clic izquierdo` | Añade un vértice al polígono en curso. |
| `Clic izquierdo` cerca del primer vértice | Cierra el polígono (debe tener al menos tres vértices). |
| `Clic derecho y arrastrar` | Mueve un vértice de una figura existente; al soltar, guarda su forma en el fotograma actual. |
| `Shift` + `clic izquierdo` sobre un vértice | Elimina la figura completa. |
| `T` | Selecciona la siguiente figura para editar sus fotogramas clave o su visibilidad. |
| `V` | Alterna la visibilidad de la figura activa en el fotograma actual. |
| `K` | Guarda la forma actual como fotograma clave o elimina el fotograma clave actual. |
| `G` | Abre en la consola el menú de exportación de vídeos. |
| `Q` | Cierra la ventana y termina la aplicación. |

La ventana muestra el nombre y estado de la figura activa, el número del fotograma y una línea de tiempo. Los marcadores de la línea de tiempo indican los fotogramas clave; los tramos verdes representan visibilidad y los rojos, ocultación.

## Crear y animar figuras

1. Haz clic con el botón izquierdo para colocar vértices.
2. Cierra el polígono haciendo clic a menos de 10 píxeles del primer vértice.
3. Introduce un nombre en la consola; pulsa Enter para usar `Figura N`.
4. Para cambiar su forma a lo largo del vídeo, navega a otro fotograma, selecciona la figura con `T` si hace falta y arrastra sus vértices. Al soltar, la forma se guarda como fotograma clave.

La aplicación interpola la posición de los vértices entre fotogramas clave. Al crear una figura después del primer fotograma, también se registra como oculta desde el inicio hasta el fotograma en que se creó. Usa `V` para alternar su visibilidad en el fotograma actual. `K` permite añadir un fotograma clave con la forma interpolada actual o borrar el fotograma clave actual; no elimina el último fotograma clave de una figura.

## Exportar vídeos

Pulsa `G` y escribe en la consola el número de la opción:

| Opción | Resultado | Archivo(s) |
| --- | --- | --- |
| `1` | Dibuja los contornos de las regiones visibles sobre el vídeo original. | `MyOutputVid.avi` |
| `2` | Pone en negro las regiones visibles y conserva el resto del vídeo. | `MyOutputVid_HideFigures.avi` |
| `3` | Conserva las regiones visibles y pone en negro el fondo. | `MyOutputVid_HideBackground.avi` |
| `4` | Genera un vídeo por cada figura, aislando la región y recortándola en torno a su área. El tamaño del recorte se calcula a partir de las formas guardadas en sus fotogramas clave. | `region_<id>.avi` |

Las opciones 1–3 combinan todas las regiones visibles en cada fotograma. La opción 4 crea los archivos únicamente para las figuras con fotogramas clave válidos. Si ya existe un archivo de salida con el mismo nombre, se sobrescribe.
