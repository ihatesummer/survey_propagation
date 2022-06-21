# system_setting.py
## 상수
- N_USER: user 수
- AP_POSITIONS: 2차원 numpy로 하드코딩
  - ex. "np.array([[0, 0], [10, 0]])"
    -  AP가 두개 있고
    -  첫 AP가 좌표 (0, 0)에
    -  두번째 AP가 좌표 (10, 0)에 있음
  - 추후에 랜덤 위치로 뿌리도록 구현해야 할 수도 있겠음
- N_AP: 위 변수의 행 개수로 자동 계산
- MAX_DISTANCE: AP와 user의 최대 통신 가능 거리
<!-- - ETA: 무선통신 신호 감쇄 계수 $\eta$
  - AP와 user 사이 거리가 $d$일 때,
  - $\text{Rayleigh coefficient}=d^{-\eta}$
  - 자세한 채널 세팅은 [여기](https://ecewireless.blogspot.com/2020/04/how-to-simulate-ber-capacity-and-outage.html)를 참고했다고 함
- TX_POWER, NOISE_POWER: dBm 단위 -->
- STD_HAT ($\hat{\sigma}$): AWGN의 표준편차

## 변수
- main()
  - user_positions: user들의 위치
    - $\text{N\_USER} \times 2$ numpy array
    - 열 indexing: 0=x축, 1=y축
  - user2ap_distances: user와 AP간 거리 [m]
    - $\text{N\_AP} \times \text{N\_USER}$ numpy array
  - x: message passing에 쓰이는 각 user와 user 조합
    - $\text{N\_USER} + \binom{\text{N\_USER}}{2}$ Python list
    - $[0, 1, 2, ... , \text{N\_USER}, [0,1], [0,2], ... , [\text{N\_USER}, \text{N\_USER}-1]]$
  - y: message passing에 쓰이는 각 연결의 profit
    - $x\text{의 길이} \times \text{N\_RESOURCE}$ numpy array

## 함수
- get_map_boundaries()
  - AP들의 위치와 최대 통신거리에 따라 유효한 user 위치의 경계를 계산
  - 2차원이기 때문에 x축과 y축의 최소, 최대값을 각각 반환
- generate_user_positions()
  - user 위치를 랜덤으로 생성
  - get_map_boundaries()함수에서 받은 x, y축 경계 안에서 uniform 분포로 생성
- is_in_range(user, ap)
  - user와 ap가 최대통신거리 내에 있는지 확인해서 bool 변수 반환
- get_distances(user_positions)
  - AP와 user 사이 거리 & 방위각을 반환
  - 혹시 몰라 방위각도 반환하도록 했지만 당장은 필요 없어서 main 함수에서는 안 받음
- get_x()
  - main함수의 Python list x를 생성하고 반환
- get_G()
  - $G_{anr} \sim \mathcal{CN}(0,1)$ 샘플링을 AP, user, resource 조합별로 샘플링
  - $\text{N\_AP} \times \text{N\_USER} \times \text{N\_RESOURCE}$ numpy array 반환
- get_y(x, ap2user_distances)
  - main함수의 Python list y를 생성하고 반환
<!-- - db2pow(power_dbm)
  - dBm단위의 power를 linear한 값으로 변환
  - $y_{dB}=10\operatorname{log_{10}}y \Rightarrow y=10^{\frac{y_{dB}}{10}}$
- get_snr(user2ap_distances)
  - $\text{SNR}=\text{Rayleigh coeff.} \cdot \frac{\text{TX power}}{\text{noise power}}$ -->
- plot_positions(user_positions)
  - user 위치를 검은색 숫자로 표시
  - AP 위치를 다이아몬드로 표시하고 각 AP의 통신 범위를 동그라미로 표시


# survey_propagation.py
## 상수
- N_CASE: 실험 반복 횟수
  - 나중에 반복 실험을 위해 선언해둠
- N_ITER: iteration 횟수
- EPS: 작은 숫자 $\epsilon$
  - 수렴 판단 기준
- DAMP: damping 상수 $\in [0,1]$
  - 0이면 damping 없음
  - 1이면 안 변함

## 함수
- get_neighbor_indices(x, idx)
  - x[idx]의 이웃들의 index들을 반환
  - idx가 한 user를 가리킬 경우와 두 user들을 가리키는 경우를 분리해 구현함
  - 후자의 경우 두 user를 분리한 후 동일 함수를 재귀적으로 호출함
- update_xxx(.)
  - Message update 식들
- make_decision(.)
  - 현재 message 값들을 보고 각 x에 대한 resource 번호 지정
- print_allocation(.)
  - 현재 시간 t에서 각 x에 대한 allocated resource 출력
- check_convergence(.)
  - 각 message 값들이 직전시간 대비 EPS보다 적게 변했는지 확인
  - 모든 message 변화량이 EPS보다 작으면 True 반환
