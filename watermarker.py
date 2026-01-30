from PIL import Image, ImageDraw, ImageFont
import io
import os
import streamlit as st

def add_watermark(uploaded_file, watermark_text="마이홈케어플러스 010-6533-3137"):
    # 1. 이미지 열기 (투명도 처리를 위해 RGBA로 변환)
    original_image = Image.open(uploaded_file).convert("RGBA")
    width, height = original_image.size
    draw = ImageDraw.Draw(original_image)

    # 2. 폰트 크기 자동 계산 (이미지 너비의 4% 정도 크기)
    font_size = int(width / 25)
    if font_size < 20: font_size = 20 # 너무 작아지지 않게 최소 크기 설정

    # 3. 폰트 불러오기 (서버에 있는 기본 고딕 폰트 시도)
    try:
        # 리눅스(스트림릿 서버)에 흔히 있는 폰트 경로 시도
        # 한글 표시를 위해 나눔고딕 계열이나 기본 폰트를 찾습니다.
        font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf", # 1순위: 나눔고딕 볼드
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", # 2순위: 영문 기본 볼드
            "arial.ttf" # 3순위: 윈도우 테스트용
        ]
        font = None
        for path in font_paths:
            if os.path.exists(path) or (path == "arial.ttf"): # arial은 윈도우에서 기본적으로 찾음
                try:
                    font = ImageFont.truetype(path, font_size)
                    break
                except: continue
        
        if font is None: raise Exception("폰트 못 찾음")

    except:
        # 폰트 로드 실패 시, 아주 기본적인 폰트 사용 (크기 조절 불가, 한글 깨질 수 있음)
        font = ImageFont.load_default()
        st.toast("⚠️ 기본 폰트가 사용되었습니다. (글자가 작거나 한글이 깨질 수 있습니다)", icon="😅")


    # 4. 글씨 위치 계산 (오른쪽 하단)
    # 글씨가 차지할 박스 크기를 계산합니다.
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    margin = int(font_size / 2) # 여백
    x = width - text_width - margin
    y = height - text_height - margin

    # 5. 그리기 (가독성을 위해 '검은 테두리 + 흰색 글씨'로 그립니다)
    outline_color = (0, 0, 0, 180) # 반투명 검은색 테두리
    text_color = (255, 255, 255, 230) # 반투명 흰색 글씨
    stroke_width = int(font_size / 15) # 테두리 두께
    if stroke_width < 1: stroke_width = 1

    draw.text((x, y), watermark_text, font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=outline_color)

    # 6. 결과물 준비 (JPG로 저장하기 위해 RGB로 변환)
    final_image = original_image.convert("RGB")
    
    # 다운로드 버튼에 넣기 위해 메모리에 임시 저장
    img_byte_arr = io.BytesIO()
    final_image.save(img_byte_arr, format='JPEG', quality=95)
    img_byte_arr = img_byte_arr.getvalue()

    return final_image, img_byte_arr