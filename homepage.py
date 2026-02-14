import streamlit as st
from PIL import Image
from streamlit_image_comparison import image_comparison
import folium
from streamlit_folium import st_folium
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import io
import pandas as pd
from datetime import datetime
import random

# [중요] 우리가 만든 파일들 불러오기
import calculator
import watermarker

# 1. 페이지 설정
st.set_page_config(page_title="마이홈케어플러스", page_icon="🏠", layout="wide")

# 2. 디자인(CSS) 설정
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
    
    .hero-title { font-size: 3rem; color: #1E3A8A; font-weight: 900; line-height: 1.2; margin-bottom: 20px; }
    .hero-subtitle { font-size: 1.3rem; color: #444; font-weight: 500; margin-bottom: 30px; }
    .highlight { color: #d32f2f; font-weight: bold; }

    .feature-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08); text-align: center; border: 1px solid #f0f0f0; height: 100%;
        transition: transform 0.3s ease;
    }
    .feature-card:hover { transform: translateY(-5px); }
    .feature-icon { font-size: 3rem; margin-bottom: 15px; }
    .feature-title { font-weight: bold; font-size: 1.2rem; color: #1E3A8A; margin-bottom: 10px; }
    .feature-text { font-size: 1rem; color: #666; line-height: 1.6; }

    .review-card {
        background-color: #FFF8E1; padding: 20px; border-radius: 15px;
        border: 1px solid #FFECB3; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .stars { color: #FFD700; font-size: 1.2rem; }
    .review-text { font-size: 1.1rem; font-weight: bold; color: #333; margin: 10px 0; }
    .review-info { font-size: 0.9rem; color: #666; text-align: right; }

    .kakao-btn {
        background-color: #FEE500; color: #3C1E1E; padding: 12px 20px;
        border-radius: 8px; text-decoration: none; font-weight: bold;
        display: block; text-align: center; margin: 10px 0; font-size: 1rem;
    }
    .service-box {
        background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px;
        border-left: 5px solid #1E3A8A;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바
with st.sidebar:
    st.title("🏠 마이홈케어플러스")
    st.markdown("부산/경남 집수리의 모든 것")
    st.divider()
    menu = st.radio("메뉴", ["홈", "서비스 소개", "시공 갤러리", "출장 지역", "견적 문의", "🔒 관리자 모드"])
    st.divider()
    st.markdown("""<a href="https://open.kakao.com/o/sExample" target="_blank" class="kakao-btn">💬 카카오톡 무료 상담</a>""", unsafe_allow_html=True)
    st.markdown("### 📞 010-6533-3137")

# --- 구글 시트 연결 및 데이터 함수 ---
def get_google_sheet():
    try:
        raw_key = st.secrets["GOOGLE_SHEET_KEY"]
        try:
            json_key = json.loads(raw_key, strict=False)
        except json.JSONDecodeError:
            json_key = json.loads(raw_key.replace('\n', '\\n'), strict=False)
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
        client = gspread.authorize(creds)
        return client.open("마이홈케어 시공장부").sheet1
    except: return None

def add_to_sheet(date, place, work, price, note, review):
    sheet = get_google_sheet()
    if sheet:
        try:
            sheet.append_row([str(date), place, work, price, note, review])
            return True
        except: return False
    return False

def load_data():
    sheet = get_google_sheet()
    if sheet:
        try:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except: return pd.DataFrame()
    return pd.DataFrame()

# ==========================================
# 1. 홈 화면 (메인)
# ==========================================
if menu == "홈":
    hero_col1, hero_col2 = st.columns([4, 6], gap="large")
    with hero_col1:
        st.markdown('<h1 class="hero-title">지긋지긋한 누수,<br>확실하게 잡습니다.</h1>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">부산/경남 1등 홈케어 전문가<br><span class="highlight">"못 고치면 10원도 받지 않겠습니다."</span></p>', unsafe_allow_html=True)
        st.write("") 
        st.info("💡 지금 바로 전문가와 상담하세요!")
        st.markdown("### 📞 010-6533-3137 (긴급출동)")
    with hero_col2:
        st.write("")
        tab1, tab2, tab3 = st.tabs(["🛁 욕실 리모델링", "💧 누수 탐지", "🧱 방수 공사"])
        with tab1:
            try: image_comparison(img1="case1_before.jpg", img2="case1_after.jpg", label1="철거 전", label2="리모델링 완료", width=800, in_memory=True)
            except: st.warning("case1_before.jpg, case1_after.jpg 사진을 올려주세요!")
        with tab2:
            try: image_comparison(img1="case2_before.jpg", img2="case2_after.jpg", label1="누수 피해", label2="탐지 및 복구", width=800, in_memory=True)
            except: st.warning("case2_before.jpg, case2_after.jpg 사진을 올려주세요!")
        with tab3:
            try: image_comparison(img1="case3_before.jpg", img2="case3_after.jpg", label1="방수 전", label2="방수 완료", width=800, in_memory=True)
            except: st.warning("case3_before.jpg, case3_after.jpg 사진을 올려주세요!")
    
    st.divider()

    st.subheader("⭐⭐⭐⭐⭐ 고객님들의 찐 후기")
    df = load_data()
    if not df.empty and '후기' in df.columns:
        reviews = df[df['후기'].astype(str).str.strip() != ""]
        if not reviews.empty:
            recent_reviews = reviews.tail(3).iloc[::-1]
            r_col1, r_col2, r_col3 = st.columns(3)
            for idx, row in enumerate(recent_reviews.itertuples()):
                short_review = row.후기[:50] + "..." if len(str(row.후기)) > 50 else row.후기
                card_html = f"""
                <div class="review-card">
                    <div class="stars">⭐⭐⭐⭐⭐</div>
                    <div class="review-text">"{short_review}"</div>
                    <div class="review-info">{row.현장명} 고객님<br>({row.시공내용})</div>
                </div>
                """
                if idx % 3 == 0: r_col1.markdown(card_html, unsafe_allow_html=True)
                elif idx % 3 == 1: r_col2.markdown(card_html, unsafe_allow_html=True)
                else: r_col3.markdown(card_html, unsafe_allow_html=True)
        else: st.info("아직 등록된 후기가 없습니다.")
    else: st.info("후기 데이터를 불러오는 중입니다...")

    st.divider()
    st.subheader("왜 마이홈케어플러스인가요?")
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">첨단 장비 정밀 탐지</div>
            <div class="feature-text">청음식/가스식 최신 장비 보유.<br>미세한 누수까지 찾아냅니다.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2: 
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">책임 시공 보장</div>
            <div class="feature-text">누수 원인을 못 찾으면<br>비용을 일절 받지 않습니다.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3: 
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <div class="feature-title">부산 전 지역 긴급출동</div>
            <div class="feature-text">해운대, 수영, 동래 어디든<br>빠르게 달려갑니다.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 2. 서비스 소개
# ==========================================
elif menu == "서비스 소개":
    st.header("🛠️ 마이홈케어플러스 전문 시공")
    st.write("부산/경남 대표 홈케어! 아래 모든 항목을 직접 시공합니다.")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💧 누수 & 방수 전문")
        st.markdown("""<div class="service-box"><b>1. 누수 출장 점검</b><br>- 정확한 원인 파악 및 전문가 소견서 발급</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>2. 누수 탐지 (책임 시공)</b><br>- 청음식/가스식 첨단 장비 보유<br>- 못 찾으면 비용 0원!</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>3. 욕실 방수 공사</b><br>- 철거부터 방수, 타일 마감까지 원스톱 해결</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>4. 외부 창틀 로프 코킹</b><br>- 아파트 베란다 빗물 누수 완벽 차단 (로프 작업)</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>5. 욕조 배수구 교체</b><br>- 욕조 파손 없이 배수구만 교체하는 특수 기술</div>""", unsafe_allow_html=True)

    with col2:
        st.subheader("🛁 생활 설비 & 인테리어")
        st.markdown("""<div class="service-box"><b>6. 도배 (실크/합지)</b><br>- 부분 도배부터 전체 도배까지 깔끔한 마감</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>7. 각종 수전(수도꼭지) 교체</b><br>- 주방, 세면대, 샤워기, 베란다 수전 등</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>8. 양변기 교체</b><br>- 치마형, 투피스 등 최신 도기 설치 및 폐기물 처리</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>9. 샤워기 설치</b><br>- 해바라기 샤워기, 선반형 샤워기 설치</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="service-box"><b>10. 환풍기 교체</b><br>- 힘 쎈 환풍기, 댐퍼형(냄새 차단) 환풍기 교체</div>""", unsafe_allow_html=True)

# ==========================================
# 3. 시공 갤러리
# ==========================================
elif menu == "시공 갤러리":
    st.header("✨ 시공 전/후 비교")
    try: image_comparison(img1="before.jpg", img2="after.jpg", label1="Before", label2="After", width=700, in_memory=True)
    except: st.error("사진 파일 필요")

# ==========================================
# 4. 출장 지역
# ==========================================
elif menu == "출장 지역":
    st.header("📍 출장 가능 지역")
    m = folium.Map(location=[35.1796, 129.0756], zoom_start=11)
    folium.Circle(location=[35.1796, 129.0756], radius=20000, color="red", fill=True, fill_opacity=0.1).add_to(m)
    st_folium(m, width=800, height=500)

# ==========================================
# 5. 견적 문의
# ==========================================
elif menu == "견적 문의":
    calculator.show_estimate()

# ==========================================
# 6. 관리자 모드
# ==========================================
elif menu == "🔒 관리자 모드":
    password = st.text_input("비밀번호", type="password")
    
    if password == st.secrets.get("ADMIN_PW", ""):
        st.success("✅ 로그인 성공")
        
        tab1, tab2, tab3, tab4 = st.tabs(["📝 블로그 글쓰기 (2.5 Flash)", "📊 시공 장부 (매출)", "🖼️ 사진 워터마크", "📱 QR코드 생성"])
        
        # [탭1] 블로그 글쓰기 (Gemini 2.5 Flash)
        with tab1:
            st.subheader("🔥 AI 블로그 파트너 (Gemini 2.5 Flash)")
            st.info("현장 사진을 넣으면 AI가 사진을 보고 글을 써줍니다!")
            
            with st.form("blog_form_v2"):
                col1, col2 = st.columns(2)
                with col1:
                    topic = st.text_input("주제 (키워드)", placeholder="예: 대연자이 아파트 누수")
                with col2:
                    uploaded_files = st.file_uploader("현장 사진 업로드 (여러 장 가능)", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'heic'])
                
                context = st.text_area("작업 내용 및 특이사항", height=150, placeholder="예: 아랫집 천장 누수. 공기압 검사하니 온수관 문제...")
                
                submit_blog = st.form_submit_button("📝 블로그 포스팅 생성 시작")
                
            # 폼 바깥에서 결과 처리 (저장 버튼 때문에 폼 밖으로 뺌)
            if submit_blog:
                if not topic or not context:
                    st.warning("주제와 작업 내용을 입력해주세요!")
                else:
                    try:
                        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        image_parts = []
                        if uploaded_files:
                            for uploaded_file in uploaded_files:
                                image = Image.open(uploaded_file)
                                image_parts.append(image)
                        
                        prompt_text = f"""
                        당신은 부산 누수/방수 1인 시공 전문가 '마이홈케어플러스'의 블로그 파트너입니다.
                        아래 입력된 정보와 사진을 바탕으로 네이버 블로그 상위 노출을 위한 포스팅을 작성해주세요.
                        
                        [입력 정보]
                        - 주제: {topic}
                        - 현장 상황 및 스토리: {context}
                        
                        [요청 사항 - 출력 형식]
                        1. **제목 추천:** 클릭을 유도하는 후킹한 제목 3가지를 먼저 제시하세요.
                        2. **본문 작성:** - 서론-본론(진단-원인-해결)-결론 구조로 작성하세요.
                           - 말투는 신뢰감 있는 50대 전문가 톤 (~했습니다, ~했거든요)을 유지하세요.
                           - 중간중간 **[이미지 배치]** 라고 표시하고, 업로드된 사진 중 어떤 장면이 들어가야 할지, 그리고 그 사진의 **ALT 태그**는 무엇으로 할지 구체적으로 명시하세요.
                        3. **해시태그:** 유입을 높이는 해시태그 10개를 마지막에 추천하세요.
                        """
                        
                        request_content = [prompt_text]
                        if image_parts:
                            request_content.extend(image_parts)
                            request_content.append("위 사진들은 실제 현장 사진입니다. 사진의 내용을 분석해서 본문 묘사에 활용해주세요.")
                            
                        with st.spinner("AI(2.5 Flash)가 글을 쓰는 중입니다..."):
                            response = model.generate_content(request_content)
                            
                            # 세션 상태에 저장 (새로고침 방지용)
                            st.session_state['generated_blog'] = response.text
                            st.session_state['blog_topic'] = topic

                    except Exception as e:
                        st.error(f"에러 발생: {e}")
            
            # 생성된 글이 있으면 화면에 표시하고 저장 버튼 활성화
            if 'generated_blog' in st.session_state:
                st.success("작성 완료! 아래 내용을 복사해서 블로그에 쓰세요.")
                st.markdown(st.session_state['generated_blog'])
                
                st.divider()
                st.markdown("### 💾 장부에 기록하기")
                st.write("이 글의 내용을 시공 장부(비고란)에 저장하시겠습니까?")
                
                if st.button("네, 장부에 저장할게요"):
                    today = datetime.now().strftime("%Y-%m-%d")
                    saved_topic = st.session_state['blog_topic']
                    saved_content = st.session_state['generated_blog']
                    
                    # 시공 장부에 저장 (날짜, 주제, '블로그포스팅', 0원, 내용, '')
                    if add_to_sheet(today, saved_topic, "블로그 AI 작성", 0, saved_content, ""):
                        st.success("✅ 장부에 저장되었습니다! '시공 장부' 탭에서 확인하세요.")
                    else:
                        st.error("저장에 실패했습니다. 잠시 후 다시 시도해주세요.")

        # [탭2] 시공 장부
        with tab2:
            st.subheader("📊 마이홈케어 매출 현황")
            df = load_data()
            if not df.empty and '금액' in df.columns:
                try:
                    df['금액'] = df['금액'].astype(str).str.replace(',', '').astype(int)
                    total_revenue = df['금액'].sum()
                    count_work = len(df)
                    m1, m2 = st.columns(2)
                    m1.metric("💰 누적 총 매출", f"{total_revenue:,}원")
                    m2.metric("🔨 총 시공 건수", f"{count_work}건")
                    st.divider()
                    st.write("📋 **최근 시공 내역**")
                    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
                except: st.dataframe(df)
            else: st.info("아직 데이터가 없습니다.")
            st.divider()
            st.write("✍️ **새로운 매출 & 후기 입력하기**")
            with st.form("sheet_form"):
                date = st.date_input("날짜")
                s_place = st.text_input("현장명")
                s_work = st.text_input("시공 내용")
                s_price = st.number_input("받은 금액 (원)", step=10000)
                s_note = st.text_input("비고")
                st.markdown("---")
                s_review = st.text_input("💬 고객 후기 (홈페이지 메인 노출)", placeholder="예: 사장님 최고!")
                submit_sheet = st.form_submit_button("💾 장부에 저장하기")
                if submit_sheet:
                    with st.spinner("저장 중..."):
                        if add_to_sheet(date, s_place, s_work, s_price, s_note, s_review):
                            st.success(f"✅ 저장 완료! {s_price}원 입력됨.")
                        else: st.error("저장 실패")

        # [탭3] 워터마크
        with tab3:
            st.subheader("📸 사진 도장 찍기 (워터마크)")
            uploaded_file = st.file_uploader("사진 파일을 드래그하거나 클릭해서 올리세요", type=["jpg", "png", "jpeg"])
            if uploaded_file is not None:
                default_text = "마이홈케어플러스 010-6533-3137"
                watermark_text = st.text_input("들어갈 문구", value=default_text)
                if st.button("도장 쾅! 찍기"):
                    with st.spinner("도장 찍는 중..."):
                        final_img, img_bytes = watermarker.add_watermark(uploaded_file, watermark_text)
                        st.success("완성! 다운로드하세요.")
                        st.image(final_img, caption="결과물", use_container_width=True)
                        st.download_button(label="💾 다운로드", data=img_bytes, file_name=f"watermarked_{uploaded_file.name}", mime="image/jpeg")

        # [탭4] QR코드 생성
        with tab4:
            st.subheader("📱 홈페이지 QR코드 만들기")
            st.write("명함이나 작업 차량에 붙일 QR코드를 생성합니다.")
            my_url = st.text_input("우리 홈페이지 주소 (https:// 포함)", "https://myhomecare-web.streamlit.app")
            if st.button("QR코드 생성하기"):
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={my_url}"
                st.image(qr_url, caption="📷 핸드폰으로 찍어보세요!", width=300)
                st.markdown(f"**[Tip]** 위 이미지를 마우스 오른쪽 클릭 -> '이미지 저장' 하셔서 명함집에 보내시면 됩니다.")