"""
Single tool registry for the multi-agent system.

One definition per tool, expressed as a LangChain StructuredTool. Because the
whole stack runs on LangChain, there is no second (OpenAI/Ollama) schema to keep
in sync — `bind_tools` accepts these directly for every provider.

Tools fall into two groups:

  * "executable" tools whose Python func runs server-side and returns a string
    (consultar_guia_formato, consultar_guia_tipo, buscar_en_documentos,
    guardar_investigacion, leer_investigacion, leer_documento).

  * "intercepted" tools whose schema is bound so the model can call them, but
    whose *effect* is handled by the runtime:
      - generar_documento_markdown -> rapid Markdown engine + __file_ready__
      - generar_documento_codigo   -> code (Python) engine + __file_ready__
      - invocar_creador_documentos -> runtime spawns the creator sub-agent
    Their func is a stub that is never executed.
"""
from __future__ import annotations

from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

from app.agents.context import RunContext
from app.services.documents import read_format_guide, read_type_guide


# --------------------------------------------------------------------------- #
# Argument schemas
# --------------------------------------------------------------------------- #
class _ConsultarGuiaFormatoInput(BaseModel):
    formato: str = Field(description="Formato del archivo: pdf, docx, xlsx, pptx, html, md, txt.")


class _ConsultarGuiaTipoInput(BaseModel):
    tipo: str = Field(
        description="Slug del tipo de documento (p.ej. reporte_profesional, presentacion, "
        "factura, carta, dashboard). Mira el catalogo de guias en tu prompt."
    )


class _BuscarInput(BaseModel):
    consulta: str = Field(
        description="Consulta en lenguaje natural, específica y orientada al dato buscado. "
        "Ej.: 'ventas totales Q1 2024', 'cláusulas de rescisión'."
    )


class _GuardarInvestigacionInput(BaseModel):
    nombre: str = Field(description="Nombre descriptivo del contenido, sin extensión.")
    contenido_md: str = Field(
        description="Contenido fuente completo en Markdown que el creador convertirá en "
        "documento (informe, texto de un CV, carta, resumen, datos...)."
    )


class _LeerInvestigacionInput(BaseModel):
    nombre: str = Field(description="Nombre del archivo de investigación a leer.")


class _LeerDocumentoInput(BaseModel):
    nombre: str = Field(
        description="Nombre del archivo del documento generado a leer (con o sin extensión)."
    )


class _GenerarMarkdownInput(BaseModel):
    formato: str = Field(description="Formato de salida: docx, pdf, html, txt o md.")
    contenido_markdown: str = Field(
        description="El documento escrito en Markdown (encabezados, listas, tablas, "
        "negrita/cursiva, citas, bloques de código). Se convierte al formato pedido."
    )
    nombre_archivo: str = Field(description="Nombre sin extensión. Solo letras, números y guiones.")
    estilo_css: str | None = Field(
        default=None,
        description="CSS opcional para pdf/html (reglas @page, body, h1, table...). "
        "Si se omite se usa un estilo profesional por defecto.",
    )


class _GenerarCodigoInput(BaseModel):
    formato: str = Field(description="Formato de salida: docx, pdf, pptx o xlsx.")
    codigo_python: str = Field(
        description="Código Python que construye el documento con la librería del formato "
        "(python-docx / reportlab / python-pptx / openpyxl). Dispones de la variable "
        "OUTPUT_PATH y del helper guardar_documento(objeto). Termina llamando a "
        "guardar_documento(objeto) (o guarda tú mismo en OUTPUT_PATH)."
    )
    nombre_archivo: str = Field(description="Nombre sin extensión. Solo letras, números y guiones.")


class _InvocarCreadorInput(BaseModel):
    nombre_informe: str = Field(
        description="Nombre del contenido fuente guardado a usar como base."
    )
    instruccion: str = Field(
        description="Qué documento generar, con qué cambios y estilo. Sé explícito si es "
        "replicar/modificar (p.ej. 'replica este CV cambiando el puesto a X') y en qué formato."
    )
    formato: str | None = Field(
        default=None,
        description="Formato deseado (pdf, docx, xlsx, pptx, html, md, txt) o vacío para que elija el creador.",
    )


# --------------------------------------------------------------------------- #
# Executable tool funcs
# --------------------------------------------------------------------------- #
def _build_executable(name: str, ctx: RunContext) -> StructuredTool:
    if name == "consultar_guia_formato":
        return StructuredTool(
            name="consultar_guia_formato",
            description=(
                "Devuelve la guia tecnica de un formato (que herramienta usar, el contrato "
                "exacto de entrada y los errores comunes a evitar). Llamala ANTES de generar "
                "para producir el archivo sin fallos. Formatos: pdf, docx, xlsx, pptx, html, md, txt."
            ),
            func=read_format_guide,
            args_schema=_ConsultarGuiaFormatoInput,
        )

    if name == "consultar_guia_tipo":
        return StructuredTool(
            name="consultar_guia_tipo",
            description=(
                "Devuelve una guia de buenas practicas para un TIPO de documento (reporte "
                "profesional, presentacion, factura, carta, dashboard...). Usala cuando la "
                "peticion encaje con un tipo del catalogo, para estructurarlo con calidad. "
                "El catalogo con descripciones esta en tu prompt."
            ),
            func=read_type_guide,
            args_schema=_ConsultarGuiaTipoInput,
        )

    if name == "buscar_en_documentos":
        from app.services.rag import retrieve, format_rag_context

        def _search(consulta: str) -> str:
            chunks = retrieve(ctx.project_id, consulta)
            if not chunks:
                return (
                    "No se encontraron fragmentos relevantes para: "
                    f"'{consulta}'. Prueba terminos mas especificos."
                )
            return format_rag_context(chunks)

        return StructuredTool(
            name="buscar_en_documentos",
            description=(
                "Busca informacion especifica dentro de los documentos del proyecto (RAG). "
                "Usala SOLO cuando necesites datos que no tienes ya delante: cifras, fechas, "
                "nombres, clausulas o tablas que estan en documentos no incluidos en el contexto. "
                "Si el documento relevante ya aparece completo en tu contexto, usalo directamente "
                "en vez de buscar. No es obligatorio llamarla en cada peticion."
            ),
            func=_search,
            args_schema=_BuscarInput,
        )

    if name == "guardar_investigacion":
        from app.services.research_store import save_research

        def _save(nombre: str, contenido_md: str) -> str:
            filename = save_research(nombre, contenido_md)
            ctx.saved_research.append(filename)
            return (
                f"Contenido guardado como '{filename}'. "
                "Pasa este nombre exacto a invocar_creador_documentos."
            )

        return StructuredTool(
            name="guardar_investigacion",
            description=(
                "Guarda en Markdown el CONTENIDO FUENTE que el creador convertira en documento "
                "(un informe, el texto de un CV, una carta, un resumen, datos...) y devuelve su "
                "nombre de archivo. Es el puente hacia invocar_creador_documentos. No tiene que "
                "ser una 'investigacion': usala siempre que vayas a generar un documento, con el "
                "material ya reunido."
            ),
            func=_save,
            args_schema=_GuardarInvestigacionInput,
        )

    if name == "leer_investigacion":
        from app.services.research_store import read_research

        def _read(nombre: str) -> str:
            return read_research(nombre)

        return StructuredTool(
            name="leer_investigacion",
            description=(
                "Lee el contenido fuente guardado (informe, texto de CV, carta, datos...), "
                "por su nombre de archivo."
            ),
            func=_read,
            args_schema=_LeerInvestigacionInput,
        )

    if name == "leer_documento":
        from app.services.documents import read_generated

        def _read_doc(nombre: str) -> str:
            return read_generated(nombre)

        return StructuredTool(
            name="leer_documento",
            description=(
                "Lee el contenido de texto de un documento YA GENERADO (el archivo descargable: "
                "pdf, docx, xlsx, pptx, html, md, txt), por su nombre. Usala cuando necesites "
                "revisar o modificar un documento entregado anteriormente."
            ),
            func=_read_doc,
            args_schema=_LeerDocumentoInput,
        )

    raise KeyError(name)


# --------------------------------------------------------------------------- #
# Intercepted tool stubs (schema only — runtime handles the effect)
# --------------------------------------------------------------------------- #
def _stub(**_: object) -> str:  # pragma: no cover - never executed
    return ""


def _build_intercepted(name: str) -> StructuredTool:
    if name == "generar_documento_markdown":
        return StructuredTool(
            name="generar_documento_markdown",
            description=(
                "VIA RAPIDA: genera un documento descargable a partir de Markdown que tu escribes. "
                "Formatos: docx, pdf, html, txt, md. Es la via por defecto para texto estructurado: "
                "informes, cartas, CVs, memos, documentacion, resumenes. Consulta antes "
                "consultar_guia_formato."
            ),
            func=_stub,
            args_schema=_GenerarMarkdownInput,
        )
    if name == "generar_documento_codigo":
        return StructuredTool(
            name="generar_documento_codigo",
            description=(
                "UNICAMENTE para generar un documento ejecutando codigo Python que tu escribes "
                "(python-docx / reportlab / python-pptx / openpyxl). Formatos: docx, pdf, pptx, "
                "xlsx. Usalo cuando necesites diseño a medida que el Markdown no permite: colores, "
                "tipografias, graficos, dashboards, certificados, posicionamiento exacto; y SIEMPRE "
                "para pptx y xlsx. Para texto estructurado normal usa la via rapida (markdown). "
                "Consulta antes consultar_guia_formato."
            ),
            func=_stub,
            args_schema=_GenerarCodigoInput,
        )
    if name == "invocar_creador_documentos":
        return StructuredTool(
            name="invocar_creador_documentos",
            description=(
                "Lanza al agente creador para generar un archivo descargable (crear, replicar o "
                "modificar un documento) a partir del contenido fuente que guardaste. Usalo siempre "
                "que el usuario quiera un documento, no solo para informes de investigacion."
            ),
            func=_stub,
            args_schema=_InvocarCreadorInput,
        )
    raise KeyError(name)


_INTERCEPTED = {
    "generar_documento_markdown",
    "generar_documento_codigo",
    "invocar_creador_documentos",
}


def build_tools(tool_names: tuple[str, ...], ctx: RunContext) -> tuple[list, dict]:
    """Return (tools_for_bind_tools, executables_by_name) for an agent.

    `tools_for_bind_tools` includes intercepted tools (schema only) so the model
    can call them. `executables_by_name` maps only the runnable tools, which the
    runtime invokes directly.
    """
    bound: list = []
    executables: dict = {}
    for name in tool_names:
        if name in _INTERCEPTED:
            bound.append(_build_intercepted(name))
        else:
            tool = _build_executable(name, ctx)
            bound.append(tool)
            executables[name] = tool
    return bound, executables
