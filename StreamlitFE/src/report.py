import streamlit as st
import base64
import requests
import matplotlib.pyplot as plt
from scipy.stats import shapiro, spearmanr, probplot
import numpy as np

# 화면 구성 wide
st.set_page_config(layout="wide")

# base64로 인코딩된 이미지를 반환하는 함수
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 상단 배경 이미지를 설정하는 함수
def set_background(png_file):
    bin_str = get_base64(png_file)
    css = f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
                    url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .title {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60px;
        color: black;
        font-size: 3rem;
        font-weight: bold;
    }}
    .content {{
        display: grid;
        justify-content: center;
        align-items: center;
        height: 80vh;
        color: black;
        font-size: 2rem;
        font-weight: bold;
    }}
    .phase-content {{
        justify-content: center;
        font-size: 1.0rem;
        font-weight: bold;
        color: black;
        text-align: Left;
        margin: auto;
    }}
    .phase-title {{
        font-size: 2rem;  /* 더 큰 글자 크기 */
        font-weight: bold;
        color: black;
        text-align: left;
    }}
    .phase-title2 {{
        font-size: 1.5rem;  /* 더 큰 글자 크기 */
        font-weight: bold;
        color: black;
        text-align: left;
    }}
    .indented {{
        margin-left: 20px;  /* 들여쓰기 설정 */
    }}
    .compact {{
        margin-left : 5px
        margin-bottom: 5px;  /* 문구 사이의 공백을 줄이기 위해 margin 조정 */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def report():
    # 이미지 파일 경로 설정
    image_path = '../static/images/battleground1.png'
    # 배경 이미지 설정 함수 호출
    set_background(image_path)

    # GET 요청을 보낼 기본 URL
    base_url = 'http://192.168.0.79:5000'
    endpoints = "/whitezoneAnalysis/phases"
    header = {
        "Accept": "application/json"
    }

    # GET 요청 보내기
    get_response = requests.get(url=base_url + endpoints, headers=header)

    # 응답 데이터 출력
    if get_response.status_code == 200:
        data = get_response.json()
    else:
        st.write('Failed to retrieve data')
        data = {}

    # 거리 리스트 초기화
    distance_list = []
    phase_coordinates = []

    for i in range(len(data)):
        phase_list = []
        coordinates_list = []
        phase_key = f"Phase{i + 1}"
        if phase_key in data:
            for j in range(len(data[phase_key])):
                x1 = data[phase_key][j]["user_geometry_center_x"]
                x2 = data[phase_key][j]["white_zone_center_x"]
                y1 = data[phase_key][j]["user_geometry_center_y"]
                y2 = data[phase_key][j]["white_zone_center_y"]
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                phase_list.append(distance)
                coordinates_list.append((x1, y1, x2, y2))
            distance_list.append(phase_list)
            phase_coordinates.append(coordinates_list)

    # 이상치 제거 함수 (상한치만 고려)
    def remove_upper_outliers(data):
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1
        upper_bound = Q3 + 3.5 * IQR
        return [x for x in data if x <= upper_bound]

    # 초기 x축 끝값 설정 및 페이즈별 줄어드는 비율
    x_end_values = [400000, 219970.803617571057, 131740.25348840904, 78900.030827725155, 51230.391445946857,
                    33270.6639480441026, 21600.2976675614, 15100.0693623677593]

    # 각 페이즈별로 샤피로-윌크 검정 수행 및 히스토그램 시각화
    num_phases = len(distance_list)
    correlation_results = []

    for i in range(num_phases):
        specific_phase = remove_upper_outliers(distance_list[i])

        #히스토그램 그리기
        x_end = x_end_values[i]
        bins = np.linspace(0, x_end, 35)  # 35개의 bin으로 나누기

        fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        counts, bins, _ = ax[0].hist(specific_phase, bins=bins, edgecolor='black', alpha=0.5)
        bin_centers = 0.5 * (bins[1:] + bins[:-1])
        ax[0].plot(bin_centers, counts, linestyle='-', marker='o', color='blue')
        ax[0].set_title(f'Histogram of Phase {i + 1}')
        ax[0].set_xlabel('Distance')
        ax[0].set_ylabel('Frequency')
        ax[0].set_xlim(0, x_end)

        # QQ 플롯 생성
        probplot(specific_phase, dist="norm", plot=ax[1])
        ax[1].set_title(f'QQ Plot of Phase {i + 1}')
        ax[1].set_xlabel('Theoretical Quantiles')
        ax[1].set_ylabel('Sample Quantiles')

        # 컬럼 레이아웃 사용
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig)  # 히스토그램을 작은 영역에 표시
        with col2:
            # 샤피로-윌크 검정
            stat, p_value1 = shapiro(specific_phase)
            # 스피어만 상관분석
            corr, p_value2 = spearmanr(bin_centers, counts)
            correlation_results.append((i + 1, corr, p_value2))
            st.markdown(f'''
                            <div class="phase-content">
                                <div class="phase-title">Phase {i + 1}</div>
                            </div>''', unsafe_allow_html=True)
            if p_value1 > 0.05:
                st.markdown(f'<div class="phase-title2">Shapiro-Wilk Test</div>', unsafe_allow_html=True)
                st.markdown(f'''
                                <div class="phase-content">
                                <div class="compact">
                                    <span class="indented">Statistics = {stat:.4f}, p-value = {p_value1:.6f}</span><br>
                                    <span class="indented">Phase {i + 1} 데이터는 정규성을 만족한다</span>
                                </div></div>''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="phase-title2">Shapiro-Wilk Test</div>', unsafe_allow_html=True)
                st.markdown(f'''
                                <div class="phase-content">
                                <div class="compact">
                                    <span class="indented">Statistics = {stat:.4f}, p-value = {p_value1:.6f}</span><br>
                                    <span class="indented">Phase {i + 1} 데이터는 정규성을 만족하지 않는다</span>
                                </div></div>''', unsafe_allow_html=True)

            if p_value2 <= 0.05:
                st.markdown(f'<div class="phase-title2">Spearman Correlation Analysis</div>', unsafe_allow_html=True)
                st.markdown(f'''
                                <div class="phase-content">
                                <div class="compact">
                                    <span class="indented">Statistics = {round(corr, 4)}, p-value = {round(p_value2, 6)}</span><br>
                                    <span class="indented">Phase {i + 1} 유저들의 기하학적 중심과 실제 whitezone의 중심이 생성되는 위치가 상관성을 갖는다</span>
                                </div>
                                </div></div>''', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="phase-title2">Spearman Correlation Analysis</div>', unsafe_allow_html=True)
                st.markdown(f'''
                                <div class="phase-content">
                                <div class="compact">
                                    <span class="indented">Statistics = {round(corr, 4)}, p-value = {round(p_value2, 6)}</span><br>
                                    <span class="indented">Phase {i + 1} 유저들의 기하학적 중심과 실제 whitezone의 중심이 생성되는 위치가 상관성을 갖지 않는다</span>
                                </div>
                                </div></div>''', unsafe_allow_html=True)










