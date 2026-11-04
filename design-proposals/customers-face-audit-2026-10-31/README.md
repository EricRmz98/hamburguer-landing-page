# Fase 1: revisión exclusiva de los 24 rostros

Referencias corregidas, pendientes de aprobación. No se han sustituido los clientes activos del juego. La revisión de cuerpos queda para una segunda fase.

## Correcciones

| Antes | Después | Motivo |
| --- | --- | --- |
| Parche oscuro en el extremo inferior derecho de la cara | Piel de color plano dentro del contorno, sin parche lateral | Evita la mancha que torcía visualmente la mandíbula. |
| Mandíbulas dibujadas con polígonos cuyo rasterizado variaba entre ambos lados | Cada fila del contorno se construye desde un único eje central | Garantiza el mismo ancho a izquierda y derecha sin borrar las diferencias entre personajes. |
| Ambos ojos usaban el mismo desplazamiento hacia un lado | El ojo derecho se refleja del izquierdo | Pupilas, cejas y gestos quedan alineados respecto a la nariz. |
| Nariz con un píxel hacia la derecha | Marca vertical sobre el eje de la cara | Elimina el desplazamiento lateral de la nariz. |
| Gafas dibujadas por separado con pupilas descentradas dentro de cada lente | Montura derecha reflejada de la izquierda y puente centrado | Ambos lentes tienen el mismo tamaño y la misma relación con los ojos. |
| Barbas limitadas al interior de la cara, dejando el contorno de piel por fuera | La barba ocupa también el borde exterior de la mandíbula | Elimina el halo de piel alrededor de Nico e Ivo. |
| Parche rectangular de piel para dibujar la boca dentro de la barba | Boca trazada directamente sobre el color de la barba | Evita el recuadro de piel flotante. |
| Bigote rasterizado en una sola línea con escalones desiguales | Ambas mitades se dibujan por reflexión | Mantiene el bigote de Chema simétrico. |

## Verificación

Se inspeccionaron visualmente los 24 rostros ampliados y las dos láminas de personajes completos. El generador comprueba para cada cliente:

- Igualdad exacta de colores y transparencia entre ambas mitades del rostro, incluyendo sus rasgos; el pelo se mantiene en capas independientes y conserva su asimetría.
- Simetría exacta de las monturas.
- Color base de piel idéntico en ambas mejillas.
- Ausencia de colores de piel dentro de la máscara de barba, incluido su borde exterior.
- Cuerpos, brazos, manos, ropa y poses idénticos al generador anterior al renderizarlos sin cabeza.
- Filas por debajo de la mandíbula idénticas en los sprites completos anterior y nuevo.
- Tamaño de 64 × 80, transparencia binaria, paleta Endesga 32 y 24 sprites diferentes.

Las 24 comprobaciones individuales están en [checks.json](checks.json). El pelo se reproduce con los mismos módulos, escala y geometría de la versión anterior; no se refleja junto con la cara. Se conservan los accesorios del pelo, incluidos los colores diferentes de los goggles de Noa.

## Imágenes

- [24 rostros corregidos](faces-24.png)
- [Comparación antes/después de ocho casos](faces-before-after.png)
- [Personajes completos 01–12](customers-face-audit-01-12.png)
- [Personajes completos 13–24](customers-face-audit-13-24.png)

Cada rostro también se entrega separado en `face-NN-1x.png`; cada personaje completo, en `customer-NN-1x.png`.
