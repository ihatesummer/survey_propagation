# system_setting.py
## 상수
- N_USER: user 수
- AP_POSITIONS: 2차원 numpy로 하드코딩
  - ex. "np.array([[0, 0], [10, 0]])"
    -  AP가 두개 있고
    -  첫 AP가 좌표 (0, 0)에
    -  두번째 AP가 좌표 (10, 0)에 있음
  - 추후에 랜덤 위치로 뿌리도록 구현해야 할 수도 있겠음
- N_AP: 위 변수의 행 수로 자동 계산
- MAX_DISTANCE: AP와 user의 최대 통신 가능 거리
- ETA: 무선통신 신호 감쇄 계수 $\eta$
  - AP와 user 사이 거리가 $d$일 때,
  - $\text{Rayleigh coefficient}=d^{-\eta}$
  - 자세한 채널 세팅은 [여기](https://ecewireless.blogspot.com/2020/04/how-to-simulate-ber-capacity-and-outage.html)를 참고했다고 함
- TX_POWER, NOISE_POWER: dBm 단위
- INF: 최대
## 함수, 변수
- main()
  - user_positions: user들의 위치
    - $\text{N\_USER}\times 2$차원 numpy
    - 행: user index, 열: x, y
  - user2ap_distances: user와 AP간 거리 [m]
    - $\text{N\_AP}\times \text{N\_USER}$차원 numpy
  -  snr
     - $\text{N\_AP}\times \text{N\_USER}$차원 numpy
- get_map_boundaries()
  - AP들의 위치와 최대 통신거리에 따라 유효한 user 위치의 경계를 계산
  - 2차원이기 때문에 x축과 y축의 최소, 최대값을 각각 반환
- generate_user_positions()
  - user 위치를 랜덤으로 생성
  - get_map_boundaries()함수에서 받은 x, y축 경계 안에서 uniform 분포로 생성
- get_distances(user_positions)
  - AP와 user 사이 거리 & 방위각을 반환
  - 혹시 몰라 방위각도 반환하도록 했지만 당장은 필요 없어서 main 함수에서는 안 받음
- db2pow(power_dbm)
  - dBm단위의 power를 linear한 값으로 변환
  - $y_{dB}=10\operatorname{log_{10}}y \Rightarrow y=10^{\frac{y_{dB}}{10}}$
- get_snr(user2ap_distances)
  - $\text{SNR}=\text{Rayleigh coeff.} \cdot \frac{\text{TX power}}{\text{noise power}}$
- plot_positions(user_positions)
  - user 위치를 검은색 숫자로 표시
  - AP 위치를 다이아몬드로 표시하고 각 AP의 통신 범위를 동그라미로 표시


# survey_propagation.py
## 상수
- N_RESOURCE: 각 AP당 채널 수
- N_CASE: 실험 반복 횟수
  - 알고리즘이 돌아가는것을 확인 한 후 나중에 반복 실험을 위해 일단 선언해둠
## 함수, 변수