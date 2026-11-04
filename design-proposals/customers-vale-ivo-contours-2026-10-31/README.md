# Vale e Ivo: contornos

Elenco aprobado por el usuario tras revisar `customers-all-24.png` e integrado en el juego. Derivado de `customers-three-adjustments-2026-10-31`; los otros veintidós clientes, incluido Alex, permanecen idénticos. La fuente de producción es `scripts/sprites/customers-approved.json`, independiente de estas propuestas.

- **Vale:** recupera el rostro fino de `customers-final-polish-2026-10-31`. Se redibuja únicamente la parte superior de la cabeza rapada para eliminar las puntas que sobresalían sobre las sienes. Conserva la cresta rosa. Desde la fila 13 de la cabeza hasta la barbilla, el retrato coincide exactamente con el rostro fino anterior.
- **Ivo:** se elimina un único píxel de la forma del antebrazo que generaba un saliente cuadrado con su contorno. El resultado modifica cuatro píxeles finales: uno de relleno y tres del borde. El borde inferior queda nivelado en ese tramo. Pose, grosor, manos, playera y cabeza se conservan.

## Entrega

- `vale-ivo-review.png`: clientes y detalles antes/después.
- `customers-vale-ivo-contours-01-12.png` y `customers-vale-ivo-contours-13-24.png`: elenco completo.
- `customer-NN-1x.png`: sprites de referencia nativos de 64 × 80 con transparencia.
- `face-NN-1x.png`: cabezas de referencia.

## Verificación

Inspección visual ampliada de los laterales de Vale y del contorno de Ivo. El generador verifica paleta, transparencia, márgenes, siluetas conectadas, contacto de gestos, brazos sin líneas interiores en los codos y alcance de los cambios: solo Vale e Ivo cambian. `scope-checks.json` documenta la restauración exacta de la cara fina y los cuatro píxeles corregidos en Ivo.

Se preservan las versiones anteriores. El cuadro de espera de cada cliente de producción coincide exactamente con esta referencia aprobada; las reacciones del juego solo modifican rasgos faciales.
