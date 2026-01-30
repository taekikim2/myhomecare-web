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
import prompts      
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

    /* 후기 카드 스타일 */
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

# 장부에 데이터 쓰기 (후기 포함)
def add_to_sheet(date, place, work, price, note, review):
    sheet = get_google_sheet()
    if sheet:
        try:
            sheet.append_row([str(date), place, work, price, note, review])
            return True
        except: return False
    return False

# 장부에서 데이터 읽기
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
        # 시공 전후 사진 탭
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

    # 고객 후기 섹션
    st.subheader("⭐⭐⭐⭐⭐ 고객님들의 찐 후기")
    df = load_data()
    if not df.empty and '후기' in df.columns:
        reviews = df[df['후기'].astype(str).str.strip() != ""]
        if not reviews.empty:
            recent_reviews = reviews.tail(3).iloc[::-1] # 최신 3개
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
        else:
            st.info("아직 등록된 후기가 없습니다.")
    else:
        st.info("후기 데이터를 불러오는 중입니다...")

    st.divider()
    st.subheader("왜 마이홈케어플러스인가요?")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="feature-card"><div class="feature-icon">🔍</div><div class="feature-title">첨단 장비 정밀 탐지</div><div class="feature-text">청음식/가스식 최신 장비 보유.<br>미세한 누수까지 찾아냅니다.</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="feature-card"><div class="feature-icon">🛡️</div><div class="feature-title">책임 시공 보장</div><div class="feature-text">누수 원인을 못 찾으면<br>비용을 일절 받지 않습니다.</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="feature-card"><div class="feature-icon">🚀</div><div class="feature-title">부산 전 지역 긴급출동</div><div class="feature-text">해운대, 수영, 동래 어디든<br>빠르게 달려갑니다.</div></div>', unsafe_allow_html=True)

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
        st.markdown('<div class="service-box"><b>1. 누수 출장 점검</b><br>- 정확한 원인 파악 및 전문가 소견서 발급</div>', unsafe_allow_html=True)
        st.markdown('<div class="service-box"><b>2. 누수 탐지 (책임