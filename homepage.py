import streamlit as st
from PIL import Image
# [새로 추가된 도구] 이미지 비교 슬라이더
from streamlit_image_comparison import image_comparison

# 1. 페이지 설정
st.set_page_config(
    page_title="마이홈케어플러스 - 부산 1등 홈케어",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 디자인 및 스타일 (카톡 버튼 꾸미기 포함)
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .sub-header { font-size: 1.5rem; color: #4B5563; }
    /* 카카오톡 버튼 스타일 */
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
    menu = st.radio("메뉴 이동", ["홈(Home)", "서비스 소개", "시공 전/후(New!)", "견적 문의"])
    st.markdown("---")
    
    # [기능 2] 카카오톡 상담 버튼 (사이드바에 고정)
    # 실제 사장님 오픈채팅방 주소가 있다면 '#' 대신 넣으세요
    st.markdown("""
        <a href="https://open.kakao.com/o/seH2dLdi" target="_blank" class="kakao-btn">
            💬 카카오톡 무료 상담
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📞 010-6533-3137")

# 4. 메인 화면

# [홈]
if menu == "홈(Home)":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    st.image("after.jpg", caption="마이홈케어플러스의 완벽한 마감", use_container_width=True)
    
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

# [시공 전/후] - 여기가 핵심! (기능 1)
elif menu == "시공 전/후(New!)":
    st.markdown('<p class="main-header">✨ 놀라운 변화를 확인하세요</p>', unsafe_allow_html=True)
    st.caption("가운데 바를 마우스로 잡고 좌우로 움직여보세요!")

    # 슬라이더 만들기
    # (폴더에 before.jpg, after.jpg가 없으면 에러가 날 수 있으니 꼭 넣어주세요)
    try:
        image_comparison(
            img1="before.jpg",  # 공사 전 사진
            img2="after.jpg",   # 공사 후 사진
            label1="시공 전 (Before)",
            label2="시공 후 (After)",
            width=700,
            starting_position=50,
            show_labels=True,
            make_responsive=True,
            in_memory=True
        )
        st.success("👆 낡고 물 새던 곳이 이렇게 깔끔하게 변했습니다.")
        
    except FileNotFoundError:
        st.error("⚠️ 폴더에 'before.jpg'와 'after.jpg' 사진을 넣어주세요!")

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