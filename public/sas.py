import os
from PIL import Image, ImageDraw, ImageFont

# Папки
SKINS_DIR = "skins"
FACES_DIR = "faces"

# Создаём папку для лиц, если её нет
os.makedirs(FACES_DIR, exist_ok=True)

# Шрифт для цифры (если Pillow не находит, использует дефолтный)
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

# Функция для определения цвета цифры
def get_contrast_color(image):
    """
    Определяет среднюю яркость изображения и выбирает контрастный цвет:
    - Если фон светлый, цифры будут чёрными.
    - Если фон тёмный, цифры будут белыми.
    """
    grayscale = image.convert("L")  # Преобразуем в чёрно-белое
    pixels = grayscale.getdata()
    avg_brightness = sum(pixels) / len(pixels)  # Средняя яркость

    return (0, 0, 0, 255) if avg_brightness > 128 else (255, 255, 255, 255)  # Чёрный или белый


# Проходим по всем скинам
for filename in os.listdir(SKINS_DIR):
    if filename.endswith(".png"):
        skin_path = os.path.join(SKINS_DIR, filename)
        face_path = os.path.join(FACES_DIR, filename)

        # Загружаем изображение
        skin = Image.open(skin_path).convert("RGBA")

        # Вырезаем лицо (8x8 пикселей в верхнем левом углу)
        face = skin.crop((8, 8, 16, 16))

        # Создаём изображение с увеличением (чтобы лучше выглядело)
        face = face.resize((64, 64), Image.NEAREST)

        # Определяем цвет цифры
        text_color = get_contrast_color(face)

        # Рисуем цифру
        draw = ImageDraw.Draw(face)
        number = os.path.splitext(filename)[0]  # Извлекаем число из имени

        # Добавляем контур для лучшей видимости
        outline_color = (0, 0, 0, 255) if text_color == (255, 255, 255, 255) else (255, 255, 255, 255)
        
        x, y = 48, 48
        draw.text((x-1, y), number, font=font, fill=outline_color)
        draw.text((x+1, y), number, font=font, fill=outline_color)
        draw.text((x, y-1), number, font=font, fill=outline_color)
        draw.text((x, y+1), number, font=font, fill=outline_color)
        draw.text((x, y), number, font=font, fill=text_color)  # Основной текст

        # Сохраняем результат
        face.save(face_path)
        print(f"Сохранено: {face_path}")

print("✅ Все лица сохранены в папке faces/")
