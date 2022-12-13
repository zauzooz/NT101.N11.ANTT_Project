# DDOS ATTACK DETECTION USING INFORMATION DISTANCE

## Reference:

- Sahoo, K. S., Puthal, D., Tiwary, M., Rodrigues, J. J., Sahoo, B., & Dash, R. (2018). An early detection of low rate DDoS attack to SDN based data center networks using information distance metrics. Future Generation Computer Systems, 89, 685-697.
- *Update later...*

## Members

|Name              |                 ID|
|-----------------:|------------------:|
|Nguyen Ngoc Tai   |20521858           |
|Tran Tri Duc      |20520454           |
|Huynh The Hao     |20521291           |
|Le Thanh Dat      |20521169           |


## Description

- `statistic_app.py`: SDN application of our project. It uses to statistic the destination IP address comes to the controller.
- `normal_topology.py`: SDN topology of our project - normal traffic.
- `attack_topoloty.py`: SDN topology of our project - attack traffic.
- `upd_normal.py`: send a normal UDP packet to the victim.
- `udp_spoof.py`: send a spoofing UDP packet to the victim.
- `entropy_calculator.py`: calculate entropy depends on `log.txt` file.
- `ddos_deticiton.py`: SDN application of our project. It uses to detect DDoS attack.
- *Update later...*

## Requirements

- OS: Ubuntu 20.04 LTS
- Use Containernet (https://github.com/containernet/containernet) to build a SDN topology.
- Use Ryu (https://github.com/faucetsdn/ryu) to write SDN application.
- *Update later...*
