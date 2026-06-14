# Guía de formato: PDF

Hay **dos vías** para producir un PDF. Elige según la complejidad visual.

## Vía rápida — `generar_documento_markdown` (recomendada por defecto)
Escribe el documento en **Markdown** y el motor lo convierte a PDF (Markdown → HTML → PDF con WeasyPrint). Soporta Unicode completo, tablas, listas, citas, código y **CSS propio**.

Contrato:
- `formato`: `"pdf"`
- `contenido_markdown`: el documento en Markdown.
- `nombre_archivo`: sin extensión, solo letras/números/guiones.
- `estilo_css` (opcional): reglas CSS completas (`@page`, `body`, `h1`, `table`...). Si lo omites se aplica un estilo profesional por defecto (A4, tipografía limpia, tablas con cabecera de color).

Úsala para informes, memos, documentación, propuestas y cualquier documento que sea texto estructurado. Para un acabado de marca, pasa tu propio `estilo_css`.

Errores comunes a evitar:
- No incluyas el bloque `<html>` ni `<style>`: solo Markdown (y opcionalmente CSS por separado en `estilo_css`).
- Las tablas Markdown necesitan la fila de separación `|---|---|`.
- Para saltos de página en CSS usa `page-break-before: always;` en un selector.

## Vía código — `generar_documento_codigo`
Solo si necesitas **control milimétrico**: certificados, posicionamiento absoluto, gráficos vectoriales, portadas con imágenes a sangre. Escribes Python con **reportlab**.

Contrato:
- `formato`: `"pdf"`
- `codigo_python`: script que construye el PDF. Tienes `OUTPUT_PATH` (ruta destino) y el helper `guardar_documento(obj)`. Con reportlab normalmente escribes directo en `OUTPUT_PATH`.
- `nombre_archivo`: sin extensión.

Ejemplo mínimo:
```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)
c.setFont("Helvetica-Bold", 24)
c.drawString(72, 760, "Título")
c.showPage()
c.save()
```

Errores comunes:
- Recuerda llamar a `c.save()` (o `doc.build(...)` con platypus) o el archivo quedará vacío.
- Las coordenadas de reportlab tienen el origen abajo-izquierda.
- Para texto largo con estilos usa `platypus` (SimpleDocTemplate + Paragraph), no `drawString`.

**Decisión rápida:** ¿es texto estructurado? → vía rápida. ¿es diseño a medida? → vía código.
