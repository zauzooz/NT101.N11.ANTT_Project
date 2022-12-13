from math import log2
from fractions import Fraction

DISTRIBUTION = [] # each line in log.txt is a item, this item is a list.
TOTAL = []        # total number of packet is captured in each item in DISTRIBUTION.
NORMAL_LOGS = []

def mean(list):
    S = 0
    N = len(list)
    for i in list:
        S += i
    return S/N 

def analize(link):
    global DISTRIBUTION
    global TOTAL
    f = open(link, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        capture = eval(line)
        DISTRIBUTION.append(capture)
        S = 0
        for key in capture:
            S += capture[key]
        TOTAL.append(S)

def generalized_Entropy(alpha):
    pass

def Shanon_Entropy(capture, total):
    entropy = 0
    for key in capture:
        proba = Fraction(capture[key]/total)
        entropy += -1*proba*log2(proba)
    return entropy

if __name__=="__main__":
    print("#### NORMAL TRAFFIC ####")
    for i in range(0, 10):
        analize(f"log/normal_traffic_{i}.txt")
        entropy_list = []
        for i in range(0, len(TOTAL)):
            entropy_list.append(Shanon_Entropy(DISTRIBUTION[i], TOTAL[i]))
        print(mean(entropy_list))
        DISTRIBUTION = []
        TOTAL = []
    
    print("#### ATTACK TRAFFIC ####")
    for i in range(0, 5):
        analize(f"log/attack_traffic_{i}.txt")
        entropy_list = []
        for i in range(0, len(TOTAL)):
            entropy_list.append(Shanon_Entropy(DISTRIBUTION[i], TOTAL[i]))
        print(mean(entropy_list))
        DISTRIBUTION = []
        TOTAL = []