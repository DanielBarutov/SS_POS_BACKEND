import datetime
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
import textwrap
from decimal import Decimal
from app.driver.setting import FONT_PATH, LOGO_PATH, DEVICE, LABEL_WIDTH

def build_receipt(header_text, items_text):
    try:
        font_header = ImageFont.truetype(FONT_PATH, 28)
        font_body   = ImageFont.truetype(FONT_PATH, 22)
    except:
        font_header = font_body = ImageFont.load_default()

    header_lines = header_text.split("\n")
    item_lines_final = []
    chars_per_line = 44 
    
    for line in items_text.split("\n"):
        if line.strip():
            wrapped = textwrap.wrap(line, width=chars_per_line)
            item_lines_final.extend(wrapped)

    # Рассчитываем высоту
    line_height = 38
    logo_height = 0
    
    # Пытаемся загрузить логотип для расчета высоты
    logo_img = None
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
            # Масштабируем логотип, чтобы он вписался в ширину (например, 200px шириной)
            canvas = Image.new("RGBA", logo_img.size, (255, 255, 255, 255))
            canvas.paste(logo_img, (0, 0), logo_img)
            logo_bw = canvas.convert("1")
            base_w = 200 
            w_percent = (base_w / float(logo_bw.size[0]))
            h_size = int((float(logo_bw.size[1]) * float(w_percent)))
            logo_img = logo_bw.resize((base_w, h_size), Image.Resampling.LANCZOS)
            logo_height = h_size + 20 # Высота + отступ
        except Exception as e:
            print(f"Ошибка лого: {e}")

    total_lines_count = len(header_lines) + 2 + len(item_lines_final) + 2
    height = total_lines_count * line_height + 20 + logo_height

    img = Image.new("1", (LABEL_WIDTH, height), 1)
    draw = ImageDraw.Draw(img)
    
    y = 10

    # 0. Печатаем LOGO (ЦЕНТР)
    if logo_img:
        logo_x = (LABEL_WIDTH - logo_img.size[0]) // 2
        img.paste(logo_img, (logo_x, y))
        y += logo_height

    # 1. Печатаем заголовок (ЦЕНТР)
    for line in header_lines:
        bbox = draw.textbbox((0, 0), line, font=font_header)
        w = bbox[2] - bbox[0]
        draw.text(((LABEL_WIDTH - w) // 2, y), line, font=font_header, fill=0)
        y += line_height

    y += 10
    draw.text((0, y), "-" * 48, font=font_body, fill=0) # Разделитель
    y += line_height

    # 2. Печатаем позиции (ЛЕВО)
    # Можно добавить небольшой отступ слева (например, 5-10 пикселей)
    padding_left = 10
    for line in item_lines_final:
        draw.text((padding_left, y), line, font=font_body, fill=0)
        y += line_height

    # 3. Печатаем итог (ЦЕНТР или ПРАВО)
    y += 10
    
    return img

def print_bitmap(img):
    w, h = img.size
    bitmap = img.tobytes()
    width_bytes = w // 8
    
    # Высота в мм (h / 8 при 203dpi)
    h_mm = h // 8

    # В TSPL используем BITMAP 0,0 (без смещений)
    
    tspl = f"SIZE 48 mm,{h_mm} mm\nCLS\nDIRECTION 0\n".encode()
    tspl += f"BITMAP 10,0,{width_bytes},{h},0,".encode()
    tspl += bitmap
    tspl += b"\nPRINT 1,1\n"

    with open(DEVICE, "wb") as p:
        p.write(tspl)

# Данные для теста


def print_stats_data_check(income_cash: float|None = None, income_card: float|None = None, total_orders: int|None = None, income_total: float|None = None, income_average: float|None = None):
    header = f"SUSHI SAN\nул. Славы, 25\n{datetime.now().strftime('%d.%m.%Y %H:%M')}"
    items_text = "\n\n"
    items_text += f"Наличными: {Decimal(income_cash).quantize(Decimal('0.00'))} руб\n"
    items_text += f"Картами: {Decimal(income_card).quantize(Decimal('0.00'))} руб\n"
    items_text += f"Приход за день: {Decimal(income_total).quantize(Decimal('0.00'))} руб\n"
    items_text += f"Средний чек: {Decimal(income_average).quantize(Decimal('0.00'))} руб\n"
    items_text += f"Кол-во заказов: {total_orders}\n"
    
    img = build_receipt(header, items_text)
    print_bitmap(img)

