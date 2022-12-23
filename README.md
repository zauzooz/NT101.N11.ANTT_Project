# PHÁT HIỆN TẤN CÔNG DDOS BẰNG SHANNON ENTROPY VÀ KHOẢNG CÁCH THÔNG TIN

## Bài báo tham khảo

- Sahoo, K. S., Puthal, D., Tiwary, M., Rodrigues, J. J., Sahoo, B., & Dash, R. (2018). An early detection of low rate DDoS attack to SDN based data center networks using information distance metrics. Future Generation Computer Systems, 89, 685-697.

## Nhóm 3000

Các thành viên:

|             Tên |     MSSV |
| --------------: | -------: |
| Nguyễn Ngọc Tài | 20521858 |
|    Trần Trí Dức | 20520454 |
|   Huỳnh Thế Hào | 20521291 |
|    Lê Thành Đạt | 20521169 |

## Mô tả các file trong dự án

- `statistic_app.py`: ứng dụng SDN để thu thập các địa chỉ đích của gói tin đến Controller.
- `ddos_deticiton.py`: ứng dụng SDN để phát hiện tấn công DDoS
- `normal_topology.py`: Mô hình mạng SDN chạy traffic bình thường. Bao gồm 16 máy (có một máy làm server cho các máy còn lại gửi gói tin UDP đến.), mỗi 4 host kết nối với 1 switch.
- `attack_topoloty.py`: Mô hình mạng SDN khi có một host thực hiện tấn công DDoS. Bao gồm 16 host (trong 16 host sẽ có 1 host làm attacker, 1 máy là server để các máy khác gửi gói tin đến), mỗi 4 host kết nối với 1 switch.
- `udp_server.py`: máy server sẽ chạy ứng dụng này.
- `upd_normal.py`: các máy thông thường sẽ gửi các gói tin.
- `udp_spoof.py`: máy attacker sẽ gửi gói tin.
- `parameter_setting.py`: cài đặt các tham số THRESHOLD_1, THRESHOLD_2 và STANDARD_NORMAL_TRAFFIC.
- `evaluation_metrics.py`: Tính toán độ chính xác.

## Các yêu cầu cài đặt

- Hệ điều hành: Ubuntu 20.04 LTS
- Sử dụng Containernet (https://github.com/containernet/containernet) để xây dựng topology mạng SDN.
- Sử dụng Ryu (https://github.com/faucetsdn/ryu) để viết các ứng dụng SDN.

## Cách chạy dự án

Bước 1: Đảm bảo phải cài đặt Containernet và Ryu như đã đề cập ở trên.

Bước 2: Clone dự án về

```Shell
git clone https://github.com/zauzooz/NT101.N11.ANTT_Project.git
```

Bước 3: Mở 2 terminal, 2 terminal đều vào thư mục NT101.N11.ANTT_Project

Bước 4:

- Ở terminal thứ nhất thực hiện chạy ứng dụng SDN:

```Shell
ryu-manager ddos_detection.py
```

- Ở terminal còn lại, thực hiện chạy topology (normal_topology.py hoặc là attack_topology.py)

```Shell
python3 normal_topology.py
```

Bước 5: Quay lại bên terminal chạy ứng dụng SDN để xem kết quả.
