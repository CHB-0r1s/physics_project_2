from flask import Flask, request, render_template
from electromagnetics import calculate_E
from pot import phi
import numpy as np

app = Flask(__name__)

points = []  # Список точек
vectors = []  # Список векторов
CENTER: np.array = np.array([0.5, 0.5])
ROTATION: float = 0
TAU: float = 1e-8
LENGTH: float = 1
response_pot = ""
response_nap = ""
x_val_c, y_val_c = 0, 0

x1, y1 = calculate_E(1, 1e-8, CENTER, ROTATION, np.array([25 / 100, 25 / 100]))
norma_up = (((25 + x1 * 100) ** 2 + (25 + y1 * 100) ** 2) ** 0.5)
x1, y1 = calculate_E(1, 1e-8, CENTER, ROTATION, np.array([800 - 25, 800 - 25]))
norma_down = (((800 - 25 + x1 * 100) ** 2 + (800 - 25 + y1 * 100) ** 2) ** 0.5)
print(f"{norma_up=}")
print(f"{norma_down=}")


@app.route('/')
def index():
    return render_template('index.html', vectors=vectors, x_c=CENTER[0] * 400, y_c=CENTER[1] * 400, length=LENGTH * 400,
                           response_pot=response_pot, response_nap=response_nap, x_val_c=x_val_c, y_val_c=y_val_c)


@app.route('/add_point', methods=['POST'])
def add_point():
    data = request.json
    if 'x' in data and 'y' in data:
        x = int(data['x'])
        y = int(data['y'])

        # 1e-8 1e-7 2e-7 3e-7...

        points.append([x, y])
        x1, y1 = calculate_E(1, 5e-7, CENTER, ROTATION, np.array([x / 100, y / 100]))
        x1_ort = x + x1 * 100 / (((x + x1 * 100) ** 2 + (y + y1 * 100) ** 2) ** 0.5)
        y1_ort = y + y1 * 100 / (((x + x1 * 100) ** 2 + (y + y1 * 100) ** 2) ** 0.5)

        # Добавляем новый вектор на основе точки
        # vectors.append([x, y, x + x1 * 100, y + y1 * 100, min(((x1 ** 2 + y1 ** 2) ** 0.5) / 10000, 1)])
        # vectors.append([x, y, x1_ort, y1_ort])
        # print([_ / 100 for _ in [x, y, x1_ort, y1_ort]])
        print([x, y, x + x1 * 100, y + y1 * 100, min(((x1 ** 2 + y1 ** 2) ** 0.5) / 10000, 1)])
        print((x1 ** 2 + y1 ** 2) ** 0.5)

        global response_pot
        response_pot = round(phi(*CENTER, x / 400, y / 400, LENGTH, np.rad2deg(ROTATION), 9e9, TAU), 1)
        global response_nap
        response_nap = round((x1 ** 2 + y1 ** 2) ** 0.5, 1)
        global x_val_c, y_val_c
        x_val_c = round(x / 400, 2)
        y_val_c = round(y / 400, 2)

        return "OK"
    else:
        return 'Invalid data format'


def init_vector():
    global vectors
    vectors = []
    for x in range(25, 800, 50):
        for y in range(25, 800, 50):
            x1, y1 = calculate_E(LENGTH, TAU, CENTER, ROTATION, np.array([x / 400, y / 400]))
            norma = (((x + x1 * 400) ** 2 + (y + y1 * 400) ** 2) ** 0.5)
            x1_ort = x + x1 * 400 / (((x + x1 * 400) ** 2 + (y + y1 * 400) ** 2) ** 0.5)
            y1_ort = y + y1 * 400 / (((x + x1 * 400) ** 2 + (y + y1 * 400) ** 2) ** 0.5)

            opacity = min(((x1 ** 2 + y1 ** 2) ** 0.5) / 1000, 1)
            vectors.append([x, y, x1_ort, y1_ort, opacity,
                            min(phi(*CENTER, x / 400, y / 400, LENGTH, np.rad2deg(ROTATION), 9e9, TAU) / 1000, 1)])


@app.route('/change_center', methods=['POST'])
def change_center():
    global CENTER
    data = request.json
    CENTER[0] = data["x"]
    CENTER[1] = data["y"]
    init_vector()
    return "success change center"


@app.route('/change_rotate', methods=['POST'])
def change_rotate():
    global LENGTH
    data = request.json
    LENGTH = float(data["rotate"])
    init_vector()
    return "success change center"


@app.route('/change_tau', methods=['POST'])
def change_tau():
    global TAU
    data = request.json
    tau = int(data["tau"])
    if tau == 1:
        TAU = 1e-8
    if tau == 2:
        TAU = 2e-8
    if tau == 3:
        TAU = 3e-8
    if tau == 4:
        TAU = 4e-8
    init_vector()
    return "success change tau"


if __name__ == '__main__':
    init_vector()
    app.run()
