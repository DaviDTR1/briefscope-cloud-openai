<!-- desc: Informe profesional extenso (análisis, due diligence, memo ejecutivo) con portada, resumen ejecutivo, secciones y conclusiones. -->
# Tipo: Reporte profesional

Documento de texto estructurado y con autoridad. Mejor en **PDF** o **DOCX** vía `generar_documento_markdown`. Si el cliente pide identidad de marca fuerte, pasa `estilo_css` propio (PDF) o usa la vía código.

## Estructura recomendada
1. **Portada / título** — título claro, subtítulo, fecha, autor/organización.
2. **Resumen ejecutivo** — 3-6 frases con los hallazgos y la recomendación principal. Que se entienda todo leyendo solo esto.
3. **Contexto / objetivo** — qué se analizó y por qué.
4. **Hallazgos** — una sección (`##`) por tema. Usa subtítulos, tablas para cifras y citas para texto fuente relevante.
5. **Análisis / implicaciones** — qué significan los hallazgos.
6. **Recomendaciones** — accionables, priorizadas.
7. **Conclusión** y, si aplica, **anexos** (datos de respaldo, fuentes).

## Buenas prácticas
- Apóyate en los datos del proyecto: usa `buscar_en_documentos` y cita cifras/fechas/cláusulas concretas, no generalidades.
- Una afirmación, una evidencia. Evita el relleno.
- Usa tablas para comparativas y números; prosa para razonamiento.
- Encabezados Markdown jerárquicos (`#`, `##`, `###`) para que el documento tenga navegación y, en DOCX, estilos de título reales.
- Tono objetivo y profesional. Si hay incertidumbre, decláralo.

## Errores a evitar
- No inventes datos que no estén en las fuentes.
- No mezcles niveles de encabezado de forma incoherente.
- Evita muros de texto: divide en secciones digeribles.
