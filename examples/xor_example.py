"""
Тест запуска нейронной сети на мемристорах
Нейронная сеть: XOR
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from simulator.src import BoardSimulator # коннект к плате
from MemriNeurons.cores import HardCore # ядро
from MemriNeurons.hardlayers import ElementWiseMatMulLayer # слой
from MemriNeurons.components import Activations # функции активации
from MemriNeurons.keras2nmp import convert_keras_2_nmp # конвертер
from MemriNeurons.components import load_model # загрузчик модели

# настройки отображения табличек
np.set_printoptions(precision=4, suppress=True, formatter={'all': lambda x: f'{x:0.4f}'})

# выберете какой тест провести
TEST_READ_WRITE = 1 # проверка записи и чтения весов
TEST_READ_WRITE_MATRIX = 1 # тест чтения записи матрицы
TEST_MULTIPLICATION = 1 # проверка умножения
TEST_DOT_PRODUCT = 1 # проверка скалярного произведения
TEST_WEIGHT_RANGE = 1 # динамический диапазон весов
TEST_CUSTOM_NEURON = 1 # создание одного нейрона
TEST_ANN = 1 # тест ИНС собранной вручную
TEST_ANN_TF = 1 # тест ИНС с автоматической конвертацией

# подключаем плату
CONN = BoardSimulator()
_ = CONN.connect('simulator')

# создаем обработчик ядра
device = HardCore(CONN)

# ВНИМАНИЕ!!! ПРОВЕРЬ НАПРЯЖЕНИЯ
device.V_RESET = 3
device.V_SET = 3
device.V_STEP = 0.01
device.T_US = 10

if TEST_READ_WRITE: # тесты чтения и записи
    print('\n'+50*'*')
    print('Тест записи чтения')
    print(50*'*')
    WEIGHT = np.random.uniform(0, 0.3)
    WL = 0
    BL = 0
    print(f'\nВес {BL}, {WL} = {device.read_one_weight(BL, WL)}')
    print(f'Пишем вес {WEIGHT}')
    _, weight_history = device.write_weight(BL, WL, WEIGHT)
    plt.plot(weight_history, '--o')
    plt.axhline(WEIGHT, color='r')
    plt.xlabel('Iteration')
    plt.ylabel('Weight')
    plt.grid(True, linestyle='--')
    plt.show()
    print(f'Вес {BL}, {WL} = {device.read_one_weight(BL, WL)}')

if TEST_READ_WRITE_MATRIX: # тест чтения записи матрицы    
    print('\nВсе веса:')
    print(device.read_raw_weights())
    print('\nЗапишем рандомные веса:')
    random_weights = np.random.uniform(0.07, 0.33, size=(32, 8))
    print(random_weights)
    _, _ = device.write_matrix(random_weights)
    print('\nЗаписанные веса:')
    print(device.read_raw_weights())
    WEIGHT_CORRECTION = 10
    print(f'\nЧтение весов с коэффициентом масштабирования {WEIGHT_CORRECTION}:')
    if not os.path.exists('xor'):
        os.mkdir('xor')
    _ = device.read_mem_weights(save_folder='xor',
                                silent=False,
                                weight_correction=WEIGHT_CORRECTION)

if TEST_MULTIPLICATION: # тест уможения
    print('\n'+50*'*')
    print('Тест умножения')
    print(50*'*')
    WEIGHT = 0.1
    BL = 0
    WL = 0
    print(f'Пишем вес {WEIGHT}')
    _ = device.write_weight(BL, WL, WEIGHT)
    print(f'\nВес {BL}, {WL} = {device.read_one_weight(BL, WL)}')
    X = 0.3
    print(f'Умножение на X={X}')
    print(f'Результат: {device.multiplication(X, BL, WL)[0]}')
    print(f'Эталон: {X*WEIGHT}')

if TEST_DOT_PRODUCT: # тест скалярного произведения
    print('\n'+50*'*')
    print('Тест скалярного произведения')
    print(50*'*')
    device.set_mvm()
    RANDOM_WEIGHTS = np.random.uniform(0.0033, 0.05, size=(32,1))
    device.write_matrix(RANDOM_WEIGHTS, silent=False)
    X = np.random.uniform(0, 0.3, size=(32,))
    WL = 0
    all_weights = device.read_raw_weights()
    weight_vector = all_weights[:,WL]
    print(f'Эталонный выход: {weight_vector @ X}')
    print(f'Результат с платы: {device.dot_product(X, WL)[0]}')
    device.set_wr()

if TEST_WEIGHT_RANGE: # динамический диапазон весов
    print('\n'+50*'*')
    print('Динамический диапазон весов')
    print(50*'*')
    WL = 0
    BL = 0
    weight_range = np.linspace(0, 0.5, 10)
    actual_weights = []
    for weight_value in weight_range:
        _ = device.write_weight(BL, WL, weight_value)
        actual_weights.append(device.read_one_weight(BL, WL))
    print(f'Диапазон весов для контура записи/чтения: {min(actual_weights)}-{max(actual_weights)}')
    plt.plot(weight_range, weight_range, '--', label='target')
    plt.plot(weight_range, actual_weights, label='actual')
    plt.grid(True, linestyle='--')
    plt.xlabel('Target Weight')
    plt.ylabel('Actual Weight')
    plt.legend()
    plt.show()
    device.set_mvm()
    weight_range = np.linspace(0, 0.05, 10)
    actual_weights = []
    for weight_value in weight_range:
        _ = device.write_weight(BL, WL, weight_value)
        actual_weights.append(device.read_one_weight(BL, WL))
    print(f'Диапазон весов для контура матричного умножения: {min(actual_weights)}-{max(actual_weights)}')
    plt.plot(weight_range, weight_range, '--', label='target')
    plt.plot(weight_range, actual_weights, label='actual')
    plt.grid(True, linestyle='--')
    plt.xlabel('Target Weight')
    plt.ylabel('Actual Weight')
    plt.legend()
    plt.show()
    device.set_wr()

if TEST_CUSTOM_NEURON: # создание одного нейрона
    w1 = np.random.uniform(-0.3, 0.3)
    w2 = np.random.uniform(-0.3, 0.3)
    x1 = np.random.uniform(-0.3, 0.3)
    x2 = np.random.uniform(-0.3, 0.3)
    _ = device.write_weight(0, 0, w1)
    _ = device.write_weight(1, 0, w2)
    linear = lambda x: x
    output = linear(device.multiplication(x1, 0, 0, sign_w=np.sign(w1))[0] + device.multiplication(x2, 1, 0, sign_w=np.sign(w2))[0])
    etalon_output = linear(x1*w1 + x2*w2)
    print(f'Параметры нейрона: x1={round(x1,2)}, x2={round(x2,2)}, w1={round(w1,2)} w2={round(w2,2)}')
    print(f'Записанные значения: w1={round(device.read_one_weight(0, 0),2)} w2={round(device.read_one_weight(1, 0),2)}')
    print(f'Эталонный результат: {etalon_output}')
    print(f'Результат на мемристорах: {output}')

if TEST_ANN: # двухслойная сеть собранная вручную
    if not os.path.exists('xor'):
        os.mkdir('xor')

    w1 = np.array([[3.6725047, 5.21765],
                   [3.6788058, 5.24961]], dtype=float)
    b1 = np.array([-5.5291667, -2.2139354], dtype=float)
    w2 = np.array([[-5.7410617],
                   [5.4596796]], dtype=float)
    b2 = np.array([-2.4699624], dtype=float)

    sigmoid = Activations().sigmoid

    # обработчик слоя
    hardlayer1 = ElementWiseMatMulLayer(device, 'Dense_1', save_folder='xor')
    hardlayer1.find_weights_model([w1, b1], 0.33)

    hardlayer2 = ElementWiseMatMulLayer(device, 'Dense_2', save_folder='xor')
    hardlayer2.find_weights_model([w2, b2], 0.33)

    x = [[0, 0], [0, 1], [1, 0], [1, 1]]
    out1_etalon = sigmoid(x @ w1 + b1)
    out1 = sigmoid(hardlayer1.matmul(x))
    print('Layer 1')
    for i, item in enumerate(out1):
        print(item, out1_etalon[i])
    out2_etalon = sigmoid(out1_etalon @ w2 + b2)
    out2 = sigmoid(hardlayer2.matmul(out1))
    print('Layer 2')
    for i, item in enumerate(out2):
        print(item, out2_etalon[i])

if TEST_ANN_TF: # загрузка сети из файла

    SOURCE_MODEL_PATH = os.path.join('MemriNeurons', 'XOR.keras')
    NEW_MODEL_PATH = 'XOR.custom'

    new_model = convert_keras_2_nmp(SOURCE_MODEL_PATH, NEW_MODEL_PATH) # конвертация модели
    new_model = load_model(NEW_MODEL_PATH) # загрузка модели

    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    output_etalon = new_model.predict(x) # эталонный выход

    hardlayer1 = ElementWiseMatMulLayer(device, 'Dense_1', save_folder='xor') # создаем слой
    hardlayer1.find_weights_model(new_model.layers[0].get_weights(), 0.33) # маппим веса
    new_model.layers[0].matmul = hardlayer1.matmul # подменяем функцию матричного умножения

    hardlayer2 = ElementWiseMatMulLayer(device, 'Dense_2', save_folder='xor') # создаем слой
    hardlayer2.find_weights_model(new_model.layers[1].get_weights(), 0.33) # маппим веса
    new_model.layers[1].matmul = hardlayer2.matmul # подменяем функцию матричного умножения

    output = new_model.predict(x)
    for i, item in enumerate(output):
        print(item, output_etalon[i])
