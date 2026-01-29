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

# 2. 스타일 설정
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

# === [기능 6: 관리자 모드 (Gemini 2.5 Flash 적용)] ===
elif menu == "🔒 관리자 모드":
    st.header("🤖 사장님 전용 AI 비서 (Ver 2.5)")
    
    password = st.text_input("관리자 비밀번호를 입력하세요", type="password")
    
    # [수정됨] Secrets에서 바로 꺼내오도록 변경 (KeyError 해결!)
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공! 최신 Gemini 2.5 Flash가 대기 중입니다.")
        st.markdown("---")
        
        with st.form("blog_form"):
            col1, col2 = st.columns(2)
            with col1:
                topic = st.selectbox("공사 종류", ["누수 탐지", "욕실 방수", "수전 교체", "화장실 리모델링"])
                location = st.text_input("현장 위치", "부산 해운대구 좌동")
            
            detail = st.text_area("특이사항 (예: 아랫집 천장에 물이 샜음, 3시간 만에 해결)")
            
            if st.form_submit_button("📝 블로그 글 생성하기"):
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    
                    # [여기!] 사장님 요청대로 2.5 Flash 적용 완료
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    당신은 부산 최고의 설비 업체 '마이홈케어플러스'의 블로그 마케터입니다.
                    아래 내용을 바탕으로 네이버 블로그 포스팅을 작성해주세요.
                    
                    - 주제: {topic}
                    - 위치: {location}
                    - 내용: {detail}
                    - 필수 포함: 업체명(마이홈케어플러스), 전화번호(010-6533-3137)
                    - 말투: 친절하고 전문적인 '해요체' 사용. 이모지 많이 사용.
                    """
                    
                    with st.spinner("Gemini 2.5가 글을 쓰고 있습니다..."):
                        response = model.generate_content(prompt)
                        st.markdown("### 👇 복사해서 블로그에 붙여넣으세요!")
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"에러가 났어요: {e}")
                    st.caption("※ 만약 모델 에러가 뜨면 서버가 아직 2.5를 못 받아들이는 상태일 수 있으니 알려주세요.")
    
    elif password:
        st.error("❌ 비밀번호가 틀렸습니다.")