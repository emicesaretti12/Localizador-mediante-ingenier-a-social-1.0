from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/captura', methods=['POST'])
def captura():
    data = request.get_json()
    with open("ubicaciones.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - LAT: {data['lat']}, LON: {data['lon']}, ACC: {data['acc']}m\n")
    return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
