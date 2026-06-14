<!-- desc: Presentación de diapositivas (pitch, resumen ejecutivo visual, informe para reunión) en PowerPoint. -->
# Tipo: Presentación

Diapositivas. Siempre **PPTX** vía `generar_documento_codigo` (consulta la guía de formato `pptx`). El objetivo es comunicar visualmente, no volcar texto.

## Estructura recomendada
1. **Portada** — título potente, subtítulo, fecha/autor. Fondo de color de marca.
2. **Agenda / contexto** (opcional) — qué se va a cubrir.
3. **Una idea por diapositiva** — título afirmativo (la conclusión, no el tema) + apoyo visual.
4. **Datos** — una cifra grande destacada o una tabla/gráfico simple por diapositiva.
5. **Cierre** — conclusiones y siguientes pasos / llamada a la acción.

## Buenas prácticas
- 16:9 (`Inches(13.333) × Inches(7.5)`).
- Paleta coherente: define 2-3 `RGBColor` (primario, acento, texto) y reúsalas en todas las diapositivas.
- Títulos de pocas palabras; viñetas de máximo una línea; 3-5 viñetas por diapositiva.
- Texto grande y legible (título ≥ 32pt, cuerpo ≥ 18pt).
- Usa contraste: texto claro sobre fondo oscuro o viceversa.
- Si hay números clave, muéstralos enormes en vez de en una frase.

## Errores a evitar
- Párrafos enteros en una diapositiva (es una presentación, no un documento).
- Más de ~6 líneas de texto por diapositiva.
- Colores incoherentes entre diapositivas.
- Olvidar `guardar_documento(prs)`.
