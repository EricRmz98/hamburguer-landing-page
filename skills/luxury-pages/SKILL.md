---
name: luxury-pages
description: Crear o refinar Luxury Pages en esta plantilla Astro usando Luxury Web Design como metodología y referencias de páginas seleccionadas según el proyecto.
---

# Luxury Pages

## Metodología de trabajo

Leer y aplicar [Luxury Web Design](skillBaseLuxuryPages.md) al iniciar o refinar una Luxury Page. Es la metodología común: concepto, dirección artística, experiencia, composición, motion, interacción, selección tecnológica, optimización y revisión visual. Mantener una identidad propia por marca y justificar cada efecto por su función y calidad percibida.

Las herramientas y skills mencionadas en la metodología se utilizan cuando aportan al encargo. La preparación de las skills complementarias se rige por la sección siguiente. Esto no autoriza publicaciones ni otras acciones externas ajenas a esa preparación.

## Preparación de skills complementarias

Antes de crear o refinar una landing con esta plantilla, comprobar si el agente tiene disponibles las siguientes skills de la sección 33 de Luxury Web Design:

- `animation-vocabulary`
- `animate`
- `find-animation-opportunities`
- `improve-animations`
- `apple-design`
- `emil-design-eng`
- `ui-ux-pro-max`
- `mobile-native`
- `break-ui`
- `dataviz`

Si falta alguna, instalarla usando el instalador o mecanismo de skills del agente. Esta plantilla solicita esa preparación automática dentro de los permisos del entorno; no volver a pedir confirmación por rutina cuando la instalación ya esté autorizada. Consultar primero el catálogo del entorno y después, si es necesario, el repositorio o catálogo oficial del autor. Verificar la identidad, el propósito y el archivo `SKILL.md` antes de instalar: no asumir que un paquete con el mismo nombre es la skill buscada ni inventar URLs o autores. Si la fuente es ambigua, solicitar únicamente la fuente que falta.

Usar el directorio y formato de instalación compatibles con el agente que abra el proyecto; no fijar rutas personales ni asumir que todos los agentes usan Codex. Conservar las skills ya instaladas, sin sobrescribirlas ni actualizarlas automáticamente. Registrar la fuente y revisión instalada cuando el mecanismo lo permita. Leer las skills pertinentes al encargo después de prepararlas y aplicar sus criterios junto con esta metodología.

Si la instalación requiere permisos adicionales, respetar el mecanismo de aprobación del entorno. Si no hay una fuente verificable, acceso a red o instalador compatible, explicar qué skill quedó pendiente y por qué; continuar con la metodología local cuando sea posible. No afirmar que se instaló o cargó una skill sin comprobarlo. Si el agente necesita otra sesión o turno para descubrir las nuevas skills, indicarlo.

## Referencias de páginas

La carpeta `references/` reúne análisis de sitios concretos. Consultar las referencias pertinentes al concepto y a las interacciones del proyecto; extraer principios y adaptarlos a la marca. Las observaciones de un sitio no sustituyen la metodología ni imponen su estética, sus activos o su estructura a todos los proyectos.

| Referencia | Cuándo consultarla | Archivo |
| --- | --- | --- |
| The Watch — 60fps | Para estudiar continuidad cinematográfica del producto, cursor contextual, selección de variantes, materialidad y narrativa de scroll. Representa el nivel de ambición visual e interactiva solicitado. | [The Watch](references/the-watch.md) |

Cada análisis distingue comportamientos observados, criterios derivados y aspectos sin verificar. No presentar sugerencias como hechos comprobados ni deducir la tecnología interna solo por la apariencia. No reutilizar activos o textos de un sitio sin autorización.

## Incorporar nuevas referencias

Guardar cada nuevo análisis en un archivo propio `references/<nombre-del-sitio>.md` y añadirlo a la tabla con su utilidad para el proyecto. Incluir URL, fecha, alcance de navegación, composición, secuencia visual, interacciones probadas, resultados, límites de verificación y principios transferibles. Conservar los detalles específicos en ese archivo.

Leer las referencias seleccionadas para el encargo y explicar qué principios se aplicarán. Incorporar a la metodología únicamente aprendizajes generales que aporten a distintos proyectos; mantener los ejemplos de cada página en su referencia.

## Implementación en esta plantilla

Aprovechar Astro, Tailwind, GSAP y Lenis existentes. Inspeccionar su inicialización antes de añadir otra; evitar múltiples bucles de animación o gestores de scroll. Mantener contenido semántico en HTML.

Elegir fotografía, vídeo, secuencia de imágenes o 3D según los activos disponibles, impacto y rendimiento. Coordinar las animaciones que afectan a un mismo elemento, limpiar sus recursos al retirar escenas y proporcionar alternativas ante fallos de medios.

## Verificación y entrega

Aplicar la revisión de calidad y el polish de Luxury Web Design. Recorrer en navegador escritorio, tableta y móvil; revisar estados intermedios y desplazamiento en ambos sentidos. Probar las interacciones implementadas, teclado, foco, tacto, movimiento reducido y errores de medios. Ejecutar la compilación cuando cambie la implementación.

La entrega explica la dirección elegida, las referencias utilizadas, sus principios adaptados, las interacciones implementadas y lo que quedó sin verificar.
