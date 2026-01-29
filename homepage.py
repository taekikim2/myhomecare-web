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

# 2. 스타일 설정 (카톡 버튼 디자인 유지)
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    /* 카카오톡 버튼 스타일 */
    .kakao-btn {
        background-color: #FEE500;
        color: #3C1E1E;
        padding: 10px 20px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        margin: 10px 0;
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
    
    # [카톡 버튼 유지] 본인 오픈채팅방 주소로 꼭 확인하세요!
    st.markdown("""
        <a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">
            💬 카카오톡 무료 상담
        </a>
    """, unsafe_allow_html=True)
    
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

# === [기능 6: 관리자 모드 (Gemini 2.5 + 해시태그 강화)] ===
elif menu == "🔒 관리자 모드":
    st.header("🤖 블로그 포스팅 (중소형 키워드 타겟팅)")
    
    password = st.text_input("관리자 비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공! 해시태그 분석 기능이 활성화되었습니다.")
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
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # [업그레이드] 해시태그 전략이 추가된 프롬프트
                    MASTER_PROMPT = f"""
                    # Role: 마이홈케어플러스 대표 (부산 누수/방수 전문가) + SEO 마케팅 전문가
                    
                    # [현장 정보]
                    - 시공 종류: {topic}
                    - 현장 위치: {location}
                    - 상세 내용: {detail}

                    # [작성 가이드라인]
                    1. 글자 수: 1500~2000자 내외.
                    2. 구조: [제목] -> [도입부] -> [현장 정밀 분석] -> [해결 과정] -> [마무리] -> [FAQ] -> [추천 태그]
                    3. 키워드 배치: '{location} {topic}' 같은 세부 지역 키워드를 본문에 자연스럽게 5회 이상 녹일 것.
                    4. 가독성: 모바일 최적화 (3~4줄 문단 나누기).
                    
                    # [★중요: 해시태그 전략 (중소형 키워드)]
                    - 단순히 #누수 #방수 같은 경쟁 심한 '대형 키워드'만 쓰지 마세요.
                    - **검색량은 적지만 구매 전환율이 높은 '중소형(세부) 키워드' 10개를 반드시 추출**하여 글 맨 마지막에 달아주세요.
                    - 조합 예시: 지역명+동이름+시공명 (예: #해운대좌동누수), 아파트명+시공명 (예: #벽산아파트방수), 증상+해결 (예: #천장물샘해결)
                    
                    # [톤앤매너]
                    - 신뢰감 있는 '해요체' 사용.
                    - **이모지 절대 사용 금지** (오직 텍스트로만 전문성 강조).
                    - 업체명(마이홈케어플러스), 연락처(010-6533-3137) 필수 포함.
                    """
                    
                    with st.spinner("Gemini 2.5가 황금 키워드를 분석 중입니다..."):
                        response = model.generate_content(MASTER_PROMPT)
                        st.markdown("### 👇 블로그에 복사해서 쓰세요 (해시태그 포함)")
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"에러가 발생했습니다: {e}")
    
    elif password:
        st.error("❌ 비밀번호가 틀렸습니다.")