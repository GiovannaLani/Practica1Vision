# Guía de `generarVideoPorRegion.py`

Este programa permite marcar regiones poligonales sobre un vídeo, ajustar su
posición en distintos fotogramas y generar vídeos en los que se conserva o se
oculta el contenido de esas regiones.

## Preparación

1. Coloca `Video Práctica.mp4` en la misma carpeta que el script.
2. Ejecuta `generarVideoPorRegion.py`.
3. Se abrirá una ventana con el vídeo. La posición de las regiones se define
   haciendo clic en esa ventana.

El programa lee el vídeo desde el principio al iniciarse. Las teclas de
navegación permiten cambiar de fotograma mientras se marcan o ajustan las
figuras.

## Teclas

| Tecla | Acción |
| --- | --- |
| `Espacio` | Avanza un fotograma. |
| `d` | Avanza un fotograma, igual que la barra espaciadora. |
| `f` | Avanza aproximadamente un segundo, usando la cantidad de fotogramas por segundo del vídeo. |
| `s` | Retrocede un fotograma. |
| `a` | Retrocede aproximadamente un segundo. |
| `Ctrl+Z` | Deshace el último paso al dibujar: si estás colocando puntos, elimina el último punto; si acabas de cerrar una figura, la vuelve a abrir y quita el último punto. |
| `B` | Borra del fotograma actual las figuras y los puntos que se están editando y registra que en este punto de la secuencia no hay regiones. El cambio se tiene en cuenta al generar los vídeos. |
| `G` | Genera `MyOutputVid.avi`: conserva el contenido situado dentro de todas las figuras y pone en negro el exterior. |
| `M` | Genera un vídeo por región, con nombres `VideoFigura1.avi`, `VideoFigura2.avi`, etc. Cada vídeo conserva únicamente el contenido dentro de la figura correspondiente y pone el resto en negro. |
| `L` | Genera `VideoRegionesEnNegro.avi`: pone en negro el contenido dentro de todas las figuras y conserva el exterior. |
| `Q` | Cierra la ventana y termina el programa. |

Las teclas de acción (`B`, `G`, `M` y `L`) funcionan tanto en mayúsculas como en
minúsculas. Los vídeos se guardan en la carpeta desde la que se ejecuta el
programa; si ya existe un archivo con el mismo nombre, se sobrescribe.

## Dibujar y editar regiones

- **Dibujar un polígono:** haz clic con el botón izquierdo para añadir vértices.
  Para cerrar la figura, haz clic con el botón izquierdo cerca del primer
  vértice (a menos de 10 píxeles). Se necesitan al menos tres vértices para que
  la figura oculte o conserve píxeles.
- **Mover un vértice:** mantén pulsado el botón derecho sobre un vértice y
  arrástralo. Suelta el botón para guardar la posición ajustada.
- **Cambiar la forma a lo largo del vídeo:** si guardas una figura en dos
  fotogramas distintos y tiene el mismo número de puntos en ambos, el programa
  la mueve poco a poco entre esas dos posiciones.
- El contador de la esquina de la ventana muestra el fotograma actual y el
  número total de fotogramas.

## Diferencia entre los vídeos

- `G` conserva las regiones marcadas y oculta todo lo demás.
- `M` hace lo mismo que `G`, pero crea un archivo independiente para cada
  región.
- `L` oculta las regiones marcadas y conserva todo lo demás.

Las tres opciones procesan el vídeo completo, no solo el fotograma visible al
pulsar la tecla. Conviene guardar las regiones en los fotogramas deseados antes
de generar los archivos.