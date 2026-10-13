"""Servidor Flask de AIRIS SUITE.

Flujo: /upload guarda los archivos en uploads/<task_id>,
/process los convierte (PDF -> JPEG y/o JPEG/PNG -> Word) en outputs/<task_id>,
/download entrega el .docx y borra ambas carpetas.

Lógica de conversión: pdf_renderer.py. Lógica de Word: word_builder.py.
"""
import concurrent.futures
import os
import shutil
import sys
import uuid

import fitz
from flask import Flask, jsonify, request, send_file

from pdf_renderer import convert_page_worker
from word_builder import generate_word

WORD_FILENAME = "Imagenes.docx"
JPEG_QUALITY = 95
DPI_BY_QUALITY = {'Estandar': 150, 'HD': 300, 'Ultra': 600}
DEFAULT_DPI = 300
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# Al compilarse con PyInstaller los recursos viven en sys._MEIPASS
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_folder=os.path.join(os.path.dirname(base_path), 'static'),
            static_url_path='/static')
app.config['UPLOAD_FOLDER'] = os.path.join(base_path, 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(base_path, 'outputs')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def _pdf_page_tasks(task_folder, output_folder, dpi):
    """Una tarea por página de cada PDF subido: <nombre>_p<n>.jpg."""
    tasks = []
    for pdf in os.listdir(task_folder):
        if not pdf.lower().endswith('.pdf'):
            continue
        pdf_path = os.path.join(task_folder, pdf)
        name = os.path.splitext(pdf)[0]
        with fitz.open(pdf_path) as doc:
            page_count = len(doc)
        for i in range(page_count):
            out = os.path.join(output_folder, f"{name}_p{i+1}.jpg")
            tasks.append((pdf_path, i, out, dpi, JPEG_QUALITY, True))
    return tasks


def _convert_pdfs(task_folder, output_folder, dpi):
    tasks = _pdf_page_tasks(task_folder, output_folder, dpi)
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        list(executor.map(convert_page_worker, tasks))
    return [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.jpg')]


def _uploaded_images(task_folder):
    return [os.path.join(task_folder, f) for f in os.listdir(task_folder)
            if f.lower().endswith(IMAGE_EXTENSIONS)]


@app.route('/')
def index():
    return send_file('../static/index.html')


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    mode = request.form.get('mode', 'pdf')
    task_id = str(uuid.uuid4())
    task_folder = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
    os.makedirs(task_folder, exist_ok=True)
    for f in files:
        f.save(os.path.join(task_folder, f.filename))
    return jsonify({'task_id': task_id, 'mode': mode})


@app.route('/process', methods=['POST'])
def process():
    data = request.json
    task_id = data['task_id']
    mode = data['mode']
    dpi = DPI_BY_QUALITY.get(data.get('quality', 'HD'), DEFAULT_DPI)

    task_folder = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
    output_folder = os.path.join(app.config['OUTPUT_FOLDER'], task_id)
    os.makedirs(output_folder, exist_ok=True)

    if mode == 'pdf':
        images = _convert_pdfs(task_folder, output_folder, dpi)
        make_word = data.get('gen_word', True)
    else:
        images = _uploaded_images(task_folder)
        make_word = True

    word_ok = False
    if images and make_word:
        word_ok = generate_word(images, os.path.join(output_folder, WORD_FILENAME))

    if word_ok:
        return jsonify({'ready': True, 'task_id': task_id})
    return jsonify({'ready': False, 'error': 'No se generaron archivos'})


@app.route('/download/<task_id>/<filename>')
def download(task_id, filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], task_id, filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], task_id)
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], task_id)

    response = send_file(path, as_attachment=True)

    @response.call_on_close
    def cleanup():
        try:
            if os.path.exists(upload_path):
                shutil.rmtree(upload_path)
            if os.path.exists(output_path):
                shutil.rmtree(output_path)
        except Exception as e:
            print(f"Error en limpieza: {e}")

    return response


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(base_path)

    port = 5000
    print(f"Running on http://localhost:{port}/")
    app.run(debug=False, port=port)
