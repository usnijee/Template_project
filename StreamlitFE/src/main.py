import streamlit as st
from matplotlib import pyplot as plt
import numpy as np

from submit import page1to2

def page1(navigate_to):
    # 상단에 배경 이미지를 설정한 헤더 추가
    st.markdown('<div class="centered">SSB.GG</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 5])
        with col1:
            st.selectbox(" ", ["kakao", "steam"], key="platform")
        with col2:
            st.text_input(" ", placeholder="닉네임을 입력하세요", key="nickname", on_change=page1to2)
        st.markdown('</div>', unsafe_allow_html=True)
def page2(navigate_to):
    # player_stats 변수에 get 응답 json데이터를 저장
    ## player_stats = st.session_state.get('player_stats', {'wins': 0, 'top10s': 0})
    # 상단바 스타일 설정
    st.markdown("""
        <style>
        .custom-header {
            background-color: #333333;
            padding: 20px;  /* 상단바의 패딩을 20px로 설정 */
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            color: #FFA500;
            height: 100px;
        }
        .content {
            padding-top: 120px; /* 상단바 높이만큼 패딩 추가 */
        }
        .custom-header .title {
            color : #FFA500;
            font-size: 60px;
            font-weight: bold;
            padding-bottom : 40px;
            margin-right : 40px;
        }
        .custom-header .menu {
            display: flex;
            align-items: center;
        }
        .custom-header .menu a {
            color: #FFA500;
            text-decoration: none;
            margin-left: auto;
            font-size: 20px;
            margin-right: 150px;
        }
        .search-bar {
            display: flex;
            align-items: center;
        }
        .search-bar input {
            font-size: 10px;
            padding: 5px;
            margin-right: 0px;
        }
        .search-bar button {
            font-size: 15px; /* 버튼의 글자 크기 조절 */
            color: black;
        }
        .custom-container {
            border: 2px solid #FFA500; /* 테두리 색상 설정 */
            border-radius: 10px; /* 테두리 모서리 둥글게 설정 */
            padding: 10px; /* 내부 여백 추가 */
            margin-bottom: 20px; /* 컨테이너 간 간격 추가 */
            background-color: rgba(255, 255, 255, 0.1); /* 반투명 배경 설정 */
            width: 100%;
        }
        .custom-image {
        
        width: 200px; /* 원하는 너비로 설정 */
        height: auto; /* 비율을 유지하면서 높이를 자동으로 조절 */
        }
        .custom-row {
        display: flex;
        align-items: stretch;
        justify-content: space-between;
        height: 500px; /* 줄일 높이 설정 */
        }
        .custom-col {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        }
        .custom-col img, .custom-col div, .custom-col canvas {
            max-width: 100%;
            max-height: 100%;
        }
        </style>
        """, unsafe_allow_html=True)

    # 상단바
    st.markdown("""
        <div class="custom-header">
            <div class="title">SBB.GG</div>
            <div class="menu">
                <a href="#heatmap">HeatMap</a>
                <div class="search-bar">
                    <input type="text" placeholder="enter_player_name" />
                    <button>search</button>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 컨텐츠를 상단바 아래로 이동시키기 위한 패딩 추가
    st.markdown('<div class="content">', unsafe_allow_html=True)

    with st.container():
        # 플레이어 정보와 이미지 그룹화
        st.markdown('<div class="custom-row">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1,1,2])

        with col1:
            st.markdown('<div class="custom-col">', unsafe_allow_html=True)
            st.image("https://cdn-icons-png.flaticon.com/512/10568/10568151.png", caption="", use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                    <div class="custom-col">
                        <h2>Lv.???</h2>
                        <p>Player Name</p>
                        <p>clan ID</p>
                        <p>승률 : 20%</p>
                        <p>Top 10 비율 : 44%</p>
                        <p>평균 피해량 : 000.0</p>
                        <p>평균 생존시간 : 00:00</p>
                    </div>
                    """, unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="custom-col">', unsafe_allow_html=True)
            st.pyplot(create_pie_chart())
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 최근 플레이 로그
    for i in range(1, 6):
        with st.expander(f"Recent play{i}", expanded=False):
            with st.container():
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                                    <div class="custom-col">
                                        <h2>Lv.???</h2>
                                        <p>Player Name</p>
                                        <p>clan ID</p>
                                        <p>승률 : 20%</p>
                                        <p>Top 10 비율 : 44%</p>
                                        <p>평균 피해량 : 000.0</p>
                                        <p>평균 생존시간 : 00:00</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                with col2:
                    st.pyplot(create_radar_chart())  # 레이더 차트 추가
                with col3:
                    st.pyplot(create_radar_chart())

def create_pie_chart():
    labels = '1st', 'Top10'
    sizes = [16.7, 83.3]
    colors = ['blue', 'yellow']
    explode = (0.1, 0)  # explode 1st slice

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')  # 파이 차트 전체 배경 투명하게 설정
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.patch.set_facecolor('none')  # 파이 차트의 축 배경 투명하게 설정

    return fig

def create_radar_chart():
    labels = np.array(['호전성', '생존력', '유틸성', '전투력', '저격능력'])
    stats = np.array([65, 59, 90, 81, 56])

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    stats = np.concatenate((stats, [stats[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='red', alpha=0.25)
    ax.plot(angles, stats, color='red', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)

    return fig







