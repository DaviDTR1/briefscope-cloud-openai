# Guía de formato: XLSX (Excel)

Una sola vía: **`generar_documento_codigo`** con `formato: "xlsx"`. (No hay vía Markdown para hojas de cálculo.)

Escribes Python con **openpyxl**. Tienes `OUTPUT_PATH` y el helper `guardar_documento(obj)` (acepta el workbook y llama a `.save()`).

Contrato:
- `formato`: `"xlsx"`
- `codigo_python`: construye el `Workbook()` y termina con `guardar_documento(wb)`.
- `nombre_archivo`: sin extensión.

Esqueleto recomendado:
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Resumen"

headers = ["Concepto", "Q1", "Q2", "Total"]
ws.append(headers)
head_fill = PatternFill("solid", fgColor="0F3460")
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = head_fill
    c.alignment = Alignment(horizontal="center")

ws.append(["Ventas", 1000, 1200, "=B2+C2"])

# ancho de columnas
for i, _ in enumerate(headers, 1):
    ws.column_dimensions[get_column_letter(i)].width = 18

ws.freeze_panes = "A2"
guardar_documento(wb)
```

Buenas prácticas:
- Cabeceras en negrita con relleno de color y `freeze_panes` para fijar la fila de títulos.
- Usa **fórmulas reales** (`"=SUM(B2:B10)"`) en vez de calcular en Python cuando el usuario querrá editarlas.
- Ajusta `column_dimensions[...].width` para que el contenido se lea.
- Aplica formato numérico con `cell.number_format = "#,##0.00"` o `"0%"`.
- Para varias secciones usa varias hojas (`wb.create_sheet("Detalle")`).

Errores comunes:
- No olvides `guardar_documento(wb)` al final.
- Los colores van en hex **sin** `#` (`"0F3460"`, no `"#0F3460"`).
- Las fórmulas se escriben como string empezando por `=`.
- `wb.active` es la primera hoja ya creada; no la dupliques con `create_sheet`.
