# Guía de formato: HTML

Una sola vía: **`generar_documento_markdown`** con `formato: "html"`.

Escribe el documento en **Markdown** y el motor lo envuelve en una página HTML5 autónoma y con estilo (un solo archivo, sin dependencias externas).

Contrato:
- `formato`: `"html"`
- `contenido_markdown`: el documento en Markdown (tablas, listas, código con resaltado básico, citas).
- `nombre_archivo`: sin extensión.
- `estilo_css` (opcional): CSS completo que reemplaza el estilo por defecto. Úsalo para colores de marca, tipografía o layout propio. Si lo omites se aplica un estilo profesional limpio.

Úsala para páginas standalone, reportes navegables, fichas o cualquier entregable que se vea en navegador.

Errores comunes:
- No envuelvas el contenido en `<html>`/`<body>`: el motor ya genera la página completa. Pasa solo Markdown.
- Si quieres CSS propio va **entero** en `estilo_css`, no incrustado en el Markdown.
- Las tablas Markdown requieren la fila separadora `|---|---|`.

Para PDF a partir del mismo contenido, usa `formato: "pdf"` (mismo motor, mismo CSS).
