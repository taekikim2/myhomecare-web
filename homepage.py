import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
# [지도 도구 추가]
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="마이홈케어플러스 - 부산 1등 홈케어",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 디자인 및 스타일
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .sub-header { font-size: 1.5rem; color: #4B5563; }
    .kakao-btn {
        background-color: #FEE500;
        color: #3C1E1E;
        padding: 10px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    st.markdown("부산/경남 집수리의 모든 것")
    st.markdown("---")
    # [메뉴에 '출장 지역' 추가됨]
    menu = st.radio("메뉴 이동", ["홈(Home)", "서비스 소개", "시공 전/후", "출장 지역(Map)", "견적 문의"])
    st.markdown("---")
    
    # [본인의 카톡방 주소로 꼭 유지하세요!]
    st.markdown("""
        <a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">
            💬 카카오톡 무료 상담
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📞 010-6533-3137")

# 4. 메인 화면

# [홈]
if menu == "홈(Home)":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    try:
        st.image("after.jpg", caption="마이홈케어플러스의 완벽한 마감", use_container_width=True)
    except:
        st.info("📸 폴더에 'after.jpg' 사진을 넣어주세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1: st.info("💧 **누수 탐지/방수**\n\n첨단 장비로 원인 불명 누수 해결")
    with col2: st.info("🛁 **욕실 리모델링**\n\n호텔 같은 욕실로 변신")
    with col3: st.info("🛠️ **종합 집수리**\n\n수전, 변기, 싱크대 부분 수리")

# [서비스 소개]
elif menu == "서비스 소개":
    st.header("🛠️ 전문 시공 분야")
    tab1, tab2 = st.tabs(["누수/방수", "인테리어/수리"])
    with tab1:
        st.write("- **청음식 탐지:** 배관 누수음을 증폭시켜 정확한 위치 포착")
        st.write("- **가스식 탐지:** 미세한 가스를 주입해 탐지")
        st.write("- **방수 공사:** 옥상 우레탄, 화장실 비파괴 방수")
    with tab2:
        st.write("- **욕실:** 타일 덧방, 돔천장, 위생도기 세팅")
        st.write("- **주방:** 싱크대 수전 교체, 상판 연마")

# [시공 전/후]
elif menu == "시공 전/후":
    st.markdown('<p class="main-header">✨ 놀라운 변화를 확인하세요</p>', unsafe_allow_html=True)
    st.caption("가운데 바를 마우스로 잡고 좌우로 움직여보세요!")
    try:
        image_comparison(
            img1="before.jpg", img2="after.jpg",
            label1="시공 전", label2="시공 후",
            width=700, starting_position=50,
            show_labels=True, make_responsive=True, in_memory=True
        )
        st.success("👆 낡고 물 새던 곳이 이렇게 깔끔하게 변했습니다.")
    except FileNotFoundError:
        st.error("⚠️ 사진 파일(before.jpg, after.jpg)을 확인해주세요.")

# [출장 지역] - 여기가 새로 추가된 지도 기능! 🗺️
elif menu == "출장 지역(Map)":
    st.markdown('<p class="main-header">📍 어디까지 출장 가나요?</p>', unsafe_allow_html=True)
    st.markdown("### 부산 전 지역 / 김해 / 양산 출장 가능")
    
    # 1. 지도 중심 잡기 (부산 시청 근처)
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    
    # 2. 마커 찍기 (우리 업체 위치 - 대략적인 부산 중심)
    folium.Marker(
        [35.1796, 129.0756], 
        popup="마이홈케어플러스", 
        tooltip="부산 본점",
        icon=folium.Icon(color="blue", icon="home")
    ).add_to(m)
    
    # 3. 출장 가능 범위 원 그리기 (반경 20km)
    folium.Circle(
        location=[35.1796, 129.0756],
        radius=20000, # 20km
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.1,
        popup="출장 가능 지역"
    ).add_to(m)
    
    # 4. 화면에 보여주기
    st_folium(m, width=800, height=500)
    
    st.success("🚗 고객님이 계신 곳으로 신속하게 달려갑니다!")

# [견적 문의]
elif menu == "견적 문의":
    st.header("📝 30초 간편 견적 신청")
    with st.form("contact"):
        c1, c2 = st.columns(2)
        with c1: st.text_input("성함")
        with c2: st.text_input("연락처")
        st.text_area("문의 내용")
        if st.form_submit_button("상담 신청하기"):
            st.success("접수되었습니다! 확인 후 바로 연락드리겠습니다.")