import datetime
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
import textwrap
from app.driver.setting import FONT_PATH, LOGO_PATH, DEVICE, LABEL_WIDTH

def build_receipt(header_text, items_text):
    try:
        font_header = ImageFont.truetype(FONT_PATH, 28)
        font_body   = ImageFont.truetype(FONT_PATH, 24)
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
    line_height = 32
    logo_height = 0
    
    # Пытаемся загрузить логотип для расчета высоты
    

    total_lines_count = len(header_lines) + 2 + len(item_lines_final) + 2
    height = total_lines_count * line_height  + logo_height

    img = Image.new("1", (LABEL_WIDTH, height), 1)
    draw = ImageDraw.Draw(img)
    
    y = 10

    

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


def print_receipt_cook(items, order_id, devices, comment):
    header = f"SUSHI SAN\nул. Славы, 25\n{datetime.now().strftime('%d.%m.%Y %H:%M')}"
    items_text = "\n\n"
    items_text += f"Заказ №{order_id}\n"
    items_text += f"Персон: {devices}\n"
    items_text += f"Комментарий: {comment}\n"
    items_text += "\n" + "-" * 44 + "\n\n"
    for item in items:
        items_text += f"{item.name} - {item.qty}шт\n"
    items_text += "\n" + "-" * 44 + "\n\n\n"
    img = build_receipt(header, items_text)
    print_bitmap(img)

