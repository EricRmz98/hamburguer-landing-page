# Revisión de consistencia del comedor

Corrección identificada: las sillas de la tanda anterior usaban un tamaño en pantalla con multiplicadores independientes, mientras mesas y bancos usaban coordenadas de la escena. Se sustituyeron por sillas modeladas con la misma proyección y medidas comunes a todo el mobiliario.

- Asiento de sillas y bancos: 0.35 unidades sobre el suelo.
- Tablero: 0.65; cara inferior: 0.56. Separación vertical asiento/tablero: 0.30.
- Respaldo de silla: 0.92; banco: 0.95.
- Silla: 0.62 × 0.60 de huella; mesas centrales: 1.30 × 0.88.
- Dos bancos bajo ventanas con mesa y dos sillas opuestas cada uno.
- Cuatro conjuntos laterales de banco, mesa y silla enfrentada.
- Dos mesas centrales con dos sillas cada una.

Total: ocho mesas, seis bancos y doce sillas. Se dibujan desde el fondo hacia el primer plano. Todas las sillas tienen patas, asiento y respaldo; su tamaño cambia exclusivamente con la profundidad. Se mantienen los detalles de los tableros, tapicería roja, interior industrial y barra recta aprobada.

Verificación: ambas imágenes inspeccionadas visualmente. Comprobación automática de huellas de todas las piezas sin intersecciones en el plano del suelo y de pertenencia a Endesga 32. Estas unidades sirven para coherencia visual; no son un plano arquitectónico ni certifican anchos reglamentarios de circulación. El cliente y algunos muebles ocultan naturalmente piezas posteriores; la vista limpia permite revisar los conjuntos.

`selected-interior-4x.png`: comedor limpio. `selected-context-4x.png`: muestra contextual. Versiones ×1 incluidas. Generador `generate.py`, requiere Pillow y las herramientas de la tanda cartoon anterior.

Sin integración ni cambios de sprites finales. Pendientes comanda/globo/HUD, móvil, otros clientes y animación.
