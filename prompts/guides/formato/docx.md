# Guía de formato: DOCX (Word)

Dos vías. La rápida cubre la mayoría de los casos.

## Vía rápida — `generar_documento_markdown` (recomendada)
Escribe el documento en **Markdown** y pandoc lo convierte a un `.docx` rico y **editable** (encabezados como estilos de Word, tablas, listas, negrita/cursiva, citas, código).

Contrato:
- `formato`: `"docx"`
- `contenido_markdown`: el documento en Markdown (GitHub Flavored Markdown).
- `nombre_archivo`: sin extensión.
- `estilo_css`: **se ignora** para DOCX (pandoc usa la plantilla de Word por defecto).

Úsala para informes, cartas, memos, propuestas, actas — cualquier documento de texto que el usuario quiera abrir y editar en Word.

Errores comunes:
- Las tablas necesitan la fila separadora `|---|---|`.
- Usa encabezados Markdown (`#`, `##`, `###`) para que Word genere estilos de título reales (y tabla de contenido si hace falta).
- No metas HTML crudo; pandoc lo trata como texto literal.

## Vía código — `generar_documento_codigo`
Solo para control fino: estilos de párrafo personalizados, anchos de columna exactos, encabezados/pies, imágenes posicionadas. Escribes Python con **python-docx**.

Contrato:
- `formato`: `"docx"`
- `codigo_python`: construye un `Document()` y termina con `guardar_documento(doc)` (o `doc.save(OUTPUT_PATH)`).
- `nombre_archivo`: sin extensión.

Ejemplo mínimo:
```python
from docx import Document
from docx.shared import Pt, RGBColor
doc = Document()
h = doc.add_heading("Título", level=1)
doc.add_paragraph("Texto del cuerpo.")
guardar_documento(doc)
```

Errores comunes:
- No olvides `guardar_documento(doc)` al final.
- Para color/tamaño de fuente trabaja sobre `run.font` (no sobre el párrafo).
- `add_heading` con `level=0` crea un título de documento, no un H1.

**Decisión rápida:** ¿texto editable estándar? → vía rápida. ¿maquetación específica de Word? → vía código.
