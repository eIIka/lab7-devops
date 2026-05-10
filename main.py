# Модель: Модель балки Ейлера-Бернуллі (5 семестр)
# Автор: Калкатін Владислав, група АІ-235

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify

class BridgeLoadModel:
    def __init__(self, length=20.0, q=10000.0, E=2e11, I=0.0054, n=200):
        self.L = length
        self.q = q
        self.E = E
        self.I = I
        self.n = n
        self.dx = self.L / (self.n - 1)
        self.x = np.linspace(0, self.L, self.n)
        self.w = np.zeros(self.n)
        self.M = np.zeros(self.n)
        self.sigma = np.zeros(self.n)

    def solve_beam_deflection(self):
        A = np.zeros((self.n, self.n))
        b = np.full(self.n, self.q / (self.E * self.I))

        for i in range(2, self.n - 2):
            A[i, i - 2] = 1
            A[i, i - 1] = -4
            A[i, i] = 6
            A[i, i + 1] = -4
            A[i, i + 2] = 1
        A = A / (self.dx ** 4)

        A[0, 0] = 1
        A[1, 0:3] = [1, -2, 1]
        A[-2, -3:] = [1, -2, 1]
        A[-1, -1] = 1

        b[0] = 0
        b[1] = 0
        b[-2] = 0
        b[-1] = 0

        self.w = np.linalg.solve(A, b)

    def calculate_moment_and_stress(self, y_max=0.3):
        d2w = np.gradient(np.gradient(self.w, self.dx), self.dx)
        self.M = -self.E * self.I * d2w
        self.sigma = self.M * y_max / self.I

# Flask API
app = Flask(__name__)

@app.route('/calculate', methods=['GET'])
def calculate():
    # Варіант 10 (парний). Параметри передаються через URL
    # Зчитуємо параметри, якщо вони не передані, то беремо значення за замовчуванням
    length = float(request.args.get('length', 20.0))
    q = float(request.args.get('q', 10000.0))

    # Ініціалізація та обчислення
    model = BridgeLoadModel(length=length, q=q)
    model.solve_beam_deflection()
    model.calculate_moment_and_stress()

    # Формування результату
    max_deflection = float(np.min(model.w))
    max_moment = float(np.max(np.abs(model.M)))
    max_stress_mpa = float(np.max(np.abs(model.sigma)) / 1e6)

    return jsonify({
        "input": {
            "length": length,
            "q": q
        },
        "result": {
            "max_deflection_m": max_deflection,
            "max_moment_Nm": max_moment,
            "max_stress_MPa": max_stress_mpa
        }
    })

if __name__ == '__main__':
    # Запуск сервера на порту 5000
    app.run(host='0.0.0.0', port=5000)