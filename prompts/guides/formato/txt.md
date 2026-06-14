# Guía de formato: TXT (texto plano)

Una sola vía: **`generar_documento_markdown`** con `formato: "txt"`.

Escribe el contenido en **Markdown** y el motor lo reduce a texto plano legible (quita encabezados `#`, negritas, cursivas, enlaces, imágenes y bloques de código, conservando el texto).

Contrato:
- `formato`: `"txt"`
- `contenido_markdown`: el contenido. Puedes usar Markdown ligero; se limpiará.
- `nombre_archivo`: sin extensión.
- `estilo_css`: se ignora.

Úsala para notas, logs, salidas que se pegarán en otra herramienta, o cuando el usuario pida explícitamente texto plano sin formato.

Errores comunes:
- No esperes tablas bonitas: en texto plano la sintaxis de tabla Markdown se conserva tal cual. Si necesitas columnas alineadas, formatéalas tú mismo con espacios.
- Para conservar saltos de línea exactos, escríbelos directamente en el contenido.

Si el usuario quiere conservar el formato Markdown (encabezados, listas) en crudo, usa `formato: "md"` en su lugar.
