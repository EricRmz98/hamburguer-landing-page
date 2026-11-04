# Plan de trabajo de la landing

Este plan organiza la construcción de la landing de hamburguesas. Su pieza distintiva es un minijuego de pixel art en la segunda sección: el visitante prepara hamburguesas para clientes en un mostrador, primero con un tutorial guiado que invita a pedir la hamburguesa real y después en un modo infinito.

El nombre de la marca y el hero siguen pendientes.

## Etapas

| Etapa | Alcance | Estado |
| --- | --- | --- |
| 01 | Hero | Alcance por definir |
| 02 | [Minijuego de hamburguesas](02-minijuego/PLAN.md) | F1–F4 implementadas; arte aprobado con doce clientes nativos y Endesga-64. Siguen sonido (F5) e integración/revisión final (F6) |
| 03 | Resto de la landing y contenido comercial | Alcance por definir |
| 04 | Revisión conjunta de responsive, accesibilidad y rendimiento | Alcance por definir; cada etapa también debe comprobar estos aspectos |

Crear una carpeta por etapa cuando se concrete su alcance. Dentro de cada carpeta, `PLAN.md` describe el objetivo, las decisiones, las tareas y los criterios de aceptación. Añadir otros documentos únicamente cuando sean necesarios.

## Documentos de la etapa 02

- [PLAN.md](02-minijuego/PLAN.md): decisiones, mecánicas, recetas, tutorial, motor, sonido, fases y pendientes.
- [ASSETS.md](02-minijuego/ASSETS.md): sprites definidos como texto con paleta, horneado a imágenes, herramientas, guía de estilo e inventario.
- [Revisiones visuales](../design-proposals/README.md): capturas del acabado aprobado e historial de propuestas.

Último cierre visual: 3 de noviembre de 2026. Composición horizontal/vertical con una escala entera compartida, cocina detallada, tres quemadores disponibles desde el inicio y salseros alargados de 16 × 42. Validación: 161 pruebas y compilación correctas. La revisión en teléfono físico sigue pendiente.

## Cómo mantener el plan

Distinguir las decisiones acordadas de los valores iniciales propuestos. Al afinar un detalle, actualizar el documento correspondiente para que no se contradigan. Marcar tareas completadas únicamente cuando se hayan implementado y comprobado.
