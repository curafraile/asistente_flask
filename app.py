from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiala por algo más seguro en producción

# Carpetas
CARPETA_ACTIVIDADES = 'actividades'
CARPETA_VIDEOS = os.path.join('static', 'videos')
CARPETA_ENTREGAS = 'uploads'
CLAVE_DOCENTE = 'docente123'

# Crear carpetas si no existen
for carpeta in [CARPETA_ACTIVIDADES, CARPETA_VIDEOS, CARPETA_ENTREGAS]:
    os.makedirs(carpeta, exist_ok=True)

@app.route('/')
def index():
    actividades = os.listdir(CARPETA_ACTIVIDADES)
    videos = os.listdir(CARPETA_VIDEOS)
    return render_template('index.html', actividades=actividades, videos=videos)

@app.route('/subir', methods=['POST'])
def subir_entrega():
    nombre = request.form.get('nombre')
    archivo = request.files.get('archivo')

    if not nombre or not archivo:
        return 'Falta nombre o archivo'

    nombre_archivo = f"{nombre}_{archivo.filename}"
    archivo.save(os.path.join(CARPETA_ENTREGAS, nombre_archivo))
    return 'Entrega enviada con éxito'

@app.route('/docente', methods=['GET', 'POST'])
def docente():
    if request.method == 'POST':
        clave = request.form.get('clave')
        if clave == CLAVE_DOCENTE:
            session['docente_logueado'] = True
            return redirect(url_for('subir_docente'))
        else:
            return render_template('login_docente.html', error='Clave incorrecta')
    return render_template('login_docente.html')

@app.route('/subir_docente', methods=['GET', 'POST'])
def subir_docente():
    if not session.get('docente_logueado'):
        return redirect(url_for('docente'))

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        archivo = request.files.get('archivo')

        if not archivo or not tipo:
            return 'Falta tipo o archivo'

        if tipo == 'actividad':
            archivo.save(os.path.join(CARPETA_ACTIVIDADES, archivo.filename))
        elif tipo == 'video':
            archivo.save(os.path.join(CARPETA_VIDEOS, archivo.filename))
        else:
            return 'Tipo no válido'

        return 'Archivo subido con éxito'

    return render_template('docente.html')

@app.route('/descargar/<carpeta>/<nombre>')
def descargar(carpeta, nombre):
    ruta = CARPETA_ACTIVIDADES if carpeta == 'actividades' else CARPETA_VIDEOS
    return send_from_directory(ruta, nombre)

@app.route('/logout')
def logout():
    session.pop('docente_logueado', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
