import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(
    page_title="마이홈케어플러스 - 부산 1등 홈케어",
    page_icon="🏠",
    layout="wide"
)

# 2. 스타일 설정 (깔끔하게)
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .kakao-btn {
        background-color: #FEE500; color: #3C1E1E; padding: 10px 20px;
        border-radius: 10px; text-decoration: none; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 메뉴
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    st.markdown("부산/경남 집수리의 모든 것")
    st.markdown("---")
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.markdown("---")
    st.markdown("### 📞 010-6533-3137")

# === [기능 1~5: 일반 고객용 화면] ===

if menu == "홈":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    try:
        st.image("after.jpg", caption="마이홈케어플러스의 완벽한 마감", use_container_width=True)
    except: st.info("사진을 넣어주세요")
    st.info("💧 누수 탐지 | 🛁 욕실 리모델링 | 🛠️ 종합 집수리")

elif menu == "서비스 소개":
    st.header("🛠️ 전문 시공 분야")
    st.write("누수 탐지, 방수 공사, 욕실 리모델링, 수전 교체 등 집수리 전반")

elif menu == "시공 갤러리":
    st.header("✨ 시공 전/후 비교")
    try:
        image_comparison(
            img1="before.jpg", img2="after.jpg", label1="Before", label2="After",
            width=700, starting_position=50, show_labels=True, in_memory=True
        )
    except: st.error("사진 파일(before.jpg, after.jpg)이 필요합니다.")

elif menu == "출장 지역":
    st.header("📍 출장 가능 지역")
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    folium.Circle(location=[35.1796, 129.0756], radius=20000, color="red", fill=True, fill_opacity=0.1).add_to(m)
    st_folium(m, width=800, height=500)

elif menu == "견적 문의":
    st.header("📝 상담 신청")
    st.write("010-6533-3137 번으로 문자나 전화 주세요!")

# === [기능 6: 관리자 모드 (사장님 요청 완벽 반영)] ===
elif menu == "🔒 관리자 모드":
    st.header("🤖 블로그 자동 포스팅 (Gemini 2.5 Flash)")
    
    password = st.text_input("관리자 비밀번호", type="password")
    
    # [수정] .get()을 써서 비밀번호 키가 없어도 에러가 안 나게 안전장치 추가
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공! 최신 Gemini 2.5 모델이 대기 중입니다.")
        st.markdown("---")
        
        with st.form("blog_form"):
            col1, col2 = st.columns(2)
            with col1:
                topic = st.selectbox("공사 종류", ["누수 탐지", "욕실 방수", "수전 교체", "화장실 리모델링", "기타 집수리"])
                location = st.text_input("현장 위치", "부산 해운대구 좌동")
            
            detail = st.text_area("작업 내용 (최대한 자세히 적어주세요)", height=150)
            
            submit = st.form_submit_button("📝 블로그 글 생성하기 (2.5 Flash)")
            
            if submit:
                try:
                    # 1. API 설정
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    
                    # [여기!] 사장님이 말씀하신 최신 버전 적용 (2026년 기준)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # 2. 이모지 박멸 + 전문가 프롬프트
                    MASTER_PROMPT = f"""
                    # Role: 마이홈케어플러스 대표 (부산 누수/방수 전문가) + SEO 마케팅 전문가
                    
                    # [현장 정보]
                    - 시공 종류: {topic}
                    - 현장 위치: {location}
                    - 상세 내용: {detail}

                    # [작성 가이드라인]
                    1. 글자 수: 1500~2000자 내외로 네이버 로직에 맞춰 작성.
                    2. 구조: [제목] -> [도입부] -> [현장 정밀 분석] -> [해결 과정] -> [마무리] -> [FAQ]
                    3. 키워드: '{location} {topic}', '부산 {topic}' 키워드를 자연스럽게 5회 이상 반복.
                    4. 가독성: 모바일 환경을 고려하여 문단은 3~4줄로 짧게 끊기.
                    5. 필수 포함:
                       - 업체명: 마이홈케어플러스
                       - 연락처: 010-6533-3137 (중간과 끝에 강조)
                       - 슬로건: "고치지 못하면 돈을 받지 않습니다"
                    
                    # [매우 중요: 톤앤매너]
                    - 신뢰감 있고 전문적인 어조 ('해요체' 사용).
                    - **절대 이모지(😊, ✨, 💧 등)를 사용하지 마세요.** 오직 텍스트와 문장력으로만 승부하세요.
                    - 특수문자는 가독성을 위한 점(·), 대시(-) 정도만 허용합니다.
                    """
                    
                    with st.spinner("Gemini 2.5가 분석 중입니다... (이모지 제거 중 🧹)"):
                        response = model.generate_content(MASTER_PROMPT)
                        st.markdown("### 👇 아래 내용을 블로그에 복사해 주세요.")
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"에러가 발생했습니다: {e}")
                    st.caption("※ 혹시 모델을 못 찾으면 'gemini-2.0-flash'로 변경해 보세요.")
    
    elif password:
        st.error("❌ 비밀번호가 틀렸습니다.")