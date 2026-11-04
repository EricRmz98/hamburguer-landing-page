# Acero de la barra basado en puerta y plancha

Se usaron como referencias locales la placa metálica inferior de la puerta y el frontal de la plancha. `referencias-material.png` muestra, de arriba abajo, la puerta, la plancha y la versión anterior de la barra, ampliadas por factores enteros para inspección.

La barra utiliza ahora la base `gris` de la plancha, reflejos localizados en `gris-claro` y `plata`, y sombra de canto en `gris-azul` y `pizarra`. La reflexión se distribuye en planos estrechos, con modulación fina del cepillado dentro del brillo. Se retira la franja blanca ancha que dominaba la superficie. El resultado se dibuja directamente en las celdas nativas con los colores existentes de Endesga64.

Solo se modifican `barra_roja` y `barra_roja_v`. La basura con bolsa y borde elevado, la puerta, la plancha, los ingredientes, los clientes y todas las posiciones mantienen sus matrices. `checks.json` verifica tamaños, paleta y conservación de los demás sprites.

161 pruebas y compilación correctas. Revisión de las composiciones horizontal y vertical. `composicion-final.png` reúne capturas reales del navegador; `antes-despues.png` compara con la barra anterior. No se revisó en teléfono físico.
