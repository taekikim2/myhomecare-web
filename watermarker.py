from PIL import Image, ImageDraw, ImageFont
import io
import os

def add_watermark(uploaded_file, watermark_text="마이홈케어플러스 010-6533-3137"):
    # 1. 이미지 열기
    original_image = Image.open(uploaded_file).convert("RGBA")
    width, height = original_image.size
    draw = ImageDraw.Draw(original_image)

    # 2. 폰트 크기 자동 계산 (사진 크기에 맞춰서 적당히)
    font_size = int(width / 20)
    if font_size < 30: font_size = 30

    # 3. [핵심] 폰트 불러오기 (사장님이 올린 font.ttf 사용!)
    try:
        font_path = "font.ttf" 
        
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # 혹시라도 파일이 없으면 에러 (기본 폰트로 넘어감)
            raise Exception("폰트 파일 없음")
            
    except:
        # 폰트가 없으면 어쩔 수 없이 기본 폰트 사용 (이 경우 한글이 깨짐)
        font = ImageFont.load_default()
        print("⚠️ 폰트 파일을 못 찾았습니다. font.ttf가 깃허브에 있는지 확인하세요.")

    # 4. 글씨 위치 계산 (오른쪽 하단)
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    margin = int(font_size / 2)
    x = width - text_width - margin
    y = height - text_height - margin

    # 5. 그리기 (검은 테두리 + 노란색 글씨 = 가독성 최고!)
    outline_color = (0, 0, 0, 255)  # 진한 검은색 테두리
    text_color = (255, 255, 0, 255) # 쨍한 노란색 글씨
    
    stroke_width = int(font_size / 10) # 테두리 두께
    
    # 테두리 먼저 그리고 -> 그 위에 글씨 얹기
    draw.text((x, y), watermark_text, font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=outline_color)

    # 6. 저장 준비
    final_image = original_image.convert("RGB")
    img_byte_arr = io.BytesIO()
    final_image.save(img_byte_arr, format='JPEG', quality=95)
    img_byte_arr = img_byte_arr.getvalue()

    return final_image, img_byte_arr