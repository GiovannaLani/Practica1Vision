# Guía

Este programa permite marcar regiones poligonales sobre un vídeo, ajustar su posición en distintos fotogramas y generar vídeos en los que se conserva o se oculta el contenido de esas regiones.

## Preparación

1. Coloca `Video Práctica.mp4` en la misma carpeta que el script.
2. Ejecuta `main.py`.
3. Se abrirá una ventana con el vídeo. La posición de las regiones se define haciendo clic en esa ventana.

El programa lee el vídeo desde el principio al iniciarse. Las teclas de navegación permiten cambiar de fotograma mientras se marcan o ajustan las figuras.

## Teclas

| Tecla | Acción |
| --- | --- |
| `d` | Avanza un fotograma. |
| `f` | Avanza un segundo. |
| `s` | Retrocede un fotograma. |
| `a` | Retrocede un segundo. |
|  |  |
| `Ctrl+Z` | Deshace el último paso al dibujar: si estás colocando puntos, elimina el último punto; si acabas de cerrar una figura, la vuelve a abrir y quita el último punto. |
| `Shift + Click Izq` | Borra una figura |
|  |  |
| `V` | Alterna la visibilidad de las figuras en el fotograma actual. |
| `K` | Guarda o elimina un fotograma clave. |
| `T` | Selecciona la siguiente figura. |
| | |
| `G` | Abre el menú para generar vídeos. |
| `Q` | Cierra la ventana y termina el programa. |

Los vídeos se guardan en la carpeta desde la que se ejecuta el
programa, si ya existe un archivo con el mismo nombre, se sobrescribe.

## Dibujar y editar regiones

- **Dibujar un polígono:** haz clic con el botón izquierdo para añadir vértices.Para cerrar la figura, haz clic con el botón izquierdo cerca del primer vértice (a menos de 10 píxeles). Al cerrar la figura se tiene que introducir su nombre por consola.
- **Mover un vértice:** mantén pulsado el botón derecho sobre un vértice y arrástralo. Suelta el botón para guardar la posición ajustada.
- **Borrar una figura completa:** mantén pulsada la tecla Shift y haz clic con el botón izquierdo sobre uno de sus puntos. Se elimina la figura correspondiente
- **Cambiar la forma a lo largo del vídeo:** si guardas una figura en fotogramas distintos el programa la mueve poco a poco entre esas dos posiciones.

El panel de la ventana muestra información sobre la figura activa, el fotograma actual y la línea de tiempo.

## Diferencia entre los vídeos
Pulsa G para abrir el menú de generación. Después, introduce en la consola el número de la opción que quieras ejecutar.

| Opción | Resultado |
| --- | --- |
| `1` | Genera un vídeo que resalta las regiones. |
| `2` | Genera un vídeo que pone en negro el contenido dentro de las regiones seleccionadas y conserva el exterior. |
| `3` | Genera un vídeo que muestra únicamente las regiones seleccionadas y pone en negro el resto. |
| `4` | Genera un vídeo independiente por cada región seleccionada. |
