# Clientes con la cuadrícula y la paleta del minijuego

Esta versión sustituye la propuesta de 64 × 80 ampliada al 150 %. Los doce personajes se convierten directamente desde las referencias originales a matrices de **96 × 120**, sin ampliar los sprites anteriores. La vista de desarrollo `/clientes-prueba` utiliza esta versión.

Un píxel nativo del cliente equivale a un píxel lógico del escenario. El factor cliente/layout es **1**, y ambos se amplían únicamente con la escala entera general del juego. Los colores se extraen de `src/game/sprites/palette.ts`: exclusivamente Endesga 32, hasta 16 colores por personaje, transparencia binaria y sin dithering.

La cintura está en la fila 114: en horizontal `8 + 114 = 122`; en vertical `86 + 114 = 200`. Coincide con el borde de la barra. Se conservan las proporciones mediante una única escala por referencia y se reserva margen para la paciencia por encima del cabello.

## Revisión de proporciones y orientación

Inés se convierte al 85 % de la escala de encuadre anterior, por igual en ambos ejes. Su altura de cabeza a cintura pasa de 106 a 90 píxeles y la guía facial de 45,3 a 38,5 píxeles; la mediana de las otras once guías es de 37,6 píxeles. Estas guías son recuadros de referencia aproximados, no medidas anatómicas exactas. La cintura permanece en la fila 114, de modo que se percibe más bajita sin estirar el cuerpo para llenar el marco. Su límite superior pasa de la fila 8 a la 24.

Las orientaciones se alternan en el orden de revisión: Lía, Zoe, Mika, Rafa, Vega y Gael miran a la derecha; Bruno, Ciro, Alma, Dante, Inés y Sasha, a la izquierda. La orientación se guarda en las propias celdas del sprite, sin transformaciones CSS. El manifiesto registra orientación, reflejo, factor de proporción y límites faciales finales. Las otras once figuras conservan su tamaño.

`revision-proporciones/antes/` conserva los PNG y el manifiesto de la revisión anterior. `revision-proporciones/review-checks.json` comprueba la escala uniforme de Inés, la alternancia, la conservación exacta de las otras once siluetas y la ausencia de solapamiento de rostros con la comanda o la paciencia.

## Archivos

- `individuales/`: PNG transparentes nativos de 96 × 120.
- `ampliados/`: vistas de detalle a 4×, por vecino más cercano.
- `12-clientes-nativos.png`: lámina de revisión de los doce.
- `plantilla-96x120-transparente.png`: doce celdas de 96 × 120, cuatro columnas y tres filas.
- Los doce `.ts`, `customers.ts` y `sprite-definitions.json`: matrices importables por el motor actual.
- `composicion/`: capturas de la primera conversión nativa, anteriores a la revisión de proporciones.
- `revision-proporciones/composicion/`: capturas actualizadas de los doce en horizontal y vertical, y comparativa de Inés antes/después.
- `12-clientes-nativos.zip`: PNG, matrices, lámina, paleta, manifiesto y comprobaciones.

## Verificación y reproducción

1. `prepare.py` reduce las ilustraciones originales directamente al tamaño final y cuantiza a la paleta real. No utiliza los PNG de 64 × 80.
2. `node convert.mjs` comprueba dimensiones, alfa binario, paleta exacta, rasterización y copia al atlas sin cambios, y anclaje a ambos layouts. Escribe `engine-checks.json`.
3. `render.py` prepara las láminas y el paquete.
4. `composicion/browser-grid-checks.json` registra las 24 verificaciones en el navegador: el cliente y la pared tienen exactamente el mismo tamaño de fondo del atlas y sus posiciones se alinean con el mismo píxel lógico. A escala 2, los sprites miden 192 × 240 píxeles de pantalla, con cada píxel nativo en bloques uniformes de 2 × 2.

La comprobación global del centroide de luz se documenta como excepción por las distintas prendas, piel y cabello; se conservan las otras validaciones y se registran los avisos originales. La revisión visual sigue siendo necesaria para valorar rostros y materiales.

Entrega de revisión con un cuadro de espera por cliente. Todavía no sustituye el reparto activo ni incluye expresiones adicionales.
