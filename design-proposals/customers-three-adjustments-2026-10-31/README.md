# Vale, Alex e Ivo: tres ajustes

Referencias derivadas de `customers-final-polish-2026-10-31`, sin integración en el juego. Los otros veintiún clientes conservan exactamente los píxeles de esa versión.

- **Vale:** mejillas inferiores algo más llenas y barbilla más ancha y suave, manteniendo el alto de la cabeza, la cresta rosa, los ojos, la nariz, la boca y los piercings. El contorno inferior sigue siendo simétrico.
- **Alex:** peinado corto de lado, con raya visible, nacimiento irregular, mechones y sienes cortas. Se conserva la paleta de pelo gris azulado y la cara.
- **Ivo:** se afina gradualmente el antebrazo desde el codo hacia la muñeca. El grosor del brazo superior, la posición del codo, la pose, la cabeza y la playera conservan su diseño anterior.

## Imágenes

- `vale-alex-ivo-review.png`: los tres clientes y detalles antes/después.
- `customers-three-adjustments-01-12.png` y `customers-three-adjustments-13-24.png`: elenco completo.
- `customers-three-adjustments-context.png`: composición en el escenario.
- `customer-NN-1x.png` y `face-NN-1x.png`: sprites y cabezas nativas con transparencia.

## Verificación

Inspección visual de los tres sprites ampliados y de sus detalles antes/después. El generador valida paleta, transparencia, márgenes, siluetas conectadas, facciones conservadas y alcance de los cambios: solo dos cabezas modificadas y tres sprites modificados entre los veinticuatro. Los brazos conservan el contorno continuo, sin líneas de separación en los codos.

`scope-checks.json` comprueba además que todos los píxeles cambiados en Ivo se sitúan en el área de los antebrazos. `checks.json` y `gesture-contact-checks.json` contienen las comprobaciones del elenco. Estas comprobaciones complementan la revisión visual.

Se preservan las referencias anteriores y los clientes de producción.
