# AIRIS SUITE v1.0

Aplicación para conversión de PDF a imágenes de alta calidad y compilación en documentos Word (.docx).

## Características

- Conversión masiva de PDF a imágenes (JPEG) con calidad configurable
- Generación automática de documentos Word con imágenes centradas
- Interfaz web minimalista y moderna
- Procesamiento paralelo para máxima velocidad
- Auto-recorte inteligente de márgenes blancos
- Múltiples niveles de calidad: Estándar (150 DPI), HD (300 DPI), Ultra (600 DPI)
- Modo "Solo Word" para compilar imágenes existentes

## Tecnologías

- **Backend**: Python + Flask
- **Procesamiento**: PyMuPDF, Pillow, python-docx
- **Interfaz**: HTML5 + CSS3 + JavaScript
- **Escritorio**: CustomTkinter (opcional)

## Instalación

```bash
git clone https://github.com/jlmv-airis/PDF_IMG_WORD.git
cd PDF_IMG_WORD
pip install -r requirements.txt
```

## Uso

### Aplicación Web

```bash
python backend/app.py
```

Abrir navegador en: http://localhost:5000/

### Aplicación de Escritorio

```bash
pip install customtkinter tkinterdnd2
python desktop-app/AIRIS_Converter.py
```

## Estructura

```
PDF_IMG_WORD/
├── backend/
│   └── app.py              # Servidor Flask
├── static/
│   └── index.html         # Interfaz web
├── desktop-app/
│   └── AIRIS_Converter.py # App de escritorio
├── docs/                   # Documentación
├── requirements.txt       # Dependencias
└── README.md
```

## Licencia

Uso libre para fines educativos y comerciales.

**Desarrollado por Jorge Meneses**  
Contacto: jorge.meneses@airis-ae.com.mx
