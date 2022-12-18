from math import log2
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np

NORMAL_TRAFFIC_LIST = []
NORMAL_TRAFFIC_ENTROPY = []
ATTACK_TRAFFIC_LIST = []
ATTACK_TRAFFIC_ENTROPY = []

MAX_N = 10

def mean(list):
    S = 0
    N = len(list)
    for i in list:
        S += i
    return S/N 

def analize(link):
    FLOWS = []
    TOTAL = []
    f = open(link, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        capture = eval(line)
        FLOWS.append(capture)
        S = 0
        for key in capture:
            S += capture[key]
        TOTAL.append(S)
    return (FLOWS, TOTAL)

def Shanon_Entropy(capture, total):
    entropy = 0
    for key in capture:
        proba = Fraction(capture[key]/total)
        entropy += -1*proba*log2(proba)
    return entropy



if __name__=="__main__":
    i = 1 # 0 <= i <= 9
    j = 2 # 0 <= j <= 9
    (nor_flows, _) = analize(f'./log/normal_traffic_{i}.txt')
    (atk_flows, _) = analize(f'./log/attack_traffic_{j}.txt')
    normal_entroy = []
    attack_entropy = []
    for flow in nor_flows:
        normal_entroy.append(Shanon_Entropy(flow, MAX_N))
    for flow in atk_flows:
        attack_entropy.append(Shanon_Entropy(flow, MAX_N))
    X = [i for i in range(1, len(nor_flows)+1)]
    y_nor_points = np.array(normal_entroy)
    x_nor_points = np.array([i for i in range(1, len(nor_flows)+1)])

    y_atk_points = np.array(attack_entropy[0:len(nor_flows)])
    x_atk_points = np.array([i for i in range(1, len(nor_flows)+1)])

    plt.plot(x_nor_points, y_nor_points, color = 'green')
    plt.plot(x_atk_points, y_atk_points, color = 'red')
    plt.show()