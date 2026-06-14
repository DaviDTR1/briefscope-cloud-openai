<!-- desc: Tablero de datos / cuadro de mando con métricas, tablas y gráficos a partir de los datos del proyecto (Excel o PDF visual). -->
# Tipo: Dashboard / cuadro de datos

Vista de datos con métricas, tablas y gráficos. Dos opciones según el uso:

- **XLSX** vía `generar_documento_codigo` (openpyxl) — si el usuario querrá filtrar, editar o seguir trabajando con los datos. Permite fórmulas, varias hojas y gráficos nativos de Excel.
- **PDF** vía `generar_documento_codigo` (reportlab) — si es un informe visual de solo lectura con KPIs y gráficos posicionados.

## Estructura recomendada
1. **Cabecera** — título, periodo de los datos, fecha de generación.
2. **KPIs principales** — 3-6 métricas clave destacadas (cifra grande + etiqueta + variación).
3. **Tablas de detalle** — datos desglosados, con cabecera de color y totales.
4. **Gráficos** — tendencias o comparativas (barras, líneas, pastel) según corresponda.
5. **Notas / fuente de los datos**.

## Buenas prácticas
- Extrae las cifras reales del proyecto con `buscar_en_documentos`; no inventes datos.
- KPIs primero, detalle después (pirámide invertida).
- En XLSX: cabeceras con relleno de color, `freeze_panes`, formato numérico (`#,##0`, `0%`) y **fórmulas reales** para los totales.
- En XLSX puedes añadir gráficos con `openpyxl.chart` (BarChart, LineChart) referenciando rangos.
- Paleta coherente y consistente con la marca si se conoce.

## Errores a evitar
- Volcar una tabla gigante sin resumen ni KPIs.
- Colores hex con `#` en openpyxl (van sin `#`).
- Calcular en Python lo que debería ser fórmula editable.
- Gráficos sin títulos ni etiquetas de ejes.
