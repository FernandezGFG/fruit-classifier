import numpy as np
import random
import pickle

f = open('data.pkl', 'rb')
data = pickle.load(f)
f.close()

banana_data = []
orange_data = []
lemon_data = []

for element in data:
    if (element.label == 'banana'):
        banana_data.append(element)
    if (element.label == 'orange'):
        orange_data.append(element)
    if (element.label == 'lemon'):
        lemon_data.append(element)

b_mean = list(random.choice(banana_data).feature)
o_mean = list(random.choice(orange_data).feature)
l_mean = list(random.choice(lemon_data).feature)

b_flag = True
o_flag = True
l_flag = True

b_len = [0, 0]
o_len = [0, 0]
l_len = [0, 0]

iter = 0

# while (b_flag or o_flag or l_flag):
while (iter < 20):

    banana_data = []
    orange_data = []
    lemon_data = []

    # ASIGNACION

    for element in data:
        sum_b = 0
        sum_o = 0
        sum_l = 0

        for i in range(0, len(element.feature)-1):
            sum_b += np.power(np.abs(b_mean[i] - element.feature[i]), 2)
            sum_o += np.power(np.abs(o_mean[i] - element.feature[i]), 2)
            sum_l += np.power(np.abs(l_mean[i] - element.feature[i]), 2)

        dist_b = np.sqrt(sum_b)
        dist_o = np.sqrt(sum_o)
        dist_l = np.sqrt(sum_l)

        aux = dist_b
        if (dist_o < aux):
            aux = dist_o
        if (dist_l < aux):
            aux = dist_l

        if (aux == dist_b):
            banana_data.append(element.feature)
        elif (aux == dist_o):
            orange_data.append(element.feature)
        elif(aux == dist_l):
            lemon_data.append(element.feature)

    # ACTUALIZACION
    sum_b = [0, 0]
    for b in banana_data:
        sum_b[0] += b[0]
        sum_b[1] += b[1]

    sum_o = [0, 0]
    for o in orange_data:
        sum_o[0] += o[0]
        sum_o[1] += o[1]

    sum_l = [0, 0]
    for l in lemon_data:
        sum_l[0] += l[0]
        sum_l[1] += l[1]

    b_mean[0] = sum_b[0] / len(banana_data)
    b_mean[1] = sum_b[1] / len(banana_data)
    o_mean[0] = sum_o[0] / len(orange_data)
    o_mean[1] = sum_o[1] / len(orange_data)
    l_mean[0] = sum_l[0] / len(lemon_data)
    l_mean[1] = sum_l[1] / len(lemon_data)

    # print(len(banana_data), len(orange_data), len(lemon_data))

    # CONVERGENCIA Y CONDICIÓN DE SALIDA
    print(len(banana_data), len(orange_data), len(lemon_data))

    if (b_mean == b_len):
        b_flag = False
    else:
        b_len = b_mean

    if (o_mean == o_len):
        o_flag = False
    else:
        o_len = o_mean

    if (l_mean == l_len):
        l_flag = False
    else:
        l_len = l_mean

    iter += 1

f = open('means.pkl', 'wb')
pickle.dump([b_mean, o_mean, l_mean], f)
f.close()