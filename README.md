# AIRIS SUITE v1.0

Aplicación para conversión de PDF a imágenes de alta calidad y compilación en documentos Word (.docx).

## Características

- Conversión masiva de PDF a imágenes (JPEG) con calidad configurable
- Generación automática de documentos Word con imágenes centradas
- Interfaz web minimalista y moderna con modo oscuro
- Procesamiento paralelo para máxima velocidad
- Auto-recorte inteligente de márgenes blancos
- Múltiples niveles de calidad: Estándar (150 DPI), HD (300 DPI), Ultra (600 DPI)
- Modo "Solo Word" para compilar imágenes existentes

## Tecnologías

- **Backend**: Python + Flask
- **Procesamiento**: PyMuPDF, Pillow, python-docx
- **Interfaz**: HTML5 + CSS3 + JavaScript
- **Escritorio**: CustomTkinter (opcional)

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.7 o superior instalado en tu sistema
- pip (gestor de paquetes de Python)

### Windows

1. **Descargar el proyecto:**
   ```cmd
   git clone https://github.com/jlmv-airis/PDF_IMG_WORD.git
   cd PDF_IMG_WORD
   ```

2. **Crear entorno virtual (recomendado):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```cmd
   python backend\app.py
   ```

5. **Abrir en el navegador:**
   - Ir a: http://localhost:5000/

### macOS / Linux

1. **Descargar el proyecto:**
   ```bash
   git clone https://github.com/jlmv-airis/PDF_IMG_WORD.git
   cd PDF_IMG_WORD
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python3 backend/app.py
   ```

5. **Abrir en el navegador:**
   - Ir a: http://localhost:5000/

---

## 📦 Crear Ejecutable (.exe)

### Windows

1. **Instalar PyInstaller:**
   ```cmd
   pip install pyinstaller
   ```

2. **Crear el ejecutable:**
   ```cmd
   pyinstaller --onefile --add-data "backend;backend" --add-data "static;static" backend/app.py --name AIRIS_SUITE
   ```

3. **El ejecutable se creará en:** `dist/AIRIS_SUITE.exe`

4. **Ejecutar:**
   - Doble clic en `AIRIS_SUITE.exe`
   - Se abrirá automáticamente el navegador

### Para distribución

1. Copiar el archivo `dist/AIRIS_SUITE.exe`
2. Compartir con los usuarios
3. Los usuarios solo deben hacer doble clic para ejecutar

---

## 🖥️ Aplicación de Escritorio (Opcional)

### Instalación de dependencias adicionales:

```bash
pip install customtkinter tkinterdnd2
```

### Ejecución:

```bash
python desktop-app/AIRIS_Converter.py
```

---

## 📁 Estructura del Proyecto

```
PDF_IMG_WORD/
├── backend/
│   ├── app.py              # Servidor Flask (rutas)
│   ├── pdf_renderer.py     # PDF → JPEG
│   ├── word_builder.py     # Imágenes → Word
│   ├── uploads/            # Archivos subidos temporalmente (se crea al ejecutar)
│   └── outputs/            # Archivos generados temporalmente (se crea al ejecutar)
├── static/
│   ├── index.html          # Interfaz web
│   └── images.jpg          # Logo
├── desktop-app/
│   ├── AIRIS_Converter.py  # App de escritorio
│   └── worker.py           # Worker para procesamiento
├── Shared_Project/         # Instrucciones de uso
├── requirements.txt        # Dependencias de Python
├── CLAUDE.md               # Guía técnica para asistentes de código
└── README.md               # Este archivo
```

---

## 🌙 Modo Oscuro

La aplicación incluye modo oscuro. Toggle en la esquina superior derecha para cambiar entre modo claro y oscuro.

---

## 📝 Uso de la Interfaz

### Modo PDF a Imagen + Word:
1. Arrastra archivos PDF o haz clic para seleccionar
2. Configura la calidad (Estándar/HD/Ultra)
3. Activa/desactiva auto-recorte y generación de Word
4. Presiona "INICIAR CONVERSIÓN"
5. Descarga el archivo Word automáticamente

### Modo Solo Word:
1. Selecciona "Solo Word" en la barra superior
2. Arrastra imágenes (JPG/PNG)
3. Presiona "INICIAR CONVERSIÓN"
4. Descarga el documento Word compilado

---

## 🔧 Solución de Problemas

### Error: "Python no se reconoce como comando"
- Agregar Python al PATH de Windows o usar la ruta completa

### Error: "Port 5000 en uso"
- Cambiar el puerto en `backend/app.py`:
  ```python
  app.run(debug=False, port=5001)
  ```

### Error: "ModuleNotFoundError"
- Ejecutar: `pip install -r requirements.txt`

---

## 📄 Licencia

Uso libre para fines educativos y comerciales.

---

**Desarrollado por Jorge Meneses**  
Contacto: jorge.meneses@airis-ae.com.mx  
© 2026 AIRIS SUITE. Todos los derechos reservados.
