from parameter_setting import ATTACK_TRAFFIC_ENTROPY, NORMAL_TRAFFIC_ENTROPY, init_entropy_value
import pickle

init_entropy_value()
attack_traffic_entropy = ATTACK_TRAFFIC_ENTROPY
attack_traffic_label = []
normal_trafic_entropy= NORMAL_TRAFFIC_ENTROPY
normal_traffic_label = []
standard_normal_traffic = 0
with open('./value_setting/standard_normal_traffic.pkl', 'rb') as f:
    standard_normal_traffic = pickle.load(f)
threhold_1 = 0
with open('./value_setting/threshold1.pkl', 'rb') as f:
    threhold_1 = pickle.load(f)
threhold_2 = 0
with open('./value_setting/threshold2.pkl', 'rb') as f:
    threhold_2 = pickle.load(f)

def returnLabelTraffic(list):
    counter = 0
    x = [i for i in range(0, len(standard_normal_traffic))]
    for i in x:
        h = list[i]
        id = abs(standard_normal_traffic[i] - h)
        if id >= threhold_2 and h <= threhold_1:
            counter = counter + 1
            if counter == 3:
                return "attack"
        else:
            counter = 0
    return "normal"

def trainTest():
    global normal_traffic_label
    global attack_traffic_label
    for flow in normal_trafic_entropy:
        normal_traffic_label.append(returnLabelTraffic(flow))
    print(normal_traffic_label)
    for flow in attack_traffic_entropy[0:11]:
        attack_traffic_label.append(returnLabelTraffic(flow))
    print(attack_traffic_label)


def accuracy(_normal_traffic_label, _attack_traffic_label):  
    TP = _attack_traffic_label.count('attack')     # attack data is correctly classified as an attack
    FP = _normal_traffic_label.count('attack')     # normal data is incorrectly classified as an attack
    TN = _normal_traffic_label.count('normal')     # normal data is correctly classified as an normal
    FN = _attack_traffic_label.count('normal')   # attack data is incorrectly classified as an normal
    return (TP + TN) / (TP + TN + FP + FN)

def precision(_normal_traffic_label, _attack_traffic_label):
    TP = _attack_traffic_label.count('attack')     # attack data is correctly classified as an attack
    FP = _normal_traffic_label.count('attack')     # normal data is incorrectly classified as an attack
    # TN = _normal_traffic_label.count('normal')     # normal data is correctly classified as an normal
    # FN = _attack_traffic_label.count('normal')   # attack data is incorrectly classified as an normal
    return TP/(TP + FP)

def recall(_normal_traffic_label, _attack_traffic_label):
    TP = _attack_traffic_label.count('attack')     # attack data is correctly classified as an attack
    # FP = _normal_traffic_label.count('attack')     # normal data is incorrectly classified as an attack
    # TN = _normal_traffic_label.count('normal')     # normal data is correctly classified as an normal
    FN = _attack_traffic_label.count('normal')   # attack data is incorrectly classified as an normal
    return TP/(TP + FN)

def f1_score(_normal_traffic_label, _attack_traffic_label):
    _precision = precision(_normal_traffic_label, _attack_traffic_label)
    _recall = recall(_normal_traffic_label, _attack_traffic_label)
    return 2*_precision*_recall/(_precision+_recall)

if __name__=="__main__":
    trainTest()
    TP = attack_traffic_label.count('attack')     # attack data is correctly classified as an attack
    FP = normal_traffic_label.count('attack')     # normal data is incorrectly classified as an attack
    TN = normal_traffic_label.count('normal')     # normal data is correctly classified as an normal
    FN = attack_traffic_label.count('normal')   # attack data is incorrectly classified as an normal
    print(TP)
    print(FP)
    print(TN)
    print(FN)
    print(accuracy(normal_traffic_label, attack_traffic_label))
    print(precision(normal_traffic_label, attack_traffic_label))
    print(recall(normal_traffic_label, attack_traffic_label))
    print(f1_score(normal_traffic_label, attack_traffic_label))

