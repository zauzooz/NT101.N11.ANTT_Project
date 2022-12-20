from math import log2
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt

NORMAL_TRAFFIC_ENTROPY = []
ATTACK_TRAFFIC_ENTROPY = []
STANDARD_NORMAL_TRAFFIC = []
THRESHOLD_1 = 0
THRESHOLD_2 = 0

MAX_N = 10

def mean(list):
    S = 0
    N = len(list)
    for i in list:
        S += i
    return S/N

def standart_deriation(list, mean):
    SD = 0
    S_2 = 0
    N = len(list)
    for e in list:
        S_2 = S_2 + (e - mean)**2
    from math import sqrt
    SD = sqrt(S_2/N)
    return SD

def confident_interval(list):
    the_mean = mean(list)
    confident_level = 0.95 # 0.90, 0.99
    n_size = len(list)
    one_tailed_prob = (1 - confident_level)/2
    degrees_of_freedom = n_size - 1
    import scipy.stats
    z = 0
    if n_size < 30:    
        z = scipy.stats.t.ppf(q=1-one_tailed_prob, df=degrees_of_freedom)
    else:
        z = scipy.stats.norm.ppf(confident_level) # normal distribution, when n_size > 30
    from math import sqrt
    CI_max = the_mean + z * standart_deriation(list, the_mean)/sqrt(n_size)
    CI_min = the_mean - z * standart_deriation(list, the_mean)/sqrt(n_size)
    CI = CI_max - CI_min
    return (CI_min, CI_max, CI)

def threshold_1_setting(nor_list, atk_list):
    (nor_ci_min, nor_ci_max, nor_ci) = confident_interval(nor_list)
    nor_mean = mean(nor_list)
    (atk_ci_min, atk_ci_max, atk_ci) = confident_interval(atk_list)
    atk_mean = mean(atk_list)
    return atk_ci_max - nor_ci_min

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

# create plot img
def create_img():
    LIST = [i for i in range(0, 10)]
    for i in LIST:
        for j in LIST:
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
            x_nor_points = np.array([f'{i}' for i in range(1, len(nor_flows)+1)])

            y_atk_points = np.array(attack_entropy[0:len(nor_flows)])
            x_atk_points = np.array([f'{i}' for i in range(1, len(nor_flows)+1)])

            plt.plot(x_nor_points, y_nor_points, color = 'green')
            plt.plot(x_atk_points, y_atk_points, color = 'red')
            plt.grid()
            manager = plt.get_current_fig_manager()
            manager.resize(*manager.window.maxsize())
            plt.savefig(f"./img/nor{i}_vs_atk{j}.png")
            plt.clf() # clear

def entropy_mean_of_traffic(link):
    try:
        (flows, _) = analize(link=link)
        entropy = []
        for flow in flows:
            entropy.append(Shanon_Entropy(flow, MAX_N))
        return (entropy, mean(entropy))
    except:
        return

def show_nor():
    LIST = [i for i in range(0, 10)]
    for i in LIST:
        (nor_flows, _) = analize(f'./log/normal_traffic_{i}.txt')
        nor_entropys = []
        for flow in nor_flows:
            nor_entropys.append(Shanon_Entropy(flow, MAX_N))
        y_nor_points = np.array(nor_entropys)
        x_nor_points = np.array([f'{i}' for i in range(1, len(nor_flows)+1)])
        plt.plot(x_nor_points, y_nor_points, marker='o', color='green')
    plt.show()
    plt.clf() 

def show_atk():
    LIST = [i for i in range(0, 10)]
    for i in LIST:
        (atk_flows, _) = analize(f'./log/attack_traffic_{i}.txt')
        atk_entropys = []
        for flow in atk_flows:
            atk_entropys.append(Shanon_Entropy(flow, MAX_N))
        y_nor_points = np.array(atk_entropys)
        x_nor_points = np.array([f'{i}' for i in range(1, len(atk_flows)+1)])
        plt.plot(x_nor_points[0:11], y_nor_points[0:11], marker='o', color='red')
    plt.show()
    plt.clf()

def show_nor_and_atk():
    LIST = [i for i in range(0, 10)]
    for i in LIST:
        for j in LIST:
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
            x_nor_points = np.array([f'{i}' for i in range(1, len(nor_flows)+1)])

            y_atk_points = np.array(attack_entropy[0:len(nor_flows)])
            x_atk_points = np.array([f'{i}' for i in range(1, len(nor_flows)+1)])

            plt.plot(x_nor_points, y_nor_points, color = 'green', ls='', marker='o')
            plt.plot(x_atk_points, y_atk_points, color = 'red', ls='', marker='o')
            plt.grid()
    plt.show()

def init_entropy_value():
    global NORMAL_TRAFFIC_ENTROPY
    global ATTACK_TRAFFIC_ENTROPY
    LIST = [i for i in range(0, 10)]
    LIST = [i for i in range(0, 10)]
    for i in LIST:
        (nor_flows, _) = analize(f'./log/normal_traffic_{i}.txt')
        nor_entropys = []
        for flow in nor_flows:
            nor_entropys.append(Shanon_Entropy(flow, MAX_N))
        NORMAL_TRAFFIC_ENTROPY.append(nor_entropys)
    for i in LIST:
        (atk_flows, _) = analize(f'./log/attack_traffic_{i}.txt')
        atk_entropys = []
        for flow in atk_flows:
            atk_entropys.append(Shanon_Entropy(flow, MAX_N))
        ATTACK_TRAFFIC_ENTROPY.append(atk_entropys)

def return_distance_list(nor_list, atk_list):
    x = [i for i in range(0, 10)]
    distance_list = []
    for i in x:
        for j in x:
            for t in range(0, len(nor_list)):
                distance_list.append(abs(nor_list[i][t] - atk_list[j][t]))
    return distance_list

def rand_a_float_between_2_floats(min, max):
    import random
    return random.uniform(min, max)

def set_threshold_1():
    global THRESHOLD_1
    x = [i for i in range(0, 10)]
    threshold1 = []
    for i in x:
        for j in x:
            threshold = threshold_1_setting(nor_list=NORMAL_TRAFFIC_ENTROPY[i],
                            atk_list=ATTACK_TRAFFIC_ENTROPY[j][0:len(NORMAL_TRAFFIC_ENTROPY[i])])
            threshold1.append(threshold)    
    threshold1 = confident_interval(threshold1)
    THRESHOLD_1 = rand_a_float_between_2_floats(threshold1[0], threshold1[1])
    return threshold1

def set_threshold_2():
    threshold2 = confident_interval(return_distance_list(NORMAL_TRAFFIC_ENTROPY, ATTACK_TRAFFIC_ENTROPY))
    global THRESHOLD_2
    THRESHOLD_2 = rand_a_float_between_2_floats(threshold2[0], threshold2[1])
    return threshold2

def set_standart_normal_traffic():
    global STANDARD_NORMAL_TRAFFIC
    normal_standard_traffic = []
    for i in range(0, 10):
        list = []
        for j in range(0, 10):
            try:
                list.append(NORMAL_TRAFFIC_ENTROPY[j][i])
            except:
                print(f'{j}_{i}')
                return
        nor = confident_interval(list)
        normal_standard_traffic.append(rand_a_float_between_2_floats(nor[0], nor[1]))
    STANDARD_NORMAL_TRAFFIC = normal_standard_traffic
    return normal_standard_traffic


def parameter_setting():
    set_threshold_1()
    set_threshold_2()
    set_standart_normal_traffic()
    import pickle
    with open('./value_setting/threshold1.pkl', 'wb') as f:
        pickle.dump(THRESHOLD_1, f)
    with open('./value_setting/threshold2.pkl', 'wb') as f:
        pickle.dump(THRESHOLD_2, f)
    with open('./value_setting/standart_normal_traffic.pkl', 'wb') as f:
        pickle.dump(STANDARD_NORMAL_TRAFFIC, f)

def load_values():
    import pickle
    with open('./value_setting/threshold1.pkl', 'rb') as f:
        print(pickle.load(f))
    with open('./value_setting/threshold2.pkl', 'rb') as f:
        print(pickle.load(f))
    with open('./value_setting/standart_normal_traffic.pkl', 'rb') as f:
        print(pickle.load(f))

if __name__=="__main__":
    init_entropy_value()
    parameter_setting()
