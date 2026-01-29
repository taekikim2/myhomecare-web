import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai

# [핵심] 방금 만든 프롬프트 파일(prompts.py)을 불러옵니다!
import prompts 

# 1. 페이지 설정
st.set_page_config(page_title="마이홈케어플러스", page_icon="🏠", layout="wide")

# 2. 스타일 설정
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #1E3A8A; font-weight: 700; }
    .kakao-btn {
        background-color: #FEE500; color: #3C1E1E; padding: 10px 20px;
        border-radius: 10px; text-decoration: none; font-weight: bold;
        display: block; text-align: center; margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    st.markdown("부산/경남 집수리의 모든 것")
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.markdown("""<a href="https://open.kakao.com/o/seH2dLdi" target="_blank" class="kakao-btn">💬 카카오톡 무료 상담</a>""", unsafe_allow_html=True)
    st.markdown("### 📞 010-6533-3137")

# === 메인 화면 기능들 ===

if menu == "홈":
    st.markdown('<p class="main-header">"고치지 못하면 돈을 받지 않습니다"</p>', unsafe_allow_html=True)
    try: st.image("after.jpg", use_container_width=True)
    except: st.info("사진 필요")
    st.info("💧 누수 탐지 | 🛁 욕실 리모델링 | 🛠️ 종합 집수리")

elif menu == "서비스 소개":
    st.header("🛠️ 전문 시공 분야")
    st.write("누수 탐지, 방수 공사, 욕실 리모델링, 수전 교체 등 집수리 전반")

elif menu == "시공 갤러리":
    st.header("✨ 시공 전/후 비교")
    try:
        image_comparison(img1="before.jpg", img2="after.jpg", label1="Before", label2="After", width=700, in_memory=True)
    except: st.error("사진 파일 필요")

elif menu == "출장 지역":
    st.header("📍 출장 가능 지역")
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    folium.Circle(location=[35.1796, 129.0756], radius=20000, color="red", fill=True, fill_opacity=0.1).add_to(m)
    st_folium(m, width=800, height=500)

elif menu == "견적 문의":
    st.header("📝 상담 신청")
    st.write("010-6533-3137 문자/전화 환영")

# === [관리자 모드] ===
elif menu == "🔒 관리자 모드":
    st.header("🤖 블로그 포스팅 (프롬프트 분리형)")
    
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        
        with st.form("blog_form"):
            col1, col2 = st.columns(2)
            with col1:
                topic = st.selectbox("공사 종류", ["누수 탐지", "욕실 방수", "수전 교체", "화장실 리모델링", "기타"])
                location = st.text_input("현장 위치", "부산 해운대구 좌동")
            detail = st.text_area("작업 내용", height=150)
            
            submit = st.form_submit_button("📝 글 생성 (2.5 Flash)")
            
            if submit:
                try:
                    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # [핵심] 여기서 prompts.py 파일에 있는 내용을 가져옵니다!
                    # 코드가 훨씬 짧아졌죠?
                    final_prompt = prompts.get_blog_prompt(topic, location, detail)
                    
                    with st.spinner("Gemini 2.5가 대본집(prompts.py)을 읽고 글을 씁니다..."):
                        response = model.generate_content(final_prompt)
                        st.markdown("### 결과물")
                        st.code(response.text)
                        
                except Exception as e:
                    st.error(f"에러: {e}")