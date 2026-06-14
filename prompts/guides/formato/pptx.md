# Guía de formato: PPTX (PowerPoint)

Una sola vía: **`generar_documento_codigo`** con `formato: "pptx"`. (No hay vía Markdown para presentaciones.)

Escribes Python con **python-pptx**. Tienes la variable `OUTPUT_PATH` y el helper `guardar_documento(obj)` (acepta la presentación y llama a `.save()` por ti).

Contrato:
- `formato`: `"pptx"`
- `codigo_python`: construye la `Presentation()` y termina con `guardar_documento(prs)`.
- `nombre_archivo`: sin extensión.

Esqueleto recomendado:
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9
prs.slide_height = Inches(7.5)

# Portada (layout en blanco para control total)
blank = prs.slide_layouts[6]
s = prs.slides.add_slide(blank)
# fondo de color
from pptx.oxml.ns import qn
fill = s.background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(0x0F, 0x34, 0x60)

tb = s.shapes.add_textbox(Inches(0.8), Inches(2.8), Inches(11.7), Inches(2))
p = tb.text_frame.paragraphs[0]
p.text = "Título de la presentación"
p.font.size = Pt(44); p.font.bold = True
p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

guardar_documento(prs)
```

Buenas prácticas:
- Define `slide_width`/`slide_height` para 16:9 (13.333 × 7.5 in).
- Usa el layout en blanco (`slide_layouts[6]`) y coloca cajas de texto tú mismo para diseño consistente; o usa layouts con placeholders (`[0]` título, `[1]` contenido) para rapidez.
- Mantén una paleta coherente (define constantes `RGBColor` y reúsalas).
- Una idea por diapositiva; títulos cortos; viñetas de pocas palabras.

Errores comunes:
- No olvides `guardar_documento(prs)` al final.
- `add_slide` necesita un *layout*, no un índice suelto: `prs.slide_layouts[i]`.
- Los placeholders varían según el layout; si `slide.placeholders[1]` falla, usa una caja de texto manual.
- Las medidas van en EMU: usa siempre `Inches(...)` o `Pt(...)`, nunca números crudos.
