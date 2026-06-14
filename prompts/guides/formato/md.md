# Guía de formato: MD (Markdown)

Una sola vía: **`generar_documento_markdown`** con `formato: "md"`.

Entrega el documento como un archivo `.md` **tal cual lo escribes** (sin conversión). El contenido se guarda íntegro, conservando encabezados, listas, tablas, negritas, enlaces y bloques de código.

Contrato:
- `formato`: `"md"`
- `contenido_markdown`: el documento en Markdown final.
- `nombre_archivo`: sin extensión.
- `estilo_css`: se ignora.

Úsala cuando el usuario quiera el fuente Markdown reutilizable (READMEs, documentación técnica, notas que editará en otro editor, contenido para un sistema que ya renderiza Markdown).

Errores comunes:
- Asegúrate de que la sintaxis Markdown sea válida (filas separadoras de tabla, cierres de bloques de código con ```).
- Si lo que el usuario quiere es un documento **renderizado** (no el fuente), elige `pdf`, `docx` o `html`.
