# Landing de hamburguesas

Proyecto Astro con un minijuego de preparación de hamburguesas: tutorial guiado, modo infinito, recetas por dificultad y récord local. La marca, el hero y el destino de pedidos siguen pendientes.

## Estado actual

La dirección visual aprobada utiliza exactamente los 64 colores de Endesga-64 y una cuadrícula común para clientes, entorno y cocina. Los doce clientes tienen retratos nativos de 96 × 120, proporciones revisadas y orientaciones alternadas. El comedor industrial, la barra roja con acero, los ingredientes y los salseros siguen ese mismo acabado.

El escenario tiene composiciones horizontal de 320 × 212 y vertical de 180 × 300, ampliadas siempre con una escala entera. La plancha dispone de tres quemadores desde el inicio. Los salseros finales miden 16 × 42, con cuerpo alargado, boquilla fina y sombra de apoyo.

F1–F4 están implementadas. Siguen pendientes el sonido (F5), la integración y revisión final de la landing (F6) y la comprobación en un teléfono físico. La validación actual comprende 161 pruebas y la compilación de producción.

## Desarrollo

Requiere Node.js 22.12 o superior y pnpm. Las dependencias están fijadas en `pnpm-lock.yaml`.

```sh
pnpm install --frozen-lockfile
pnpm dev
```

| Ruta | Uso |
| --- | --- |
| `/#minijuego` | Minijuego integrado en la landing |
| `/clientes-prueba` | Composición real con selector de los doce clientes y vistas horizontal/vertical |
| `/sprites` | Inspección del atlas y las definiciones de sprites |

Las dos páginas de revisión existen únicamente con el servidor de desarrollo y no se publican en la compilación.

```sh
pnpm test
pnpm build
pnpm preview
```

## Fuentes y documentación

- [Plan de trabajo](working-plan/README.md): etapas y estado del proyecto.
- [Minijuego](working-plan/02-minijuego/PLAN.md): reglas, arquitectura, fases y pendientes.
- [Activos](working-plan/02-minijuego/ASSETS.md): paleta, matriz de píxeles, tamaños y dirección artística vigente.
- [Generadores de sprites](scripts/sprites/README.md): regeneración de cocina, clientes y entorno desde las fuentes editables.
- [Revisiones visuales](design-proposals/README.md): referencias, iteraciones y capturas del resultado aprobado.

Los recursos de producción son las definiciones de `src/game/sprites/`. Las fuentes editables están en `scripts/sprites/`; la compilación y la regeneración habitual no dependen de las propuestas archivadas.
