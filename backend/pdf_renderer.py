"""Convierte una página de PDF en una imagen JPEG.

Lo usa el backend Flask (con ProcessPoolExecutor). La versión de escritorio
tiene su propia copia en desktop-app/worker.py: si cambias la lógica aquí,
actualízala también allá.
"""
import fitz
from PIL import Image as PILImage, ImageOps

# Lado máximo en píxeles; páginas más grandes se reducen para no agotar memoria
MAX_DIM = 8000
# Umbral de "blanco" para el auto-recorte (0-255)
CROP_THRESHOLD = 5
# Margen (px) que se deja alrededor del contenido recortado
CROP_PADDING = 15


def render_page(pdf_path, page_num, output_file, dpi, quality, auto_crop):
    """Renderiza una página a JPEG. Devuelve True si se guardó la imagen."""
    doc = fitz.open(pdf_path)
    try:
        page = doc.load_page(page_num)
        zoom = dpi / 72
        rect = page.rect
        width, height = rect.width * zoom, rect.height * zoom
        if width > MAX_DIM or height > MAX_DIM:
            zoom *= MAX_DIM / max(width, height)

        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        img = PILImage.frombytes("RGB", (pix.width, pix.height), pix.samples)

        if auto_crop:
            img = _crop_white_margins(img)

        if img.width < 10 or img.height < 10:
            return False
        img.save(output_file, "JPEG", quality=quality, optimize=True)
        return True
    finally:
        doc.close()


def _crop_white_margins(img):
    """Recorta los márgenes casi blancos, dejando un pequeño borde de respaldo."""
    gray = img.convert("L")
    inverted = ImageOps.invert(gray)
    mask = inverted.point(lambda x: 0 if x < CROP_THRESHOLD else 255)
    bbox = mask.getbbox()
    if not bbox:
        return img
    left, top, right, bottom = bbox
    left = max(0, left - CROP_PADDING)
    top = max(0, top - CROP_PADDING)
    right = min(img.width, right + CROP_PADDING)
    bottom = min(img.height, bottom + CROP_PADDING)
    return img.crop((left, top, right, bottom))


def convert_page_worker(args):
    """Adaptador para executor.map: recibe una tupla y nunca lanza excepciones."""
    pdf_path, page_num, output_file, dpi, quality, auto_crop = args
    try:
        return render_page(pdf_path, page_num, output_file, dpi, quality, auto_crop)
    except Exception as e:
        print(f"Error en convert_page_worker: {e}")
        return False
