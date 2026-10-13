# CLAUDE.md — AIRIS SUITE v1.0

Guía para trabajar en este repo. Lee esto antes de tocar código.

## Qué es

Convierte PDFs en imágenes JPEG y compila imágenes en un `.docx` (una imagen por hoja carta).
Interfaz y mensajes en **español**. Autor: Jorge Meneses (AIRIS).

Dos frontends sobre la misma lógica:
- **Web**: Flask (`backend/`) + `static/index.html`. Es la vía principal (`python backend/app.py` → http://localhost:5000).
- **Escritorio**: CustomTkinter (`desktop-app/AIRIS_Converter.py`), empaquetado con `AIRIS_Converter.spec`.

## Mapa del código

| Archivo | Responsabilidad |
|---|---|
| `backend/app.py` | Rutas Flask: `/`, `/upload`, `/process`, `/download/<task>/<file>`. Solo orquesta. |
| `backend/pdf_renderer.py` | PDF página → JPEG (render a DPI, recorte de márgenes blancos). |
| `backend/word_builder.py` | Imágenes → `.docx` (reglas de layout, ver abajo). |
| `desktop-app/worker.py` | Copia de `pdf_renderer.py` para el escritorio (proceso hijo). |
| `desktop-app/AIRIS_Converter.py` | GUI de escritorio. Trae **su propia copia** de la generación de Word. |
| `static/index.html` | Toda la UI web (HTML, CSS y JS en un solo archivo). |
| `AIRIS_Converter.spec` | Config de PyInstaller del escritorio. Tiene rutas absolutas de Windows del autor. |

Flujo web: `/upload` guarda en `backend/uploads/<task_id>/`; `/process` escribe en
`backend/outputs/<task_id>/`; `/download` entrega el `.docx` y borra ambas carpetas.
Ambas carpetas están en `.gitignore` y se crean al arrancar.

## Reglas de layout de Word (`word_builder.py`)

Estas reglas existen por un bug de paginación. No las cambies sin verificar con un .docx real:

- Márgenes laterales 0.5", verticales fijos 0.75" → ancho útil 7.5".
- La imagen se centra en un bloque de 9.5" moviendo **solo el margen superior**.
- Escala = `min(1, 7.5/ancho, 9.0/alto)`. Nunca agranda.
- Interlineado 1.0, `space_before`/`space_after` = 0.
- Una sección (hoja) por imagen.

Si cambias estas reglas, cámbialas también en `desktop-app/AIRIS_Converter.py`
(`_process_word_generation_from_list` y `_process_word_generation`).

## Convenciones

- Orden de imágenes: siempre con `natural_key` (`doc_p2` antes que `doc_p10`). No uses `sort()` simple.
- `pdf_renderer.render_page` cierra el documento en `finally`; no dejes handles abiertos.
- Los errores de conversión se imprimen y devuelven `False`; no propagar excepciones a Flask.
- Las copias de `worker.py` y de la generación de Word en el escritorio existen a propósito
  (el `.spec` solo empaqueta `desktop-app/`). Mantenlas sincronizadas.

## Cómo probar

No hay suite de tests. Verificación manual usada hasta ahora:

1. **Backend end-to-end** con `app.test_client()`: subir un PDF (modo `pdf`) y
   varias imágenes (modo `word`), llamar `/process`, descargar `/download/...` y
   revisar que el `.docx` tenga los `word/media/*` esperados.
2. **Layout de Word**: generar `.docx` con imágenes de distintas proporciones
   (muy anchas, cuadradas, altas) y convertir a PDF con LibreOffice
   (`soffice --headless --convert-to pdf`). Cada página debe tener exactamente
   una imagen completa dentro de la hoja.

Requisitos para probar: `pip install -r requirements.txt` (Flask, PyMuPDF, Pillow, python-docx).

## Pendientes conocidos (no resueltos)

- `/download` con archivo inexistente devuelve 500 en vez de 404.
- `README.md` dice `port=5001` para cambiar el puerto, pero el código usa la variable `port = 5000` en `__main__`.
- `.env.example` es de una plantilla de Gemini/AI Studio; la app no usa esas variables.
- `AIRIS_Converter.spec` apunta a `C:/Users/Jorge Meneses/...`; no funciona en otra máquina sin editarlo.
- La generación de Word del escritorio está duplicada (ver arriba).

## Git

- Rama principal: `main`. Commits en español, prefijo tipo `fix:`, `feat:`, `docs:` (como el historial actual).
