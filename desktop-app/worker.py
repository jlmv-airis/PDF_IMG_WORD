import os
import fitz  # PyMuPDF
import PIL.Image as PILImage
import PIL.ImageOps as ImageOps

def convert_page_worker(args):
    """
    Función optimizada para procesar una sola página de PDF.
    Se ejecuta en un proceso separado para máximo rendimiento.
    """
    pdf_path, page_num, output_file, dpi, quality, auto_crop = args
    try:
        # Abrimos el documento solo para esta página (eficiencia de memoria)
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        
        # Calculamos la matriz de escalado basada en el DPI (72 es el estándar)
        zoom = dpi / 72
        
        # SEGURIDAD DE MEMORIA: Verificamos dimensiones antes de renderizar
        rect = page.bound()
        width, height = rect.width * zoom, rect.height * zoom
        
        MAX_DIM = 8000
        if width > MAX_DIM or height > MAX_DIM:
            scale = MAX_DIM / max(width, height)
            zoom *= scale
            
        mat = fitz.Matrix(zoom, zoom)
        
        # Renderizamos la página a una imagen (pixmap)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convertimos a PIL para manipulación y auto-recorte
        img = PILImage.frombytes("RGB", (pix.width, pix.height), pix.samples)
        
        if auto_crop:
            # Lógica de auto-recorte mejorada
            gray_im = img.convert("L")
            invert_im = ImageOps.invert(gray_im)
            
            # Umbral de detección: Cualquier pixel que no sea blanco puro (255) es contenido
            mask = invert_im.point(lambda x: 0 if x < 5 else 255)
            bbox = mask.getbbox()
            
            if bbox:
                # Añadimos un pequeño margen de 10px
                left, top, right, bottom = bbox
                left = max(0, left - 15)
                top = max(0, top - 15)
                right = min(img.width, right + 15)
                bottom = min(img.height, bottom + 15)
                img = img.crop((left, top, right, bottom))
        
        # Si después de todo la imagen está vacía o es inválida, evitamos guardarla
        if img.width < 10 or img.height < 10:
             doc.close()
             return False, f"Página {page_num+1} parece estar vacía tras recorte."
        
        # Guardamos la imagen con PIL
        if output_file.lower().endswith(('.jpg', '.jpeg')):
            img.save(output_file, "JPEG", quality=quality, optimize=True)
        else:
            img.save(output_file, "PNG", optimize=True)
        
        doc.close()
        return True, None
    except Exception as e:
        return False, f"Error en {os.path.basename(pdf_path)} pág {page_num+1}: {str(e)}"
