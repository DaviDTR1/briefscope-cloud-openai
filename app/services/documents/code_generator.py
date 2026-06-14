"""
Document generation from agent-written Python code (total design freedom).

The agent writes a Python snippet using the right library for the format
(python-docx / reportlab / python-pptx / openpyxl). We inject an ``OUTPUT_PATH``
variable and a ``guardar_documento(obj)`` helper, then run the snippet in an
isolated subprocess with a timeout. The document is written straight to
GENERATED_DIR.

Running in a subprocess keeps a faulty/looping snippet from taking down the API
worker, and the whole plugin already runs inside its own Docker container.
"""
from __future__ import annotations

import os
import sys
import subprocess
import tempfile
from pathlib import Path

from app.config import GENERATED_DIR
from app.logging_config import logger
from app.services.documents.store import build_dest

_VALID = ("docx", "pdf", "pptx", "xlsx")

_PREAMBLE = '''\
import sys
from pathlib import Path

# OUTPUT_PATH es un str: lo aceptan python-docx, python-pptx, openpyxl y
# reportlab (canvas.Canvas requiere str, no acepta Path).
OUTPUT_PATH = r"{output_path}"
OUTPUT_FORMAT = "{output_format}"
_OUT = Path(OUTPUT_PATH)
_OUT.parent.mkdir(parents=True, exist_ok=True)


def guardar_documento(objeto, formato=OUTPUT_FORMAT):
    """Guarda el documento generado en la ruta correcta (OUTPUT_PATH)."""
    if hasattr(objeto, "save"):
        objeto.save(OUTPUT_PATH)
    elif hasattr(objeto, "output"):
        objeto.output(OUTPUT_PATH)
    else:
        raise TypeError(
            "El objeto no se puede guardar: usa un objeto con metodo .save() "
            "(Document/Presentation/Workbook/Canvas) o llama tu mismo a c.save()."
        )
    return OUTPUT_PATH
'''

_EPILOGUE = '''\

if not _OUT.exists():
    sys.stderr.write(
        "El codigo termino sin crear el archivo. Asegurate de llamar a "
        "guardar_documento(objeto) o de guardar en OUTPUT_PATH.\\n"
    )
    sys.exit(2)
'''


def generate_code(
    python_code: str,
    formato: str,
    nombre: str,
    *,
    timeout_seconds: int = 45,
) -> dict:
    """Execute agent code that builds a document. Returns a result dict:
    {success, filename, stdout, stderr}."""
    fmt = formato.lower().strip()
    if fmt not in _VALID:
        return {
            "success": False,
            "filename": None,
            "stdout": "",
            "stderr": (
                f"Formato '{formato}' no soportado en modo codigo. "
                f"Usa uno de {_VALID} (para html/txt usa el modo Markdown)."
            ),
        }

    dest = build_dest(fmt, nombre)
    script = (
        _PREAMBLE.format(output_path=str(dest), output_format=fmt)
        + "\n# --- codigo del agente ---\n"
        + python_code
        + _EPILOGUE
    )

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(script)
        script_path = tmp.name

    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            capture_output=True, text=True,
            timeout=timeout_seconds, cwd=str(GENERATED_DIR),
        )
        ok = proc.returncode == 0 and dest.exists()
        if ok:
            logger.info("Documento (codigo) generado: %s (%d bytes)", dest.name, dest.stat().st_size)
        else:
            logger.warning("Fallo generacion por codigo (%s): %s", fmt, proc.stderr[-500:])
        return {
            "success": ok,
            "filename": dest.name if ok else None,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False, "filename": None, "stdout": "",
            "stderr": f"Tiempo de ejecucion agotado ({timeout_seconds}s).",
        }
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Error ejecutando codigo de documento: %s", exc)
        return {"success": False, "filename": None, "stdout": "", "stderr": str(exc)}
    finally:
        os.unlink(script_path)
